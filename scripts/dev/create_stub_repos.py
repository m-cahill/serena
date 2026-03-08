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
    # paths.py asserts ldm/models/diffusion/ddpm.py
    touch(os.path.join(REPOS, sd, "ldm", "models", "diffusion", "ddpm.py"), "# stub\n")
    touch(os.path.join(REPOS, sd, "ldm", "__init__.py"))
    touch(os.path.join(REPOS, sd, "ldm", "modules", "__init__.py"))
    touch(os.path.join(REPOS, sd, "ldm", "modules", "encoders", "__init__.py"))
    # ldm.modules.encoders.modules: FrozenCLIPEmbedder, FrozenOpenCLIPEmbedder, CLIPTextModel
    ldm_modules = (
        "class FrozenCLIPEmbedder:\n    pass\n"
        "class FrozenOpenCLIPEmbedder:\n    pass\n"
        "class CLIPTextModel:\n    pass\n"
    )
    touch(os.path.join(REPOS, sd, "ldm", "modules", "encoders", "modules.py"), ldm_modules)

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

    # k-diffusion: k_diffusion.sampling
    kd = "k-diffusion"
    touch(os.path.join(REPOS, kd, "k_diffusion", "__init__.py"))
    touch(os.path.join(REPOS, kd, "k_diffusion", "sampling.py"), "# stub\n")

    # BLIP: models/blip.py
    touch(os.path.join(REPOS, "BLIP", "models", "blip.py"), "# stub\n")

    # stable-diffusion-webui-assets (optional, paths may warn)
    touch(os.path.join(REPOS, "stable-diffusion-webui-assets", ".gitkeep"))

    print("Stub repositories created.")


if __name__ == "__main__":
    main()
