#!/usr/bin/env python3
"""
Test different file upload formats for Skills API
"""
import os
import tempfile
import zipfile
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

def test_file_upload_format():
    """Test different ways to upload files to Skills API"""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    print("🧪 Testing file upload formats...\n")
    
    # Create a simple test skill
    grammar_path = Path("skills/grammar")
    
    # Create a temporary zip file
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in grammar_path.rglob('*'):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    arcname = file_path.relative_to(grammar_path)
                    zip_file.write(file_path, arcname)
        
        print(f"Created temp zip: {temp_zip.name}")
        
        # Test 1: Try with files parameter
        try:
            print("Test 1: Using 'files' parameter with file object")
            with open(temp_zip.name, 'rb') as f:
                response = client.beta.skills.versions.create(
                    skill_id="skill_01LEoRLHpcopdFfXjv9gj9hj",
                    files=f,
                    betas=["code-execution-2025-08-25", "skills-2025-10-02"]
                )
                print(f"✅ Success: {response}")
                return True
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        # Test 2: Try with files[] parameter
        try:
            print("\nTest 2: Using 'files' parameter with tuple")
            with open(temp_zip.name, 'rb') as f:
                response = client.beta.skills.versions.create(
                    skill_id="skill_01LEoRLHpcopdFfXjv9gj9hj",
                    files=('skill.zip', f, 'application/zip'),
                    betas=["code-execution-2025-08-25", "skills-2025-10-02"]
                )
                print(f"✅ Success: {response}")
                return True
        except Exception as e:
            print(f"❌ Failed: {e}")
        
        # Clean up
        os.unlink(temp_zip.name)
    
    return False

if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY environment variable not set")
        exit(1)
    
    test_file_upload_format()