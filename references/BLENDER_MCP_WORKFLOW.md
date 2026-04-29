# Blender-Claude MCP Feedback Loop Workflow
## Interactive Review & Refinement Pipeline

---

## 📋 Overview

This system creates a **callback-based feedback loop** where:

1. **Blender captures** viewport screenshots
2. **Claude reviews** them via MCP integration
3. **Claude generates** MCP commands for improvements
4. **Blender executes** changes automatically
5. **Cycle repeats** until quality targets are met

**Result:** Real-time collaborative refinement with precise, trackable changes.

---

## 🚀 Setup Instructions

### Step 1: Load the Blender Callback System

In **Blender Script Editor** (Alt+Tab):

```python
# Copy-paste: /home/claude/blender_mcp_callback_system.py contents
# Or load directly:
exec(open('/home/claude/blender_mcp_callback_system.py').read())
```

**Verify output:**
```
✓ Blender MCP Callback System initialized
  Session ID: 20240115_103000
  Output directory: /path/to/mcp_callbacks
```

---

### Step 2: Initialize Session in Blender

```python
# In Blender Script Editor
mcp_system = BlenderMCPCallbackSystem()

# Test: Capture initial screenshot
screenshot = mcp_system.capture_viewport_screenshot("initial_state.png")

print("Screenshot captured:", screenshot['filename'])
print("\nScene State:")
import json
print(json.dumps(screenshot['scene_state'], indent=2))
```

**Output:**
```json
{
  "render_engine": "BLENDER_EEVEE",
  "sample_count": 128,
  "viewport_shading": {
    "type": "MATERIAL",
    "use_scene_lights": true
  },
  "selected_objects": ["Cube", "Material_Sphere"],
  "objects_count": 3,
  "materials_count": 5
}
```

---

## 🔄 Workflow Cycle

### Phase 1: Review in Claude

**Copy this into a Claude chat:**

```
I'm starting a Blender-Claude feedback loop. Here's my current viewport:

[PASTE SCREENSHOT - base64 or PNG]

**Scene State:**
{paste JSON scene_state here}

Please analyze this viewport and:
1. Identify quality/rendering issues
2. Suggest improvements with priority
3. Provide MCP commands to fix them

Format response as:
```json
{
  "analysis": {
    "quality_score": 75,
    "issues": [
      {
        "category": "rendering",
        "severity": "high",
        "description": "...",
        "fix": "..."
      }
    ]
  },
  "commands": [
    {"command": "set_render_engine", "params": {"engine": "CYCLES", "samples": 256}}
  ],
  "reasoning": "...",
  "expected_improvements": ["better quality", "reduced noise"]
}
```
```

### Phase 2: Extract & Execute Commands in Blender

**Claude returns MCP commands. Execute them:**

```python
# In Blender Script Editor

claude_response = """
{
  "commands": [
    {"command": "set_render_engine", "params": {"engine": "CYCLES", "samples": 256}},
    {"command": "set_viewport_shading", "params": {"shading_type": "RENDERED"}},
    {"command": "adjust_material", "params": {
      "object_name": "Sphere",
      "material_name": "Material",
      "adjustments": {"roughness": 0.4}
    }}
  ],
  "reasoning": "Switching to CYCLES for better quality, enabling rendered preview, and adjusting material roughness for better appearance"
}
"""

# Parse commands
import json
data = json.loads(claude_response)

# Execute each command
for cmd in data['commands']:
    result = mcp_system.apply_mcp_command(cmd)
    print(f"✓ {cmd['command']}: {result['status']}")

print("\n✓ All commands executed. Viewport updated.")
```

### Phase 3: Capture Updated Viewport

```python
# Capture after changes
updated_screenshot = mcp_system.capture_viewport_screenshot("after_changes.png")

# Export for next review
review_payload = mcp_system.export_for_claude_review(updated_screenshot)

print("Ready for next review cycle")
print(f"Quality Score Progress: {updated_screenshot['scene_state']}")
```

### Phase 4: Loop (Optional)

If quality isn't sufficient:
1. Export updated screenshot with `export_for_claude_review()`
2. Return to Claude with new screenshot
3. Repeat cycle

---

## 📊 Feedback Loop Architecture

```
┌─────────────────────────────────────────────┐
│           Blender Viewport                  │
│  (3D Scene, Materials, Lighting, Camera)    │
└────────────────┬────────────────────────────┘
                 │
                 ▼
         ┌──────────────────┐
         │  Screenshot +    │
         │  Scene State     │
         │  (base64 + JSON) │
         └────────┬─────────┘
                  │
                  ▼
        ╔══════════════════════╗
        ║  Claude (This Chat)  ║
        ║  - Analyze viewport  ║
        ║  - Identify issues   ║
        ║  - Generate commands ║
        ╚═════════┬════════════╝
                  │
                  ▼ (MCP Commands)
         ┌──────────────────┐
         │  Execute MCP     │
         │  Commands:       │
         │  • Render engine │
         │  • Shading mode  │
         │  • Materials     │
         │  • Camera        │
         └────────┬─────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │ Updated Blender     │
        │ Viewport            │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Quality > Target?  │
        └──────┬──────┬───────┘
               │yes   │no
               ▼      ▼
           ✓ Done   Loop ▲
```

---

## 🛠️ Available MCP Commands

### Rendering & Viewport

```python
# Set render engine
{
  "command": "set_render_engine",
  "params": {"engine": "CYCLES", "samples": 256}
}

# Set viewport shading
{
  "command": "set_viewport_shading",
  "params": {"shading_type": "RENDERED"}  # WIREFRAME, SOLID, MATERIAL, RENDERED
}

# Render and save
{
  "command": "render_viewport",
  "params": {"output_path": "render.png"}
}
```

### Object & Selection

```python
# Select object
{
  "command": "select_object",
  "params": {"object_name": "Cube"}
}

# Set active camera
{
  "command": "set_camera_view",
  "params": {"camera_name": "Camera.001"}
}
```

### Materials & Appearance

```python
# Adjust material properties
{
  "command": "adjust_material",
  "params": {
    "object_name": "Sphere",
    "material_name": "Material",
    "adjustments": {
      "roughness": 0.5,
      "metallic": 0.0,
      "ior": 1.45
    }
  }
}
```

---

## 📈 Quality Metrics

Claude analyzes and scores based on:

| Category | Factors |
|----------|---------|
| **Rendering** | Engine quality, sample count, denoising |
| **Lighting** | Brightness, shadows, contrast, key light |
| **Materials** | Roughness, metallicity, colors, reflections |
| **Composition** | Framing, depth, focus, balance |
| **Camera** | Position, angle, focal length, DOF |
| **Performance** | Render time, VRAM usage, responsiveness |

**Quality Score Breakdown:**
- **85-100:** Production-ready
- **70-84:** Good, minor refinements needed
- **50-69:** Significant improvements possible
- **<50:** Major overhaul recommended

---

## 💡 Pro Tips

### 1. **Batch Operations**
```python
# Multi-material adjustment
for material in bpy.data.materials:
    if material.name.startswith("Mat_"):
        # Claude will see this and optimize all at once
        pass
```

### 2. **Render Comparison**
```python
# Capture before
before = mcp_system.capture_viewport_screenshot("before.png")

# [Execute Claude's MCP commands]

# Capture after
after = mcp_system.capture_viewport_screenshot("after.png")

# Send both to Claude for comparison analysis
```

### 3. **Session Tracking**
```python
# Get full session history
summary = mcp_system.get_review_summary()
print(summary)  # JSON with all reviews and changes

# Find specific iteration
specific = mcp_system.callback_log[3]  # 4th screenshot
```

### 4. **Auto-Refinement Loop**
```python
# Multiple iterations without manual intervention
for cycle in range(5):  # 5 refinement cycles
    screenshot = mcp_system.capture_viewport_screenshot(f"cycle_{cycle}.png")
    # [Send to Claude, get response]
    # [Execute commands]
    
    # Check if satisfied
    if quality_score >= 85:
        break
```

---

## 🔍 Debugging

### Issue: Commands not applying

**Check:**
```python
# Verify Blender state
print("Active object:", bpy.context.active_object.name)
print("Selected objects:", [o.name for o in bpy.context.selected_objects])
print("Scene camera:", bpy.context.scene.camera)

# Test command manually
result = mcp_system.apply_mcp_command({
    "command": "select_object",
    "params": {"object_name": "Cube"}
})
print("Result:", result)
```

### Issue: Screenshot not saving

**Check:**
```python
# Verify output directory exists
import os
output_path = mcp_system.output_dir / mcp_system.session_id
os.makedirs(output_path, exist_ok=True)

# Verify render settings
scene = bpy.context.scene
print(f"Render path: {scene.render.filepath}")
print(f"Resolution: {scene.render.resolution_x}x{scene.render.resolution_y}")
```

### Issue: Base64 encoding fails

**Check:**
```python
# Verify PIL availability
try:
    from PIL import Image
    print("✓ PIL available")
except ImportError:
    print("✗ Install Pillow: pip install Pillow")
```

---

## 📝 Complete Example Workflow

### Session Start

```python
# 1. Initialize
mcp_system = BlenderMCPCallbackSystem()

# 2. Capture and review
ss1 = mcp_system.capture_viewport_screenshot("state_1.png")
payload1 = mcp_system.export_for_claude_review(ss1)

# 3. Send to Claude (with scene_state JSON)
# [User sends payload to Claude]
```

### Claude Analysis Response

```json
{
  "analysis": {
    "quality_score": 65,
    "issues": [
      {
        "severity": "high",
        "description": "EEVEE engine lacks quality. Switch to CYCLES.",
        "fix": "Set render engine to CYCLES with 256+ samples"
      },
      {
        "severity": "medium",
        "description": "Materials look flat. Adjust roughness.",
        "fix": "Increase material complexity and roughness variation"
      }
    ]
  },
  "commands": [
    {
      "command": "set_render_engine",
      "params": {"engine": "CYCLES", "samples": 256}
    },
    {
      "command": "adjust_material",
      "params": {
        "object_name": "MainSphere",
        "material_name": "Plastic",
        "adjustments": {"roughness": 0.3}
      }
    }
  ],
  "expected_improvements": ["Higher quality output", "Better material appearance"]
}
```

### Execution & Next Cycle

```python
# Execute commands from Claude
for cmd in response['commands']:
    result = mcp_system.apply_mcp_command(cmd)
    print(f"✓ {cmd['command']}")

# Capture updated state
ss2 = mcp_system.capture_viewport_screenshot("state_2.png")

# Ready for next review (if needed)
# quality score should improve
```

---

## 🎯 Use Cases

### 1. **Product Visualization**
- Start with basic model
- Claude reviews lighting/materials iteratively
- Achieve product-ready renders in 3-4 cycles

### 2. **Architectural Visualization**
- Claude analyzes spatial composition
- Suggests camera angles, lighting setups
- Refines until presentation-ready

### 3. **Character/Model Development**
- Iterative material refinement
- Claude identifies modeling issues
- Texture and appearance improvements

### 4. **Learning & Optimization**
- Understand best practices through Claude's feedback
- Get suggestions for performance optimization
- Learn proper Blender workflows

---

## 🚨 Performance Considerations

### Blender-side Optimization
```python
# Disable real-time updates during batch operations
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.tag_redraw = False  # After changes, enable

# Use faster viewport shading during iteration
mcp_system.apply_mcp_command({
    "command": "set_viewport_shading",
    "params": {"shading_type": "SOLID"}  # Fast preview
})
```

### Recommended Specs
- **GPU:** NVIDIA with CUDA (best), AMD with HIP, CPU fallback
- **VRAM:** 4GB minimum (8GB recommended)
- **Samples:** Start at 64-128, increase to 256+ after composition locked

---

## 📚 Next Steps

1. **Load the Blender script** in your .blend file
2. **Capture initial screenshot** and analyze with Claude
3. **Execute the first batch of MCP commands**
4. **Iterate** until satisfied with quality
5. **Export final render** when complete

**Questions?** Ask Claude in this chat with your Blender scene state!

---

**Last Updated:** 2024-01-15  
**Compatible with:** Blender 3.5+, Claude API via MCP
