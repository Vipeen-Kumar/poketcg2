#!/usr/bin/env python3
"""Simple test: extract tarball, run game, confirm completion."""

import os
import sys
import tarfile
import tempfile
import json
from pathlib import Path

def test_submission():
    tar_path = Path("C:/Users/vipee/Desktop/study/project/submission_test/submission.tar.gz")
    
    if not tar_path.exists():
        print(f"ERROR: Tarball not found at {tar_path}")
        return False
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        print(f"[1] Extracting tarball...")
        
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(tmpdir)
        
        main_py = tmpdir / "main.py"
        deck_csv = tmpdir / "deck.csv"
        
        if not main_py.exists() or not deck_csv.exists():
            print("ERROR: Files missing after extraction")
            return False
        
        print("    ✓ Files extracted to root level")
        
        print("\n[2] Creating CABT environment...")
        try:
            import kaggle_environments
            env = kaggle_environments.make("cabt", debug=False)
            print("    ✓ Environment created")
        except Exception as e:
            print(f"ERROR: {e}")
            return False
        
        print("\n[3] Running game (this may take 1-2 minutes)...")
        try:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            print(f"    Working directory: {tmpdir}")
            print(f"    Agent paths: {str(main_py)} vs {str(main_py)}")
            
            result = env.run([str(main_py), str(main_py)])
            
            os.chdir(original_cwd)
        except Exception as e:
            os.chdir(original_cwd)
            print(f"ERROR during game execution: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print("    ✓ Game executed without fatal errors")
        
        print("\n[4] Checking results...")
        print(f"    Result type: {type(result)}")
        print(f"    Result length: {len(result)}")
        
        if isinstance(result, list) and len(result) >= 2:
            print(f"    Result[0] type: {type(result[0])}")
            print(f"    Result[1] type: {type(result[1])}")
        
        # Print first 500 chars of stringified result
        result_str = str(result)[:500]
        print(f"    First 500 chars: {result_str}")
        
        print("\n" + "="*60)
        print("✓ GAME COMPLETED SUCCESSFULLY")
        print("="*60)
        return True

if __name__ == "__main__":
    success = test_submission()
    sys.exit(0 if success else 1)
