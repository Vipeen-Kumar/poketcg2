# Quick Reference Guide

## 🎯 What This Project Does

Build AI agents to play Pokémon TCG matches on Kaggle, optimizing through systematic experimentation.

## 📊 One-Page Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     KAGGLE COMPETITION                           │
│  Upload: main.py + deck.csv + cg/ (in tarball)                │
│  Runs: agent(observation_dict) → action_indices                │
│  Rates: Win/Loss/Draw using skill rating system                │
└─────────────────────────────────────────────────────────────────┘

                            ↓

┌─────────────────────────────────────────────────────────────────┐
│                    AGENT DECISION LOGIC                          │
│                                                                   │
│  1. Load Deck (60 cards from deck.csv)                         │
│  2. Parse Observation (game state)                             │
│  3. Get Legal Options (valid actions)                          │
│  4. Score Each Option (heuristics)                             │
│  5. Sort by Priority (EVOLVE > ABILITY > ATTACH > ... > END)  │
│  6. Return Top-K Choices (respecting min/max constraints)      │
│                                                                   │
│  If Error → Fallback to Default (deck or safe moves)           │
└─────────────────────────────────────────────────────────────────┘

                            ↓

┌─────────────────────────────────────────────────────────────────┐
│                  LOCAL TESTING WORKFLOW                          │
│                                                                   │
│  1. Create Candidate                                            │
│     candidates/new_variant/ ← copy agent/                      │
│                                                                   │
│  2. Local Evaluation                                            │
│     Notebook 02: Play 20 games vs control agents              │
│     Record: Win/loss/draw counts                               │
│                                                                   │
│  3. Decision                                                    │
│     If better? → Copy to agent/ → Submit to Kaggle            │
│     Else → Keep as watchlist or reject                         │
│                                                                   │
│  4. Track                                                       │
│     docs/submissions/: Record score + insights                │
│     docs/experiments/: Write detailed report                   │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start: Running an Experiment

### Step 1: Create a Variant
```bash
cd candidates/
cp -r agent/ my_new_idea_v1
cd my_new_idea_v1
# Edit main.py (agent logic) OR deck.csv (cards), but not both
```

### Step 2: Test Locally
1. Open `notebooks/02_agent_baseline_and_local_evaluation.ipynb`
2. Point it to `candidates/my_new_idea_v1`
3. Run: Get win rate vs random + control agents
4. Expected: > 0.50 win rate to be competitive

### Step 3: Decide
- **Better than current best?** → Copy to `agent/` + submit
- **Worse but interesting?** → Keep in `watchlist.md`
- **Failed?** → Archive and move on

### Step 4: Track
- Record decision in `docs/6_experiment_log.md`
- Write short report in `docs/experiments/NN_your_idea.md`
- If submitting: Record score in `docs/submissions/NN_your_idea.md`

## 📈 Current Performance

| Rank | Name | Score | Why Best |
|------|------|-------|----------|
| 🥇 | Kojimar v1 | **861.4** | Complex scoring + opponent detection |
| 🥈 | Lucario v3 | 708.3 | Balanced heuristics |
| 🥉 | Lucario v1 | 662.0 | Simpler baseline |

## 💡 12 Ideas to Improve (Ranked by Effort vs Reward)

| # | Idea | Effort | Potential | Status |
|---|------|--------|-----------|--------|
| 1 | Meta-specific counters | 1 day | HIGH | Easy win |
| 2 | Energy lookahead | 2 days | HIGH | Solid improvement |
| 3 | Deck variants | 3 days | MEDIUM | Test 5-card swaps |
| 4 | Opponent modeling | 1 week | MEDIUM | Requires replays |
| 5 | Hybrid decision trees | 3 days | MEDIUM | Context-aware logic |
| 6 | Endgame planning | 1 day | MEDIUM | When ≤3 prizes left |
| 7 | First-player exploit | 1 day | MEDIUM | Use notebook #6 data |
| 8 | Replay analysis | 2 days | HIGH | Find systematic errors |
| 9 | MCTS lookahead | 1 week | HIGH | Deeper planning |
| 10 | Neural net | 2 weeks | HIGH | Learns patterns |
| 11 | Self-play evolution | 1 week | MEDIUM | Auto-tune weights |
| 12 | Ensemble voting | 2 days | LOW | Reduces variance |

## 🔧 Key Files to Understand

### Must Read (Order)
1. **README.md** — Project overview
2. **PROJECT_SUMMARY.md** — This detailed guide (you are here)
3. **docs/3_agent_strategy.md** — Current strategy details
4. **agent/main.py** — 100 lines, core decision logic
5. **candidates/kojimar_simple_baseline_v1/main.py** — 600 lines, best agent

### Should Skim
- **notebooks/02_agent_baseline_and_local_evaluation.ipynb** — Testing workflow
- **docs/5_kaggle_runbook.md** — Kaggle submission process
- **docs/6_experiment_log.md** — Past experiments + decisions

### Reference Only
- **notebooks/04-07_*.ipynb** — Advanced experiment notebooks
- **docs/experiments/** — 45+ detailed experiment reports
- **docs/submissions/** — Kaggle score history

## 🎮 Game State Example

```python
observation = {
    'select': {
        'type': 0,  # MAIN action selection
        'context': 0,  # Current game context
        'minCount': 1,  # Must select ≥1
        'maxCount': 1,  # Can select ≤1
        'option': [  # Available actions
            {'type': 9, 'area': 2, 'index': 0},  # EVOLVE hand[0]
            {'type': 8, 'area': 2, 'index': 1},  # ATTACH hand[1]
            {'type': 13, 'attackId': 42},         # ATTACK #42
            {'type': 14},                         # END turn
        ]
    },
    'current': {
        'yourIndex': 0,
        'turn': 5,
        'players': [
            {  # Your board state
                'active': [Pokémon(id=721, hp=100, ...)],
                'bench': [Pokémon(id=722, hp=80, ...)],
                'hand': [Card(id=3), Card(id=1102), ...],
                'prize': 5,  # Cards remaining
            },
            {  # Opponent board state
                'active': [Pokémon(...)],
                'bench': [...],
                'handCount': 4,  # Can't see cards
                'prize': 6,
            }
        ]
    }
}

# Agent must return:
action = [0]  # Select option index 0 (EVOLVE)
```

## 🧠 Decision Pipeline (Kojimar Agent)

```python
MAIN_ACTION_PRIORITY = {
    EVOLVE: 0,        # ← Try these first
    ABILITY: 1,
    ATTACH: 2,
    PLAY: 3,
    ATTACK: 4,
    RETREAT: 5,
    DISCARD: 6,
    END: 7            # ← Try this last
}

For each option:
  score = _score_option(option)

Sort by: (priority[type], stable_key(option))
  ↓
Select top-K respecting constraints
  ↓
Return indices
```

## 📊 Metrics to Track

### Local Testing
- **Win rate** vs random (target: > 0.60)
- **Win rate** vs current best (target: > 0.50 to promote)
- **Game length** (turns: low = aggressive, high = defensive)
- **Error rate** (should be 0%)

### Kaggle Ladder
- **Score** (1000 = 50% win, 900 = expected, 700 = below avg)
- **Uncertainty** (higher = need more games)
- **Trend** (daily check: is it drifting up or down?)

## 🚨 Common Mistakes

❌ **Don't**:
- Change both policy AND deck in same experiment
- Submit without local testing (notebooks)
- Forget to document experiment reports
- Keep candidates without version numbers
- Ignore negative results (they tell you what doesn't work)

✅ **Do**:
- Lock one component, change only the other
- Run 20+ local games before deciding
- Write brief reports for everything
- Name clearly: `{archetype}_{strategy}_v{N}`
- Archive learnings even from failures

## 🎯 Common Experiments (Copy-Paste Patterns)

### Pattern 1: Policy Tuning
```
1. Copy agent/ → candidates/my_policy_tweak_v1/
2. Keep deck.csv unchanged
3. Edit main.py scoring weights (±10%)
4. Test vs controls
5. If >50% vs current best → promote
```

### Pattern 2: Deck Tuning
```
1. Copy agent/ → candidates/my_deck_swap_v1/
2. Keep main.py unchanged
3. Swap 3-5 cards (lock rest)
4. Test vs controls (notebook 05)
5. If >50% vs current best → promote
```

### Pattern 3: Archetype Testing
```
1. Find top opponent archetype (from losses)
2. Create anti-meta deck (exploit its weakness)
3. Test vs that archetype clone
4. If >60% specific matchup → submit as meta counter
```

## 📞 Getting Help

1. **Strategy questions?** → Read `docs/3_agent_strategy.md`
2. **How to test?** → Read `notebooks/02_*.ipynb` (copy-paste)
3. **Kaggle errors?** → Read `docs/5_kaggle_runbook.md` Failure Diagnosis
4. **Stuck?** → Review `docs/experiments/` for similar attempts

## 🏁 Success Checklist

Before submitting to Kaggle:
- [ ] Local test: >60% vs random
- [ ] Local test: >50% vs current best
- [ ] No timeouts or errors
- [ ] Tarball validated (main.py + deck.csv + cg/ at root)
- [ ] Experiment report written
- [ ] Submission ID recorded
- [ ] Ready to check ladder score daily for drift

---

**TL;DR**: Copy agent/ → modify one thing → test locally → if better, promote & submit → track score → repeat.
