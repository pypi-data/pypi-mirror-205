import torch
import torch.nn as nn


# define which things will be exported
__all__ = ["Normed", "empirical_init", "get_wrapped_submodules", "wrap_all_leaf_modules"]


# constants
EPSILON = 1e-12


def names_bias_param(s):
  s = s.casefold()
  return "bias" in s


class GradScale(torch.autograd.Function):
  """ identity function, scales the backwards-flowing gradient by a specified amount """
  @staticmethod
  def forward(ctx, x, a):
    ctx.a = a
    return x
  @staticmethod
  def backward(ctx, grad_y):
    return ctx.a*grad_y, None
grad_scale = GradScale.apply



def bigO(tensor):
  with torch.no_grad():
    if torch.is_complex(tensor):
      return float(torch.sqrt(torch.real(tensor*torch.conj(tensor)).mean()))
    else:
      return float(torch.sqrt((tensor**2).mean()))

def inplace_add(t, x):
  """ add x to tensor t, leaving t in place """
  t.add_(x + torch.zeros_like(t))
  return t


class Normed(nn.Module):
  """ wraps a module and provides proper normalization on its inputs and outputs """
  def __init__(self, module):
    super().__init__()
    self.module = module
    # new weights will be randn(), correct for this by measuring current weights since they're approximately correct
    parameter_scale = min(bigO(param) for param in self.module.parameters() if bigO(param) > 0)
    # register all these values as buffers so they will be included in the state dict:
    self.register_buffer("scale_actv_y", torch.tensor(parameter_scale))
    self.register_buffer("scale_grad_x", torch.tensor(parameter_scale))
    self.register_buffer("scale_grad_y", torch.tensor(1.0))
    self.init_all_parameters()
  def forward(self, *inputs):
    scaled_inputs = [
      grad_scale(x, self.scale_grad_x)
      for x in inputs ]
    y = self.module(*scaled_inputs)
    return grad_scale(self.scale_actv_y*y, self.scale_grad_y)
  def init_all_parameters(self):
    with torch.no_grad():
      for nm, param in self.module.named_parameters():
        if names_bias_param(nm):
          nn.init.constant_(param.data, 0.)
        else:
          nn.init.normal_(param.data)


class ModuleMonitor:
  def __init__(self, module):
    assert isinstance(module, Normed), "can't track modules unless they're wrapped in a normalization module"
    self.module = module
  def zero_grad(self):
    self.module.zero_grad()
  def reset(self):
    self.module.init_all_parameters()
    self.zero_grad()
  def set_activation_hook(self):
    def hook(mod, x, y):
      self.input_activations = [xi.detach() for xi in x]
      self.activation = y.detach()
    self.activation_hook_handle = self.module.register_forward_hook(hook)
  def clear_activation_hook(self):
    self.activation_hook_handle.remove()
  def set_gradient_hook(self):
    def hook(mod, grad_x, grad_y):
      assert len(grad_y) == 1
      self.input_gradient = grad_y[0].detach()
      self.gradient = [
        (grad_xi if grad_xi is not None else None)
        for grad_xi in grad_x ]
    self.gradient_hook_handle = self.module.register_full_backward_hook(hook)
  def clear_gradient_hook(self):
    self.gradient_hook_handle.remove()
  def set_eval_order_hook(self, eval_order_list):
    self.eval_count = 0
    def hook(mod, x, y):
      eval_order_list.append(self)
      self.eval_count += 1
    self.eval_order_hook_handle = self.module.register_forward_hook(hook)
  def clear_eval_order_hook(self):
    assert self.eval_count > 0, "module was never called"
    assert self.eval_count == 1, "module was called too many times: %d" % self.eval_count
    self.eval_order_hook_handle.remove()
  def collect_param_update_data(self, test_lr):
    self.param_gradients = {nm: param.grad for nm, param in self.module.named_parameters()}
    with torch.no_grad():
      prev_activation = self.activation.clone()
      for nm, param in self.module.named_parameters():
        # perform a small update to this particular param in the direction of the gradient
        grad = self.param_gradients[nm]
        inplace_add(param, -test_lr*grad)
      # rerun the module with all parameters updated
      self.activation = self.module(*self.input_activations)
      # save the result, corrected for the scaling we did
      self.activation_update = (self.activation - prev_activation)/test_lr
  def show(self):
    def tensor_to_datastr(t):
      bigO_t = bigO(t)
      if torch.is_complex(t):
        t = torch.real(t)
      return "O(%f), z=%d%s" % (bigO_t, round(100*float(t.mean()/(EPSILON + bigO_t))), "%")
    print(type(self.module.module))
    print("X ---(%f)--> [...] ---(%f)--> Y" % (1.0, self.module.scale_actv_y))
    print("X <--(%f)--- [...] <--(%f)--- Y" % (self.module.scale_grad_x, self.module.scale_grad_y))
    print("ACTIVATION")
    print("    %s" % tensor_to_datastr(self.activation))
    print("GRADIENTS")
    for grad in self.gradient:
      if grad is None:
        print("    None")
      else:
        print("    %s" % tensor_to_datastr(grad))
    print("CHANGE IN ACTIVATION")
    print("    %s" % tensor_to_datastr(self.activation_update))
    print("PARAM GRADIENTS")
    for nm in self.param_gradients:
      print("    %s: %s" % (nm, tensor_to_datastr(self.param_gradients[nm])))
    print()


def get_eval_order(monitors, run_model):
  """ Run the model once to determine evaluation order """
  eval_order = []
  for monitor in monitors:
    monitor.set_eval_order_hook(eval_order)
  run_model() # SIDE EFFECT: eval_order should now be populated
  for monitor in monitors:
    monitor.clear_eval_order_hook()
  return eval_order

def tune_outgoing_act(monitors, run_model):
  """ Tune Outgoing Activations: Fine tune by running a full forward pass through the model several times.
      For stability reasons, it's best to tune the earliest-evaluated modules first.
      Expects monitors sorted from earliest-evaluated to latest. """
  for monitor in monitors:
    monitor.set_activation_hook()
  for monitor in monitors:
    for i in range(0, 5):
      run_model()
      bigO_actv = bigO(monitor.activation)
      # square root the correction for better stability
      monitor.module.scale_actv_y /= EPSILON + bigO_actv**0.5
  for monitor in monitors:
    monitor.clear_activation_hook()

def tune_outgoing_grad(monitors, run_model):
  """ Tune Outgoing Gradients: Fine tune by running a full backward pass through the model several times.
      For stability reasons, it's best to tune the last-evaluated modules first.
      Expects monitors sorted from earliest-evaluated to latest. """
  for monitor in monitors:
    monitor.set_gradient_hook()
  for monitor in reversed(monitors):
    for i in range(0, 5):
      run_model()
      bigO_grad = 0.
      for grad in monitor.gradient:
        if grad is not None:
          bigO_grad = max(bigO(grad), bigO_grad)
      if bigO_grad > EPSILON:
        # square root the correction for better stability
        monitor.module.scale_grad_x /= EPSILON + bigO_grad**0.5
  for monitor in monitors:
    monitor.clear_gradient_hook()

def tune_incoming_grad(monitors, run_model, test_lr):
  """ Tune Incoming Gradients:
      Fine tune by running a full forward and backward pass through the model several times.
      At this point, the product of the scalings for grad_x and grad_y should not change. """
  for monitor in monitors:
    monitor.set_activation_hook()
    monitor.set_gradient_hook()
  for i in range(0, 20):
    run_model()
    # changes are internal to module, so we can update all modules on each run
    for monitor in monitors:
      monitor.collect_param_update_data(test_lr)
      bigO_param_update = bigO(monitor.activation_update)
      # square root to get correction, then square root that for better stability
      scaling_factor = EPSILON + bigO_param_update**0.25
      monitor.module.scale_grad_x *= scaling_factor
      monitor.module.scale_grad_y /= scaling_factor
  for monitor in monitors:
    monitor.clear_activation_hook()
    monitor.clear_gradient_hook()

def show_tuning_results(monitors, run_model, test_lr):
  for monitor in monitors:
    monitor.set_activation_hook()
    monitor.set_gradient_hook()
  run_model()
  print("\nTuning Results:")
  for monitor in monitors:
    monitor.collect_param_update_data(test_lr)
    monitor.show()
  for monitor in monitors:
    monitor.clear_activation_hook()
    monitor.clear_gradient_hook()



def empirical_init(wrappers, forward, get_input, get_loss, batchsz=64, test_lr=1e-5):
  """ empirically initialize a model, requires that model work on batched data
      wrappers  - list of empirical_init wrappers to tune, can be obtained by calling .get_tunable_modules()
      forward   - function to call to evaluate the model being tuned
      get_input - function to call to get a random representative input for the model, takes batchsz as parameter
      get_loss  - function to call to get a random representative loss for the model, takes model output as parameter
      batchsz   - size of the batch, this is what we do a statistical average over
      test_lr   - test learning rate for when we try adjusting the parameters """
  monitors = [ModuleMonitor(wrapper) for wrapper in wrappers]
  
  def run_model():
    """ Re-initializes the model, runs the model, and computes gradients. """
    for monitor in monitors:
      monitor.reset()
    dummy_input = get_input(batchsz)
    model_output = forward(dummy_input)
    dummy_loss = get_loss(model_output)
    dummy_loss.backward()
  
  monitors = get_eval_order(monitors, run_model)
  tune_outgoing_act(monitors, run_model)
  tune_outgoing_grad(monitors, run_model)
  tune_incoming_grad(monitors, run_model, test_lr)
  show_tuning_results(monitors, run_model, test_lr)
  # finally, we reinitialize all the modules a final time
  for monitor in monitors:
    monitor.reset()


def get_wrapped_submodules(module):
  return [mod for mod in module.modules() if isinstance(mod, Normed)]

def is_wrappable_leaf_module(module):
  submodules = sum(1 for _ in module.modules())
  parameters = sum(1 for _ in module.parameters())
  return submodules == 1 and parameters > 0

def wrap_all_leaf_modules(module_init_fn):
  def new_module_init_fn(self, *args, **kwargs):
    ans = module_init_fn(self, *args, **kwargs)
    modules = {}
    wrappable_leaf_modules = set()
    for nm, module in self.named_modules():
      modules[nm] = module
      if is_wrappable_leaf_module(module):
        print("Wrapping %s" % nm)
        wrappable_leaf_modules.add(nm)
    for module_nm in wrappable_leaf_modules:
      if module_nm != "":
        parent_module = modules[".".join(module_nm.split(".")[:-1])]
        setattr(parent_module, module_nm.split(".")[-1], Normed(modules[module_nm]))
    return ans
  return new_module_init_fn

# --- TODO List ---
# TODO: make things work better when modules have multiple inputs
# TODO: add a "wrap all children" decorator, maybe a "wrap all descendants" one too
# TODO: make things work better when modules have multiple outputs
# TODO: make epsilon a passable parameter rather than a constant


