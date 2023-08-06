import torch
import torch.nn as nn
from empirical_init import wrap_all_leaf_modules, get_wrapped_submodules, empirical_init

# Test Code:
def test_empirical_init():
  import torch.nn.functional as F

  class SubmodulesModule(nn.Module):
    def __init__(self, W, device="cpu"):
      super().__init__()
      self.lin0 = nn.Linear(W, W, bias=False, device=device)
      self.lin1 = nn.Linear(W, W, bias=False, device=device)
    def forward(self, x):
      return self.lin1(torch.tanh(self.lin0(x)))
  
  class TestModel(nn.Module):
    @wrap_all_leaf_modules
    def __init__(self, device="cpu"):
      super().__init__()
      self.device = device
      self.lin0 = nn.Linear(20, 64, device=device)
      self.lin1 = nn.Linear(64, 128, device=device)
      self.lin2 = nn.Linear(128, 256, bias=False, device=device)
      self.smdm = SubmodulesModule(256, device=device)
      self.lin3 = nn.Linear(256, 128, bias=False, device=device)
      self.lin4 = nn.Linear(128, 32, bias=False, device=device)
      self.lin5 = nn.Linear(32, 2, bias=False, device=device)
    def forward(self, x):
      logits = self.lin5(
        F.relu(self.lin4(
        F.relu(self.lin3(
        F.relu(self.smdm(
        F.relu(self.lin2(
        F.relu(self.lin1(
        F.relu(self.lin0(
        x)))))))))))))
      return F.softmax(logits, dim=-1)
  def loss(model_output, labels):
    return -torch.log(model_output.gather(-1, labels)).mean()
  def dummy_input(batch):
    """ a method we define so we can use empirical_init() on this model """
    return torch.randn(batch, 20)
  def dummy_loss(model_output):
    """ a method we define so we can use empirical_init() on this model """
    batch, *_ = model_output.shape
    labels = torch.randint(2, (batch, 1))
    return loss(model_output, labels)
  
  model = TestModel()
  empirical_init(
    get_wrapped_submodules(model), model,
    dummy_input, dummy_loss,
    batchsz=64)


if __name__ == "__main__":
  test_empirical_init()


