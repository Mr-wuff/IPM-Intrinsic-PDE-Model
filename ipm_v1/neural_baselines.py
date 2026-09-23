from __future__ import annotations
import os
import torch
import torch.nn as nn
import torch.nn.functional as F

class ResidualBlock1D(nn.Module):
    def __init__(self,channels=32,kernel_size=5,dilation=1):
        super().__init__()
        pad=(kernel_size//2)*dilation
        self.c1=nn.Conv1d(channels,channels,kernel_size,padding=pad,dilation=dilation)
        self.c2=nn.Conv1d(channels,channels,kernel_size,padding=pad,dilation=dilation)
    def forward(self,x):
        y=F.gelu(self.c1(x))
        y=self.c2(y)
        return F.gelu(x+y)

class ResNet1D(nn.Module):
    """Compact convolutional one-step field surrogate."""
    def __init__(self,in_channels=1,out_channels=1,width=32,blocks=6,kernel_size=5):
        super().__init__()
        self.stem=nn.Conv1d(in_channels,width,1)
        self.blocks=nn.Sequential(*[
            ResidualBlock1D(width,kernel_size,dilation=1) for _ in range(blocks)
        ])
        self.head=nn.Conv1d(width,out_channels,1)
    def forward(self,x):
        return self.head(self.blocks(F.gelu(self.stem(x))))

class UNet1D(nn.Module):
    """Three-level 1-D U-Net baseline with periodic-friendly convolutions."""
    def __init__(self,in_channels=1,out_channels=1,base=16):
        super().__init__()
        def block(ci,co):
            return nn.Sequential(
                nn.Conv1d(ci,co,5,padding=2),
                nn.GELU(),
                nn.Conv1d(co,co,5,padding=2),
                nn.GELU(),
            )
        self.e1=block(in_channels,base)
        self.e2=block(base,base*2)
        self.e3=block(base*2,base*4)
        self.pool=nn.AvgPool1d(2)
        self.bottleneck=block(base*4,base*8)
        self.u3=nn.ConvTranspose1d(base*8,base*4,2,stride=2)
        self.d3=block(base*8,base*4)
        self.u2=nn.ConvTranspose1d(base*4,base*2,2,stride=2)
        self.d2=block(base*4,base*2)
        self.u1=nn.ConvTranspose1d(base*2,base,2,stride=2)
        self.d1=block(base*2,base)
        self.out=nn.Conv1d(base,out_channels,1)

    @staticmethod
    def _match(a,b):
        if a.shape[-1]==b.shape[-1]:
            return a
        return F.interpolate(a,size=b.shape[-1],mode="linear",align_corners=False)

    def forward(self,x):
        e1=self.e1(x)
        e2=self.e2(self.pool(e1))
        e3=self.e3(self.pool(e2))
        z=self.bottleneck(self.pool(e3))
        z=self._match(self.u3(z),e3)
        z=self.d3(torch.cat([z,e3],dim=1))
        z=self._match(self.u2(z),e2)
        z=self.d2(torch.cat([z,e2],dim=1))
        z=self._match(self.u1(z),e1)
        z=self.d1(torch.cat([z,e1],dim=1))
        return self.out(z)

def make_fno_1d(in_channels=1,out_channels=1,n_modes=16,hidden_channels=32,n_layers=4):
    from neuralop.models import FNO
    return FNO(
        n_modes=(int(n_modes),),
        in_channels=in_channels,
        out_channels=out_channels,
        hidden_channels=hidden_channels,
        n_layers=n_layers,
        positional_embedding="grid",
    )

def make_tfno_1d(in_channels=1,out_channels=1,n_modes=16,hidden_channels=32,n_layers=4,rank=0.25):
    from neuralop.models import TFNO
    return TFNO(
        n_modes=(int(n_modes),),
        in_channels=in_channels,
        out_channels=out_channels,
        hidden_channels=hidden_channels,
        n_layers=n_layers,
        positional_embedding="grid",
        rank=float(rank),
    )

def make_uno_1d(in_channels=1,out_channels=1,hidden_channels=32):
    from neuralop.models import UNO
    return UNO(
        in_channels=in_channels,
        out_channels=out_channels,
        hidden_channels=hidden_channels,
        lifting_channels=32,
        projection_channels=32,
        uno_out_channels=[16,32,32,32,16],
        uno_n_modes=[[16],[16],[8],[16],[16]],
        uno_scalings=[[1.0],[0.5],[1.0],[2.0],[1.0]],
        horizontal_skips_map=None,
        channel_mlp_skip="linear",
        n_layers=5,
    )

class DeepONet1D(nn.Module):
    """Thin adapter around the official DeepXDE PyTorch DeepONetCartesianProd."""
    def __init__(self,n_grid=256,latent=64,width=64):
        super().__init__()
        # DeepXDE backend selection must happen before import in fresh processes.
        os.environ.setdefault("DDE_BACKEND","pytorch")
        from deepxde.nn.pytorch import DeepONetCartesianProd
        self.n_grid=int(n_grid)
        self.net=DeepONetCartesianProd(
            [self.n_grid,width,width,latent],
            [1,width,width,latent],
            "tanh",
            "Glorot normal",
        )
        self.register_buffer(
            "coords",
            torch.linspace(0,1,self.n_grid,dtype=torch.float32)[:,None]
        )
    def forward(self,x):
        if x.shape[-1]!=self.n_grid:
            raise ValueError(
                f"DeepONet1D branch input is frozen to n_grid={self.n_grid}, got {x.shape[-1]}"
            )
        branch=x[:,0,:]
        y=self.net((branch,self.coords.to(x.device,x.dtype)))
        return y[:,None,:]

def make_deeponet_1d(n_grid=256,latent=64,width=64):
    return DeepONet1D(n_grid=n_grid,latent=latent,width=width)

def count_parameters(model):
    return int(sum(p.numel() for p in model.parameters() if p.requires_grad))

def build_b1q0_suite(n_grid=256):
    return {
        "ResNet1D":ResNet1D(width=32,blocks=6),
        "UNet1D":UNet1D(base=16),
        "FNO_official":make_fno_1d(hidden_channels=32,n_modes=16,n_layers=4),
        "TFNO_official":make_tfno_1d(hidden_channels=32,n_modes=16,n_layers=4,rank=0.25),
        "UNO_official":make_uno_1d(hidden_channels=32),
        "DeepONet_official":make_deeponet_1d(n_grid=n_grid,latent=64,width=64),
    }


def sanitize_state_dict_for_strict_load(state_dict):
    """Remove non-parameter serialization metadata keys before strict reload.

    NeuralOperator state dictionaries may contain a top-level "_metadata"
    entry after torch.save/torch.load. That entry is not a module parameter
    and causes strict load_state_dict() to reject an otherwise valid checkpoint.
    """
    cleaned=state_dict.__class__()
    for key,value in state_dict.items():
        if key=="_metadata" or key.endswith("._metadata"):
            continue
        cleaned[key]=value
    if hasattr(state_dict,"_metadata"):
        try:
            cleaned._metadata=getattr(state_dict,"_metadata")
        except Exception:
            pass
    return cleaned
