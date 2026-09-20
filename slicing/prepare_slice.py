import json, pathlib, hashlib, urllib.request, struct, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROFILES = pathlib.Path(r'C:\Program Files\OrcaSlicer\resources\profiles\Voron')
OUT = ROOT / 'slicing'
def flatten(kind, name):
    base=PROFILES if kind!='filament' else PROFILES.parent/'OrcaFilamentLibrary'
    matches=list((base/kind).rglob(name+'.json'))
    if len(matches)!=1: raise ValueError((name,matches))
    p=matches[0]
    d=json.loads(p.read_text(encoding='utf-8'))
    parent=d.get('inherits')
    out=flatten(kind,parent) if parent else {}
    out.update(d)
    out.pop('inherits',None)
    return out

machine=flatten('machine','Voron 0.1 0.5 nozzle')
process=flatten('process','0.20mm Standard @Voron')
filament=flatten('filament','Generic PLA @System')
machine.update(name='CBP analytical envelope', printer_settings_id='CBP analytical envelope',
    printable_area=['0x0','80x0','80x80','0x80'],printable_height='60',
    machine_start_gcode='; ANALYSIS ONLY - NOT FOR PRINTING\nG90\nM83',machine_end_gcode='; END ANALYSIS',
    before_layer_change_gcode='',layer_change_gcode='',change_filament_gcode='',
    gcode_flavor='klipper',use_relative_e_distances='1',retraction_length=['0.4'],retraction_speed=['40'],
    deretraction_speed=['40'],z_hop=['0'],machine_max_speed_x=['2000'],machine_max_speed_y=['2000'],
    machine_max_speed_z=['30'],machine_max_speed_e=['150'],
    machine_max_acceleration_x=['100000'],machine_max_acceleration_y=['100000'],
    machine_max_acceleration_z=['1000'],machine_max_acceleration_e=['20000'],
    machine_max_acceleration_extruding=['100000'],machine_max_acceleration_travel=['100000'],
    machine_max_jerk_x=['20'],machine_max_jerk_y=['20'])
process.update(name='CBP SBR analytical 0.25',print_settings_id='CBP SBR analytical 0.25',
    layer_height='0.25',initial_layer_print_height='0.25',wall_loops='2',top_shell_layers='3',
    bottom_shell_layers='3',top_shell_thickness='0',bottom_shell_thickness='0',
    sparse_infill_density='10%',sparse_infill_pattern='rectilinear',infill_combination='0',
    wall_generator='classic',detect_thin_wall='0',enable_support='0',enable_prime_tower='0',
    skirt_loops='0',skirt_height='0',brim_width='0',brim_type='no_brim',
    elephant_foot_compensation='0',elefant_foot_compensation='0',
    default_acceleration='100000',outer_wall_acceleration='100000',inner_wall_acceleration='100000',
    initial_layer_acceleration='100000',top_surface_acceleration='100000',travel_acceleration='100000',
    outer_wall_speed='1500',inner_wall_speed='1500',sparse_infill_speed='1500',
    internal_solid_infill_speed='1500',top_surface_speed='1500',gap_infill_speed='1500',
    initial_layer_speed='1500',initial_layer_infill_speed='1500',travel_speed='2000',
    bridge_speed='1500',internal_bridge_speed='1500',slow_down_for_overhangs='0',
    overhang_1_4_speed='1500',overhang_2_4_speed='1500',overhang_3_4_speed='1500',overhang_4_4_speed='1500',
    small_perimeter_speed='1500',bridge_flow='1',internal_bridge_flow='1',
    line_width='0.5',outer_wall_line_width='0.5',inner_wall_line_width='0.5',
    initial_layer_line_width='0.5',sparse_infill_line_width='0.5',internal_solid_infill_line_width='0.5',
    top_surface_line_width='0.5',gap_infill_line_width='0.5',support_line_width='0.5',
    reduce_crossing_wall='0',seam_position='nearest',arc_fitting='0')
filament.update(name='CBP PLA analysis',filament_settings_id=['CBP PLA analysis'],
    filament_type=['PLA'],filament_diameter=['1.75'],filament_density=['1.24'],filament_flow_ratio=['1'],
    filament_max_volumetric_speed=['500'],nozzle_temperature=['240'],nozzle_temperature_initial_layer=['240'],
    slow_down_for_layer_cooling=['0'],slow_down_layer_time=['0'],close_fan_the_first_x_layers=['0'],
    filament_start_gcode=[''],filament_end_gcode=[''])
for name,d in [('machine',machine),('process',process),('filament',filament)]:
    d.update(**{'from':'system','instantiation':'true'})
    d['compatible_printers']=['CBP analytical envelope']
    (OUT/(name+'.json')).write_text(json.dumps(d,indent=2)+'\n')
stl=OUT/'models/3DBenchy.stl'
b=stl.read_bytes(); n=struct.unpack_from('<I',b,80)[0]
mins=[float('inf')]*3; maxs=[-float('inf')]*3
for i in range(n):
    coords=struct.unpack_from('<9f',b,84+i*50+12)
    for j,v in enumerate(coords):
        k=j%3; mins[k]=min(mins[k],v);maxs[k]=max(maxs[k],v)
req=urllib.request.Request('https://api.github.com/repos/CreativeTools/3DBenchy/commits/master',headers={'User-Agent':'Codex-Benchy-Engineering'})
sha=json.load(urllib.request.urlopen(req))['sha']
provenance={'model':'Original CreativeTools single-part 3DBenchy','source':'https://github.com/CreativeTools/3DBenchy',
'commit':sha,'sha256':hashlib.sha256(b).hexdigest(),'triangles':n,'bounds_mm':[mins,maxs],
'dimensions_mm':[maxs[i]-mins[i] for i in range(3)],'scale':1,'slicer':'OrcaSlicer 2.3.2',
'profile_origin':'Installed Orca Voron generic defaults flattened, then overridden; no printer architecture is copied or selected.',
'warning':'Analytical toolpath only. Deliberately unattainable speed and flow caps expose motion/flow requirements. Do not print.'}
(OUT/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
print(json.dumps(provenance,indent=2))
