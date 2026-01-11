"""Gemini API client for orchestration and planning."""
import os
from typing import Optional, List, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class GeminiOrchestrator:
    """Gemini-powered orchestrator for planning and coordination."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini client."""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def plan_task(self, task_description: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Use Gemini to create a plan for a given task.

        Args:
            task_description: The task to plan
            context: Optional context information

        Returns:
            The plan as a string
        """
        prompt = f"""You are an orchestrator AI. Your job is to break down tasks into clear, actionable steps.

Task: {task_description}

{f"Context: {context}" if context else ""}

Please create a detailed plan with numbered steps. Be specific about what needs to be done.
Focus on the logic and architecture, not the implementation details.
"""

        response = self.model.generate_content(prompt)
        return response.text

    def orchestrate(self, user_request: str) -> Dict[str, Any]:
        """
        Orchestrate a user request by creating a plan and determining what to code.

        Args:
            user_request: The user's request

        Returns:
            Dictionary containing the plan and coding tasks
        """
        prompt = f"""You are an orchestration AI working with a coding AI (Claude).
Your role is to analyze requests, create plans, and specify what code needs to be written.

User Request: {user_request}

Please provide:
1. A high-level plan (what needs to happen)
2. Specific coding tasks (what files/functions need to be created/modified)
3. Any design decisions or architectural considerations

Format your response as:
PLAN:
[Your plan here]

CODING TASKS:
[Specific tasks for the coding AI]

ARCHITECTURE NOTES:
[Any important design decisions]
"""

        response = self.model.generate_content(prompt)
        return {
            "raw_response": response.text,
            "plan": self._extract_section(response.text, "PLAN:"),
            "coding_tasks": self._extract_section(response.text, "CODING TASKS:"),
            "architecture": self._extract_section(response.text, "ARCHITECTURE NOTES:")
        }

    def _extract_section(self, text: str, section_marker: str) -> str:
        """Extract a section from the response."""
        if section_marker not in text:
            return ""

        parts = text.split(section_marker)
        if len(parts) < 2:
            return ""

        section_text = parts[1]
        # Find the next section marker or end of text
        next_markers = ["PLAN:", "CODING TASKS:", "ARCHITECTURE NOTES:"]
        end_pos = len(section_text)

        for marker in next_markers:
            if marker != section_marker and marker in section_text:
                pos = section_text.index(marker)
                end_pos = min(end_pos, pos)

        return section_text[:end_pos].strip()


if __name__ == "__main__":
    # Example usage
    orchestrator = GeminiOrchestrator()
    result = orchestrator.orchestrate("Build a web scraper that extracts product prices")
    print("=== ORCHESTRATION RESULT ===")
    print(result["raw_response"])
