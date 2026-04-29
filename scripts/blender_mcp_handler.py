"""
Claude MCP Handler for Blender Integration
Analyzes Blender viewport screenshots and generates MCP commands for refinement

This handler:
1. Receives viewport screenshots from Blender
2. Analyzes them for visual/technical issues
3. Generates structured MCP commands for Blender
4. Manages iterative refinement cycles
"""

import json
import base64
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class IssueCategory(Enum):
    """Categories of issues detected in Blender renders"""
    LIGHTING = "lighting"
    MATERIAL = "material"
    COMPOSITION = "composition"
    RENDERING = "rendering"
    MODELING = "modeling"
    CAMERA = "camera"
    PERFORMANCE = "performance"


@dataclass
class ViewportIssue:
    """Represents an identified issue in the viewport"""
    category: IssueCategory
    severity: str  # "critical", "high", "medium", "low"
    description: str
    location: Optional[str] = None
    recommended_fix: Optional[str] = None
    mcp_commands: Optional[List[Dict]] = None


class BlenderMCPHandler:
    """Main handler for Claude-Blender MCP interaction"""
    
    def __init__(self):
        self.review_queue = []
        self.executed_commands = []
        self.issue_history = []
        
    def analyze_viewport_screenshot(self, screenshot_data: Dict) -> Dict:
        """
        Analyze a Blender viewport screenshot for issues and opportunities
        
        Args:
            screenshot_data: {
                'image_base64': str,
                'scene_state': Dict,
                'timestamp': str,
                'callback_index': int
            }
        
        Returns:
            Analysis result with identified issues and recommended MCP commands
        """
        scene_state = screenshot_data.get('scene_state', {})
        
        analysis = {
            'timestamp': screenshot_data['timestamp'],
            'callback_index': screenshot_data['callback_index'],
            'scene_state': scene_state,
            'identified_issues': [],
            'recommended_commands': [],
            'priority_actions': [],
            'quality_score': 0.0,
        }
        
        # Analyze render engine and settings
        issues = self._analyze_render_settings(scene_state)
        analysis['identified_issues'].extend(issues)
        
        # Analyze viewport shading
        shading_issues = self._analyze_viewport_shading(scene_state)
        analysis['identified_issues'].extend(shading_issues)
        
        # Analyze composition
        composition_issues = self._analyze_composition(scene_state)
        analysis['identified_issues'].extend(composition_issues)
        
        # Generate MCP commands from issues
        commands = self._generate_mcp_commands(analysis['identified_issues'], scene_state)
        analysis['recommended_commands'] = commands
        
        # Prioritize actions
        analysis['priority_actions'] = self._prioritize_actions(analysis['identified_issues'])
        
        # Calculate quality score
        analysis['quality_score'] = self._calculate_quality_score(analysis['identified_issues'])
        
        return analysis
    
    def _analyze_render_settings(self, scene_state: Dict) -> List[ViewportIssue]:
        """Analyze rendering engine and quality settings"""
        issues = []
        
        engine = scene_state.get('render_engine', '')
        samples = scene_state.get('sample_count')
        
        # Check render engine
        if engine == 'BLENDER_EEVEE':
            issues.append(ViewportIssue(
                category=IssueCategory.RENDERING,
                severity="medium",
                description="Using EEVEE (faster but lower quality). Consider CYCLES for production renders.",
                recommended_fix="Switch to CYCLES with appropriate sample count",
                mcp_commands=[{
                    "command": "set_render_engine",
                    "params": {"engine": "CYCLES", "samples": 256}
                }]
            ))
        
        # Check sample count
        if samples and samples < 128:
            issues.append(ViewportIssue(
                category=IssueCategory.RENDERING,
                severity="high",
                description=f"Low sample count ({samples}). Image will be noisy.",
                recommended_fix="Increase samples to at least 256-512",
                mcp_commands=[{
                    "command": "set_render_engine",
                    "params": {"engine": "CYCLES", "samples": 256}
                }]
            ))
        
        return issues
    
    def _analyze_viewport_shading(self, scene_state: Dict) -> List[ViewportIssue]:
        """Analyze viewport shading and lighting setup"""
        issues = []
        
        shading = scene_state.get('viewport_shading', {})
        shading_type = shading.get('type', '')
        
        # Check if scene lights are being used
        if not shading.get('use_scene_lights') and shading_type in ['MATERIAL', 'RENDERED']:
            issues.append(ViewportIssue(
                category=IssueCategory.LIGHTING,
                severity="high",
                description="Scene lights are disabled. Results may look unlit.",
                recommended_fix="Enable scene lights for proper visualization",
                mcp_commands=[{
                    "command": "set_viewport_shading",
                    "params": {"shading_type": "MATERIAL"}
                }]
            ))
        
        # Recommend rendered view for best preview
        if shading_type != 'RENDERED':
            issues.append(ViewportIssue(
                category=IssueCategory.RENDERING,
                severity="low",
                description=f"Using {shading_type} shading. RENDERED view gives most accurate preview.",
                recommended_fix="Switch to RENDERED viewport shading",
                mcp_commands=[{
                    "command": "set_viewport_shading",
                    "params": {"shading_type": "RENDERED"}
                }]
            ))
        
        return issues
    
    def _analyze_composition(self, scene_state: Dict) -> List[ViewportIssue]:
        """Analyze scene composition and camera setup"""
        issues = []
        
        selected_count = len(scene_state.get('selected_objects', []))
        camera = scene_state.get('camera')
        
        # Check if camera is set
        if not camera:
            issues.append(ViewportIssue(
                category=IssueCategory.CAMERA,
                severity="critical",
                description="No camera set in scene. Rendering will fail.",
                recommended_fix="Create and set a camera for the scene",
                mcp_commands=[{
                    "command": "create_and_set_camera",
                    "params": {}
                }]
            ))
        
        # Check if multiple objects are selected (good for batch operations)
        if selected_count > 1:
            issues.append(ViewportIssue(
                category=IssueCategory.COMPOSITION,
                severity="low",
                description=f"{selected_count} objects selected. Ready for batch operations.",
                recommended_fix="None - this is good for multi-object workflows"
            ))
        
        return issues
    
    def _generate_mcp_commands(self, issues: List[ViewportIssue], 
                               scene_state: Dict) -> List[Dict]:
        """Generate MCP commands from identified issues"""
        commands = []
        
        # Collect all recommended commands from issues
        for issue in issues:
            if issue.mcp_commands:
                commands.extend(issue.mcp_commands)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_commands = []
        for cmd in commands:
            cmd_str = json.dumps(cmd, sort_keys=True)
            if cmd_str not in seen:
                seen.add(cmd_str)
                unique_commands.append(cmd)
        
        return unique_commands
    
    def _prioritize_actions(self, issues: List[ViewportIssue]) -> List[Dict]:
        """Prioritize action items by severity"""
        priority_map = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        
        sorted_issues = sorted(
            issues,
            key=lambda x: priority_map.get(x.severity, 99)
        )
        
        return [
            {
                'priority': i + 1,
                'severity': issue.severity,
                'category': issue.category.value,
                'description': issue.description,
                'fix': issue.recommended_fix,
            }
            for i, issue in enumerate(sorted_issues)
        ]
    
    def _calculate_quality_score(self, issues: List[ViewportIssue]) -> float:
        """Calculate render quality score (0-100)"""
        score = 100.0
        
        severity_penalty = {
            "critical": 30,
            "high": 15,
            "medium": 5,
            "low": 1
        }
        
        for issue in issues:
            penalty = severity_penalty.get(issue.severity, 0)
            score -= penalty
        
        return max(0.0, score)
    
    def generate_claude_prompt(self, analysis: Dict) -> str:
        """Generate a structured prompt for Claude based on analysis"""
        
        prompt = f"""
## Blender Viewport Analysis

**Quality Score:** {analysis['quality_score']:.1f}/100

### Identified Issues:
"""
        
        for i, issue in enumerate(analysis['identified_issues'], 1):
            issue_obj = ViewportIssue(
                category=IssueCategory[issue.get('category', 'RENDERING').upper()] 
                         if isinstance(issue, dict) else issue.category,
                severity=issue.get('severity', 'medium') if isinstance(issue, dict) else issue.severity,
                description=issue.get('description', '') if isinstance(issue, dict) else issue.description,
            )
            prompt += f"\n{i}. **[{issue_obj.severity.upper()}] {issue_obj.category.value.title()}**\n"
            prompt += f"   {issue_obj.description}\n"
        
        prompt += "\n### Recommended MCP Commands:\n"
        for i, cmd in enumerate(analysis['recommended_commands'], 1):
            prompt += f"\n{i}. `{cmd.get('command')}`\n"
            if 'params' in cmd:
                prompt += f"   Parameters: {json.dumps(cmd['params'], indent=4)}\n"
        
        prompt += "\n### Priority Actions:\n"
        for action in analysis['priority_actions']:
            prompt += f"\n- [{action['priority']}] {action['description']}\n"
        
        return prompt
    
    def process_mcp_response(self, claude_response: str) -> List[Dict]:
        """
        Parse Claude's response and extract MCP commands
        
        Expected format:
        ```json
        {
            "commands": [
                {"command": "set_render_engine", "params": {...}},
                ...
            ],
            "reasoning": "explanation of changes",
            "expected_improvements": ["improvement1", "improvement2"]
        }
        ```
        """
        try:
            # Extract JSON from Claude response
            import re
            json_match = re.search(r'```json\n(.*?)\n```', claude_response, re.DOTALL)
            
            if json_match:
                response_data = json.loads(json_match.group(1))
                return response_data.get('commands', [])
            else:
                # Try to parse entire response as JSON
                response_data = json.loads(claude_response)
                return response_data.get('commands', [])
        
        except json.JSONDecodeError:
            return []
    
    def create_feedback_loop(self, initial_screenshot: Dict) -> Dict:
        """
        Create a complete feedback loop cycle
        
        Returns structure for iterative refinement
        """
        loop_cycle = {
            'cycle_number': len(self.review_queue) + 1,
            'initial_screenshot': initial_screenshot,
            'analysis': self.analyze_viewport_screenshot(initial_screenshot),
            'status': 'ready_for_claude_review',
            'next_steps': [
                '1. Review the analysis above',
                '2. Provide MCP commands to fix issues',
                '3. Blender will execute the commands',
                '4. Capture new screenshot for comparison',
                '5. Iterate until quality score >= 85'
            ]
        }
        
        self.review_queue.append(loop_cycle)
        return loop_cycle


# ============================================================================
# EXAMPLE USAGE - Format for Claude prompts
# ============================================================================

def example_claude_integration():
    """Shows how to use the handler with Claude"""
    
    handler = BlenderMCPHandler()
    
    # Simulated Blender viewport data
    blender_data = {
        'image_base64': 'iVBORw0KGgo...',  # Would be actual screenshot
        'scene_state': {
            'render_engine': 'BLENDER_EEVEE',
            'sample_count': 64,
            'viewport_shading': {
                'type': 'SOLID',
                'use_scene_lights': True,
                'use_scene_world': False
            },
            'selected_objects': ['Cube', 'Camera'],
            'camera': 'Camera',
            'objects_count': 3,
            'materials_count': 2,
        },
        'timestamp': '2024-01-15T10:30:00',
        'callback_index': 0
    }
    
    # Analyze
    analysis = handler.analyze_viewport_screenshot(blender_data)
    
    # Create feedback loop
    feedback = handler.create_feedback_loop(blender_data)
    
    # Generate prompt for Claude
    claude_prompt = handler.generate_claude_prompt(analysis)
    
    return {
        'analysis': analysis,
        'feedback_loop': feedback,
        'claude_prompt': claude_prompt
    }


if __name__ == "__main__":
    result = example_claude_integration()
    print("Handler ready for integration with Claude MCP")
    print(json.dumps(result['analysis'], indent=2, default=str))
