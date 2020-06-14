bl_info = {
    "name": "Blender Instant Denoise. By Moby Motion",
    "blender": (2, 82, 0),
    "category": "Object",
    "description": "Apply the new Intel denoiser in a single click.",
    "author": "Moby Motion",
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": ""
}

# Imports
import bpy

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

        # Create add node

        # Move add node to right of input nodes

        # Build links between input nodes and add node 

        return add_node

    def multiply(self, input_one, input_two):

        # Create multiply node

        # Move multiply node to right of input nodes

        # Build links between input nodes and multiply node 

        return multiply_node

    def denoise(self, input_socket_one, input_socket_two, 
                input_socket_three):

        # Create denoise node

        # Move denoise node to right of the input sockets

        # Build links between input sockets and denoise node

        return denoise_node

    def denoise_pass_type(self, pass_type):
        """ Given a pass type (diffuse, glossy or transmission), this 
        will denoise each light type (direct, indirect and colour), 
        and combine them appropriately"""

        light_types = ["direct", "indirect", "color"]

        # For type in light types, call self.denoise

        # Add together direct and indirect

        # Multiply the result of adding direct and indirect, with colour

        return

    def initialise_settings(self, context):

        scene = context.scene

        # Initialise important miscellaneous settings
        scene.use_nodes = True
        context.view_layer.cycles.denoising_store_passes = True

        # Enable necessary render layers
        context.scene.render.use_compositing = True

        # Enable advanced light passes that differentiate this class
        pass_types = ["diffuse", "glossy", "transmission"]
        light_types = ["direct", "indirect", "color"]

        for pass_type in pass_types:
            for light_type in light_types:

                code = ("scene.view_layers['View Layer'].use_pass_" + 
                        pass_type + "_" + light_type + " = True")

                exec(code)

        return

    def execute(self, context):
        """Called when blender runs this operator"""

        scene = context.scene

        self.initialise_settings(context)
        
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
    
