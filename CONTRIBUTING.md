# Contributing to Blender-Claude MCP Feedback

Thank you for your interest in contributing! This guide will help you get started.

## 🚀 Getting Started

### Prerequisites
- Blender 3.5+
- Python 3.8+
- Claude API access (for testing)
- Git

### Fork & Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/blender-mcp-screenshot-api.git
cd blender-mcp-screenshot-api

# Add upstream remote
git remote add upstream https://github.com/ajvizganapathy-pixel/blender-mcp-screenshot-api.git
```

### Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
```

## 📝 Contribution Types

### Bug Reports

**Before reporting:**
- Check existing issues
- Reproduce with latest version
- Gather system info (Blender version, Python version, OS)

**When reporting, include:**
1. Blender version
2. Python version
3. Operating system
4. Steps to reproduce
5. Expected vs. actual behavior
6. Error traceback (if applicable)

### Feature Requests

**Before requesting:**
- Check existing issues and pull requests
- Ensure it aligns with skill's scope

**When requesting, describe:**
1. The feature in detail
2. Why it's useful
3. Example use cases
4. Potential implementation approach

### Code Contributions

**Process:**

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Follow Python style guide (PEP 8)
   - Add docstrings to functions
   - Include comments for complex logic

3. **Test thoroughly:**
   ```bash
   # Test in Blender Script Editor
   # Run manual test cases
   # Check for edge cases
   ```

4. **Commit with clear messages:**
   ```bash
   git commit -m "Add: Description of changes

   - Point 1
   - Point 2
   
   Fixes #123"
   ```

5. **Push and create Pull Request:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **PR Template:**
   - [ ] All tests pass
   - [ ] New code follows style guidelines
   - [ ] PR description is clear
   - [ ] Documentation updated
   - [ ] Issue number referenced

## 📐 Code Style

### Python Guidelines

```python
# Good: Clear function documentation
def apply_mcp_command(command: dict) -> dict:
    """
    Execute a single MCP command in Blender.
    
    Args:
        command: MCP command dict with 'command' and 'params' keys
        
    Returns:
        Status dict with 'status', 'command', and optional 'message' keys
        
    Raises:
        ValueError: If command format is invalid
    """
    pass

# Good: Type hints
def capture_screenshot(output_path: str = None) -> str:
    """Capture viewport and return base64 encoded image."""
    pass

# Bad: Unclear naming and no docs
def cap_ss(p=None):
    pass
```

### Naming Conventions

```python
# Classes: PascalCase
class BlenderMCPCallbackSystem:
    pass

# Functions/Variables: snake_case
def export_scene_state():
    scene_data = {}
    return scene_data

# Constants: UPPER_SNAKE_CASE
DEFAULT_SAMPLE_COUNT = 256
MCP_COMMAND_TIMEOUT = 30

# Private methods: leading underscore
def _internal_helper():
    pass
```

## 🧪 Testing

### Manual Testing in Blender

```python
# 1. Load the script
exec(open('/path/to/blender_quick_template.py').read())

# 2. Test initialization
mcp = QuickBlenderMCP()
assert mcp is not None, "Failed to initialize"

# 3. Test capture
state = mcp.capture_and_export()
assert 'iteration' in state, "Missing iteration field"
assert state['iteration'] > 0, "Invalid iteration"

# 4. Test command execution
commands = [
    {"command": "set_render_engine", "params": {"engine": "CYCLES", "samples": 128}}
]
mcp.apply_changes(commands)

print("✓ All manual tests passed")
```

### Edge Cases to Test

- Empty scene
- Very large scene (100+ objects)
- Missing render engine
- Invalid object/material names
- Various Blender versions
- Different operating systems

## 📚 Documentation

### Updating Docs

- **SKILL.md** — Skill definition and quick reference
- **API_REFERENCE.md** — Complete API documentation
- **BLENDER_MCP_WORKFLOW.md** — Detailed workflow guide

### Doc Standards

1. Clear, concise language
2. Code examples for complex topics
3. Table of contents for long docs
4. Links to related sections
5. Keep examples up-to-date with code

## 🔄 Pull Request Workflow

1. **Check existing PRs** — Avoid duplicate work
2. **Create branch** — Use descriptive name (e.g., `fix/viewport-capture-issue`)
3. **Make changes** — Small, focused commits
4. **Test thoroughly** — Both manual and automated
5. **Update docs** — If adding features
6. **Create PR** — With clear description and issue reference

## ✅ PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass (manual + automated if applicable)
- [ ] Documentation updated
- [ ] Docstrings added/updated
- [ ] No breaking changes (or clearly documented)
- [ ] Issue number referenced
- [ ] Changelog updated (if major change)

## 🎯 Priority Areas for Contribution

### High Priority
- Bug fixes
- Performance improvements
- Documentation improvements
- User experience enhancements

### Medium Priority
- New MCP commands
- Extended platform support
- Better error handling
- More comprehensive testing

### Nice to Have
- Visual enhancements
- Additional examples
- Tutorial videos
- Community examples

## 📞 Communication

- **Issues** — Bug reports and feature requests
- **Discussions** — General questions and ideas
- **PRs** — Code contributions

## 🎓 Development Tips

### Debugging in Blender

```python
# 1. Enable verbose output
import logging
logging.basicConfig(level=logging.DEBUG)

# 2. Print intermediate values
print(f"DEBUG: scene_state = {scene_state}")

# 3. Use Python debugger
import pdb; pdb.set_trace()

# 4. Check Blender System Console
# Window → Toggle System Console
```

### Common Issues & Solutions

**Issue:** MCP command not executing  
**Solution:** Verify object/material names, check Blender is at Object Level

**Issue:** Screenshot not saving  
**Solution:** Ensure .blend file is saved, check permissions

**Issue:** Memory errors with large scenes  
**Solution:** Reduce sample count, optimize geometry, enable denoising

## 📋 Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (no logic change)
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `test:` Adding/updating tests

**Example:**
```
feat: Add support for EEVEE material adjustments

- Implement material property adjustment for EEVEE-rendered objects
- Add new MCP command: adjust_eevee_material
- Update API documentation

Closes #42
```

## 🚀 Publishing Changes

1. Ensure all tests pass
2. Update version number in SKILL.md
3. Update CHANGELOG.md
4. Create release branch
5. Create GitHub Release with changelog

## 📖 Additional Resources

- [Blender Python API Docs](https://docs.blender.org/api/current/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Git Workflow Guide](https://git-scm.com/book/en/v2)

## 💡 Ideas & Inspiration

Potential contributions:

### New Features
- Real-time viewport streaming
- Batch processing multiple scenes
- Integration with Blender add-ons
- Custom analysis rules for specific domains

### Improvements
- Performance optimization for large scenes
- Better error messages and logging
- Expanded platform support
- More comprehensive testing

### Documentation
- Video tutorials
- Written guides for specific use cases
- API reference expansion
- Best practices guide

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Your contributions help make this project better for everyone. We appreciate your time and effort!

---

**Questions?** Feel free to open an issue or discussion. Happy coding! 🎉
