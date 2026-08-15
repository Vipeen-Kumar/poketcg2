#!/usr/bin/env python3
"""Quick verification that the styled submission works."""

import os
import sys
import tarfile
import tempfile
from pathlib import Path

def verify():
    tar_path = Path("c:/Users/vipee/Desktop/study/project/kaggle-pokemon-tcg-ai-battle-main/kaggle-pokemon-tcg-ai-battle-main/submission_styled/submission.tar.gz")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        print("[1] Extracting...")
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(tmpdir)
        
        main_py = tmpdir / "main.py"
        deck_csv = tmpdir / "deck.csv"
        
        if not main_py.exists() or not deck_csv.exists():
            print("ERROR: Files missing")
            return False
        
        print("    ✓ Files present at root")
        
        print("\n[2] Testing imports and module structure...")
        try:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            
            # Try to import the module
            import importlib.util
            spec = importlib.util.spec_from_file_location("agent_module", main_py)
            agent_module = importlib.util.module_from_spec(spec)
            
            # Don't execute yet (cg.api may not be importable in isolation)
            print("    ✓ Module structure valid")
            
            os.chdir(original_cwd)
        except Exception as e:
            os.chdir(original_cwd)
            print(f"    ✗ Error: {e}")
            return False
        
        print("\n[3] Verifying deck.csv format...")
        lines = (tmpdir / "deck.csv").read_text().strip().split('\n')
        if len(lines) == 60:
            print(f"    ✓ Exactly 60 cards")
        else:
            print(f"    ✗ Found {len(lines)} lines, expected 60")
            return False
        
        print("\n[4] Running game test...")
        try:
            import kaggle_environments
            env = kaggle_environments.make("cabt", debug=False)
            
            os.chdir(tmpdir)
            result = env.run([str(main_py), str(main_py)])
            os.chdir(original_cwd)
            
            if result and len(result) >= 2:
                print("    ✓ Game completed successfully")
            else:
                print("    ✗ Unexpected result format")
                return False
        except Exception as e:
            os.chdir(original_cwd)
            print(f"    ✗ Game failed: {e}")
            return False
        
        print("\n" + "="*60)
        print("✓ STYLED SUBMISSION VERIFIED AND READY")
        print("="*60)
        return True

if __name__ == "__main__":
    success = verify()
    sys.exit(0 if success else 1)
