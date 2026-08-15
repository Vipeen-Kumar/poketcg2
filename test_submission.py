#!/usr/bin/env python3
"""Test the submission tarball using kaggle_environments CABT environment."""

import os
import sys
import tarfile
import tempfile
from pathlib import Path

# Test extraction and game execution
def test_submission():
    tar_path = Path("C:/Users/vipee/Desktop/study/project/submission_test/submission.tar.gz")
    
    if not tar_path.exists():
        print(f"ERROR: Tarball not found at {tar_path}")
        return False
    
    # Create a temporary directory for extraction
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        print(f"[1] Extracting tarball to {tmpdir}...")
        
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(tmpdir)
        
        # Verify files exist at root
        extracted_files = list(tmpdir.glob("*"))
        print(f"    Extracted files: {[f.name for f in extracted_files]}")
        
        main_py = tmpdir / "main.py"
        deck_csv = tmpdir / "deck.csv"
        
        if not main_py.exists():
            print("ERROR: main.py not found at root level after extraction")
            return False
        if not deck_csv.exists():
            print("ERROR: deck.csv not found at root level after extraction")
            return False
        
        print("    ✓ Both main.py and deck.csv present at root")
        
        # Now test with kaggle_environments
        print("\n[2] Testing with kaggle_environments CABT environment...")
        try:
            import kaggle_environments
        except ImportError:
            print("ERROR: kaggle_environments not installed")
            return False
        
        try:
            env = kaggle_environments.make("cabt", debug=False)
            print("    ✓ Environment created successfully")
        except Exception as e:
            print(f"ERROR: Failed to create environment: {e}")
            return False
        
        # Run the game with both players using the same agent
        print("\n[3] Running game with file-path agents...")
        try:
            # Change to the extracted directory so relative paths work
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            print(f"    Working directory: {tmpdir}")
            
            # Run the game: both players use the same extracted agent
            result = env.run([str(main_py), str(main_py)])
            
            os.chdir(original_cwd)
        except Exception as e:
            os.chdir(original_cwd)
            print(f"ERROR: Game execution failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print("    ✓ Game executed without Python errors")
        
        # Check results
        print("\n[4] Verifying game completion...")
        
        if len(result) < 2:
            print(f"ERROR: Expected 2 results, got {len(result)}")
            return False
        
        states = [result[0], result[1]]
        statuses = [s.get("status") for s in states]
        player_names = ["Player 0", "Player 1"]
        
        print(f"    Player 0 status: {statuses[0]}")
        print(f"    Player 1 status: {statuses[1]}")
        
        # Check for valid completion
        valid_statuses = {"DONE"}  # Both should be DONE
        
        for i, status in enumerate(statuses):
            if status not in valid_statuses:
                print(f"ERROR: {player_names[i]} has invalid status '{status}' (expected 'DONE')")
                return False
        
        print("    ✓ Both players completed with status DONE")
        
        # Determine outcome
        player_0_score = states[0].get("reward", 0)
        player_1_score = states[1].get("reward", 0)
        print(f"\n[5] Game outcome:")
        print(f"    Player 0 reward: {player_0_score}")
        print(f"    Player 1 reward: {player_1_score}")
        
        if player_0_score > player_1_score:
            outcome = "Player 0 (agent1) won"
        elif player_1_score > player_0_score:
            outcome = "Player 1 (agent2) won"
        else:
            outcome = "Draw"
        print(f"    Outcome: {outcome}")
        
        # Estimate game length from turn count if available
        turn_count = states[0].get("turn", states[1].get("turn", "unknown"))
        print(f"    Game length (turns): {turn_count}")
        
        print("\n" + "="*60)
        print("✓ SUBMISSION VALIDATION PASSED")
        print("="*60)
        return True

if __name__ == "__main__":
    success = test_submission()
    sys.exit(0 if success else 1)
