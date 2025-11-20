#!/usr/bin/env python3
"""
Test script to verify the setup is working correctly.
"""

import sys
from pathlib import Path

def test_imports():
    """Test that required dependencies are available."""
    print("Testing imports...")
    try:
        from PIL import Image
        print("✅ Pillow (PIL) is installed")
        return True
    except ImportError:
        print("❌ Pillow (PIL) is not installed")
        print("   Run: pip install -r requirements.txt")
        return False

def test_directory_structure():
    """Test that required directories exist."""
    print("\nTesting directory structure...")
    required_dirs = [
        Path('scripts'),
        Path('output'),
        Path('.github/workflows')
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if dir_path.exists():
            print(f"✅ {dir_path}/ exists")
        else:
            print(f"❌ {dir_path}/ is missing")
            all_exist = False
    
    return all_exist

def test_files():
    """Test that required files exist."""
    print("\nTesting required files...")
    required_files = [
        Path('scripts/generate_stickers.py'),
        Path('.github/workflows/generate-stickers.yml'),
        Path('requirements.txt'),
        Path('README.md')
    ]
    
    all_exist = True
    for file_path in required_files:
        if file_path.exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} is missing")
            all_exist = False
    
    return all_exist

def test_source_repo():
    """Check if source repository is cloned."""
    print("\nChecking source repository...")
    source_dir = Path('source-repo')
    
    if source_dir.exists():
        print(f"✅ Source repository found at {source_dir}/")
        # Count images
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
        images = []
        for ext in image_extensions:
            images.extend(source_dir.rglob(f'*{ext}'))
        
        if images:
            print(f"   Found {len(images)} images")
            return True
        else:
            print("   ⚠️  No images found in source repository")
            return False
    else:
        print(f"ℹ️  Source repository not cloned yet")
        print("   This is normal if running in CI/CD")
        print("   To test locally, run:")
        print("   git clone https://github.com/knobiknows/all-the-bufo.git source-repo")
        return None  # Not a failure, just not ready for local testing

def main():
    """Run all tests."""
    print("🐸 Bufo Stickers Setup Test\n")
    print("=" * 50)
    
    results = {
        'imports': test_imports(),
        'directories': test_directory_structure(),
        'files': test_files(),
        'source': test_source_repo()
    }
    
    print("\n" + "=" * 50)
    print("\nTest Summary:")
    
    failures = [name for name, result in results.items() if result is False]
    warnings = [name for name, result in results.items() if result is None]
    
    if not failures:
        print("✅ All tests passed!")
        if warnings:
            print(f"ℹ️  {len(warnings)} warning(s) - see above for details")
        print("\nYou're ready to:")
        print("1. Push this repository to GitHub")
        print("2. Enable GitHub Actions")
        print("3. Run the workflow to generate stickers")
        return 0
    else:
        print(f"❌ {len(failures)} test(s) failed")
        print(f"   Failed tests: {', '.join(failures)}")
        print("\nPlease fix the issues above before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

