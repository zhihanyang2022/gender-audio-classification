import torch.nn as nn

class Flatten(nn.Module):
    def forward(self, xb):
        return xb.view(-1, 1)