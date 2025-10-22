# 3D Skull Reconstruction

## Overview

This repository provides a computational pipeline for converting CT DICOM series into three-dimensional skull mesh representations (STL format) using the Visualization Toolkit (VTK) and NumPy. The implementation is designed for medical imaging applications, including surgical planning and anatomical modeling.

The `3Drecon.py` script implements a streamlined workflow that:

1. Reads CT DICOM series data
2. Segments bone tissue using Hounsfield unit thresholding
3. Generates surface meshes via Discrete Marching Cubes algorithm
4. Renders visualizations using VTK's rendering pipeline
5. Exports STL files (`craneo.stl`) suitable for 3D printing and further analysis

This documentation provides comprehensive instructions for reproducing results on Windows systems using PowerShell. The software was developed and tested with Python 3.11.

---

## System Requirements

- **Operating System**: Windows (PowerShell environment)
- **Python Version**: 3.11 (development and testing baseline)
- **Package Manager**: Conda (recommended for stable VTK installations)
- **Core Dependencies**: `vtk`, `numpy`
- **Optional Dependencies**: `plotly` (for 2D visualization and heatmaps)

## Installation

### Method 1: Conda (Recommended)

1. Create a dedicated conda environment with Python 3.11:

```powershell
conda create -n skull python=3.11 -y
conda activate skull
```

2. Install required packages from conda-forge:

```powershell
conda install -n skull -c conda-forge vtk numpy plotly -y
```

### Method 2: pip

Within an activated conda environment:

```powershell
pip install vtk numpy plotly
```

Alternatively, use the provided requirements file:

```powershell
pip install -r requirements.txt
```

**Note**: On Windows platforms, conda-forge distributions of VTK typically provide superior stability and compatibility.

## Repository Structure

- **`3Drecon.py`** — Primary reconstruction script implementing the VTK pipeline
  - Automatic DICOM directory detection (searches `./CTDataset`, `./CTDataset/CTDataset`, `./dcmfolder`)
  - Reader output validation with diagnostic reporting
  - Dynamic middle-slice selection
  - STL export via `vtkSTLWriter`
- **`CTDataset/`** — Sample DICOM series directory (if provided)
- **`requirements.txt`** — Python package dependency specification

## Usage

### Basic Execution

From the repository root directory in PowerShell:

```powershell
conda activate skull
python 3Drecon.py
```

If conda activation is unavailable in your shell session:

```powershell
conda run -n skull python 3Drecon.py
```

### Expected Output

Upon successful execution, the script will:

- Locate and validate DICOM series data from candidate directories
- Display pixel spacing and volumetric extent information
- Generate 2D slice visualizations (original and thresholded) using Plotly (if installed)
- Launch an interactive VTK rendering window displaying the reconstructed mesh and bounding box
- Export the mesh to `craneo.stl` in the working directory

## Troubleshooting

### VTK Installation Issues

```powershell
conda install -n skull -c conda-forge vtk
```

or

```powershell
pip install vtk
```

### "Couldn't get sorted files" Error

This error from `vtkDICOMImageReader` indicates:
- The target directory lacks `.dcm` files
- The DICOM series is incomplete or corrupted

**Resolution**: Verify DICOM file presence and integrity. Relocate files to a supported candidate directory or modify the directory path in `3Drecon.py`.

### Slice Selection IndexError

The script automatically selects the middle slice from the dataset. If an IndexError occurs:
- The reader returned zero-dimensional data
- Review printed data extent diagnostics
- Verify DICOM series consistency and completeness

## Configuration Parameters

### Hounsfield Unit Threshold

The script applies a default threshold value for bone segmentation. This parameter should be adjusted based on the specific CT scan characteristics and desired tissue isolation.

### Discrete Marching Cubes Settings

The Discrete Marching Cubes algorithm may expose additional parameters for multi-threshold extraction and surface generation refinement.

## References

- **VTK Documentation**: https://vtk.org/documentation/
- **vtkDICOMImageReader API**: https://vtk.org/doc/nightly/html/classvtkDICOMImageReader.html
- **Marching Cubes Algorithm**: Lorensen, W.E., & Cline, H.E. (1987). Marching cubes: A high resolution 3D surface construction algorithm. *ACM SIGGRAPH Computer Graphics, 21*(4), 163-169.
- **Hounsfield Scale Reference**: https://en.wikipedia.org/wiki/Hounsfield_scale
- **VTK-NumPy Integration**: Consult VTK documentation for `vtk_to_numpy` utilities
- **Tutorial Reference**: https://pyscience.wordpress.com/2014/09/11/surface-extraction-creating-a-mesh-from-pixel-data-using-python-and-vtk/

## Future Development

Potential enhancements for extended functionality:

- **Command-line Interface**: Implement `--dicom-dir` argument for dynamic input path specification
- **Headless Mode**: Add non-interactive export functionality for server environments
- **Post-processing Pipeline**: Integrate mesh smoothing, decimation, and validation operations prior to STL export
- **Multi-threshold Segmentation**: Support for extracting multiple tissue types simultaneously

## Acknowledgments

This implementation builds upon established VTK and NumPy methodologies within the medical imaging community. Primary technical guidance was derived from VTK project documentation and community tutorials.


---

**Last Updated**: 21 Oct, 2025