---
name: blender-mcp-feedback
description: "Interactive Blender viewport review and refinement via screenshot feedback loops. Use this skill whenever a user wants to iteratively improve their Blender renders, materials, lighting, or camera setup through Claude analysis. Triggers include: 'review my Blender viewport', 'improve this render', 'help me refine my Blender scene', 'analyze my viewport', 'suggest rendering improvements', or when a user sends a Blender screenshot/scene state for feedback. This skill creates a callback pipeline where Blender captures screenshots, Claude analyzes them, and sends MCP commands back to Blender for automatic refinement — enabling rapid iteration cycles for 3D visualization projects."
compatibility: "Blender 3.5+, Python 3.8+, MCP-enabled Claude session"
---

# Blender-Claude MCP Feedback Loop Skill

**Interactive viewport review with automated scene refinement through MCP command pipeline.**

This skill enables Claude to analyze Blender scenes, identify visual/technical issues, and generate precise MCP commands to improve renders iteratively. Perfect for product visualization, architectural renders, character materials, and any project requiring rapid refinement cycles.

---

## Quick Start

### 1. Load Blender Script in Your .blend File

Copy the template script into **Blender Script Editor** (Alt+Tab):

```python
exec(open('/home/claude/blender-mcp-feedback/scripts/blender_quick_template.py').read())
```

Or use the full system:

```python
exec(open('/home/claude/blender-mcp-feedback/scripts/blender_mcp_callback_system.py').read())
```

### 2. Capture Viewport & Export State

```python
# Initialize and capture
mcp = QuickBlenderMCP()
state = mcp.capture_and_export()

# Print next steps
mcp.print_instructions()
```

### 3. Send to Claude (This Chat)

Copy the printed JSON scene state and any screenshot, then ask:

```
Please review this Blender viewport:
[PASTE scene state JSON here]

Analyze for rendering, lighting, and material issues. 
Provide MCP commands to improve quality.
```

### 4. Execute Returned Commands

Claude will return MCP commands in JSON format. Execute them:

```python
commands = [
    {"command": "set_render_engine", "params": {"engine": "CYCLES", "samples": 256}},
    {"command": "set_viewport_shading", "params": {"shading_type": "RENDERED"}},
]

mcp.apply_changes(commands)
```

### 5. Iterate Until Satisfied

Capture → Send → Analyze → Execute → Repeat (typically 2-4 cycles to reach quality 85+)

---

## Core Workflow

### Phase 1: Viewport Capture (Blender)

Claude receives:
- **Screenshot**: Base64-encoded viewport image
- **Scene State**: JSON with engine, materials, objects, camera, render settings
- **Analysis Request**: Specific questions about quality, issues, suggestions

### Phase 2: Analysis & Command Generation (Claude)

Claude performs:
1. **Issue Identification** — rendering quality, lighting, materials, composition, camera
2. **Quality Scoring** — 0-100 scale (85+ = production-ready)
3. **Priority Ranking** — critical → high → medium → low
4. **Command Generation** — exact MCP instructions to fix issues

### Phase 3: Automated Refinement (Blender)

Your script executes:
- Render engine switching (EEVEE → CYCLES)
- Viewport shading mode changes
- Material property adjustments
- Camera/lighting modifications
- Viewport re-capture

### Phase 4: Iteration (Loop Back to Phase 1)

If quality < 85, repeat. Most projects converge in 2-4 cycles.

---

## Available MCP Commands

### Rendering & Quality

```json
{
  "command": "set_render_engine",
  "params": {
    "engine": "CYCLES | EEVEE",
    "samples": 128
  }
}
```

Control render quality, noise, and preview modes.

```json
{
  "command": "set_viewport_shading",
  "params": {
    "shading_type": "WIREFRAME | SOLID | MATERIAL | RENDERED"
  }
}
```

Switch preview mode for real-time quality assessment.

```json
{
  "command": "render_viewport",
  "params": {
    "output_path": "render.png"
  }
}
```

Render and save final output.

### Object Selection & Composition

```json
{
  "command": "select_object",
  "params": {
    "object_name": "Cube"
  }
}
```

Select for batch operations.

```json
{
  "command": "set_camera_view",
  "params": {
    "camera_name": "Camera"
  }
}
```

Switch active camera for different compositions.

### Material & Appearance

```json
{
  "command": "adjust_material",
  "params": {
    "object_name": "Sphere",
    "material_name": "Plastic",
    "adjustments": {
      "roughness": 0.3,
      "metallic": 0.0,
      "ior": 1.45
    }
  }
}
```

Fine-tune material properties (roughness, metallic, IOR, etc.).

---

## Quality Scoring System

Claude analyzes and scores based on:

| Score | Status | Action |
|-------|--------|--------|
| **85-100** | Production-ready | ✓ Export and finalize |
| **70-84** | Good, refinement possible | Execute next round of commands |
| **50-69** | Significant issues | 2-3 more cycles recommended |
| **<50** | Major overhaul needed | Consider redesign or major adjustments |

---

## Session Management

### Automatic Tracking

Every iteration is saved with:
- Screenshot (base64)
- Scene state (JSON)
- Timestamp
- MCP commands applied
- Quality metrics

### Access Session History

```python
# Get summary of all iterations
summary = mcp.get_review_summary()
print(summary)

# Access specific iteration
specific = mcp.callback_log[2]  # 3rd screenshot
```

### View Output Directory

All files saved to: `{blender_file_dir}/mcp_session/{session_id}/`

---

## Use Cases

### Product Visualization
Start with basic model → Claude iterates lighting/materials → 3-4 cycles → product-ready

### Architectural Renders
Compose scene → Claude suggests camera angles → Refine materials → Export presentation

### Character Materials
Adjust material properties → Claude analyzes appearance → Tweak values → Production quality

### Learning & Best Practices
Every suggestion from Claude includes reasoning — learn Blender optimization patterns

---

## Common Commands by Goal

### "Scene is too dark"
```json
[
  {"command": "set_render_engine", "params": {"engine": "CYCLES", "samples": 256}},
  {"command": "adjust_material", "params": {
    "object_name": "Cube",
    "material_name": "Material",
    "adjustments": {"roughness": 0.5}
  }}
]
```

### "Viewport shading doesn't match final render"
```json
[
  {"command": "set_viewport_shading", "params": {"shading_type": "RENDERED"}},
  {"command": "set_render_engine", "params": {"engine": "CYCLES", "samples": 512}}
]
```

### "Material looks flat/plastic"
```json
[
  {"command": "adjust_material", "params": {
    "object_name": "Sphere",
    "material_name": "Material",
    "adjustments": {
      "roughness": 0.3,
      "metallic": 0.8,
      "ior": 1.45
    }
  }}
]
```

### "Need faster preview"
```json
[
  {"command": "set_viewport_shading", "params": {"shading_type": "SOLID"}},
  {"command": "set_render_engine", "params": {"engine": "EEVEE", "samples": 64}}
]
```

---

## Workflow for Common Projects

### Product Photography (e.g., PCB Enclosure)
1. Model geometry complete in Blender
2. Basic materials assigned
3. **Send viewport to Claude** → "Review this PCB enclosure render"
4. Claude suggests: lighting angle, material refinement, background
5. Execute MCP commands
6. **Send updated screenshot** → "Improve further"
7. Final adjustments (usually 2-3 cycles)
8. Render final image

### Interactive Iteration Loop
```
Capture → Send → Analyze → Apply → Capture → ...
```

Typical timeline per cycle: **3-5 minutes**

---

## Tips & Optimization

### For Faster Feedback
- Start with EEVEE/SOLID shading for quick previews
- Switch to CYCLES/RENDERED once composition locked
- Provide context in your initial request

### For Best Results
- Include multiple angles if possible
- Mention specific concerns (too dark, colors off, materials plastic-y)
- Describe final use (product viz, animation, architecture)

### Performance
- VRAM requirement: 4GB minimum (8GB recommended)
- Render time scales with sample count — start at 128-256
- Session saves snapshots — no data loss between iterations

---

## Architecture Details

**See references/ for full technical documentation:**
- `blender_mcp_callback_system.py` — Complete Blender-side implementation
- `blender_mcp_handler.py` — Claude-side analysis engine
- `BLENDER_MCP_WORKFLOW.md` — Extended workflow guide

**Key components:**
- **Session Manager** — Tracks iterations, stores state, manages exports
- **MCP Handler** — Analyzes viewports, identifies issues, generates commands
- **Quick Template** — Minimal setup for immediate use

---

## Quick Template Code

For immediate use without reading full docs:

```python
# In Blender Script Editor:
# 1. Paste this entire function
# 2. Run it
# 3. Copy the printed JSON
# 4. Paste to Claude

class QuickBlenderMCP:
    """Minimal Blender-Claude MCP integration"""
    
    def __init__(self):
        import bpy
        from pathlib import Path
        from datetime import datetime
        self.session_dir = Path(bpy.data.filepath).parent / "mcp_session"
        self.session_dir.mkdir(exist_ok=True)
        self.iteration = 0
    
    def capture_and_export(self):
        """Capture viewport and prepare for Claude review"""
        import bpy, json
        self.iteration += 1
        
        scene = bpy.context.scene
        state = {
            'iteration': self.iteration,
            'render_engine': scene.render.engine,
            'selected_objects': [obj.name for obj in bpy.context.selected_objects],
            'camera': scene.camera.name if scene.camera else None,
            'objects_count': len([o for o in bpy.data.objects if o.type == 'MESH']),
            'materials_count': len(bpy.data.materials),
        }
        
        state_file = self.session_dir / f"state_{self.iteration:02d}.json"
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"\n✓ Iteration {self.iteration} captured")
        print(f"  State: {state_file}")
        print(f"  Engine: {state['render_engine']}")
        return state
    
    def apply_changes(self, commands):
        """Apply MCP commands from Claude"""
        import bpy
        scene = bpy.context.scene
        
        for cmd in commands:
            if cmd.get('command') == 'set_render_engine':
                scene.render.engine = cmd['params']['engine']
                if scene.render.engine == 'CYCLES':
                    scene.cycles.samples = cmd['params'].get('samples', 256)
                print(f"  ✓ Set render engine to {cmd['params']['engine']}")
            
            elif cmd.get('command') == 'set_viewport_shading':
                for area in bpy.context.screen.areas:
                    if area.type == 'VIEW_3D':
                        for space in area.spaces:
                            if space.type == 'VIEW_3D':
                                space.shading.type = cmd['params']['shading_type']
                print(f"  ✓ Set viewport to {cmd['params']['shading_type']}")
        
        print(f"\n✓ Applied {len(commands)} changes")

# Usage:
# mcp = QuickBlenderMCP()
# state = mcp.capture_and_export()
# [Send JSON to Claude]
# mcp.apply_changes([{...}])  # Paste Claude's response here
```

---

## Troubleshooting

### "Commands not applying"
- Verify Blender is in the correct context (not in edit mode)
- Check object/material names match exactly
- Print current scene state to debug

### "Screenshot not saving"
- Verify output directory permissions
- Check `bpy.data.filepath` is set (save .blend file first)
- Ensure render.filepath is configured

### "Base64 encoding fails"
- Install Pillow: `pip install Pillow` (if using custom Python)
- Verify PNG/image format support

---

## API Reference

**See `references/blender_mcp_callback_system.py` for complete class documentation**

Core methods:
- `capture_viewport_screenshot(filename)` — Capture and encode
- `export_for_claude_review(screenshot_record)` — Prepare JSON payload
- `apply_mcp_command(command_dict)` — Execute single command
- `get_scene_state()` — Current Blender state snapshot

---

## What to Ask Claude

When sending a viewport:

✅ **Good prompts:**
- "Review this Blender viewport for a product render. What would improve quality?"
- "I'm rendering an enclosure. Suggest lighting and material improvements."
- "Analyze this viewport and provide MCP commands to fix issues."

❌ **Avoid:**
- "Make my render better" (too vague)
- Without scene state (Claude can't see settings)
- Without specifying use case (product vs architecture vs character)

**Best practice:** Include scene state JSON + specific context about your project goal.

---

## Next Steps

1. **Load the template** in your next Blender session
2. **Capture initial viewport** with `mcp.capture_and_export()`
3. **Send scene state to Claude** (this chat) with context
4. **Execute returned commands** with `mcp.apply_changes(commands)`
5. **Iterate** until quality ≥ 85/100

Ready? Load the template and send your first viewport! 🚀

