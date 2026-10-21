"""Build the offline RevF010 development assembly and its reproducible evidence.

This does not automate Fusion while Windows is locked. Native Fusion scripts
remain separate and must be executed/audited before a manufacturing release.
"""
from pathlib import Path
import importlib.util
import json
import hashlib
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from cq_common import exportAssembly, interference, solid

MODULES=['01_frame_xy_cq','03_bed_z_cq','04_toolhead_cq','05_drives_cq','06_gantry_supports_cq']


def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/(name+'.py'))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m


def build():
    parts=[]
    names=MODULES+(['07_frame_bracing_cq'] if (ROOT/'07_frame_bracing_cq.py').exists() else [])
    for name in names:
        m=load(name);subset=m.build()
        for p in subset:p['builder']=name
        parts.extend(subset)
    return parts


def render(parts,path):
    import vtk
    points=vtk.vtkPoints();triangles=vtk.vtkCellArray()
    colors=vtk.vtkUnsignedCharArray();colors.SetNumberOfComponents(3)
    palette={'printed':(43,117,183),'cnc':(179,188,197),'purchased':(100,107,115),'fastener':(65,69,75)}
    for p in parts:
        s=solid(p['shape']);vertices,faces=s.tessellate(.2,.2)
        base=points.GetNumberOfPoints()
        for v in vertices:points.InsertNextPoint(v.x,v.y,v.z)
        color=palette.get(p.get('category'),(166,173,182))
        for a,b,c in faces:
            triangles.InsertNextCell(3);triangles.InsertCellPoint(base+a);triangles.InsertCellPoint(base+b);triangles.InsertCellPoint(base+c);colors.InsertNextTuple3(*color)
    data=vtk.vtkPolyData();data.SetPoints(points);data.SetPolys(triangles);data.GetCellData().SetScalars(colors)
    mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(data)
    actor=vtk.vtkActor();actor.SetMapper(mapper);actor.GetProperty().SetInterpolationToPhong()
    renderer=vtk.vtkRenderer();renderer.SetBackground(.97,.975,.985);renderer.AddActor(actor)
    camera=renderer.GetActiveCamera();camera.SetPosition(650,-850,620);camera.SetFocalPoint(0,0,155);camera.SetViewUp(0,0,1);camera.ParallelProjectionOn()
    renderer.ResetCamera();camera.Zoom(1.12)
    window=vtk.vtkRenderWindow();window.SetOffScreenRendering(1);window.SetSize(1400,1200);window.AddRenderer(renderer);window.Render()
    image=vtk.vtkWindowToImageFilter();image.SetInput(window);image.Update()
    writer=vtk.vtkPNGWriter();writer.SetFileName(str(path));writer.SetInputConnection(image.GetOutputPort());writer.Write();window.Finalize()


if __name__=='__main__':
    folder=ROOT/'exports'/'checkpoint010';folder.mkdir(parents=True,exist_ok=True)
    parts=build()
    exportAssembly(parts,folder,'CBP_RevF010_Assembly_DEVELOPMENT',individual=False)
    if '--audit' in sys.argv:
        hits=interference(parts,min_volume=.1,skip_categories=('fastener',))
        (folder/'INTERFERENCES-RAW.json').write_text(json.dumps(hits,indent=2)+'\n')
        print('Raw overlaps requiring exact mating-pair classification:',len(hits))
    source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('*.py')}
    (folder/'builder-hashes.json').write_text(json.dumps(source_hashes,indent=2)+'\n')
    render(parts,folder/'CBP_RevF010_Assembly_DEVELOPMENT.png')
