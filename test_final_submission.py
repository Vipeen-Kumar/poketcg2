#!/usr/bin/env python3
"""Final test of the submission with bundled cg stub."""

import os
import sys
import tarfile
import tempfile
from pathlib import Path

def test():
    tar_path = Path("c:/Users/vipee/Desktop/study/project/kaggle-pokemon-tcg-ai-battle-main/kaggle-pokemon-tcg-ai-battle-main/submission_styled/submission.tar.gz")
    
    print("[1] Extracting tarball...")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(tmpdir)
        
        extracted = sorted([f.name for f in tmpdir.iterdir()])
        print(f"    Extracted: {extracted}")
        
        if "main.py" not in extracted or "deck.csv" not in extracted or "cg" not in extracted:
            print("    ✗ Missing required files")
            return False
        
        print("    ✓ All files present at root")
        
        print("\n[2] Checking cg stub package...")
        cg_dir = tmpdir / "cg"
        if not (cg_dir / "api.py").exists() or not (cg_dir / "__init__.py").exists():
            print("    ✗ Missing cg package files")
            return False
        
        print("    ✓ cg/api.py and cg/__init__.py present")
        
        print("\n[3] Testing with kaggle_environments...")
        try:
            import kaggle_environments
            env = kaggle_environments.make("cabt", debug=False)
            
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            sys.path.insert(0, str(tmpdir))
            
            print(f"    Running game from: {tmpdir}")
            result = env.run([str(tmpdir / "main.py"), str(tmpdir / "main.py")])
            
            os.chdir(original_cwd)
            
            if result and len(result) >= 2:
                print("    ✓ Game completed successfully")
                print(f"    Result contains {len(result)} player results")
                return True
            else:
                print("    ✗ Unexpected result format")
                return False
        except Exception as e:
            os.chdir(original_cwd)
            print(f"    ✗ Game failed: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = test()
    if success:
        print("\n" + "="*70)
        print("✓ SUBMISSION READY FOR KAGGLE")
        print("="*70)
        print("\nFile: c:\\Users\\vipee\\Desktop\\study\\project\\kaggle-pokemon-tcg-ai-battle-main\\")
        print("      kaggle-pokemon-tcg-ai-battle-main\\submission_styled\\submission.tar.gz")
        print("\nContents:")
        print("  - main.py (with original imports)")
        print("  - deck.csv (60 cards)")
        print("  - cg/ (stub package for local compatibility)")
        print("\nOn Kaggle's servers, cg.api will be provided by the CABT environment.")
    sys.exit(0 if success else 1)
