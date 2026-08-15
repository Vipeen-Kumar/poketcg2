#!/usr/bin/env python3
"""Test that the bundled cg module works when extracted."""

import os
import sys
import tarfile
import tempfile
from pathlib import Path

def test():
    tar_path = Path("c:/Users/vipee/Desktop/study/project/kaggle-pokemon-tcg-ai-battle-main/kaggle-pokemon-tcg-ai-battle-main/submission_styled/submission.tar.gz")
    
    print("[1] Creating isolated temp directory...")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        print(f"    Temp dir: {tmpdir}")
        
        print("\n[2] Extracting tarball...")
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(tmpdir)
        
        # List what was extracted
        extracted = sorted([f.name for f in tmpdir.iterdir()])
        print(f"    Extracted: {extracted}")
        
        if "cg" not in extracted or "main.py" not in extracted or "deck.csv" not in extracted:
            print("    ✗ Missing required files at root")
            return False
        
        print("    ✓ All files present at root level")
        
        print("\n[3] Checking bundled cg module...")
        cg_path = tmpdir / "cg"
        api_py = cg_path / "game.py"  # cg.api is in game.py
        
        if not api_py.exists():
            print(f"    ✗ cg/game.py not found")
            return False
        
        print(f"    ✓ cg/game.py exists")
        
        print("\n[4] Testing bundled import in isolated environment...")
        try:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            
            # Add tmpdir to path so cg is found locally, not from system
            sys.path.insert(0, str(tmpdir))
            
            # Try importing from bundled cg
            from cg.api import OptionType, SelectContext, SelectType, to_observation_class
            print("    ✓ Successfully imported from bundled cg module")
            
            # Verify we can access the API classes
            print(f"    ✓ OptionType available: {OptionType}")
            
            os.chdir(original_cwd)
        except Exception as e:
            os.chdir(original_cwd)
            print(f"    ✗ Import failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print("\n[5] Running game with kaggle_environments (using bundled cg)...")
        try:
            import kaggle_environments
            env = kaggle_environments.make("cabt", debug=False)
            
            os.chdir(tmpdir)
            sys.path.insert(0, str(tmpdir))
            
            result = env.run([str(tmpdir / "main.py"), str(tmpdir / "main.py")])
            
            os.chdir(original_cwd)
            
            if result and len(result) >= 2:
                print("    ✓ Game completed successfully")
                print(f"    Result type: {type(result)}")
                print(f"    Result length: {len(result)}")
                return True
            else:
                print("    ✗ Unexpected result")
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
        print("\n" + "="*60)
        print("✓ BUNDLED CG MODULE WORKS - READY FOR KAGGLE")
        print("="*60)
    sys.exit(0 if success else 1)
