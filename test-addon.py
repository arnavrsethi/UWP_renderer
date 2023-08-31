bl_info = {
    "name": "My Add-on",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import socket

def my_function():
    
    class RenderingAddonPanel(bpy.types.Panel):
        bl_label = "UWP Rendering - Source"  # Updated title
        bl_idname = "PT_UWP_Rendering"
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'
        bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        # Input field for rendering task
        layout.label(text="Enter rendering task:")
        layout.prop(context.scene, "uwp_rendering_task")

        # Server settings
        layout.label(text="Server Settings:")
        layout.prop(context.scene, "uwp_server_ip")
        layout.prop(context.scene, "uwp_server_port")

        # Progress bar
        layout.prop(context.scene, "uwp_rendering_progress", text="Progress")

        # Button to start rendering
        layout.operator("uwp.start_rendering", text="Start Rendering")

        # Display rendering result
        layout.label(text="Rendering Result:")
        layout.label(text=context.scene.uwp_rendering_result)


    class StartRenderingOperator(bpy.types.Operator):
        bl_idname = "uwp.start_rendering"
        bl_label = "Start Rendering"

        def execute(self, context):
            # Get the rendering task, server IP, and server port from the UI input
            rendering_task = context.scene.uwp_rendering_task
            server_ip = context.scene.uwp_server_ip
            server_port = context.scene.uwp_server_port

            try:
                # Set up a socket connection to the UWP server
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((server_ip, server_port))
                    s.send(rendering_task.encode())

                    # Simulate rendering progress (update the progress property)
                    for progress in range(1, 101):
                        bpy.context.scene.uwp_rendering_progress = progress / 100.0  # Update progress property
                        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)  # Redraw the UI

                        # In a real scenario, you'd update the progress based on actual rendering progress

                    rendering_result = s.recv(1024).decode()

                    # Display the rendering result in Blender's UI
                    context.scene.uwp_rendering_result = rendering_result

            except ConnectionRefusedError:
                self.report({'ERROR'}, "Connection refused. Check server settings.")
            except Exception as e:
                self.report({'ERROR'}, f"Error communicating with the server: {str(e)}")

            bpy.context.scene.uwp_rendering_progress = 0.0  # Reset progress when done
            return {'FINISHED'}

def register():
    bpy.utils.register_class(MyOperator)

def unregister():
    bpy.utils.unregister_class(MyOperator)

class MyOperator(bpy.types.Operator):
    bl_idname = "object.my_operator"
    bl_label = "My Operator"

    def execute(self, context):
        my_function()
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(MyOperator.bl_idname)

def register():
    bpy.utils.register_class(MyOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(MyOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
