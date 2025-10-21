#!/usr/bin/env python3
"""
Explore Claude Skills API to understand available endpoints
"""
import os
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

def explore_skills_api():
    """Explore the Skills API to understand its structure"""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    print("🔍 Exploring Skills API endpoints...\n")
    
    try:
        # Test 1: List skills
        print("1. Testing client.beta.skills.list():")
        response = client.beta.skills.list(
            betas=["code-execution-2025-08-25", "skills-2025-10-02"]
        )
        print(f"   ✅ Success: {len(response.data)} skills found")
        for skill in response.data:
            print(f"      - {skill.id}: {skill.display_title} (v{skill.latest_version})")
        
        # Test 2: Try to understand the client structure
        print(f"\n2. Skills client structure:")
        print(f"   - client.beta.skills: {dir(client.beta.skills)}")
        
        # Test 3: Try different endpoints if they exist
        skills_obj = client.beta.skills
        print(f"\n3. Available methods on skills:")
        methods = [attr for attr in dir(skills_obj) if not attr.startswith('_')]
        for method in methods:
            print(f"   - {method}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error exploring Skills API: {e}")
        return False

if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY environment variable not set")
        exit(1)
    
    explore_skills_api()