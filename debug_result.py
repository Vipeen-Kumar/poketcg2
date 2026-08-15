#!/usr/bin/env python3
"""Debug what env.run() returns."""

import os
import sys
import tarfile
import tempfile
from pathlib import Path

def test_submission():
    tar_path = Path("C:/Users/vipee/Desktop/study/project/submission_test/submission.tar.gz")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(tmpdir)
        
        import kaggle_environments
        env = kaggle_environments.make("cabt", debug=False)
        
        original_cwd = os.getcwd()
        os.chdir(tmpdir)
        
        main_py = tmpdir / "main.py"
        result = env.run([str(main_py), str(main_py)])
        
        os.chdir(original_cwd)
        
        print("Type of result:", type(result))
        print("Length of result:", len(result))
        print("\nFirst element type:", type(result[0]))
        print("First element content (first 500 chars):", str(result[0])[:500])
        
        if len(result) > 1:
            print("\nSecond element type:", type(result[1]))
            print("Second element content (first 500 chars):", str(result[1])[:500])

if __name__ == "__main__":
    test_submission()
