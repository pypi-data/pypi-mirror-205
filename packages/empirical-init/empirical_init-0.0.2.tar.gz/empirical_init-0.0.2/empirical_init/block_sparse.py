import torch
import torch.nn as nn


class HyperCubiesFunction(torch.autograd.Function):
  """ A block-sparse function whose blocks correspond to vertices of a hypercube.
      Vertices are represented as binary integers (https://blog.plover.com/math/cube-components.html)
      two vertices are connected by an edge when popcount(a ^ b) == 1.
      Storage of weights works by having the first dimension be which vertex to end at,
      second dimension is which direction do we move to get to the starting vertex. Special case:
      dim corresponds to no movement. """
  @staticmethod
  def forward(ctx, W, x):
    """ dimensions of W: (2**dim, dim + 1, chan_out, chan_in), dimensions of x: (batch, 2**dim, chan_in) """
    # check validity of inputs
    device = x.device
    assert W.device == device, "Expected both input tensors to be on the same device"
    W_n_cubies, dim_pp, chan_out, chan_in = W.shape
    dim = dim_pp - 1
    n_cubies = 2**dim
    assert W_n_cubies == n_cubies
    batch = x.shape[0]
    assert x.shape[1] == n_cubies
    assert x.shape[2] == chan_in
    # perform actual forwards op
    ctx.save_for_backward(W, x)
    ans = torch.zeros((batch, n_cubies, chan_out), device=device)
    for v_out in range(n_cubies):
      for i_b in range(dim + 1):
        v_in = (v_out ^ (1<<i_b)) % n_cubies # vertex in direction i_b from v
        ans[:, v_out] += (W[v_out, i_b] @ (x[:, v_in].reshape(batch, chan_in, 1))).reshape(batch, chan_out)
    return ans
  @staticmethod
  def backward(ctx, grad):
    W, x = ctx.saved_tensors
    device = W.device
    batch = x.shape[0]
    dim = W.shape[1] - 1
    chan_out, chan_in = W.shape[2:]
    n_cubies = 2**dim
    # compute gradient of W
    grad_W = torch.zeros(W.shape, device=device)
    grad_x = torch.zeros(x.shape, device=device)
    for v_out in range(n_cubies):
      for i_b in range(dim + 1):
        v_in = (v_out ^ (1<<i_b)) % n_cubies # vertex in direction i_b from v
        grad_W[v_out, i_b] = (grad[:, v_out].reshape(batch, chan_out, 1) * x[:, v_in].reshape(batch, 1, chan_in)).sum(0)
        grad_x[:, v_in] += (grad[:, v_out].reshape(batch, 1, chan_out) @ W[v_out, i_b]).reshape(batch, chan_in)
    return grad_W, grad_x


hypercubies = HyperCubiesFunction.apply


class HyperCubies(nn.Module):
  """ A linear layer, but block sparse according to the hyper-cubies scheme """
  def __init__(self, chan_in, chan_out, dim):
    super().__init__()
    norm_factor = ((dim + 1)*max(chan_in, chan_out))**(-0.5)
    self.W = nn.Parameter(norm_factor*torch.randn(2**dim, dim + 1, chan_out, chan_in))
    self.dim = dim
  def forward(self, x):
    return hypercubies(self.W, x)
  def density_ratio(self):
    return (self.dim + 1)/2**self.dim
