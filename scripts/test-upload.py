#!/usr/bin/env python3
"""
Test the upload script's zip functionality without actually uploading
"""

import sys
import os
from pathlib import Path

# Add the scripts directory to path so we can import our upload script
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

# Import the function from upload-skill script
import importlib.util
spec = importlib.util.spec_from_file_location("upload_skill", script_dir / "upload-skill.py")
upload_skill = importlib.util.module_from_spec(spec)
spec.loader.exec_module(upload_skill)

def test_zip_creation():
    """Test creating a zip of the grammar skill"""
    
    # Test skills/grammar
    grammar_path = Path("skills/grammar")
    if not grammar_path.exists():
        print(f"❌ Grammar skill path not found: {grammar_path}")
        return False
    
    try:
        print("Testing grammar skill zip creation...")
        zip_data = upload_skill.create_skill_zip(grammar_path)
        print(f"✅ Grammar skill zip created successfully ({len(zip_data)} bytes)")
        
        # Test skills/sermon-writer
        sermon_path = Path("skills/sermon-writer")
        if sermon_path.exists():
            print("\nTesting sermon-writer skill zip creation...")
            zip_data = upload_skill.create_skill_zip(sermon_path)
            print(f"✅ Sermon-writer skill zip created successfully ({len(zip_data)} bytes)")
        
        return True
        
    except Exception as e:
        print(f"❌ Zip creation failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing upload script functionality...\n")
    success = test_zip_creation()
    
    if success:
        print("\n✅ All tests passed! Upload script is ready.")
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)