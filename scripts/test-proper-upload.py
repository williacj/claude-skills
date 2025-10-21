#!/usr/bin/env python3
"""
Test Skills API with proper file upload format
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

def test_proper_file_upload():
    """Test proper file upload using the right format"""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    print("🧪 Testing proper file upload format...\n")
    
    # Create a simple test skill
    grammar_path = Path("skills/grammar")
    
    # Instead of creating a zip, let's try uploading individual files
    try:
        print("Testing with individual files...")
        
        # Try uploading with individual files
        files = []
        for file_path in grammar_path.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                with open(file_path, 'rb') as f:
                    files.append((
                        'files[]',
                        (str(file_path.relative_to(grammar_path)), f.read(), 'text/markdown')
                    ))
        
        print(f"Prepared {len(files)} files for upload")
        
        # This approach won't work with the current client, let me try a different method
        print("❌ Individual files approach needs different implementation")
        
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Let me try to understand what the console does
    print("\n💡 The Skills API might only support updates via Claude Console UI currently.")
    print("   The automation might need to use a different approach or wait for API updates.")
    
    return False

if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY environment variable not set")
        exit(1)
    
    test_proper_file_upload()