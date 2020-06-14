bl_info = {
    "name": "Blender Instant Denoise. By Moby Motion",
    "blender": (2, 82, 0),
    "category": "Object",
    "description": "Apply the new Intel denoiser in a single click.",
    "author": "Moby Motion",
    "version": (0, 1, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": ""
}

# Imports
import bpy

import numpy as np 

# Classes
class InstantDenoise(bpy.types.Operator):
    """Apply the new Intel denoiser in a single click."""
    bl_idname = "object.instantdenoise"
    bl_label = "Denoise"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Called when blender runs this operator"""

        scene = context.scene

        # Initialise important settings
        scene.use_nodes = True
        context.view_layer.cycles.denoising_store_passes = True
        context.scene.render.use_compositing = True

        # Clear any existing nodes
        tree = scene.node_tree

        for node in tree.nodes:
            tree.nodes.remove(node)

        # Set up new nodes
        render_layers_node = tree.nodes.new(type='CompositorNodeRLayers')
        render_layers_node.location = 0, 0
        denoise_node = tree.nodes.new(type="CompositorNodeDenoise")
        denoise_node.location = 300, 0
        composite_node = tree.nodes.new(type='CompositorNodeComposite')
        composite_node.location = 600, 0

        # Link new nodes        
        tree.links.new(
            render_layers_node.outputs['Noisy Image'], 
            denoise_node.inputs['Image'])
        tree.links.new(
            render_layers_node.outputs['Denoising Albedo'], 
            denoise_node.inputs['Albedo'])
        tree.links.new(
            render_layers_node.outputs['Denoising Normal'], 
            denoise_node.inputs['Normal'])

        tree.links.new(
            denoise_node.outputs['Image'], 
            composite_node.inputs['Image'])

        return {'FINISHED'}

class InstantAdvancedDenoise(bpy.types.Operator):
    """Apply the new Intel denoiser in a single click."""
    bl_idname = "object.instantadvanceddenoise"
    bl_label = "Advanced Denoise"
    bl_options = {'REGISTER', 'UNDO'}

    def add(self, input_one, input_two):
        """Expects 2 denoise nodes as "input". These only have a single 
        output, which is why you have to specify socket"""

        tree = self.scene.node_tree

        # Get locations of inputs
        location_one = np.array(input_one.location)
        location_two = np.array(input_two.location)
        mean_location = np.mean([location_one, location_two], axis=0)

        # Create add node
        add_node = tree.nodes.new(type="CompositorNodeMath")
        add_node.hide = True
        add_node.operation = "ADD"

        # Move add node to right of input nodes
        add_node.location = mean_location + [300, 0]

        # Build links between input nodes and add node 
        tree.links.new(input_one.outputs[0], add_node.inputs[0])
        tree.links.new(input_two.outputs[0], add_node.inputs[1])

        return add_node

    def multiply(self, input_one, input_two):
        """Expects 2 denoise nodes as "input". These only have a single 
        output, which is why you have to specify socket"""

        tree = self.scene.node_tree

        # Get locations of inputs
        location_one = np.array(input_one.location)
        location_two = np.array(input_two.location)
        mean_location = np.mean([location_one, location_two], axis=0)

        # Create multiply node
        multiply_node = tree.nodes.new(type="CompositorNodeMixRGB")
        multiply_node.hide = True
        multiply_node.blend_type = "MULTIPLY"

        # Move multiply node to right of input nodes
        multiply_node.location = mean_location + [300, 0]

        # Build links between input nodes and add node 
        tree.links.new(input_one.outputs[0], multiply_node.inputs[0])
        tree.links.new(input_two.outputs[0], multiply_node.inputs[1])

        return multiply_node

    def denoise(self, input_socket_one, input_socket_two, 
        input_socket_three, location_offset=[300, 0]):
        """Input sockets are required, because this affects a node 
        with a large number of output sockets"""

        tree = self.scene.node_tree

        # Get locations of inputs
        location_one = np.array(self.render_layers_node.location)
        location_two = np.array(self.render_layers_node.location)
        location_three = np.array(self.render_layers_node.location)

        mean_location = np.mean(
            [location_one, location_two, location_three], axis=0)

        # Create denoise node
        denoise_node = tree.nodes.new(type="CompositorNodeDenoise")
        denoise_node.hide = True

        # Move denoise node to right of the input sockets
        denoise_node.location = mean_location + location_offset

        # Build links between input sockets and denoise node
        tree.links.new(
            input_socket_one, denoise_node.inputs["Image"])
        tree.links.new(
            input_socket_two, denoise_node.inputs["Normal"])
        tree.links.new(
            input_socket_three, denoise_node.inputs["Albedo"])

        return denoise_node

    def denoise_pass_type(self, pass_type="Diff"):
        """ Given a pass type (diffuse, glossy or transmission), this 
        will denoise each light type (direct, indirect and colour), 
        and combine them appropriately"""

        light_types = ["Dir", "Ind", "Col"]

        light_type_offset = {"Dir": 0, "Ind": -50, "Col": -100}
        pass_type_offset = {"Diff": 0, "Gloss": -300, "Trans": -600}

        denoise_nodes = {}

        # For type in light types, call self.denoise
        for i, light_type in enumerate(light_types):

            socket_one = self.render_layers_node.outputs[pass_type + light_type]
            socket_two  = self.render_layers_node.outputs["Denoising Normal"]
            socket_three  = self.render_layers_node.outputs["Denoising Albedo"]
            location_offset = [300, light_type_offset[light_type] + pass_type_offset[pass_type]]

            denoise_node = self.denoise(
                socket_one, socket_two, socket_three, location_offset)

            denoise_nodes[light_type] = denoise_node

        # Add together direct and indirect
        add_node = self.add(denoise_nodes["Dir"], denoise_nodes["Ind"])

        # Multiply the result of adding direct and indirect, with colour
        multiply_node = self.multiply(add_node, denoise_nodes["Col"])

        return multiply_node

    def initialise_settings(self):

        # Initialise important miscellaneous settings
        self.scene.use_nodes = True
        self.context.view_layer.cycles.denoising_store_passes = True

        # Enable necessary render layers
        self.context.scene.render.use_compositing = True

        # Enable advanced light passes that differentiate this class
        pass_types = ["diffuse", "glossy", "transmission"]
        light_types = ["direct", "indirect", "color"]

        for pass_type in pass_types:
            for light_type in light_types:

                code = ("self.scene.view_layers['View Layer'].use_pass_" + 
                        pass_type + "_" + light_type + " = True")

                exec(code)

        return

    def execute(self, context):
        """Called when blender runs this operator"""

        scene = context.scene
        self.context = context
        self.scene = scene

        self.initialise_settings()
        
        # Clear any existing nodes
        tree = scene.node_tree

        for node in tree.nodes:
            tree.nodes.remove(node)

        # Set up input and output nodes
        self.render_layers_node = tree.nodes.new(type='CompositorNodeRLayers')
        self.render_layers_node.location = 0, 0
        # denoise_node = tree.nodes.new(type="CompositorNodeDenoise")
        # denoise_node.location = 300, 0
        self.composite_node = tree.nodes.new(type='CompositorNodeComposite')
        self.composite_node.location = 2000, 0

        # Set up other nodes
        diffuse_multiply_node = self.denoise_pass_type("Diff")
        glossy_multiply_node = self.denoise_pass_type("Gloss")
        transmission_multiply_node = self.denoise_pass_type("Trans")

        diffuse_and_glossy = self.add(
            diffuse_multiply_node, glossy_multiply_node)
        final_addition = self.add(
            diffuse_and_glossy, transmission_multiply_node)

        tree.links.new(
            final_addition.outputs[0], 
            self.composite_node.inputs['Image'])

        return {'FINISHED'}


class InstantDenoisePanel(bpy.types.Panel):
    """The primary panel for Blender AutoFocus"""
    bl_label = "Instant AI denoise"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        
        row = layout.row()
        row.label(text="Click to apply Intel AI denoising", icon='CAMERA_DATA')

        row = layout.row()
        row.operator("object.instantdenoise")

        row = layout.row()
        row.operator("object.instantadvanceddenoise")


# Register classes
classes = (
    InstantDenoisePanel,
    InstantDenoise,
    InstantAdvancedDenoise,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

# Allows script to run directly from Blender's Text editor
if __name__ == "__main__":
    register()
    
