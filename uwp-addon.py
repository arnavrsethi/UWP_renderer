bl_info = {
    "name": "UWP Rendering",
    "blender": (2, 80, 0),
    "category": "Render",
}

import bpy
import socket

def render_on_uwp_server(render_task, server_ip, server_port):
    try:
        # Set up a socket connection to the UWP server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))
            s.send(render_task.encode())

            # Simulate rendering progress (update the progress property)
            for progress in range(1, 101):
                bpy.context.scene.uwp_rendering_progress = progress
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)  # Redraw the UI

            rendering_result = s.recv(1024).decode()

            # Display the rendering result in Blender's UI
            bpy.context.scene.uwp_rendering_result = rendering_result

    except ConnectionRefusedError:
        bpy.context.scene.uwp_rendering_result = "Connection refused. Check server settings."
    except Exception as e:
        bpy.context.scene.uwp_rendering_result = f"Error communicating with the server: {str(e)}"

    bpy.context.scene.uwp_rendering_progress = 0.0  # Reset progress when done

class UWPRenderingPanel(bpy.types.Panel):
    bl_label = "UWP Rendering"
    bl_idname = "PT_UWP_Rendering"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Render'

    def draw(self, context):
        layout = self.layout

        layout.label(text="Rendering Task:")
        layout.prop(context.scene, "uwp_rendering_task")

        layout.label(text="Server IP:")
        layout.prop(context.scene, "uwp_server_ip")

        layout.label(text="Server Port:")
        layout.prop(context.scene, "uwp_server_port")

        layout.operator("uwp.start_rendering")

class StartRenderingOperator(bpy.types.Operator):
    bl_idname = "uwp.start_rendering"
    bl_label = "Start Rendering"

    def execute(self, context):
        render_task = context.scene.uwp_rendering_task
        server_ip = context.scene.uwp_server_ip
        server_port = context.scene.uwp_server_port

        render_on_uwp_server(render_task, server_ip, server_port)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(UWPRenderingPanel)
    bpy.utils.register_class(StartRenderingOperator)
    bpy.types.Scene.uwp_rendering_task = bpy.props.StringProperty(name="Rendering Task", default="")
    bpy.types.Scene.uwp_server_ip = bpy.props.StringProperty(name="Server IP", default="127.0.0.1")
    bpy.types.Scene.uwp_server_port = bpy.props.IntProperty(name="Server Port", default=12345)
    bpy.types.Scene.uwp_rendering_result = bpy.props.StringProperty(name="Rendering Result", default="")
    bpy.types.Scene.uwp_rendering_progress = bpy.props.FloatProperty(name="Rendering Progress", default=0.0, min=0.0, max=100.0)

def unregister():
    bpy.utils.unregister_class(UWPRenderingPanel)
    bpy.utils.unregister_class(StartRenderingOperator)
    del bpy.types.Scene.uwp_rendering_task
    del bpy.types.Scene.uwp_server_ip
    del bpy.types.Scene.uwp_server_port
    del bpy.types.Scene.uwp_rendering_result
    del bpy.types.Scene.uwp_rendering_progress

if __name__ == "__main__":
    register()
