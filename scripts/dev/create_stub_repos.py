#!/usr/bin/env python3
"""
Create minimal stub repositories for CI.
Satisfies paths.py assertion and import chain without cloning external repos.
Deterministic, no network required.
"""
import os

_here = os.path.dirname(os.path.abspath(__file__))
SCRIPT_DIR = os.path.dirname(os.path.dirname(_here))
REPOS = os.path.join(SCRIPT_DIR, "repositories")


def touch(path: str, content: str = "") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main() -> None:
    sd = "stable-diffusion-stability-ai"
    # paths.py asserts ldm/models/diffusion/ddpm.py; sd_models_types imports LatentDiffusion
    ddpm_content = (
        "# stub for CI\n"
        "class LatentDiffusion:\n    pass\n"
        "class LatentDepth2ImageDiffusion(LatentDiffusion):\n    pass\n"
    )
    touch(os.path.join(REPOS, sd, "ldm", "models", "diffusion", "ddpm.py"), ddpm_content)
    # ldm.util: default, instantiate_from_config, ismap, etc. (sd_hijack_optimizations, etc.)
    touch(os.path.join(REPOS, sd, "ldm", "util.py"), "def default(a, b): return b if a is None else a\n")
    touch(os.path.join(REPOS, sd, "ldm", "__init__.py"))
    touch(
        os.path.join(REPOS, sd, "ldm", "modules", "__init__.py"),
        "from . import distributions\n",
    )
    touch(os.path.join(REPOS, sd, "ldm", "modules", "encoders", "__init__.py"))
    # ldm.modules.encoders.modules: FrozenCLIPEmbedder, FrozenOpenCLIPEmbedder, CLIPTextModel
    ldm_modules = (
        "class FrozenCLIPEmbedder:\n    pass\n"
        "class FrozenOpenCLIPEmbedder:\n    pass\n"
        "class CLIPTextModel:\n    pass\n"
    )
    touch(os.path.join(REPOS, sd, "ldm", "modules", "encoders", "modules.py"), ldm_modules)
    # ldm.modules.attention, diffusionmodules.model (sd_hijack_optimizations)
    touch(
        os.path.join(REPOS, sd, "ldm", "modules", "attention", "__init__.py"),
        "class CrossAttention:\n    def forward(self, *a, **k): pass\n",
    )
    touch(os.path.join(REPOS, sd, "ldm", "modules", "diffusionmodules", "__init__.py"))
    touch(
        os.path.join(REPOS, sd, "ldm", "modules", "diffusionmodules", "model.py"),
        "class AttnBlock:\n    def forward(self, *a, **k): pass\n",
    )
    # ldm.modules.midas (sd_models)
    touch(os.path.join(REPOS, sd, "ldm", "modules", "midas", "__init__.py"))
    # ldm.modules.distributions.distributions (textual_inversion.dataset)
    touch(os.path.join(REPOS, sd, "ldm", "modules", "distributions", "__init__.py"))
    touch(
        os.path.join(REPOS, sd, "ldm", "modules", "distributions", "distributions.py"),
        "class DiagonalGaussianDistribution:\n    pass\n",
    )

    # generative-models: sgm.modules.encoders.modules
    gm = "generative-models"
    touch(os.path.join(REPOS, gm, "sgm", "__init__.py"))
    touch(os.path.join(REPOS, gm, "sgm", "modules", "__init__.py"))
    touch(os.path.join(REPOS, gm, "sgm", "modules", "encoders", "__init__.py"))
    sgm_modules = (
        "class FrozenCLIPEmbedder:\n    pass\n"
        "class FrozenOpenCLIPEmbedder2:\n    pass\n"
        "class ConcatTimestepEmbedderND:\n    pass\n"
    )
    touch(os.path.join(REPOS, gm, "sgm", "modules", "encoders", "modules.py"), sgm_modules)
    # sgm.modules.attention, diffusionmodules.model (sd_hijack_optimizations)
    touch(
        os.path.join(REPOS, gm, "sgm", "modules", "attention", "__init__.py"),
        "class CrossAttention:\n    def forward(self, *a, **k): pass\n"
        "\nSDP_IS_AVAILABLE = True\nXFORMERS_IS_AVAILABLE = False\n",
    )
    touch(
        os.path.join(REPOS, gm, "sgm", "modules", "diffusionmodules", "__init__.py"),
        "from . import model, openaimodel\n",
    )
    touch(
        os.path.join(REPOS, gm, "sgm", "modules", "diffusionmodules", "model.py"),
        "class AttnBlock:\n    def forward(self, *a, **k): pass\n",
    )
    # sgm.models.diffusion (sd_models_xl)
    touch(os.path.join(REPOS, gm, "sgm", "models", "__init__.py"))
    touch(
        os.path.join(REPOS, gm, "sgm", "models", "diffusion", "__init__.py"),
        "class DiffusionEngine:\n    pass\n",
    )
    # sgm.modules.diffusionmodules.denoiser_scaling, discretizer (sd_models_xl)
    touch(
        os.path.join(REPOS, gm, "sgm", "modules", "diffusionmodules", "denoiser_scaling.py"),
        "class VScaling:\n    pass\n",
    )
    touch(
        os.path.join(REPOS, gm, "sgm", "modules", "diffusionmodules", "discretizer.py"),
        "class LegacyDDPMDiscretization:\n    alphas_cumprod = [1.0]\n",
    )
    # sgm.modules.GeneralConditioner (sd_models_xl)
    touch(os.path.join(REPOS, gm, "sgm", "modules", "__init__.py"))
    touch(
        os.path.join(REPOS, gm, "sgm", "modules", "conditioner.py"),
        "class GeneralConditioner:\n    pass\n",
    )
    touch(
        os.path.join(REPOS, gm, "sgm", "modules", "__init__.py"),
        "from .conditioner import GeneralConditioner\n"
        "from . import attention, diffusionmodules, encoders\n",
    )
    touch(
        os.path.join(REPOS, gm, "sgm", "modules", "diffusionmodules", "openaimodel.py"),
        "# stub\n",
    )

    # k-diffusion: k_diffusion.sampling, utils (sd_schedulers, sd_samplers_lcm)
    kd = "k-diffusion"
    touch(
        os.path.join(REPOS, kd, "k_diffusion", "__init__.py"),
        "from . import utils, sampling, external\n",
    )
    touch(os.path.join(REPOS, kd, "k_diffusion", "utils.py"), "# stub\n")
    touch(
        os.path.join(REPOS, kd, "k_diffusion", "external.py"),
        "class DiscreteEpsDDPMDenoiser:\n    pass\n"
        "class DiscreteSchedule:\n    pass\n"
        "class CompVisVDenoiser:\n    pass\n"
        "class CompVisDenoiser:\n    pass\n",
    )
    kd_sampling = (
        "import torch as _torch\n"
        "torch = _torch\n"
        "def get_sigmas_karras(*a, **k): pass\n"
        "def get_sigmas_exponential(*a, **k): pass\n"
        "def get_sigmas_polyexponential(*a, **k): pass\n"
        "def to_d(*a, **k): pass\n"
        "def default_noise_sampler(*a, **k): pass\n"
        "def trange(*a, **k): return iter([])\n"
        "class BrownianTreeNoiseSampler:\n    pass\n"
    )
    touch(os.path.join(REPOS, kd, "k_diffusion", "sampling.py"), kd_sampling)

    # BLIP: models/blip.py
    touch(os.path.join(REPOS, "BLIP", "models", "blip.py"), "# stub\n")

    # stable-diffusion-webui-assets (optional, paths may warn)
    touch(os.path.join(REPOS, "stable-diffusion-webui-assets", ".gitkeep"))

    print("Stub repositories created.")


if __name__ == "__main__":
    main()
