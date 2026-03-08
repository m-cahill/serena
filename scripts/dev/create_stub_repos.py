#!/usr/bin/env python3
"""
Create minimal stub repositories for CI.
Satisfies paths.py assertion and import chain without cloning external repos.
Deterministic, no network required.

Uses dynamic stub modules for ldm and sgm to avoid whack-a-mole import chain.
"""
import os

_here = os.path.dirname(os.path.abspath(__file__))
SCRIPT_DIR = os.path.dirname(os.path.dirname(_here))
REPOS = os.path.join(SCRIPT_DIR, "repositories")


def touch(path: str, content: str = "") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


DYNAMIC_STUB = '''"""Dynamic stub module for CI - satisfies any nested import."""
import types
import sys
import importlib.abc
import importlib.machinery

def _make_stub_class(name):
    """Stub class; forward->noop, UPPER_CASE->{}, else->noop."""
    _noop = lambda *a, **k: None
    class _Meta(type):
        def __getattribute__(cls, attr):
            try:
                return type.__getattribute__(cls, attr)
            except AttributeError:
                if attr.isupper() or (attr and attr[0].isupper() and "_" in attr):
                    d = {}
                    type.__setattr__(cls, attr, d)  # cache for future access
                    return d
                return _noop
    return _Meta(name, (), {"forward": _noop})

_const_cache = {}  # id(module) -> {attr: dict} for UPPER_CASE

class _StubModule(types.ModuleType):
    """Resolves any attribute as submodule or stub class."""

    def __getattr__(self, name):
        module_name = f"{self.__name__}.{name}"
        if module_name not in sys.modules:
            if name and name[0].isupper():
                # UPPER_CASE on module -> dict (e.g. midas.api.ISL_PATHS)
                if "_" in name or name.isupper():
                    cid = id(self)
                    if cid not in _const_cache:
                        _const_cache[cid] = {}
                    cache = _const_cache[cid]
                    if name not in cache:
                        cache[name] = {}
                    return cache[name]
                sys.modules[module_name] = _make_stub_class(name)
            else:
                m = _StubModule(module_name)
                m.__path__ = []  # package for nested imports
                m.__call__ = lambda *a, **k: None
                sys.modules[module_name] = m
        return sys.modules[module_name]

class _StubFinder(importlib.abc.MetaPathFinder):
    def __init__(self, prefix):
        self.prefix = prefix

    def find_spec(self, fullname, path, target=None):
        if fullname.startswith(self.prefix + "."):
            return importlib.machinery.ModuleSpec(fullname, _StubLoader())
        return None

class _StubLoader(importlib.abc.Loader):
    def create_module(self, spec):
        m = _StubModule(spec.name)
        m.__path__ = []
        return m

    def exec_module(self, module):
        pass

# Append finder so default finders run first; we catch modules they miss
def _install_finder():
    for prefix in ("ldm", "sgm"):
        sys.meta_path.append(_StubFinder(prefix))

_install_finder()

original = sys.modules[__name__]
stub = _StubModule(__name__)
if "__file__" in original.__dict__:
    stub.__file__ = original.__file__
if "__path__" in original.__dict__:
    stub.__path__ = original.__path__
sys.modules[__name__] = stub
'''


def main() -> None:
    sd = "stable-diffusion-stability-ai"

    # paths.py asserts ldm/models/diffusion/ddpm.py exists
    ddpm_content = (
        "# stub for CI - paths.py assertion + LatentDiffusion import\n"
        "class LatentDiffusion:\n    pass\n"
        "class LatentDepth2ImageDiffusion(LatentDiffusion):\n    pass\n"
    )
    touch(os.path.join(REPOS, sd, "ldm", "models", "diffusion", "ddpm.py"), ddpm_content)
    # Dynamic stubs at each package level so Python loads them (not namespace pkgs)
    touch(os.path.join(REPOS, sd, "ldm", "__init__.py"), DYNAMIC_STUB)
    touch(os.path.join(REPOS, sd, "ldm", "models", "__init__.py"), DYNAMIC_STUB)
    touch(os.path.join(REPOS, sd, "ldm", "models", "diffusion", "__init__.py"), DYNAMIC_STUB)

    # generative-models: paths.py checks sgm exists
    gm = "generative-models"
    touch(os.path.join(REPOS, gm, "sgm", "__init__.py"), DYNAMIC_STUB)

    # k-diffusion: paths.py checks k_diffusion/sampling.py; needs real attrs
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

    # BLIP: paths.py checks models/blip.py
    touch(os.path.join(REPOS, "BLIP", "models", "blip.py"), "# stub\n")

    # stable-diffusion-webui-assets (optional)
    touch(os.path.join(REPOS, "stable-diffusion-webui-assets", ".gitkeep"))

    print("Stub repositories created.")


if __name__ == "__main__":
    main()
