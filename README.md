# aydin-test

A uv project that runs [aydin](https://github.com/royerlab/aydin) 0.1.15 on
Windows x86_64 and macOS arm64 (Apple Silicon). `uv.lock` covers both platforms.

```sh
uv sync                                   # create .venv from uv.lock
uv run aydin                              # start the GUI
uv run aydin denoise image.tif            # writes image_denoised.tif
```

## Why it is set up this way
aydin 0.1.15 pins old packages exactly (tensorflow 2.8.1, scikit-image 0.18.3,
imagecodecs 2022.2.22, napari 0.4.15), so:

- **Python 3.9 only**: those pins have no wheels for newer Pythons.
- **Windows** uses aydin's exact pins. PyQt5-Qt5 is 5.15.2 (the last release with
  Windows wheels) and tensorflow-io-gcs-filesystem is <=0.31.
- **macOS arm64**: those pins have no arm64 wheels, so `override-dependencies`
  swaps in tensorflow-macos 2.8.0, scikit-image 0.19.x and a newer imagecodecs.
  PyQt5-Qt5 is >=5.15.11.
- numpy is pinned to 1.23.5 and pydantic to v1, because TF 2.8, scikit-image 0.18
  and napari 0.4.15 all predate the newer releases.

## GPU
On Windows the CUDA 12.6 build of PyTorch is installed. It needs an NVIDIA driver
>= 525, and it runs on the CPU when no NVIDIA GPU is present. aydin chooses at runtime:

- **CatBoost** (`noise2self_fgr`, the default denoiser) tries the GPU and falls back to
  the CPU. catboost is held below 1.2.9 because 1.2.9+ rejects the `devices='NULL'`
  that aydin passes, which makes it always fall back to the CPU.
- **numba CUDA** (feature computation) uses the GPU if one is found, otherwise numba/scipy.
- **PyTorch** (CNN denoisers) uses `cuda:0` if available, otherwise the CPU.

To force CPU-only for testing, set `CUDA_VISIBLE_DEVICES=-1`.
