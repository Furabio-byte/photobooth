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
WOOD = mat("WOOD", (.78, .20, .58, 1), metal=0.0, rough=0.55, emit=0.0)
WOODD = mat("WOODD", (.34, .08, .28, 1), metal=0.0, rough=0.72, emit=0.0)
CHROME = mat("CHROME", (.18, .98, .96, 1), metal=0.55, rough=0.1, emit=1.0)
BLACK = mat("BLACK", (.03, .03, .05, 1), metal=0.0, rough=0.8, emit=0.0)
MIRROR = mat("MIRROR", (.84, .92, .96, 1), metal=0.8, rough=0.05, emit=0.0)
CURTAIN = mat("CURTAIN", (.98, .64, .16, 1), metal=0.0, rough=0.92, emit=0.0)
SIGNBG = mat("SIGNBG", (.05, .02, .08, 1), metal=0.0, rough=0.7, emit=3.0)
GOLD = mat("GOLD", (.22, 1.00, .68, 1), metal=0.15, rough=0.18, emit=2.5)
CHECKW = mat("CHECKW", (.95, .95, .95, 1), metal=0.0, rough=0.6, emit=0.0)
FLOOR = mat("FLOOR", (.08, .08, .14, 1), metal=0.0, rough=0.7, emit=0.0)
STOOL = mat("STOOL", (.15, .95, .85, 1), metal=0.0, rough=0.65, emit=0.0)
WALL = mat("WALL", (.08, .08, .12, 1), metal=0.0, rough=1.0, emit=0.0)
GROUND = mat("GROUND", (.05, .05, .08, 1), metal=0.0, rough=1.0, emit=0.0)

# Ambiente
box("bg_wall", (0, 4.8, 4.0), (12, 0.02, 8), WALL)
box("ground", (0, 0, -0.005), (12, 12, 0.01), GROUND)

# Struttura cabina
T = 0.06
W = 1.18
D = 1.02
H = 2.15
box("wall_L", (-0.560, 0.0, 1.075), (T, D, H), WOOD)
box("wall_R", (0.560, 0.0, 1.075), (T, D, H), WOOD)
box("wall_B", (0.0, 0.480, 1.075), (1.060, T, H), WOOD)
box("roof", (0.0, 0.0, 2.120), (1.18, 1.02, T), WOOD)
box("base", (0.0, 0.0, 0.030), (1.18, 1.02, T), CHROME)
box("front_L", (-0.260, -0.480, 1.075), (0.519, T, H), WOODD)
box("front_T", (0.212, -0.480, 1.970), (0.566, T, 0.34), WOODD)
box("trim_T", (0.0, 0.0, 2.060), (1.200, 1.060, 0.06), CHROME)
box("trim_B", (0.0, 0.0, 0.11), (1.200, 1.060, 0.06), CHROME)
box("inner_B", (0.212, 0.460, 0.975), (0.506, 0.02, 1.750), BLACK)
box("inner_top", (0.212, 0.0, 1.800), (0.506, 0.960, 0.02), BLACK)
box("m_frame", (-0.260, -0.500, 1.075), (0.330, 0.025, 1.462), BLACK)
box("m_glass", (-0.260, -0.505, 1.075), (0.283, 0.010, 1.376), MIRROR)

# Tenda
curtain_z = 1.075
curtain_y = -0.450
xs = [-0.0007999999999999674, 0.1058, 0.21239999999999998, 0.31899999999999995, 0.4255999999999999]
depths = [0.04, 0.06, 0.045, 0.06, 0.04]
strip_h = 1.655
for i, (x, d) in enumerate(zip(xs, depths)):
    box(f"curtain_{i}", (x, curtain_y, curtain_z), (0.103, d, strip_h), CURTAIN)
box("curtain_bar", (0.212, -0.460, 1.930), (0.566, 0.03, 0.03), CHROME)
box("coin", (-0.260, -0.505, 1.025), (0.165, 0.04, 0.20), BLACK)
box("slit", (-0.260, -0.510, 1.145), (0.130, 0.02, 0.02), CHROME)
box("label", (-0.260, -0.505, 0.795), (0.189, 0.03, 0.12), CHECKW)
box("seat", (0.332, 0.020, 0.48), (0.24, 0.24, 0.08), STOOL)
box("seat_leg", (0.332, 0.020, 0.24), (0.05, 0.05, 0.40), CHROME)

# Pavimento a scacchi
box("floor_base", (0.212, 0.184, 0.055), (0.521, 0.734, 0.015), BLACK)
tile = 0.096
start_x = 0.020
start_y = -0.080
for r in range(5):
    for c in range(5):
        m = CHECKW if (r + c) % 2 == 0 else FLOOR
        x = start_x + c * tile
        y = start_y + r * tile
        box(f"tile_{r}_{c}", (x, y, 0.065), (0.089, 0.089, 0.01), m)

# Insegna
box("sign_stem", (0.0, 0.0, 2.280), (0.10, 0.10, 0.22), CHROME)
box("sign_body", (0.0, 0.0, 2.500), (1.440, 0.24, 0.50), CHROME)
box("sign_panel", (0.0, -0.125, 2.500), (1.322, 0.02, 0.42), SIGNBG)
box("sg_top", (0.0, -0.125, 2.710), (1.322, 0.015, 0.03), GOLD)
box("sg_bot", (0.0, -0.125, 2.290), (1.322, 0.015, 0.03), GOLD)
box("sg_L", (-0.661, -0.125, 2.500), (0.015, 0.015, 0.45), GOLD)
box("sg_R", (0.661, -0.125, 2.500), (0.015, 0.015, 0.45), GOLD)
add_text_sign("NEON SNAP", (0.0, -0.138, 2.480), 0.18, GOLD)

add_lights()
add_camera((2.4, -2.8, 1.65), (74,0,40), 48)
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
