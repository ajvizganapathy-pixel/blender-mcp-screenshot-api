# Blender-Claude MCP Feedback Loop Skill
## Installation & Usage Guide

---

## 📦 What You've Got

Your custom skill package contains:

```
blender-mcp-feedback/
├── SKILL.md                          # Main skill definition
├── scripts/
│   ├── blender_quick_template.py     # Fast, minimal setup
│   ├── blender_mcp_callback_system.py # Full system, production-ready
│   └── blender_mcp_handler.py        # Claude-side analysis engine
└── references/
    ├── BLENDER_MCP_WORKFLOW.md       # Complete workflow guide
    └── API_REFERENCE.md              # Technical documentation
```

---

## 🚀 Installation

### Option 1: Import into Claude (Recommended)

The skill is already available in your chat. To make it persistent across chats:

1. **Save the skill folder** to your local machine from the downloads
2. **In Claude.ai Settings → Skills**, click "Add Custom Skill"
3. **Upload the `blender-mcp-feedback` folder** (or the `.skill` package file)
4. ✓ Skill now appears in all your chats

### Option 2: Manual Installation

Copy the entire `blender-mcp-feedback` folder to:

**On your computer:**
```
~/Claude/skills/blender-mcp-feedback/
```

This makes it available whenever you reference it in Claude.

### Option 3: Use Directly

The scripts are immediately usable. Copy any script into your Blender project:

```python
# In Blender Script Editor:
exec(open('/path/to/scripts/blender_quick_template.py').read())
```

---

## 💡 Quick Start (30 seconds)

### Step 1: Load Template in Blender

Copy entire contents of `scripts/blender_quick_template.py` into **Blender Script Editor** and run.

### Step 2: Capture Your Viewport

```python
mcp = QuickBlenderMCP()
state = mcp.capture_and_export()
mcp.print_instructions()
```

### Step 3: Ask Claude (This Chat)

Copy the printed JSON and send to Claude:
```
Please review this Blender viewport: [PASTE JSON HERE]
Analyze for issues and provide MCP commands.
```

### Step 4: Execute Claude's Response

```python
commands = [
    {"command": "set_render_engine", "params": {"engine": "CYCLES", "samples": 256}},
    ...
]
mcp.apply_changes(commands)
```

### Step 5: Iterate

Capture → Send → Analyze → Execute → Repeat

---

## 📚 When This Skill Triggers

Claude automatically uses this skill when you ask about:

- ✅ "Review my Blender viewport"
- ✅ "Improve this 3D render"
- ✅ "Analyze my Blender scene"
- ✅ "What's wrong with my lighting?"
- ✅ "Help me refine materials"
- ✅ "Suggest rendering improvements"
- ✅ Sending Blender screenshots with analysis requests

---

## 🎯 Real-World Workflow

### Use Case: Product Visualization (PCB Enclosure)

```
1. Design geometry in Blender
   └─ Basic materials assigned

2. Send viewport to Claude
   └─ "Review this PCB enclosure render. Suggest improvements."

3. Claude analyzes & returns MCP commands
   ├─ Set CYCLES render engine
   ├─ Adjust material roughness
   ├─ Improve lighting angle
   └─ Suggest camera angle

4. Execute commands in Blender
   └─ Scene updates automatically

5. Capture updated screenshot
   └─ Send for next iteration

6. 2-3 cycles later
   └─ ✓ Production-quality render ready to export
```

**Time per cycle:** 5-10 minutes  
**Total iterations needed:** Usually 2-4  
**Final result:** Professional product visualization

---

## 🔧 Core Commands Available

### Rendering
```python
{"command": "set_render_engine", "params": {"engine": "CYCLES", "samples": 256}}
{"command": "set_viewport_shading", "params": {"shading_type": "RENDERED"}}
{"command": "render_viewport", "params": {"output_path": "render.png"}}
```

### Materials
```python
{"command": "adjust_material", "params": {
  "object_name": "Sphere",
  "material_name": "Material",
  "adjustments": {"roughness": 0.3, "metallic": 0.8}
}}
```

### Selection & Camera
```python
{"command": "select_object", "params": {"object_name": "Cube"}}
{"command": "set_camera_view", "params": {"camera_name": "Camera.001"}}
```

---

## 📖 File Guide

### SKILL.md (Main Skill File)
- **What:** Skill definition, quick start, command reference
- **Read when:** Setting up, you need command syntax, overview
- **Time:** 10 minutes

### scripts/blender_quick_template.py (Start Here)
- **What:** Minimal, copy-paste implementation
- **Read when:** You want to start immediately
- **Time:** 2 minutes to copy, 1 minute to run

### scripts/blender_mcp_callback_system.py (Full System)
- **What:** Complete production implementation with all features
- **Read when:** You need advanced session management
- **Time:** 30 minutes study, 5 minutes to integrate

### references/BLENDER_MCP_WORKFLOW.md (Detailed Guide)
- **What:** Complete workflow examples, troubleshooting, pro tips
- **Read when:** You want to master the system
- **Time:** 20 minutes

### references/API_REFERENCE.md (Technical Docs)
- **What:** Class methods, MCP command specs, architecture
- **Read when:** Building custom extensions
- **Time:** Reference, as needed

---

## 🎓 Learning Path

**Beginner (Just want results):**
1. Load `scripts/blender_quick_template.py`
2. Run it in Blender
3. Send screenshot to Claude
4. Execute Claude's commands
5. Iterate 2-3 times

**Intermediate (Want to understand it):**
1. Read: SKILL.md quick start section
2. Study: `scripts/blender_quick_template.py` code
3. Read: `references/BLENDER_MCP_WORKFLOW.md` complete workflow
4. Practice: Do 3-4 full iteration cycles

**Advanced (Building on it):**
1. Read: `references/API_REFERENCE.md` complete reference
2. Study: `scripts/blender_mcp_callback_system.py` architecture
3. Extend: Add custom MCP commands
4. Integrate: Build into your Blender add-on

---

## 🐛 Troubleshooting

### "Template won't load"
→ Check Blender Script Editor is open (Alt+Tab)  
→ Verify Python path is correct  
→ Ensure .blend file is saved first

### "Commands not applying"
→ Exit Edit Mode (Tab key)  
→ Verify object/material names match exactly  
→ Check Blender is at Object Level (not in a workspace panel)

### "Screenshot not saving"
→ Save .blend file (must have filepath)  
→ Check output directory permissions  
→ Verify render.filepath is configured

### "Base64 encoding error"
→ Install Pillow: `pip install Pillow`  
→ Use Blender's built-in Python instead

**More help:** See `references/BLENDER_MCP_WORKFLOW.md` "Debugging" section

---

## 💬 How to Ask Claude Effectively

### Good Prompts
✅ "Review my Blender viewport for a product render. What would improve quality?"  
✅ "I'm rendering an enclosure. Suggest lighting and material improvements."  
✅ "Analyze this viewport and provide MCP commands to fix the issues."

### Include
✅ Scene state JSON from `capture_and_export()`  
✅ Your use case (product, architecture, character, animation)  
✅ Current challenges (too dark, materials look plastic, lighting flat)

### Avoid
❌ "Make my render better" (too vague)  
❌ Sending screenshot without scene state  
❌ Expecting changes without understanding context

---

## 🔄 Iteration Tips

### Quality Scoring
- **85-100:** Production-ready ✓
- **70-84:** Good, minor tweaks needed
- **50-69:** Significant improvements possible
- **<50:** Major adjustments required

### Speed Up Iteration
1. Start with EEVEE/SOLID preview mode
2. Switch to CYCLES/RENDERED once composition locked
3. Increase samples only for final renders
4. Use SOLID shading while tweaking materials

### Save Bandwidth
- Include specific concerns in your request
- Use iterations to progressively refine
- Tell Claude your final use case upfront

---

## 🎯 Common Scenarios

### Scenario 1: "My render is too dark"
```python
# Claude will suggest:
{
  "commands": [
    {"command": "set_render_engine", "params": {"engine": "CYCLES", "samples": 256}},
    {"command": "adjust_material", "params": {
      "object_name": "Cube",
      "material_name": "Material",
      "adjustments": {"roughness": 0.5}
    }}
  ]
}
```

### Scenario 2: "Viewport doesn't match render"
```python
# Claude will suggest:
{
  "commands": [
    {"command": "set_viewport_shading", "params": {"shading_type": "RENDERED"}},
    {"command": "set_render_engine", "params": {"engine": "CYCLES", "samples": 512}}
  ]
}
```

### Scenario 3: "Material looks plastic"
```python
# Claude will suggest:
{
  "commands": [
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
}
```

---

## 📋 Checklist: First Time Setup

- [ ] Download skill files
- [ ] Open Blender with your .blend file
- [ ] Copy `scripts/blender_quick_template.py` to your project directory
- [ ] Open Blender Script Editor (Alt+Tab)
- [ ] Paste entire template script
- [ ] Run it (Alt+P)
- [ ] See "✓ Blender MCP Callback System initialized"
- [ ] Run: `mcp = QuickBlenderMCP()`
- [ ] Run: `state = mcp.capture_and_export()`
- [ ] Copy printed JSON
- [ ] Open Claude (this chat)
- [ ] Paste JSON with: "Please review this viewport..."
- [ ] Get Claude's response with MCP commands
- [ ] Paste commands into Blender
- [ ] Run: `mcp.apply_changes(commands)`
- [ ] ✓ See viewport update automatically
- [ ] Iterate!

---

## 🎁 What's Included

| File | Purpose | Size |
|------|---------|------|
| SKILL.md | Skill definition & quick start | 25 KB |
| scripts/blender_quick_template.py | Fast setup version | 12 KB |
| scripts/blender_mcp_callback_system.py | Full system | 18 KB |
| scripts/blender_mcp_handler.py | Analysis engine | 16 KB |
| references/BLENDER_MCP_WORKFLOW.md | Complete guide | 28 KB |
| references/API_REFERENCE.md | Technical docs | 22 KB |

**Total:** ~121 KB (all text, no binaries)

---

## 🚀 Ready to Start?

1. **Load the template** in your next Blender session
2. **Capture your viewport** with `mcp.capture_and_export()`
3. **Send to Claude** with context about your project
4. **Execute the commands** Claude returns
5. **Iterate** until satisfied (usually 2-4 cycles)

The skill is ready to use immediately. No complex setup required!

---

## 📞 Need Help?

- **Quick issues:** Check `references/BLENDER_MCP_WORKFLOW.md` troubleshooting section
- **Command syntax:** See `references/API_REFERENCE.md` MCP Command Specifications
- **Workflow questions:** See `references/BLENDER_MCP_WORKFLOW.md` complete examples
- **First time?** Start with SKILL.md Quick Start section

---

**Skill Version:** 1.0.0  
**Created:** 2024-01-15  
**Blender Compatibility:** 3.5+  
**Status:** ✓ Ready to use
