'''
This is the python script that converts a JSON of a scenario
into a Blender animation.

Felix Sosa
'''

import os
import bpy
import json
import sys

context = bpy.context
data = bpy.data
ops = bpy.ops
origin = (0, 0, 0)

# Helper functions

def create_sphere(r, name):
    '''
    Creates a sphere in blender of a given radius with a given name

    r -- radius of sphere
    name -- name of sphere
    '''
    bpy.ops.mesh.primitive_uv_sphere_add(location = (0,0,r), size = r)
    bpy.ops.object.shade_smooth()
    bpy.data.objects['Sphere'].name = name
    #bpy.data.objects['ball'].active_material.diffuse_color = (1.0, 0.0, 0.0)
    
def create_plane(radius, name):
    '''
    Creates a plane of a given radius

    radius -- radius of plane
    '''
    loc = (radius-5,radius-5,0)
    bpy.ops.mesh.primitive_plane_add(radius = radius, location = loc)
    bpy.data.objects['Plane'].name = name
    
def create_background(centerx, centery, r):
    me_background = data.meshes.new("BackgroundMesh")
    background = data.objects.new("background", me_background)
    scn = context.scene
    scn.objects.link(background)
    scn.objects.active = background
    background.select = True

    background_verts = [(centerx-r, centery-r, -1), (centerx-r, centery+r, -1), (centerx+r, centery+r, -1), (centerx+r, centery-r, -1)]
    background_faces = [[0, 1, 2, 3]]

    me_background.from_pydata(background_verts, [], background_faces)

    me_background.update()

def create_material(r, g, b):
    new_material = data.materials.new(name="MyNewMaterial")
    new_material.diffuse_color = (r, g, b)
    return new_material

def create_empty_material():
    new_material = data.materials.new(name="MyNewMaterial")
    return new_material

def assign_materials(ob, mat):
    if data.objects[ob].data.materials:
       data.objects[ob].data.materials[0] = mat
    else:
        data.objects[ob].data.materials.append(mat)     

def create_empty_material():
    new_material = data.materials.new(name="MyNewMaterial")
    return new_material
# Main

def init():   
    # Unpack json file for a given simulation
    simulation_data = json.load(open(sys.argv[-1]))
    radius = simulation_data['config']['scene']/100.0
    simulation_id = simulation_data['config']['name']

    #Camera Settings
    data.objects['Camera'].location.x = radius/2.0
    data.objects['Camera'].location.y = radius/2.0
    data.objects['Camera'].location.z = 12
    data.objects['Camera'].rotation_euler.x = 0
    data.objects['Camera'].rotation_euler.y = 0
    data.objects['Camera'].rotation_euler.z = 0
    # Point light settings
    data.objects['Point'].location.x = radius/2.0+2
    data.objects['Point'].location.y = radius/2.0
    data.objects['Point'].location.z = 9
    data.objects['Point'].rotation_euler.x = 0
    data.objects['Point'].rotation_euler.y = 0
    data.objects['Point'].rotation_euler.z = 0
    
    # Radius of spheres
    ball_r = 0.25
   
    plane_mat = create_empty_material()
    
    # Material for plane is an image
    image_path = os.path.expanduser('sand.jpg')
    try:
        img = bpy.data.images.load(image_path)
    except:
        raise NameError("Cannot load image %s" % image_path)    
    mat_name = "MyMaterial"
    plane_mat = (bpy.data.materials.get(mat_name) or
           bpy.data.materials.new(mat_name))
    plane_mat.use_nodes = True
    nt = plane_mat.node_tree
    nodes = nt.nodes
    links = nt.links
    while(nodes): nodes.remove(nodes[0])
    output  = nodes.new("ShaderNodeOutputMaterial")
    diffuse = nodes.new("ShaderNodeBsdfDiffuse")
    texture = nodes.new("ShaderNodeTexImage")
    uvmap   = nodes.new("ShaderNodeTexCoord")
    texture.image = bpy.data.images.load(image_path)
    links.new( output.inputs['Surface'], diffuse.outputs['BSDF'])
    links.new(diffuse.inputs['Color'], texture.outputs['Color'])
    links.new(texture.inputs['Vector'], uvmap.outputs['Window'])

    # Materials for the spheres
    agent_mat = bpy.data.materials.get('agent')
    patient_mat = bpy.data.materials.get('patient')
    fireball_mat = bpy.data.materials.get('fireball')

    # Create the spheres and plane
    create_sphere(ball_r, 'agent')
    create_sphere(ball_r, 'patient')
    create_sphere(ball_r, 'fireball')
    create_plane(radius, 'plane')
    
    context.scene.camera.data.clip_start = 0
    context.scene.camera.data.clip_end = 100
    
    # Assign spheres and floor their intended materials
    assign_materials('agent', agent_mat)
    assign_materials('patient', patient_mat)
    assign_materials('fireball', fireball_mat)
    assign_materials('plane', plane_mat)

    # Grab the objects in the scene
    agent = bpy.data.objects.get('agent')
    patient = bpy.data.objects.get('patient')
    fireball = bpy.data.objects.get('fireball')
    plane = bpy.data.objects.get('plane')

    # Move agents around scene and render each frame and save it as an image
    for idx in range(25, simulation_data['config']['ticks']):
        # Move agent
        agent.location.x = (simulation_data['objects']['agent'][idx]['x']/100.0)
        agent.location.y = ((simulation_data['objects']['agent'][idx]['y']/100.0) + 2)
        # Move patient
        patient.location.x = (simulation_data['objects']['patient'][idx]['x']/100.0)
        patient.location.y = ((simulation_data['objects']['patient'][idx]['y']/100.0) + 2)
        # Move fireball
        fireball.location.x = (simulation_data['objects']['fireball'][idx]['x']/100.0)
        fireball.location.y = ((simulation_data['objects']['fireball'][idx]['y']/100.0) + 2)

        bpy.context.scene.render.engine = "CYCLES"
        bpy.data.scenes['Scene'].cycles.device = 'GPU'
        bpy.data.scenes['Scene'].cycles.film_exposure = 9.0
        bpy.context.scene.render.filepath = './rendered_images/{0}/image{1}'.format(simulation_id,idx)
        ops.render.render(write_still = True)

    # Patient-Fireball collision, create sphere for fire on Patient
    create_sphere(0.15, 'patient_fire')
    patient_fire = bpy.data.objects.get('patient_fire')
    patient_fire.location.x = patient.location.x
    patient_fire.location.y = patient.location.y

    # Deselect all but the patient_fire
    agent.select = False
    patient.select = False
    fireball.select = False
    plane.select = False
    patient_fire.select = True

    # Initiate fire animation on patient
    ops.object.modifier_add(type='SMOKE')
    ops.object.material_slot_add()
    ops.object.quick_smoke()
    
    # Save time with variable names.
    mat = bpy.context.object.active_material
    mat.use_nodes = True
    material_output = mat.node_tree.nodes['Material Output']

    # Delete every node but 'Material Output'
    for k in mat.node_tree.nodes.keys():
        if k != 'Material Output':
            mat.node_tree.nodes.remove(mat.node_tree.nodes[k])

    # Always use material_output as reference.
    x,y = material_output.location

    # Add all nodes
    volume_scatter = mat.node_tree.nodes.new('ShaderNodeVolumeScatter')
    volume_scatter.location = (x - 450, y)

    volume_abs = mat.node_tree.nodes.new('ShaderNodeVolumeAbsorption')
    volume_abs.location = (x - 450, y - 150)

    add_shader1 = mat.node_tree.nodes.new('ShaderNodeAddShader')
    add_shader1.location = (x - 300, y)

    add_shader2 = mat.node_tree.nodes.new('ShaderNodeAddShader')
    add_shader2.location = (x - 150, y)

    emission = mat.node_tree.nodes.new('ShaderNodeEmission')
    emission.location = (x - 300, y - 200)

    color_ramp = mat.node_tree.nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (x - 550, y - 300)

    attr_flame = mat.node_tree.nodes.new('ShaderNodeAttribute')
    attr_flame.location = (x - 700, y - 400)

    attr_density = mat.node_tree.nodes.new('ShaderNodeAttribute')
    attr_density.location = (x - 800, y)

    bright_contr = mat.node_tree.nodes.new('ShaderNodeBrightContrast')
    bright_contr.location = (x - 600, y)

    # Link nodes together.
    mat.node_tree.links.new(add_shader2.outputs['Shader'], material_output.inputs['Volume'])
    mat.node_tree.links.new(add_shader1.outputs['Shader'], add_shader2.inputs['Shader'])
    mat.node_tree.links.new(emission.outputs['Emission'], add_shader2.inputs[1])
    mat.node_tree.links.new(color_ramp.outputs[0], emission.inputs[0])
    mat.node_tree.links.new(attr_flame.outputs[2], color_ramp.inputs[0])
    mat.node_tree.links.new(volume_scatter.outputs[0], add_shader1.inputs[0])
    mat.node_tree.links.new(volume_abs.outputs[0], add_shader1.inputs[1])
    mat.node_tree.links.new(bright_contr.outputs[0], volume_scatter.inputs[1])
    mat.node_tree.links.new(bright_contr.outputs[0], volume_abs.inputs[1])
    mat.node_tree.links.new(attr_density.outputs[2], bright_contr.inputs[0])

    # Change attribute names for density and flame.
    attr_density.attribute_name = 'density'
    attr_flame.attribute_name = 'flame'

    # Change colors in color ramp.
    color_ramp.color_ramp.elements[1].color = (1, 1, 1, 0.75)
    color_ramp.color_ramp.elements.new(0.75)
    color_ramp.color_ramp.elements[1].color = (0.509, 0.437, 0.057, 1)
    color_ramp.color_ramp.elements.new(0.5)
    color_ramp.color_ramp.elements[1].color = (0.541, 0.165, 0, 1)
    color_ramp.color_ramp.elements.new(0.25)
    color_ramp.color_ramp.elements[1].color = (0.189, 0.022, 0, 1)

    # Increase smoke density using contrast.
    bright_contr.inputs[2].default_value = 5
    # Have fire animation last for n frames
    data.scenes['Scene'].frame_start = 0
    data.scenes['Scene'].frame_end = 50
    data.objects[patient_fire.name].modifiers["Smoke"].flow_settings.smoke_flow_type = 'FIRE'
    data.objects["Smoke Domain"].modifiers["Smoke"].domain_settings.use_high_resolution = True

    # Render animation and save image of each frame
    ops.render.render(write_still = True, animation=True)
    bpy.context.scene.render.filepath = './rendered_images/{0}/image{1}##'.format(simulation_id,idx) 
    
def clear_textures():
    for tex in data.textures:
        data.textures.remove(tex)

def kill_meshes():
    bpy.ops.object.select_by_type(type='MESH')
    # remove all selected.
    bpy.ops.object.delete()

    # remove the meshes, they have no users anymore.
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)
        
clear_textures()
kill_meshes()
init()
