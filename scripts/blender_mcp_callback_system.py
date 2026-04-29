"""
Blender MCP Callback System
Interactive feedback loop between Blender and Claude via screenshots and MCP pipeline

Usage:
1. Run this script in Blender's Script Editor (Alt+Tab → Script Editor)
2. It creates a callback handler that captures viewport screenshots
3. Send screenshots to Claude for review and analysis
4. Execute MCP commands to apply changes back to Blender
"""

import bpy
import json
import base64
import os
from datetime import datetime
from pathlib import Path

class BlenderMCPCallbackSystem:
    """Main callback system for Blender-Claude interaction"""
    
    def __init__(self, output_dir=None):
        self.output_dir = output_dir or Path(bpy.data.filepath).parent / "mcp_callbacks"
        self.output_dir.mkdir(exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.callback_log = []
        self.review_history = []
        
    def capture_viewport_screenshot(self, filename=None):
        """
        Capture current viewport as screenshot
        Returns: base64 encoded image data for Claude transmission
        """
        if not filename:
            filename = f"viewport_{len(self.callback_log):04d}.png"
        
        filepath = self.output_dir / self.session_id / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Get viewport area
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                # Render viewport to file
                bpy.context.window.view_layer = bpy.context.view_layer
                
                # Use compositor for screenshot (more reliable)
                scene = bpy.context.scene
                original_engine = scene.render.engine
                scene.render.engine = 'BLENDER_EEVEE'
                
                # Render to image
                bpy.ops.render.render(write_still=True)
                rendered_file = scene.render.filepath
                
                # Copy to MCP directory
                if os.path.exists(rendered_file):
                    import shutil
                    shutil.copy(rendered_file, str(filepath))
                
                # Restore
                scene.render.engine = original_engine
                break
        
        # Convert to base64 for Claude transmission
        with open(filepath, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        screenshot_record = {
            'timestamp': datetime.now().isoformat(),
            'filename': str(filepath),
            'base64': image_data,
            'scene_state': self.get_scene_state(),
        }
        
        self.callback_log.append(screenshot_record)
        return screenshot_record
    
    def get_scene_state(self):
        """Capture current Blender scene state for context"""
        scene = bpy.context.scene
        
        state = {
            'render_engine': scene.render.engine,
            'viewport_shading': self.get_viewport_shading(),
            'selected_objects': [obj.name for obj in bpy.context.selected_objects],
            'active_object': bpy.context.active_object.name if bpy.context.active_object else None,
            'camera': scene.camera.name if scene.camera else None,
            'frame_current': scene.frame_current,
            'frame_end': scene.frame_end,
            'resolution_x': scene.render.resolution_x,
            'resolution_y': scene.render.resolution_y,
            'sample_count': scene.cycles.samples if scene.render.engine == 'CYCLES' else None,
            'objects_count': len(bpy.data.objects),
            'materials_count': len(bpy.data.materials),
        }
        return state
    
    def get_viewport_shading(self):
        """Get current viewport shading mode"""
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        shading = space.shading
                        return {
                            'type': shading.type,
                            'use_scene_lights': shading.use_scene_lights,
                            'use_scene_world': shading.use_scene_world,
                        }
        return None
    
    def export_for_claude_review(self, screenshot_record=None):
        """
        Export screenshot and scene context as JSON for Claude analysis
        Returns: JSON string ready for MCP transmission
        """
        record = screenshot_record or self.callback_log[-1]
        
        review_payload = {
            'session_id': self.session_id,
            'review_request': {
                'image_base64': record['base64'],
                'scene_state': record['scene_state'],
                'timestamp': record['timestamp'],
                'callback_index': len(self.callback_log) - 1,
                'request_type': 'viewport_review',
                'questions': [
                    'What are the current visual issues or areas for improvement?',
                    'Are there material, lighting, or composition issues?',
                    'What rendering settings would improve quality?',
                    'Suggest specific Blender adjustments for better results.',
                ]
            }
        }
        
        return json.dumps(review_payload, indent=2)
    
    def apply_mcp_command(self, mcp_command):
        """
        Apply MCP command from Claude to modify Blender scene
        MCP commands are structured Python directives
        
        Example MCP commands:
        {
            "command": "set_render_engine",
            "params": {"engine": "CYCLES", "samples": 128}
        }
        """
        try:
            if mcp_command.get('command') == 'set_render_engine':
                bpy.context.scene.render.engine = mcp_command['params']['engine']
                if mcp_command['params']['engine'] == 'CYCLES':
                    bpy.context.scene.cycles.samples = mcp_command['params'].get('samples', 128)
                return {'status': 'success', 'command': mcp_command['command']}
            
            elif mcp_command.get('command') == 'set_viewport_shading':
                for area in bpy.context.screen.areas:
                    if area.type == 'VIEW_3D':
                        for space in area.spaces:
                            if space.type == 'VIEW_3D':
                                space.shading.type = mcp_command['params']['shading_type']
                return {'status': 'success', 'command': mcp_command['command']}
            
            elif mcp_command.get('command') == 'select_object':
                obj = bpy.data.objects.get(mcp_command['params']['object_name'])
                if obj:
                    bpy.context.view_layer.objects.active = obj
                    obj.select_set(True)
                    return {'status': 'success', 'command': mcp_command['command']}
            
            elif mcp_command.get('command') == 'render_viewport':
                scene = bpy.context.scene
                scene.render.filepath = str(self.output_dir / self.session_id / "render.png")
                bpy.ops.render.render(write_still=True)
                return {'status': 'success', 'command': mcp_command['command']}
            
            elif mcp_command.get('command') == 'adjust_material':
                obj_name = mcp_command['params']['object_name']
                material_name = mcp_command['params']['material_name']
                adjustments = mcp_command['params']['adjustments']
                
                obj = bpy.data.objects.get(obj_name)
                if obj and material_name in bpy.data.materials:
                    mat = bpy.data.materials[material_name]
                    # Apply adjustments (simplified)
                    if 'roughness' in adjustments:
                        mat.roughness = adjustments['roughness']
                    return {'status': 'success', 'command': mcp_command['command']}
            
            elif mcp_command.get('command') == 'set_camera_view':
                params = mcp_command['params']
                if 'camera_name' in params:
                    cam = bpy.data.objects.get(params['camera_name'])
                    if cam:
                        bpy.context.scene.camera = cam
                return {'status': 'success', 'command': mcp_command['command']}
            
            else:
                return {'status': 'unknown_command', 'command': mcp_command.get('command')}
        
        except Exception as e:
            return {'status': 'error', 'message': str(e), 'command': mcp_command.get('command')}
    
    def get_review_summary(self):
        """Generate summary of all reviews and changes"""
        summary = {
            'session_id': self.session_id,
            'total_screenshots': len(self.callback_log),
            'total_reviews': len(self.review_history),
            'screenshots': [
                {
                    'index': i,
                    'timestamp': record['timestamp'],
                    'scene_state': record['scene_state'],
                }
                for i, record in enumerate(self.callback_log)
            ],
            'review_history': self.review_history,
        }
        return json.dumps(summary, indent=2)


# ============================================================================
# USAGE EXAMPLE - Run in Blender Script Editor
# ============================================================================

if __name__ == "__main__":
    # Initialize system
    mcp_system = BlenderMCPCallbackSystem()
    
    print("✓ Blender MCP Callback System initialized")
    print(f"  Session ID: {mcp_system.session_id}")
    print(f"  Output directory: {mcp_system.output_dir}")
    
    # Example workflow:
    # 1. Capture viewport
    print("\n[1] Capturing viewport screenshot...")
    screenshot = mcp_system.capture_viewport_screenshot()
    print(f"    Screenshot saved: {screenshot['filename']}")
    
    # 2. Export for Claude review
    print("\n[2] Exporting for Claude review...")
    review_payload = mcp_system.export_for_claude_review()
    print("    Review payload ready (see console for JSON)")
    
    # 3. Example: Apply MCP command from Claude
    print("\n[3] Applying example MCP command...")
    example_command = {
        "command": "set_render_engine",
        "params": {"engine": "CYCLES", "samples": 256}
    }
    result = mcp_system.apply_mcp_command(example_command)
    print(f"    Result: {result}")
    
    # 4. Get review summary
    print("\n[4] Session summary:")
    print(mcp_system.get_review_summary())
    
    print("\n✓ System ready for Claude MCP integration")
