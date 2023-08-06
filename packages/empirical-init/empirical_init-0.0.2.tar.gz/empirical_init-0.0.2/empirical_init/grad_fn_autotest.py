import torch


class DummyCtx:
  def save_for_backward(*args):
    pass

def autotest_custom_grad_fn(grad_fn, input_shapes, output_shape, verbose=False, epsilon=0.01):
  """ Automatically test the correctness of custom (user-defined) differentiable autograd functions.
      Compares the results from using user-defined backward to the results given by autograd.
      If your implementation would not work with autograd, then this test is not representative.
      grad_fn: is the class where you defined the forward and backward methods
        (so grad_fn.apply would be the actual differentiable func, don't pass that!)
      input_shapes: is a list of tensor shapes expected by your function
        eg. [(1, 2, 7), (5,)]
      output_shape: is the shape of the output your function will produce
        eg. (5, 7) """
  def print_if_verbose(*args):
    if verbose:
      print(*args)
  inputs = [torch.randn(*shape, requires_grad=True) for shape in input_shapes]
  grad = torch.randn(*output_shape)
  # compute gradients using autograd
  print_if_verbose("forward")
  output = grad_fn.forward(DummyCtx(), *inputs)
  print_if_verbose("automatic backward")
  output.backward(grad)
  print_if_verbose("done.")
  expected_grads = []
  for input_tensor in inputs:
    expected_grads.append(input_tensor.grad)
    input_tensor.grad = None
  # compute gradients using user-defined code
  print_if_verbose("forward")
  output = grad_fn.apply(*inputs)
  print_if_verbose("user-defined backward")
  output.backward(grad)
  print_if_verbose("done.")
  actual_grads = []
  for input_tensor in inputs:
    actual_grads.append(input_tensor.grad)
    input_tensor.grad = None
  for actual_grad, expected_grad in zip(actual_grads, expected_grads):
    rms_err = torch.sqrt(((actual_grad - expected_grad)**2).sum())
    print_if_verbose("RMS Error: ", rms_err)
    assert rms_err < epsilon, f"error is above threshold of {epsilon}"

