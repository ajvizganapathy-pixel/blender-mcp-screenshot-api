# 🚀 Blender-Claude MCP Feedback Loop

> **Interactive Viewport Review & Automated Scene Refinement via MCP Commands**

[![Blender](https://img.shields.io/badge/Blender-3.5%2B-orange)](https://www.blender.org/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)](https://github.com/)
[![Version](https://img.shields.io/badge/Version-1.0.0-blueviolet)](https://github.com/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#-quick-start-30-seconds)
- [Features](#-features)
- [Installation](#-installation)
- [Workflow](#-core-workflow)
- [Commands](#-available-commands)
- [Use Cases](#-use-cases)
- [File Structure](#-file-structure)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#license)

---

## Overview

**Blender-Claude MCP Feedback** is a cutting-edge integration that enables interactive, automated refinement of Blender viewport renders through Claude AI analysis and MCP (Model Context Protocol) commands.

### 🎯 How It Works

```
┌─────────────────────┐
│  Blender Viewport   │ ──► Screenshot + Scene State
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  Claude Analysis    │ ◄── Analyzes issues, scores quality
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  MCP Commands       │ ──► Execute render improvements
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│  Updated Render     │ ◄── Viewport updates automatically
└─────────────────────┘
```

**Result:** Professional-quality renders in 2-4 iteration cycles (~15-20 minutes)

---

## ⚡ Quick Start (30 seconds)

### Step 1: Load Template in Blender

Copy entire contents of `blender_quick_template.py` into **Blender Script Editor** (Alt+Tab):

```python
exec(open('/path/to/blender_quick_template.py').read())
```

### Step 2: Capture Your Scene

```python
mcp = QuickBlenderMCP()
state = mcp.capture_and_export()
mcp.print_instructions()
```

### Step 3: Send to Claude

Copy the printed JSON and ask Claude:

```
Please review this Blender viewport: [PASTE JSON HERE]
Analyze for issues and provide MCP commands.
```

### Step 4: Execute Commands

Claude returns MCP instructions. Execute them in Blender:

```python
commands = [
    {"command": "set_render_engine", "params": {"engine": "CYCLES", "samples": 256}},
    {"command": "set_viewport_shading", "params": {"shading_type": "RENDERED"}},
    {"command": "adjust_material", "params": {
        "object_name": "Sphere",
        "material_name": "Material",
        "adjustments": {"roughness": 0.3}
    }}
]
mcp.apply_changes(commands)
```

### Step 5: Iterate

Capture → Send → Analyze → Execute → Repeat until quality ≥ 85/100

---

## 🎯 Features

### Core Features
- ✅ **Viewport Screenshot Capture** — Base64 encoded for Claude analysis
- ✅ **Automatic Scene State Export** — JSON with all rendering parameters
- ✅ **Quality Scoring** — 0-100 metric with breakdown by category
- ✅ **MCP Command Pipeline** — Render engine, materials, lighting, camera control
- ✅ **Session Management** — Full iteration history with timestamps
- ✅ **Production-Ready** — Tested on Blender 3.5, 3.6, 4.0+

### Analysis Capabilities
- 🔍 **Issue Identification** — Lighting, materials, rendering, composition
- 📊 **Quality Metrics** — Detailed breakdown (rendering, lighting, materials, composition, technical)
- 💡 **Smart Suggestions** — Context-aware improvement recommendations
- 🎓 **Educational** — Every suggestion includes reasoning

### Integration
- 🔗 **MCP Commands** — Direct control over Blender scene properties
- 🤖 **Claude AI** — Advanced visual analysis and recommendation engine
- 💾 **Session Storage** — Automatic save of all iterations
- 📈 **Progress Tracking** — Quality score progression visible across cycles

---

## 📥 Installation

### Option A: Claude.ai Skills (Recommended)

1. **Download** the `blender-mcp-feedback/` folder
2. **Go to Claude.ai Settings** → **Skills**
3. **Click "Add Custom Skill"** → **Upload the folder**
4. ✅ **Instantly available** in all your chats

### Option B: Local Installation

```bash
# Clone or download to your machine
git clone https://github.com/yourusername/blender-mcp-feedback.git

# Copy to Claude skills directory
cp -r blender-mcp-feedback ~/Claude/skills/
```

Then reference in Claude: The skill is automatically detected.

### Option C: Direct Use (Immediate)

```python
# In Blender Script Editor:
exec(open('/path/to/blender_quick_template.py').read())
mcp = QuickBlenderMCP()
state = mcp.capture_and_export()
```

---

## 🔄 Core Workflow

### Phase 1: Viewport Capture (Blender)

```python
mcp = QuickBlenderMCP()
state = mcp.capture_and_export()
```

**Captures:**
- Viewport screenshot (base64 encoded PNG)
- Scene state (render engine, materials, camera, resolution, samples)
- Timestamp and iteration counter

### Phase 2: Analysis & Scoring (Claude)

Claude receives screenshot and state, then:
1. Identifies visual/technical issues
2. Calculates quality score (0-100 scale)
3. Ranks issues by priority (critical → high → medium → low)
4. Generates specific MCP commands

**Score Interpretation:**
- **85-100** — Production-ready ✓
- **70-84** — Good, minor refinements
- **50-69** — Significant improvements needed
- **<50** — Major overhaul required

### Phase 3: Command Execution (Blender)

```python
mcp.apply_changes(commands)
```

Automatically executes:
- Render engine switching
- Viewport shading changes
- Material adjustments
- Camera modifications

### Phase 4: Iteration Loop

Capture updated viewport → Send to Claude → Repeat

**Typical timeline:**
- Per cycle: 3-5 minutes
- Total iterations: 2-4 cycles
- Final result: 15-20 minutes to production quality

---

## 🛠️ Available Commands

### Rendering & Quality Control

```json
{
  "command": "set_render_engine",
  "params": {
    "engine": "CYCLES | EEVEE",
    "samples": 64-2048
  }
}
```

**Use when:** Adjusting quality, noise, preview mode

```json
{
  "command": "set_viewport_shading",
  "params": {
    "shading_type": "WIREFRAME | SOLID | MATERIAL | RENDERED"
  }
}
```

**Use when:** Changing preview mode

```json
{
  "command": "render_viewport",
  "params": {
    "output_path": "render.png"
  }
}
```

**Use when:** Exporting final render

### Material Adjustments

```json
{
  "command": "adjust_material",
  "params": {
    "object_name": "Sphere",
    "material_name": "Material",
    "adjustments": {
      "roughness": 0.0-1.0,
      "metallic": 0.0-1.0,
      "ior": 1.0-2.5
    }
  }
}
```

**Use when:** Tweaking material properties

### Object & Camera Selection

```json
{
  "command": "select_object",
  "params": {
    "object_name": "Cube"
  }
}
```

```json
{
  "command": "set_camera_view",
  "params": {
    "camera_name": "Camera.001"
  }
}
```

---

## 🎯 Use Cases

### 📦 Product Visualization

```
Design geometry → Basic materials → Send to Claude →
3-4 iterations → Production-quality product render
```

**Timeline:** ~15-20 minutes  
**Quality:** Professional product photography

### 🏢 Architectural Renders

```
Scene composition → Suggest camera angles →
Refine materials → Export presentation
```

**Timeline:** ~20-30 minutes  
**Quality:** Architectural visualization standard

### 👤 Character Materials

```
Adjust material properties → Claude analyzes appearance →
Tweak values → Production quality materials
```

**Timeline:** ~10-15 minutes  
**Quality:** Game-ready or film-quality

### 📚 Learning & Best Practices

Every Claude suggestion includes reasoning — **learn Blender optimization patterns** as you iterate.

---

## 📂 File Structure

```
blender-mcp-feedback/
├── SKILL.md                              # Skill definition & quick reference
├── scripts/
│   ├── blender_quick_template.py         # ⭐ START HERE - Minimal setup
│   ├── blender_mcp_callback_system.py    # Full production system
│   └── blender_mcp_handler.py            # Claude-side analysis
└── references/
    ├── API_REFERENCE.md                  # Complete technical documentation
    └── BLENDER_MCP_WORKFLOW.md           # Detailed workflow guide
```

### File Reference

| File | Size | Purpose | Best For |
|------|------|---------|----------|
| `blender_quick_template.py` | 12 KB | Minimal, copy-paste implementation | Getting started immediately |
| `blender_mcp_callback_system.py` | 18 KB | Full production system | Advanced session management |
| `blender_mcp_handler.py` | 16 KB | Analysis engine | Understanding Claude side |
| `SKILL.md` | 25 KB | Skill definition | Reference & command syntax |
| `API_REFERENCE.md` | 22 KB | Technical documentation | Building extensions |
| `BLENDER_MCP_WORKFLOW.md` | 28 KB | Complete workflow guide | Mastering the system |

---

## ⚙️ Configuration

### Basic Setup

```python
mcp = QuickBlenderMCP()

# Default configuration automatically:
# - Creates session directory: {blender_file_dir}/mcp_session/
# - Names iterations: state_01.json, state_02.json, etc.
# - Saves screenshots: viewport_0001.png, viewport_0002.png, etc.
```

### Custom Render Settings

```python
# Configure in Blender before capturing:
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.cycles.samples = 256
bpy.context.scene.cycles.use_denoising = True
```

### Session Organization

```
{blender_file_dir}/
└── mcp_session/
    └── {session_id}/
        ├── viewport_0001.png
        ├── state_01.json
        ├── viewport_0002.png
        ├── state_02.json
        └── ...
```

---

## 🐛 Troubleshooting

### Template Won't Load

**Problem:** Script error in Blender  
**Solution:**
- ✅ Verify Script Editor is open (Alt+Tab)
- ✅ Check file path is correct
- ✅ Ensure `.blend` file is saved first (required for `bpy.data.filepath`)

### Commands Not Applying

**Problem:** Blender doesn't execute MCP commands  
**Solution:**
- ✅ Exit Edit Mode (press Tab key)
- ✅ Verify object/material names match **exactly**
- ✅ Check Blender is at Object Level (not in a specific viewport)

### Screenshot Not Saving

**Problem:** Viewport screenshot fails  
**Solution:**
- ✅ Save `.blend` file (must have valid filepath)
- ✅ Check output directory permissions
- ✅ Verify render output path is configured

### Base64 Encoding Error

**Problem:** Image encoding fails  
**Solution:**
- ✅ Install Pillow: `pip install Pillow`
- ✅ Use Blender's built-in Python (not external Python)

### Scene State JSON Not Printing

**Problem:** `mcp.print_instructions()` doesn't display JSON  
**Solution:**
- ✅ Check Blender System Console (Window → Toggle System Console)
- ✅ Verify `capture_and_export()` completed successfully
- ✅ Check file permissions for session directory

---

## ❓ FAQ

### Q: How many iterations do I need?
**A:** Typically **2-4 cycles** to reach quality 85+. Most projects converge quickly once composition is locked.

### Q: Can I use EEVEE instead of CYCLES?
**A:** Yes! EEVEE is faster for previews (use samples: 64-128). Switch to CYCLES (256+ samples) for final quality.

### Q: What GPUs are supported?
**A:** 
- ✅ NVIDIA CUDA (best performance)
- ✅ AMD HIP (good support)
- ✅ Intel Arc (supported)
- ✅ CPU fallback (slower, works fine)

### Q: Can I use this with my existing Blender add-ons?
**A:** Yes! The system is purely API-based. No conflicts with existing add-ons.

### Q: Do I need internet for every iteration?
**A:** Only to communicate with Claude (send JSON, receive commands). Blender execution is fully local.

### Q: Can I extend this with custom commands?
**A:** Yes! Edit `apply_mcp_command()` in `blender_mcp_callback_system.py` to add custom commands.

### Q: What's the minimum Blender version?
**A:** Blender 3.5+ (tested and verified on 3.5, 3.6, 4.0+)

### Q: Is this free to use?
**A:** Yes! The skill is open-source. You need a Claude subscription to use MCP features.

---

## 📊 Quality Metrics Breakdown

Claude analyzes and scores based on:

| Category | Weight | What's Evaluated |
|----------|--------|------------------|
| **Rendering Quality** | 30% | Engine choice, samples, denoising, preview vs. production |
| **Lighting** | 25% | Key light, fill light, shadows, scene setup |
| **Materials** | 20% | Roughness, metallic, color, transparency, complexity |
| **Composition** | 15% | Framing, camera angle, depth of field, balance |
| **Technical** | 10% | Render time, VRAM usage, scene organization |

**Total: 100 points**

---

## 🚀 Performance Tips

### Preview vs. Production Strategy

```
PREVIEW MODE (Fast iteration)
├─ Engine: EEVEE
├─ Shading: SOLID
└─ Samples: 64-128

FEEDBACK MODE (Balanced)
├─ Engine: CYCLES
├─ Shading: MATERIAL
└─ Samples: 128-256

FINAL MODE (Best quality)
├─ Engine: CYCLES
├─ Shading: RENDERED
└─ Samples: 256-512+
```

### Speed Optimization

1. ✅ Start with **EEVEE/SOLID** for quick previews
2. ✅ Switch to **CYCLES/RENDERED** once composition locked
3. ✅ Increase samples only for **final renders**
4. ✅ Use **denoising** to reduce render time

### Memory Management

- Each iteration ~5-10 MB (depends on resolution)
- Full session for 4 iterations ~40 MB
- Clean up old sessions if storage is limited

---

## 📖 Documentation

- **SKILL.md** — Quick reference (10 min read)
- **API_REFERENCE.md** — Complete API documentation (30 min read)
- **BLENDER_MCP_WORKFLOW.md** — Detailed workflow guide (20 min read)

---

## 🤝 Contributing

Contributions welcome! Areas for extension:

- Additional MCP commands (lighting, modifiers, etc.)
- Custom analysis rules for specific domains
- Integration with other Claude features
- Performance optimizations

---

## 📝 License

MIT License — Free to use, modify, and distribute

---

## 🎓 Learning Resources

### Getting Started
1. Read this README
2. Load `blender_quick_template.py`
3. Run a single iteration cycle
4. Review Claude's suggestions and commands

### Intermediate
1. Study `SKILL.md` complete workflow
2. Execute 3-4 full iteration cycles
3. Experiment with different scene types
4. Read `BLENDER_MCP_WORKFLOW.md`

### Advanced
1. Read `API_REFERENCE.md` complete reference
2. Study `blender_mcp_callback_system.py` implementation
3. Create custom MCP commands
4. Build Blender add-on integration

---

## ✅ Checklist: First Time Setup

- [ ] Download `blender-mcp-feedback/` folder
- [ ] Open Blender with your .blend file
- [ ] Copy `blender_quick_template.py` to your project
- [ ] Open Script Editor (Alt+Tab)
- [ ] Paste entire template script
- [ ] Run it (Alt+P) or press play button
- [ ] Initialize: `mcp = QuickBlenderMCP()`
- [ ] Capture: `state = mcp.capture_and_export()`
- [ ] Copy printed JSON
- [ ] Send to Claude with context
- [ ] Get MCP commands from Claude
- [ ] Execute: `mcp.apply_changes(commands)`
- [ ] Watch viewport update! 🎉
- [ ] Iterate until quality ≥ 85/100
- [ ] Export final render

---

## 📞 Support

**Issues or questions?**

1. Check the **Troubleshooting** section above
2. Review **FAQ** for common questions
3. Consult `BLENDER_MCP_WORKFLOW.md` for detailed examples
4. Read `API_REFERENCE.md` for technical details

---

## 🎉 Ready to Start?

**1. Download** → **2. Load Template** → **3. Capture Viewport** → **4. Send to Claude** → **5. Execute Commands** → **6. Iterate!**

```python
# Your first command:
exec(open('/path/to/blender_quick_template.py').read())
mcp = QuickBlenderMCP()
state = mcp.capture_and_export()
```

---

<div align="center">

### 🚀 Transform Your Blender Renders with AI-Powered Feedback

**v1.0.0** • Blender 3.5+ • Python 3.8+ • ✓ Production Ready

[⬆ Back to Top](#blender-claude-mcp-feedback-loop) • [Report Issue](#) • [Request Feature](#)

**Made with ❤️ for Blender & AI lovers**

</div>
