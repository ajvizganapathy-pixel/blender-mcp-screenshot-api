# Blender-Claude MCP Feedback — Complete Technical Reference

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    BLENDER SCENE (Viewport)                      │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼ (Screenshot + Scene State)
         ┌──────────────────────────────────────┐
         │  BlenderMCPCallbackSystem (Blender)  │
         │  • Captures viewport                  │
         │  • Manages session                    │
         │  • Exports to base64                  │
         │  • Applies MCP commands               │
         └──────────────────┬────────────────────┘
                            │
                            ▼ (JSON Payload)
        ╔════════════════════════════════════════╗
        ║  Claude (This Chat)                    ║
        ║  • Analyzes viewport                   ║
        ║  • Identifies issues                   ║
        ║  • Generates MCP commands              ║
        ║  • Provides quality score               ║
        ╚════════────────┬═════════════════════╝
                         │
                         ▼ (MCP Commands JSON)
         ┌──────────────────────────────────────┐
         │  QuickBlenderMCP (Blender)           │
         │  • apply_changes(commands)            │
         │  • Executes render engine changes     │
         │  • Adjusts materials                  │
         │  • Switches viewports                 │
         └──────────────────┬────────────────────┘
                            │
                            ▼ (Updated Viewport)
        ┌────────────────────────────────────────┐
        │  New Iteration (Loop back or finalize) │
        └────────────────────────────────────────┘
```

---

## Class Reference

### BlenderMCPCallbackSystem (Full Implementation)

**Location:** `scripts/blender_mcp_callback_system.py`

Complete, production-ready system with session management.

#### Methods

##### `__init__(output_dir=None)`
Initialize callback system.
- **output_dir** (Path, optional): Base directory for sessions. Default: `{blender_file_dir}/mcp_callbacks`
- **Returns:** BlenderMCPCallbackSystem instance

```python
mcp = BlenderMCPCallbackSystem()
# Creates session with ID: 20240115_103022
```

##### `capture_viewport_screenshot(filename=None) → dict`
Capture Blender viewport and convert to base64.

**Returns:**
```python
{
    'timestamp': '2024-01-15T10:30:22.123456',
    'filename': '/path/to/session/viewport_0001.png',
    'base64': 'iVBORw0KGgo...',  # Full image as base64
    'scene_state': {
        'render_engine': 'CYCLES',
        'viewport_shading': {'type': 'RENDERED', ...},
        'selected_objects': ['Cube', 'Camera'],
        'camera': 'Camera',
        'frame_current': 1,
        'resolution_x': 1920,
        'resolution_y': 1080,
        'sample_count': 128,
        'objects_count': 15,
        'materials_count': 8
    }
}
```

##### `get_scene_state() → dict`
Get current Blender scene state without capturing screenshot.

Returns: Dictionary with all scene metadata (see above)

##### `export_for_claude_review(screenshot_record=None) → str`
Format screenshot + state as JSON for Claude analysis.

**Returns:** JSON string ready to paste in chat

```json
{
  "review_request": {
    "image_base64": "iVBORw0K...",
    "scene_state": {...},
    "questions": [
      "What are the current visual issues?",
      "Are there material/lighting problems?",
      "What rendering settings would help?",
      "Suggest specific Blender adjustments"
    ]
  }
}
```

##### `apply_mcp_command(mcp_command: dict) → dict`
Execute single MCP command in Blender.

**Params:**
```python
{
    "command": "set_render_engine",  # or other command
    "params": {"engine": "CYCLES", "samples": 256}
}
```

**Returns:**
```python
{
    'status': 'success',  # or 'error', 'unknown_command'
    'command': 'set_render_engine',
    'message': 'Optional error message'
}
```

##### `get_review_summary() → str`
Get full session history as JSON.

**Returns:** Complete session timeline with all iterations

##### `get_viewport_shading() → dict`
Get current viewport shading mode.

**Returns:**
```python
{
    'type': 'RENDERED',  # WIREFRAME, SOLID, MATERIAL, RENDERED
    'use_scene_lights': True,
    'use_scene_world': True
}
```

---

### QuickBlenderMCP (Fast Implementation)

**Location:** `scripts/blender_quick_template.py`

Lightweight version for rapid iteration. Drop-in replacement with same API.

#### Methods

##### `__init__()`
Initialize minimal callback system.

```python
mcp = QuickBlenderMCP()
```

##### `capture_and_export() → dict`
Single function: capture + export in one call.

Combines:
- `capture_viewport_screenshot()`
- Saves to JSON
- Returns scene_state dict

**Returns:** Scene state dictionary

##### `apply_changes(commands: list) → None`
Apply list of MCP commands.

**Params:**
```python
[
    {"command": "set_render_engine", "params": {...}},
    {"command": "adjust_material", "params": {...}},
    ...
]
```

**Output:** Prints status of each command

##### `print_instructions()`
Print formatted next steps for Claude interaction.

---

## MCP Command Specifications

All commands follow JSON structure:
```json
{
  "command": "command_name",
  "params": {
    "key": "value",
    ...
  }
}
```

### Supported Commands

#### `set_render_engine`
Switch Blender render engine and quality.

**Params:**
```python
{
  "engine": "CYCLES" | "EEVEE",
  "samples": 64-2048  # Only for CYCLES
}
```

**Effect:**
- Sets `bpy.context.scene.render.engine`
- For CYCLES, sets `bpy.context.scene.cycles.samples`

**Example:**
```python
{"command": "set_render_engine", "params": {"engine": "CYCLES", "samples": 512}}
```

---

#### `set_viewport_shading`
Change viewport visualization mode.

**Params:**
```python
{
  "shading_type": "WIREFRAME" | "SOLID" | "MATERIAL" | "RENDERED"
}
```

**Effect:**
Sets `space.shading.type` for all VIEW_3D areas

**Example:**
```python
{"command": "set_viewport_shading", "params": {"shading_type": "RENDERED"}}
```

---

#### `select_object`
Select object by name.

**Params:**
```python
{
  "object_name": "Cube"  # Exact object name
}
```

**Effect:**
- Sets as active object
- Selects it (select_set(True))

**Example:**
```python
{"command": "select_object", "params": {"object_name": "MainSphere"}}
```

---

#### `adjust_material`
Modify material properties on object.

**Params:**
```python
{
  "object_name": "Sphere",
  "material_name": "Plastic",
  "adjustments": {
    "roughness": 0.0-1.0,
    "metallic": 0.0-1.0,
    "ior": 1.0-2.5,
    ...any other numeric material property
  }
}
```

**Effect:**
Applies adjustments to material slots on object

**Example:**
```python
{
  "command": "adjust_material",
  "params": {
    "object_name": "Sphere",
    "material_name": "Material",
    "adjustments": {
      "roughness": 0.3,
      "metallic": 0.8
    }
  }
}
```

---

#### `render_viewport`
Render scene and save file.

**Params:**
```python
{
  "output_path": "/path/to/render.png"  # Optional
}
```

**Effect:**
- Executes `bpy.ops.render.render(write_still=True)`
- Saves to output_path or default location

**Example:**
```python
{"command": "render_viewport", "params": {"output_path": "final_render.png"}}
```

---

#### `set_camera_view`
Switch active camera.

**Params:**
```python
{
  "camera_name": "Camera.001"  # Exact camera object name
}
```

**Effect:**
Sets `bpy.context.scene.camera` to specified camera

**Example:**
```python
{"command": "set_camera_view", "params": {"camera_name": "Camera.001"}}
```

---

## Scene State Structure

Captured automatically by `get_scene_state()`:

```python
{
  'render_engine': 'CYCLES' | 'BLENDER_EEVEE',
  'viewport_shading': {
    'type': 'WIREFRAME' | 'SOLID' | 'MATERIAL' | 'RENDERED',
    'use_scene_lights': True | False,
    'use_scene_world': True | False
  },
  'selected_objects': ['obj1', 'obj2', ...],
  'active_object': 'obj_name' | None,
  'camera': 'Camera' | None,
  'frame_current': 1,
  'frame_end': 250,
  'resolution_x': 1920,
  'resolution_y': 1080,
  'sample_count': 128 | None,  # CYCLES only
  'objects_count': 5,
  'materials_count': 8
}
```

---

## Workflow Implementation Examples

### Example 1: Basic Iteration

```python
import bpy

# 1. Initialize
mcp = QuickBlenderMCP()

# 2. Capture current state
print("▶ Capturing viewport...")
state = mcp.capture_and_export()
print(f"✓ Captured iteration {state['iteration']}")
print(f"  Engine: {state['render_engine']}")
print(f"  Objects: {state['objects_count']}")

# 3. Print instructions for Claude
mcp.print_instructions()

# [Send JSON to Claude...]
# [Get response with MCP commands...]

# 4. Apply commands from Claude
claude_response = """
{
  "commands": [
    {"command": "set_render_engine", "params": {"engine": "CYCLES", "samples": 256}},
    {"command": "set_viewport_shading", "params": {"shading_type": "RENDERED"}}
  ]
}
"""

import json
data = json.loads(claude_response)
print("\n▶ Applying {len(data['commands'])} changes...")
mcp.apply_changes(data['commands'])

# 5. Capture updated state
print("\n▶ Capturing updated viewport...")
new_state = mcp.capture_and_export()
print("✓ Ready for next review cycle")
```

---

### Example 2: Multi-Material Batch Adjustment

```python
# Adjust multiple materials at once
commands = [
    {
        "command": "adjust_material",
        "params": {
            "object_name": "BaseMesh",
            "material_name": "Plastic",
            "adjustments": {"roughness": 0.4, "metallic": 0.0}
        }
    },
    {
        "command": "adjust_material",
        "params": {
            "object_name": "MetalFrame",
            "material_name": "Aluminum",
            "adjustments": {"roughness": 0.15, "metallic": 0.9}
        }
    },
    {
        "command": "set_render_engine",
        "params": {"engine": "CYCLES", "samples": 512}
    }
]

mcp.apply_changes(commands)
```

---

### Example 3: Camera & Composition

```python
# Switch cameras and render
commands = [
    {"command": "set_camera_view", "params": {"camera_name": "Camera.FrontView"}},
    {"command": "set_viewport_shading", "params": {"shading_type": "RENDERED"}},
    {"command": "render_viewport", "params": {"output_path": "front_view.png"}}
]

mcp.apply_changes(commands)
```

---

## Quality Metrics

Claude analyzes and scores based on these categories:

### Rendering Quality (30 points)
- Engine choice (CYCLES for quality, EEVEE for speed)
- Sample count (noise level, convergence)
- Denoising effectiveness
- Preview vs. production readiness

### Lighting (25 points)
- Key light placement
- Fill light balance
- Shadows and contrast
- Scene lighting setup
- Environmental lighting

### Materials (20 points)
- Roughness and reflectivity
- Metallic properties
- Color accuracy
- Transparency/IOR
- Texture complexity

### Composition (15 points)
- Framing and crop
- Camera angle
- Depth of field
- Focus point
- Balance and symmetry

### Technical (10 points)
- Render time efficiency
- VRAM usage
- Scene organization
- Camera setup
- Light setup

**Total: 100 points**

---

## Error Handling

All MCP commands return status:

```python
{
    'status': 'success' | 'error' | 'unknown_command',
    'command': 'command_name',
    'message': 'Optional error details'
}
```

**Common errors:**
- `object_name` doesn't exist → status: error
- Invalid `engine` value → status: error
- Samples out of range → auto-clamped to valid range

---

## Session Organization

```
{blender_file_dir}/
└── mcp_session/
    └── 20240115_103022/  (session_id)
        ├── viewport_0001.png
        ├── state_01.json
        ├── viewport_0002.png
        ├── state_02.json
        └── render.png
```

Each iteration automatically saves:
- Screenshot (PNG)
- Scene state (JSON)
- Timestamp
- Indexed for easy reference

---

## Blender Compatibility

**Tested & Verified:**
- Blender 3.5, 3.6, 4.0+
- Python 3.8+ (Blender built-in Python)
- All platforms (Windows, macOS, Linux)

**Requirements:**
- Blender Script Editor access (built-in)
- No external dependencies (pure Blender API)

**GPU Support:**
- NVIDIA CUDA (best performance)
- AMD HIP (good support)
- Intel Arc (supported)
- CPU fallback (slower)

---

## Performance Tips

1. **Preview vs. Production**
   - Start with EEVEE/SOLID for fast iteration
   - Switch to CYCLES/RENDERED once locked in

2. **Sample Count Strategy**
   - Preview: 64-128 samples
   - Feedback: 128-256 samples
   - Final: 256-512+ samples

3. **Viewport Shading**
   - WIREFRAME: Fastest, composition only
   - SOLID: Good for lighting, quick
   - MATERIAL: Material preview, slower
   - RENDERED: Full quality, slowest

4. **Session Management**
   - Each iteration ~5-10 MB (depends on resolution)
   - Clean up old sessions if needed
   - Use `get_review_summary()` to audit

---

## FAQ & Troubleshooting

**Q: Screenshot not saving**
A: Ensure .blend file is saved first. `bpy.data.filepath` must be set.

**Q: Commands executing but not visible**
A: You may be in Edit Mode. Exit to Object Mode and try again.

**Q: Materials not adjusting**
A: Verify exact material name matches. Material must exist on object.

**Q: Render stalling**
A: High sample count on slow GPU. Reduce samples or enable denoising.

**Q: Base64 encoding fails**
A: Install Pillow if using custom Python: `pip install Pillow`

---

## Advanced: Custom MCP Commands

To extend the system with custom commands, edit `apply_mcp_command()`:

```python
def apply_mcp_command(self, mcp_command):
    """Extended with custom command"""
    
    if mcp_command.get('command') == 'custom_your_feature':
        # Your implementation here
        return {'status': 'success', 'command': 'custom_your_feature'}
```

Then use in MCP payload:
```python
{"command": "custom_your_feature", "params": {...}}
```

---

**Last Updated:** 2024-01-15  
**Skill Version:** 1.0.0  
**Python:** 3.8+  
**Blender:** 3.5+
