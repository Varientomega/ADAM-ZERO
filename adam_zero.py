"""
ADAM-ZERO: AI Development and Management System
Where Gemini orchestrates and Claude codes!
"""
import os
from typing import Optional, Dict, Any
from gemini_client import GeminiOrchestrator
from chatgpt_client import ChatGPTClient


class AdamZero:
    """
    Main orchestration system combining Gemini's planning with Claude's coding.
    """

    def __init__(self):
        """Initialize ADAM-ZERO with Gemini orchestrator and ChatGPT client."""
        self.gemini = GeminiOrchestrator()
        self.chatgpt = ChatGPTClient()
        print("🚀 ADAM-ZERO initialized!")
        print("  - Gemini: Orchestration & Planning")
        print("  - Claude: Coding & Implementation")
        print("  - ChatGPT: Code Review & Suggestions")

    def process_request(self, user_request: str) -> Dict[str, Any]:
        """
        Process a user request through the full pipeline.

        1. Gemini creates the plan and defines tasks
        2. Returns the plan for Claude to implement
        3. ChatGPT can optionally review the results

        Args:
            user_request: What the user wants to build/do

        Returns:
            Dictionary with plan, tasks, and next steps
        """
        print(f"\n📝 Processing request: {user_request}")
        print("\n🧠 Gemini is orchestrating...")

        # Gemini creates the plan
        orchestration = self.gemini.orchestrate(user_request)

        print("\n✅ Orchestration complete!")
        print("\n" + "="*60)
        print("PLAN FROM GEMINI:")
        print("="*60)
        print(orchestration['plan'])

        print("\n" + "="*60)
        print("CODING TASKS FOR CLAUDE:")
        print("="*60)
        print(orchestration['coding_tasks'])

        if orchestration['architecture']:
            print("\n" + "="*60)
            print("ARCHITECTURE NOTES:")
            print("="*60)
            print(orchestration['architecture'])

        return {
            'orchestration': orchestration,
            'next_step': 'Claude should now implement the coding tasks above',
            'status': 'ready_for_coding'
        }

    def review_with_chatgpt(self, code: str, language: str = "python") -> str:
        """
        Use ChatGPT to review code that was implemented.

        Args:
            code: The code to review
            language: Programming language

        Returns:
            Review feedback
        """
        print("\n🔍 ChatGPT is reviewing the code...")
        review = self.chatgpt.review_code(code, language)
        print("\n✅ Review complete!")
        return review


def main():
    """Example usage of ADAM-ZERO."""
    adam = AdamZero()

    # Example: User wants to build something
    result = adam.process_request(
        "Build a REST API that stores user preferences and provides recommendations"
    )

    print("\n" + "="*60)
    print("🎯 NEXT STEPS:")
    print("="*60)
    print(result['next_step'])
    print("\nNow Claude (you!) should implement the coding tasks above.")


if __name__ == "__main__":
    main()
