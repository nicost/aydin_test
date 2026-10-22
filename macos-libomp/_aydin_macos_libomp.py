"""Preload PyTorch's bundled libomp at interpreter startup (run from aydin_macos_libomp.pth).

LightGBM's macOS wheels link against @rpath/libomp.dylib, with rpaths that only point at
Homebrew (/opt/homebrew/opt/libomp/lib) and MacPorts. PyTorch ships a libomp.dylib whose
install name is /opt/homebrew/opt/libomp/lib/libomp.dylib, so once it is loaded dyld uses it
for LightGBM too, and `brew install libomp` is not needed.
"""
import sys

if sys.platform == "darwin":
    try:
        import ctypes
        import importlib.util
        import os

        _spec = importlib.util.find_spec("torch")  # locates torch without importing it
        if _spec is not None and _spec.submodule_search_locations:
            _lib = os.path.join(_spec.submodule_search_locations[0], "lib", "libomp.dylib")
            if os.path.exists(_lib):
                ctypes.CDLL(_lib, mode=ctypes.RTLD_GLOBAL)
    except Exception:
        pass
