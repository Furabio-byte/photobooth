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
WOOD = mat("WOOD", (.34, .05, .06, 1), metal=0.0, rough=0.72, emit=0.0)
WOODD = mat("WOODD", (.20, .03, .04, 1), metal=0.0, rough=0.78, emit=0.0)
CHROME = mat("CHROME", (.74, .60, .22, 1), metal=0.85, rough=0.18, emit=0.0)
BLACK = mat("BLACK", (.04, .04, .04, 1), metal=0.0, rough=0.8, emit=0.0)
MIRROR = mat("MIRROR", (.80, .86, .88, 1), metal=0.8, rough=0.05, emit=0.0)
CURTAIN = mat("CURTAIN", (.88, .82, .70, 1), metal=0.0, rough=0.95, emit=0.0)
SIGNBG = mat("SIGNBG", (.08, .04, .03, 1), metal=0.0, rough=0.7, emit=2.0)
GOLD = mat("GOLD", (.96, .74, .18, 1), metal=0.7, rough=0.28, emit=1.8)
CHECKW = mat("CHECKW", (.94, .92, .88, 1), metal=0.0, rough=0.6, emit=0.0)
FLOOR = mat("FLOOR", (.10, .08, .06, 1), metal=0.0, rough=0.7, emit=0.0)
STOOL = mat("STOOL", (.72, .18, .18, 1), metal=0.0, rough=0.72, emit=0.0)
WALL = mat("WALL", (.26, .22, .18, 1), metal=0.0, rough=1.0, emit=0.0)
GROUND = mat("GROUND", (.20, .17, .14, 1), metal=0.0, rough=1.0, emit=0.0)

# Ambiente
box("bg_wall", (0, 4.8, 4.0), (12, 0.02, 8), WALL)
box("ground", (0, 0, -0.005), (12, 12, 0.01), GROUND)

# Struttura cabina
T = 0.055
W = 0.94
D = 0.88
H = 2.36
box("wall_L", (-0.442, 0.0, 1.180), (T, D, H), WOOD)
box("wall_R", (0.442, 0.0, 1.180), (T, D, H), WOOD)
box("wall_B", (0.0, 0.412, 1.180), (0.830, T, H), WOOD)
box("roof", (0.0, 0.0, 2.333), (0.94, 0.88, T), WOOD)
box("base", (0.0, 0.0, 0.028), (0.94, 0.88, T), CHROME)
box("front_L", (-0.207, -0.412, 1.180), (0.414, T, H), WOODD)
box("front_T", (0.169, -0.412, 2.180), (0.451, T, 0.34), WOODD)
box("trim_T", (0.0, 0.0, 2.270), (0.960, 0.920, 0.06), CHROME)
box("trim_B", (0.0, 0.0, 0.11), (0.960, 0.920, 0.06), CHROME)
box("inner_B", (0.169, 0.390, 1.080), (0.391, 0.02, 1.960), BLACK)
box("inner_top", (0.169, 0.0, 2.010), (0.391, 0.820, 0.02), BLACK)
box("m_frame", (-0.207, -0.430, 1.180), (0.263, 0.025, 1.605), BLACK)
box("m_glass", (-0.207, -0.435, 1.180), (0.226, 0.010, 1.510), MIRROR)

# Tenda
curtain_z = 1.180
curtain_y = -0.380
xs = [0.013600000000000029, 0.09140000000000001, 0.1692, 0.24699999999999997, 0.3248]
depths = [0.04, 0.06, 0.045, 0.06, 0.04]
strip_h = 1.817
for i, (x, d) in enumerate(zip(xs, depths)):
    box(f"curtain_{i}", (x, curtain_y, curtain_z), (0.082, d, strip_h), CURTAIN)
box("curtain_bar", (0.169, -0.390, 2.140), (0.451, 0.03, 0.03), CHROME)
box("coin", (-0.207, -0.435, 1.130), (0.132, 0.04, 0.20), BLACK)
box("slit", (-0.207, -0.440, 1.250), (0.103, 0.02, 0.02), CHROME)
box("label", (-0.207, -0.435, 0.900), (0.150, 0.03, 0.12), CHECKW)
box("seat", (0.289, 0.020, 0.48), (0.24, 0.24, 0.08), STOOL)
box("seat_leg", (0.289, 0.020, 0.24), (0.05, 0.05, 0.40), CHROME)

# Pavimento a scacchi
box("floor_base", (0.169, 0.158, 0.055), (0.415, 0.634, 0.015), BLACK)
tile = 0.077
start_x = 0.016
start_y = -0.080
for r in range(5):
    for c in range(5):
        m = CHECKW if (r + c) % 2 == 0 else FLOOR
        x = start_x + c * tile
        y = start_y + r * tile
        box(f"tile_{r}_{c}", (x, y, 0.065), (0.071, 0.071, 0.01), m)

# Insegna
box("sign_stem", (0.0, 0.0, 2.490), (0.10, 0.10, 0.22), CHROME)
box("sign_body", (0.0, 0.0, 2.710), (1.147, 0.24, 0.50), CHROME)
box("sign_panel", (0.0, -0.125, 2.710), (1.053, 0.02, 0.42), SIGNBG)
box("sg_top", (0.0, -0.125, 2.920), (1.053, 0.015, 0.03), GOLD)
box("sg_bot", (0.0, -0.125, 2.500), (1.053, 0.015, 0.03), GOLD)
box("sg_L", (-0.526, -0.125, 2.710), (0.015, 0.015, 0.45), GOLD)
box("sg_R", (0.526, -0.125, 2.710), (0.015, 0.015, 0.45), GOLD)
add_text_sign("RETRO PHOTO", (0.0, -0.138, 2.690), 0.18, GOLD)

add_lights()
add_camera((2.1, -2.7, 1.75), (74,0,40), 48)
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
