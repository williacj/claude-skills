#!/usr/bin/env python3
"""
Test Claude Skills API to verify endpoint structure
"""
import os
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

def test_list_skills():
    """Test listing skills to verify API access"""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    try:
        # Try to list skills
        response = client.beta.skills.list(
            betas=["code-execution-2025-08-25", "skills-2025-10-02"]
        )
        print("✅ Skills API is accessible!")
        print(f"Response: {response}")
        return True
    except Exception as e:
        print(f"❌ Error accessing Skills API: {e}")
        return False

if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY environment variable not set")
        exit(1)
    
    test_list_skills()