# Thanks to the research of https://pyscience.wordpress.com/2014/09/11/surface-extraction-creating-a-mesh-from-pixel-data-using-python-and-vtk/ #

import vtk
from vtk.util import numpy_support
import os
import numpy as np
import plotly
from plotly.graph_objs import Figure, Heatmap, Layout

#................FUNCTIONS DEFINITION.................#
def vtkImageToNumPy(image, pixelDims):
    """Convert a VTK image to a NumPy array with Fortran ordering.

    Args:
        image: vtkImageData
        pixelDims: list/tuple with three dimensions

    Returns:
        ndarray shaped as pixelDims
    """
    pointData = image.GetPointData()
    arrayData = pointData.GetArray(0)
    arr = numpy_support.vtk_to_numpy(arrayData)
    arr = arr.reshape(pixelDims, order='F')
    return arr

#Create a 2D heatmap from an array
def plotHeatmap(array, name="plot"):
    """Show a simple black/white heatmap using Plotly."""
    hm = Heatmap(z=array, colorscale=[[0, 'black'], [1.0, 'white']])
    layout = Layout(autosize=False, title=name)
    fig = Figure(data=[hm], layout=layout)
    return fig.show()

#plot CT slice
def vtk_show(renderer1, renderer2, width=700, height=700):
    """Render two VTK actors in a simple window."""
    ren = vtk.vtkRenderer()
    ren.SetBackground(0.0, 0.0, 0.0)
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renderWindow)
    renderer1.GetProperty().SetColor(1.0, 1.0, 1.0)
    ren.AddActor(renderer1)
    ren.AddActor(renderer2)

    renderWindow.SetSize(width, height)
    renderWindow.Render()

    iren.Initialize()
    iren.Start()

#............READING/SORTING/GROUP DICOM FILES..........#
#colors = vtk.vtkNamedColors()
#colors.SetColor("SkinColor", [255, 125, 64, 255])
# Asignación del directorio de lectura para los archivos DICOM
# Try a few likely locations (project/CTDataset, project/CTDataset/CTDataset, project/dcmfolder)
cwd = os.getcwd()
candidates = [os.path.join(cwd, "CTDataset"), os.path.join(cwd, "CTDataset", "CTDataset"), os.path.join(cwd, "dcmfolder")]
PathDicom = None
for p in candidates:
    if os.path.isdir(p):
        # check for .dcm files inside
        try:
            files = os.listdir(p)
        except Exception:
            files = []
        if any(f.lower().endswith('.dcm') for f in files):
            PathDicom = p
            break

if PathDicom is None:
    print("ERROR: could not find a DICOM directory with .dcm files in expected locations:")
    for c in candidates:
        print("  -", c)
    raise SystemExit(1)

# lectura de archivos dicom
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(PathDicom)
reader.Update()

#................. DICOM IMAGES DIMENSION ADJUSTMENT................#
# Load dimensions using `GetDataExtent`
_extent = reader.GetDataExtent()
ConstPixelDims = [_extent[1]-_extent[0]+1, _extent[3]-_extent[2]+1, _extent[5]-_extent[4]+1]
ConstPixelSpacing = reader.GetPixelSpacing()
print("Pixel Spacing:", ConstPixelSpacing)

# basic validation: ensure we have non-zero dimensions
if ConstPixelDims[0] <= 0 or ConstPixelDims[1] <= 0 or ConstPixelDims[2] <= 0:
    print("ERROR: reader did not load DICOM images correctly. Data extent:", _extent)
    raise SystemExit(1)

                #......Plot 2D skull slide.......#
# load image data and convert to NumPy
ArrayDicom = vtkImageToNumPy(reader.GetOutput(), ConstPixelDims)
# compute a safe middle slice index for the second axis
mid_idx = ConstPixelDims[1] // 2
if mid_idx < 0 or mid_idx >= ConstPixelDims[1]:
    print("ERROR: computed mid slice index is out of range", mid_idx)
    raise SystemExit(1)
try:
    plotHeatmap(np.rot90(ArrayDicom[:, mid_idx, :]), name="CT_Original")
except Exception:
    print("ERROR plotting original slice. ArrayDicom.shape:", getattr(ArrayDicom, 'shape', None))
    raise


#........ HOUNDSFIELD THRESHOLDING DATA.......#
threshold = vtk.vtkImageThreshold ()
threshold.SetInputConnection(reader.GetOutputPort())
threshold.ThresholdByLower(386)  # set value for thresholding
threshold.ReplaceInOn()
threshold.SetInValue(0)  # set all values below 386 to 0
threshold.ReplaceOutOn()
threshold.SetOutValue(1)  # set all values equal or above 386 to 1
threshold.Update()
                #......PLOT THRESHOLDED IMAGE.......#
ArrayDicom = vtkImageToNumPy(threshold.GetOutput(), ConstPixelDims)
try:
    plotHeatmap(np.rot90(ArrayDicom[:, mid_idx, :]), name="CT_Thresholded")
except Exception:
    print("ERROR plotting thresholded slice. ArrayDicom.shape:", getattr(ArrayDicom, 'shape', None))
    raise


#...........3D MESH GENERATION.........#
dmc = vtk.vtkDiscreteMarchingCubes()
dmc.SetInputConnection(threshold.GetOutputPort())
dmc.GenerateValues(1, 1, 1)
dmc.Update()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(dmc.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)
# VTK expects color values in range [0,1]
actor.GetProperty().SetColor(1.0, 1.0, 1.0)


#.......outline.....#

outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(reader.GetOutputPort())

mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())

outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
# initialize colors
colors = vtk.vtkNamedColors()
outline.GetProperty().SetColor(colors.GetColor3d("White"))

#MESH PLOT
vtk_show(actor, outline, 600, 600)

#...............GENERATE .stl FILE.............#
writer = vtk.vtkSTLWriter()
writer.SetInputConnection(dmc.GetOutputPort())
writer.SetFileTypeToBinary()
writer.SetFileName("craneo.stl")
writer.Write()
