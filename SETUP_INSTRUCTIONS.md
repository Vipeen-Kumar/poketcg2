# How to Get the Real cg/ SDK and Create the Submission

## Step 1: Download the Competition Data from Kaggle

1. Go to: **https://www.kaggle.com/competitions/pokemon-tcg-ai-battle**
2. Find the **Data** section or similar (usually on competition page)
3. Download all competition data as a ZIP file
4. Extract it locally

## Step 2: Locate the sample_submission/cg/ folder

After extraction, you should have a folder structure like:
```
pokemon-tcg-ai-battle/
├── sample_submission/
│   ├── main.py
│   └── cg/                    <-- THIS IS WHAT WE NEED
│       ├── __init__.py
│       ├── api.py             <-- The real API with OptionType, SelectContext, etc.
│       ├── game.py
│       ├── sim.py
│       ├── utils.py
│       ├── cg.dll
│       ├── libcg.so
│       ├── libcg.dylib
│       └── libcg-arm64.so
└── [other data files]
```

## Step 3: Copy the Real cg/ to Your Submission

Once you have the `sample_submission/cg/` folder:

```powershell
# Option A: Manual copy
# 1. Delete the stub cg/ folder from submission_styled:
Remove-Item "c:\Users\vipee\Desktop\study\project\kaggle-pokemon-tcg-ai-battle-main\kaggle-pokemon-tcg-ai-battle-main\submission_styled\cg" -Recurse -Force

# 2. Copy the REAL cg/ from your downloaded competition data:
Copy-Item -Path "[YOUR_EXTRACTED_DATA_PATH]\sample_submission\cg" `
          -Destination "c:\Users\vipee\Desktop\study\project\kaggle-pokemon-tcg-ai-battle-main\kaggle-pokemon-tcg-ai-battle-main\submission_styled\cg" `
          -Recurse
```

## Step 4: Verify the Real cg/api.py is Present

Open the copied file and confirm it contains real class definitions:
```powershell
Get-Content "c:\Users\vipee\Desktop\study\project\kaggle-pokemon-tcg-ai-battle-main\kaggle-pokemon-tcg-ai-battle-main\submission_styled\cg\api.py" | head -50
```

You should see:
- `class OptionType(...)`
- `class SelectContext(...)`
- `def to_observation_class(...)`
- Other API definitions

**NOT** a stub or error message.

## Step 5: Rebuild the Tarball

```powershell
cd "c:\Users\vipee\Desktop\study\project\kaggle-pokemon-tcg-ai-battle-main\kaggle-pokemon-tcg-ai-battle-main\submission_styled"
Remove-Item submission.tar.gz -Force -ErrorAction SilentlyContinue
tar -czvf submission.tar.gz main.py deck.csv cg
```

## Step 6: Verify Tarball Contents

```powershell
tar -tzf "c:\Users\vipee\Desktop\study\project\kaggle-pokemon-tcg-ai-battle-main\kaggle-pokemon-tcg-ai-battle-main\submission_styled\submission.tar.gz"
```

Should show:
```
main.py
deck.csv
cg/
cg/__init__.py
cg/api.py          <-- MUST be the real one with class definitions
cg/game.py
cg/sim.py
cg/utils.py
cg/cg.dll
cg/libcg.so
cg/libcg.dylib
cg/libcg-arm64.so
```

## Step 7: Test Locally

Once you have the real cg/, test the submission:
```powershell
python test_bundled_cg.py
```

## Summary

The stub cg/ was a placeholder. The REAL cg/ SDK with api.py must come from Kaggle's official competition data. Without it, the submission will fail with `ModuleNotFoundError: No module named 'cg.api'` on Kaggle's servers.
