#!/usr/bin/env python3
"""
Explore Claude Skills API versions endpoint
"""
import os
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

def explore_versions_api():
    """Explore the Skills versions API"""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    print("🔍 Exploring Skills versions API...\n")
    
    try:
        # Explore versions endpoint
        versions_obj = client.beta.skills.versions
        print(f"Versions object: {dir(versions_obj)}")
        
        methods = [attr for attr in dir(versions_obj) if not attr.startswith('_')]
        print(f"\nAvailable methods on skills.versions:")
        for method in methods:
            print(f"   - {method}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error exploring versions API: {e}")
        return False

if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY environment variable not set")
        exit(1)
    
    explore_versions_api()