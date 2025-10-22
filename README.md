<!-- polished README: clear, vivid, and accurate instructions -->

# 3D Skull Reconstruction

Brief & vivid: convert a CT DICOM series into a 3D skull mesh (STL) using VTK + NumPy.

`3Drecon.py` runs a compact pipeline that:

1. reads a CT DICOM series;
1. thresholds voxels by Hounsfield units to isolate bone;
1. extracts a surface mesh using Discrete Marching Cubes;
1. renders the result with VTK; and
1. exports an STL file (`craneo.stl`) for downstream processing or 3D printing.

This document is a concise, accurate guide to reproduce results on Windows (PowerShell). The script was developed using Python 3.11.

---

## Quick facts

- Platform: Windows (PowerShell examples)
- Python: 3.11 (used for development and testing)
- Recommended package manager: conda (for stable VTK installs)
- Minimum libraries: `vtk`, `numpy`; `plotly` is optional (2D heatmaps)

## Install (recommended)

1. Create and activate a conda env (Python 3.11):

```powershell
conda create -n skull python=3.11 -y
conda activate skull
```

2. Install packages (conda-forge recommended for VTK):

```powershell
conda install -n skull -c conda-forge vtk numpy plotly -y
```

Alternative (pip inside activated env — you mentioned using pip):

```powershell
pip install vtk
pip install numpy
pip install plotly
# or
pip install -r requirements.txt
```

Note: on Windows, conda-forge VTK is often the most reliable provider.

## Files in this repository

- `3Drecon.py` — main script (VTK pipeline + export). Key behaviors:
  - Auto-detects DICOM folder among `./CTDataset`, `./CTDataset/CTDataset`, `./dcmfolder`.
  - Validates reader output and prints diagnostics when loading fails.
  - Uses the middle slice automatically (no hard-coded index).
  - Writes an STL file `craneo.stl` using `vtkSTLWriter`.
- `CTDataset/` — example DICOM series (if present).
- `requirements.txt` — simple pip install list.

## Quick start (try this)

From the repo root (PowerShell):

```powershell
conda activate skull
python 3Drecon.py
```

If `conda activate` isn't available in your shell, run:

```powershell
conda run -n skull python 3Drecon.py
```

When the script runs it will:

- search for a DICOM folder among the candidates and fail early with a helpful message if not found;
- print pixel spacing and data extent information;
- show a 2D slice (original and thresholded) with Plotly if available;
- open an interactive VTK window showing the mesh and an outline; and
- save `craneo.stl` to the working directory.

## Troubleshooting (common issues)

- Missing VTK:

```powershell
conda install -n skull -c conda-forge vtk
# or
pip install vtk
```

- "Couldn't get sorted files" (vtkDICOMImageReader): ensure the directory contains `.dcm` files and that the series is coherent. If your DICOMs live elsewhere, move them into one of the candidate folders or edit `3Drecon.py` to point to the correct path.

- IndexError for slice selection: the script uses the dataset's middle slice. If an IndexError appears, the reader likely returned zero-sized dimensions — check printed data extent and file consistency.

## Parameters you may want to adjust

- Threshold value (Hounsfield): in the script a threshold is used as an example; tune this for your CT scan to better separate bone.
- Discrete Marching Cubes parameters: DMC may expose generation options if you need multiple iso-values.

## References (quick links)

- VTK documentation: <https://vtk.org/documentation/>
- vtkDICOMImageReader: <https://vtk.org/doc/nightly/html/classvtkDICOMImageReader.html>
- Marching Cubes (original paper): Lorensen & Cline, SIGGRAPH 1987
- Hounsfield scale (CT basics): <https://en.wikipedia.org/wiki/Hounsfield_scale>
- NumPy/VTK conversion notes: search for `vtk_to_numpy` in VTK docs and tutorials
- Example tutorial that inspired this workflow: <https://pyscience.wordpress.com/2014/09/11/surface-extraction-creating-a-mesh-from-pixel-data-using-python-and-vtk/>

## Next steps (optional enhancements)

- Add a `--dicom-dir` CLI flag so you can pass input paths without editing the script.
- Add a headless/export-only mode to run without an interactive VTK window (useful for servers).
- Add post-processing: smoothing, decimation, and mesh validation prior to exporting STL.

## Credits & acknowledgements

This project workflow is based on community VTK + NumPy approaches and the referenced tutorial above. The VTK project and its documentation are the primary technical references.

---

If you'd like, I can now add a `--dicom-dir` option to `3Drecon.py` and a small `run.ps1` helper that creates the `skull` environment and runs the script.
