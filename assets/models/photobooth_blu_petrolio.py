"""
Blender Photo Booth Variant
Apri Blender → Scripting → Open → Run Script
Poi: Numpad0 per la camera, Z → Rendered
"""
import bpy, math

# Reset scena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

for data_block in [bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights, bpy.data.curves]:
    for item in list(data_block):
        try:
            if item.users == 0:
                data_block.remove(item)
        except:
            pass

def mat(name, color, metal=0.0, rough=0.7, emit=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    b = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(b.outputs[0], out.inputs[0])
    def set_input(n, v):
        if n in b.inputs:
            b.inputs[n].default_value = v
    set_input("Base Color", color)
    set_input("Metallic", metal)
    set_input("Roughness", rough)
    if emit > 0:
        set_input("Emission Color", color)
        set_input("Emission", color)
        set_input("Emission Strength", emit)
    return m

def box(name, loc, size, material):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = (size[0]*0.5, size[1]*0.5, size[2]*0.5)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.clear()
    o.data.materials.append(material)
    return o

def add_camera(loc, rot_deg_xyz=(74,0,40), lens=48):
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.active_object
    cam.rotation_euler = tuple(math.radians(v) for v in rot_deg_xyz)
    cam.data.lens = lens
    bpy.context.scene.camera = cam
    return cam

def add_lights():
    bpy.ops.object.light_add(type='AREA', location=(3.0, -2.5, 3.5))
    kl = bpy.context.active_object
    kl.data.energy = 900
    kl.data.size = 2.5
    kl.rotation_euler = (math.radians(50), 0, math.radians(-40))

    bpy.ops.object.light_add(type='AREA', location=(-2.5, -1.5, 2.5))
    fl = bpy.context.active_object
    fl.data.energy = 250
    fl.data.size = 3.0
    fl.rotation_euler = (math.radians(40), 0, math.radians(50))

    bpy.ops.object.light_add(type='POINT', location=(0.0, -0.30, 2.50))
    sl = bpy.context.active_object
    sl.data.energy = 60
    sl.data.color = (1.0, .95, .65)

def add_text_sign(text, loc, size, material, yrot=90):
    bpy.ops.object.text_add(location=loc)
    t = bpy.context.active_object
    t.data.body = text
    t.data.align_x = 'CENTER'
    t.data.align_y = 'CENTER'
    t.data.size = size
    t.data.extrude = 0.012
    t.data.bevel_depth = 0.003
    t.rotation_euler = (math.radians(yrot), 0, 0)
    t.data.materials.clear()
    t.data.materials.append(material)
    return t
WOOD = mat("WOOD", (.08, .22, .28, 1), metal=0.0, rough=0.72, emit=0.0)
WOODD = mat("WOODD", (.05, .14, .18, 1), metal=0.0, rough=0.78, emit=0.0)
CHROME = mat("CHROME", (.82, .84, .88, 1), metal=0.95, rough=0.12, emit=0.0)
BLACK = mat("BLACK", (.04, .04, .04, 1), metal=0.0, rough=0.8, emit=0.0)
MIRROR = mat("MIRROR", (.76, .86, .90, 1), metal=0.8, rough=0.05, emit=0.0)
CURTAIN = mat("CURTAIN", (.72, .56, .12, 1), metal=0.0, rough=0.95, emit=0.0)
SIGNBG = mat("SIGNBG", (.04, .10, .12, 1), metal=0.0, rough=0.7, emit=2.0)
GOLD = mat("GOLD", (.90, .92, .95, 1), metal=0.25, rough=0.22, emit=1.4)
CHECKW = mat("CHECKW", (.92, .92, .90, 1), metal=0.0, rough=0.6, emit=0.0)
FLOOR = mat("FLOOR", (.10, .12, .14, 1), metal=0.0, rough=0.7, emit=0.0)
STOOL = mat("STOOL", (.18, .55, .66, 1), metal=0.0, rough=0.72, emit=0.0)
WALL = mat("WALL", (.18, .22, .24, 1), metal=0.0, rough=1.0, emit=0.0)
GROUND = mat("GROUND", (.12, .15, .17, 1), metal=0.0, rough=1.0, emit=0.0)

# Ambiente
box("bg_wall", (0, 4.8, 4.0), (12, 0.02, 8), WALL)
box("ground", (0, 0, -0.005), (12, 12, 0.01), GROUND)

# Struttura cabina
T = 0.05
W = 0.9
D = 0.82
H = 1.9
box("wall_L", (-0.425, 0.0, 0.950), (T, D, H), WOOD)
box("wall_R", (0.425, 0.0, 0.950), (T, D, H), WOOD)
box("wall_B", (0.0, 0.385, 0.950), (0.800, T, H), WOOD)
box("roof", (0.0, 0.0, 1.875), (0.9, 0.82, T), WOOD)
box("base", (0.0, 0.0, 0.025), (0.9, 0.82, T), CHROME)
box("front_L", (-0.198, -0.385, 0.950), (0.396, T, H), WOODD)
box("front_T", (0.162, -0.385, 1.720), (0.432, T, 0.34), WOODD)
box("trim_T", (0.0, 0.0, 1.810), (0.920, 0.860, 0.06), CHROME)
box("trim_B", (0.0, 0.0, 0.11), (0.920, 0.860, 0.06), CHROME)
box("inner_B", (0.162, 0.360, 0.850), (0.372, 0.02, 1.500), BLACK)
box("inner_top", (0.162, 0.0, 1.550), (0.372, 0.760, 0.02), BLACK)
box("m_frame", (-0.198, -0.400, 0.950), (0.252, 0.025, 1.292), BLACK)
box("m_glass", (-0.198, -0.405, 0.950), (0.216, 0.010, 1.216), MIRROR)

# Tenda
curtain_z = 0.950
curtain_y = -0.350
xs = [0.016000000000000014, 0.08900000000000001, 0.162, 0.235, 0.308]
depths = [0.04, 0.06, 0.045, 0.06, 0.04]
strip_h = 1.463
for i, (x, d) in enumerate(zip(xs, depths)):
    box(f"curtain_{i}", (x, curtain_y, curtain_z), (0.079, d, strip_h), CURTAIN)
box("curtain_bar", (0.162, -0.360, 1.680), (0.432, 0.03, 0.03), CHROME)
box("coin", (-0.198, -0.405, 0.900), (0.126, 0.04, 0.20), BLACK)
box("slit", (-0.198, -0.410, 1.020), (0.099, 0.02, 0.02), CHROME)
box("label", (-0.198, -0.405, 0.670), (0.144, 0.03, 0.12), CHECKW)
box("seat", (0.282, 0.020, 0.48), (0.24, 0.24, 0.08), STOOL)
box("seat_leg", (0.282, 0.020, 0.24), (0.05, 0.05, 0.40), CHROME)

# Pavimento a scacchi
box("floor_base", (0.162, 0.148, 0.055), (0.397, 0.590, 0.015), BLACK)
tile = 0.073
start_x = 0.015
start_y = -0.080
for r in range(5):
    for c in range(5):
        m = CHECKW if (r + c) % 2 == 0 else FLOOR
        x = start_x + c * tile
        y = start_y + r * tile
        box(f"tile_{r}_{c}", (x, y, 0.065), (0.068, 0.068, 0.01), m)

# Insegna
box("sign_stem", (0.0, 0.0, 2.030), (0.10, 0.10, 0.22), CHROME)
box("sign_body", (0.0, 0.0, 2.250), (1.098, 0.24, 0.50), CHROME)
box("sign_panel", (0.0, -0.125, 2.250), (1.008, 0.02, 0.42), SIGNBG)
box("sg_top", (0.0, -0.125, 2.460), (1.008, 0.015, 0.03), GOLD)
box("sg_bot", (0.0, -0.125, 2.040), (1.008, 0.015, 0.03), GOLD)
box("sg_L", (-0.504, -0.125, 2.250), (0.015, 0.015, 0.45), GOLD)
box("sg_R", (0.504, -0.125, 2.250), (0.015, 0.015, 0.45), GOLD)
add_text_sign("BLUE BOOTH", (0.0, -0.138, 2.230), 0.18, GOLD)

add_lights()
add_camera((2.05, -2.25, 1.45), (74,0,40), 48)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 128
scene.render.resolution_x = 1400
scene.render.resolution_y = 1100

w = bpy.context.scene.world
if w and w.use_nodes:
    bg = w.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (.12, .12, .13, 1)
        bg.inputs[1].default_value = .4

print("Fatto! Numpad0 → Z → Rendered")
