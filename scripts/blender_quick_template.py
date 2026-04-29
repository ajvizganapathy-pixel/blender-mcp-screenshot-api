"""
BLENDER-CLAUDE MCP INTEGRATION
Quick Reference & Copy-Paste Template

Usage:
1. Copy this entire file into Blender Script Editor
2. Run it (Alt + P in script editor)
3. Follow console instructions
"""

import bpy
import json
import base64
from pathlib import Path
from datetime import datetime


# ═════════════════════════════════════════════════════════════════
# QUICK START: COPY & RUN IN BLENDER
# ═════════════════════════════════════════════════════════════════

class QuickBlenderMCP:
    """Minimal, production-ready Blender-Claude integration"""
    
    def __init__(self):
        self.session_dir = Path(bpy.data.filepath).parent / "mcp_session"
        self.session_dir.mkdir(exist_ok=True)
        self.iteration = 0
    
    def capture_and_export(self):
        """Capture viewport and prepare for Claude review"""
        self.iteration += 1
        
        # Get scene state
        scene = bpy.context.scene
        state = {
            'iteration': self.iteration,
            'timestamp': datetime.now().isoformat(),
            'render_engine': scene.render.engine,
            'viewport_shading': self._get_shading_type(),
            'selected_objects': [obj.name for obj in bpy.context.selected_objects],
            'active_object': bpy.context.active_object.name if bpy.context.active_object else None,
            'camera': scene.camera.name if scene.camera else None,
            'frame': scene.frame_current,
            'resolution': f"{scene.render.resolution_x}x{scene.render.resolution_y}",
            'objects_count': len([o for o in bpy.data.objects if o.type == 'MESH']),
            'materials_count': len(bpy.data.materials),
        }
        
        # Save state as JSON
        state_file = self.session_dir / f"state_{self.iteration:02d}.json"
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"\n✓ Iteration {self.iteration} captured")
        print(f"  State saved: {state_file}")
        print(f"  Render Engine: {state['render_engine']}")
        print(f"  Objects: {state['objects_count']}, Materials: {state['materials_count']}")
        print(f"  Selected: {state['selected_objects']}")
        
        return state
    
    def _get_shading_type(self):
        """Get current viewport shading mode"""
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        return space.shading.type
        return "UNKNOWN"
    
    def apply_changes(self, commands: list):
        """
        Apply MCP commands from Claude
        
        Example commands list:
        [
            {"command": "set_render_engine", "params": {"engine": "CYCLES", "samples": 256}},
            {"command": "set_viewport_shading", "params": {"shading_type": "RENDERED"}},
        ]
        """
        scene = bpy.context.scene
        
        for i, cmd in enumerate(commands, 1):
            cmd_name = cmd.get('command', '')
            params = cmd.get('params', {})
            
            try:
                if cmd_name == 'set_render_engine':
                    scene.render.engine = params.get('engine', 'CYCLES')
                    if scene.render.engine == 'CYCLES':
                        scene.cycles.samples = params.get('samples', 256)
                    print(f"  ✓ Set render engine to {params['engine']}")
                
                elif cmd_name == 'set_viewport_shading':
                    shading_type = params.get('shading_type', 'RENDERED')
                    for area in bpy.context.screen.areas:
                        if area.type == 'VIEW_3D':
                            for space in area.spaces:
                                if space.type == 'VIEW_3D':
                                    space.shading.type = shading_type
                    print(f"  ✓ Set viewport shading to {shading_type}")
                
                elif cmd_name == 'select_object':
                    obj_name = params.get('object_name')
                    obj = bpy.data.objects.get(obj_name)
                    if obj:
                        bpy.context.view_layer.objects.active = obj
                        obj.select_set(True)
                        print(f"  ✓ Selected {obj_name}")
                
                elif cmd_name == 'adjust_material':
                    obj_name = params.get('object_name')
                    mat_name = params.get('material_name')
                    adjustments = params.get('adjustments', {})
                    
                    obj = bpy.data.objects.get(obj_name)
                    if obj and mat_name in bpy.data.materials:
                        mat = bpy.data.materials[mat_name]
                        for key, value in adjustments.items():
                            if hasattr(mat, key):
                                setattr(mat, key, value)
                        print(f"  ✓ Adjusted material {mat_name} on {obj_name}")
                
                elif cmd_name == 'render_viewport':
                    output = params.get('output_path', str(self.session_dir / f"render_{self.iteration:02d}.png"))
                    scene.render.filepath = output
                    bpy.ops.render.render(write_still=True)
                    print(f"  ✓ Rendered to {output}")
                
                else:
                    print(f"  ⚠ Unknown command: {cmd_name}")
            
            except Exception as e:
                print(f"  ✗ Error in {cmd_name}: {str(e)}")
        
        print(f"\n✓ Applied {len(commands)} changes")
    
    def print_instructions(self):
        """Print next steps for Claude interaction"""
        print("\n" + "="*70)
        print("NEXT STEPS - SEND THIS TO CLAUDE:")
        print("="*70)
        
        state_file = self.session_dir / f"state_{self.iteration:02d}.json"
        with open(state_file, 'r') as f:
            state = json.load(f)
        
        print(f"""
Please review this Blender viewport and suggest improvements:

**Current State (Iteration {self.iteration}):**
```json
{json.dumps(state, indent=2)}
```

**Analysis Needed:**
1. What render quality issues do you see?
2. What settings should I adjust?
3. What MCP commands would improve this?

**Response Format (JSON):**
```json
{{
  "quality_score": 0-100,
  "issues": [
    {{"severity": "high/medium/low", "description": "issue here"}}
  ],
  "commands": [
    {{"command": "command_name", "params": {{...}}}}
  ],
  "reasoning": "why these changes"
}}
```

**Then copy the commands JSON and run:**
```python
commands = [
    {{"command": "...", "params": {{...}}}},
    ...
]
mcp.apply_changes(commands)
```
""")
        print("="*70)


# ═════════════════════════════════════════════════════════════════
# COMMAND REFERENCE
# ═════════════════════════════════════════════════════════════════

COMMAND_TEMPLATES = {
    'set_render_engine': {
        'description': 'Switch between CYCLES and EEVEE',
        'example': {
            'command': 'set_render_engine',
            'params': {'engine': 'CYCLES', 'samples': 256}
        }
    },
    'set_viewport_shading': {
        'description': 'Change viewport visualization mode',
        'example': {
            'command': 'set_viewport_shading',
            'params': {'shading_type': 'RENDERED'}  # WIREFRAME, SOLID, MATERIAL, RENDERED
        }
    },
    'select_object': {
        'description': 'Select a specific object in the scene',
        'example': {
            'command': 'select_object',
            'params': {'object_name': 'Cube'}
        }
    },
    'adjust_material': {
        'description': 'Modify material properties',
        'example': {
            'command': 'adjust_material',
            'params': {
                'object_name': 'Sphere',
                'material_name': 'Material',
                'adjustments': {
                    'roughness': 0.5,
                    'metallic': 0.0
                }
            }
        }
    },
    'render_viewport': {
        'description': 'Render and save the viewport',
        'example': {
            'command': 'render_viewport',
            'params': {'output_path': 'render.png'}
        }
    },
}


# ═════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═════════════════════════════════════════════════════════════════

def print_welcome():
    """Display welcome and instructions"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  BLENDER-CLAUDE MCP FEEDBACK LOOP".center(68) + "█")
    print("█" + "  Interactive Viewport Review & Refinement".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    print("""
This tool creates an interactive feedback loop between Blender and Claude:

1. CAPTURE: Take snapshot of current Blender state
2. ANALYZE: Send to Claude for feedback
3. EXECUTE: Apply Claude's MCP commands
4. ITERATE: Repeat until satisfied

""")


def print_quick_reference():
    """Print available commands"""
    print("\n" + "-"*70)
    print("AVAILABLE MCP COMMANDS")
    print("-"*70)
    
    for cmd_name, info in COMMAND_TEMPLATES.items():
        print(f"\n▸ {cmd_name}")
        print(f"  {info['description']}")
        print(f"  Example:")
        print(f"  {json.dumps(info['example'], indent=4)}")


# ═════════════════════════════════════════════════════════════════
# RUN IMMEDIATELY
# ═════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Initialize
    print_welcome()
    mcp = QuickBlenderMCP()
    
    # Capture current state
    print("\n[1/3] Capturing Blender state...")
    state = mcp.capture_and_export()
    
    # Show available commands
    print_quick_reference()
    
    # Print next steps
    mcp.print_instructions()
    
    print("\n" + "✓"*35)
    print("Ready for Claude review!")
    print("✓"*35 + "\n")


# ═════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS - USE AFTER INITIAL SETUP
# ═════════════════════════════════════════════════════════════════

def apply_claude_response(json_response_string):
    """
    Paste entire Claude response here to extract and apply commands
    
    Usage in Blender:
    apply_claude_response('''
    {json response from Claude here}
    ''')
    """
    mcp = QuickBlenderMCP()
    
    try:
        # Extract JSON from response
        import re
        json_match = re.search(r'```json\n(.*?)\n```', json_response_string, re.DOTALL)
        
        if json_match:
            data = json.loads(json_match.group(1))
        else:
            data = json.loads(json_response_string)
        
        print(f"\n✓ Analysis Summary:")
        print(f"  Quality Score: {data.get('quality_score', 'N/A')}/100")
        print(f"  Issues Found: {len(data.get('issues', []))}")
        print(f"  Commands to Apply: {len(data.get('commands', []))}")
        
        # Apply commands
        if data.get('commands'):
            print(f"\nApplying {len(data['commands'])} commands...")
            mcp.apply_changes(data['commands'])
        
        # Capture next iteration
        print(f"\nCapturing updated state...")
        new_state = mcp.capture_and_export()
        
        print(f"\n✓ Iteration complete! Ready for next review cycle.")
        
    except json.JSONDecodeError as e:
        print(f"✗ Error parsing JSON: {e}")
        print("Make sure to paste the complete JSON response")


# ═════════════════════════════════════════════════════════════════
# CHEAT SHEET
# ═════════════════════════════════════════════════════════════════

"""
QUICK COMMANDS:

# Capture current state
state = mcp.capture_and_export()

# Apply changes from Claude
mcp.apply_changes([
    {"command": "set_render_engine", "params": {"engine": "CYCLES", "samples": 256}},
    {"command": "set_viewport_shading", "params": {"shading_type": "RENDERED"}},
])

# Or use helper
apply_claude_response('''
{paste Claude's response here}
''')

# Print available commands
print_quick_reference()

# View current state
with open(f'mcp_session/state_{mcp.iteration:02d}.json') as f:
    current_state = json.load(f)
"""
