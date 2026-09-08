# Pokémon TCG AI Battle - Project Summary

## 📋 Project Overview

This is a **research-driven Kaggle competition repository** for the **Pokémon Trading Card Game (TCG) AI Battle** competition. The project is structured as a **reproducible workflow** for developing, testing, and submitting AI agents that play Pokémon TCG matches against other participants.

### Competition Context
- **Goal**: Submit a 60-card deck + Python agent to play TCG matches
- **Evaluation**: Ladder-based rating system (Gaussian skill estimate)
- **Submission Limit**: 5 agents per day, only latest 2 tracked
- **Deadline**: August 16, 2026, 23:59 UTC
- **Leaderboard**: Win/loss/draw counts matter, not damage margins

**Current Status**: Best submission scores 861.4 (Kojimar simple baseline v1)

---

## 🏗️ Project Architecture

### Directory Structure

```
project/
├── agent/                    # Primary versioned agent
│   ├── main.py              # Decision logic (entry point)
│   └── deck.csv             # 60-card deck list
│
├── candidates/              # 50+ experimental agent variants
│   ├── kojimar_simple_baseline_v1-v25/   (best performing)
│   ├── lucario_public_sample_v1-v7/      (strong alternative)
│   ├── abomasnow_planner_v1-v2/
│   ├── planner_main_only_v1/
│   └── [other strategy variants...]
│
├── controls/                # Baseline agents for testing
│   └── [reference policies for evaluation]
│
├── notebooks/               # Kaggle-runnable analysis & experiments
│   ├── 01_card_database_eda.ipynb           (card audit)
│   ├── 02_agent_baseline_and_local_evaluation.ipynb
│   ├── 03_submission_packaging_and_validation.ipynb
│   ├── 04_action_sequence_experiment.ipynb   (policy testing)
│   ├── 05_deck_consistency_experiment.ipynb  (deck testing)
│   └── [experiments 06-12]
│
├── scripts/                 # Local evaluation tools
│   └── [builders, evaluators, trackers]
│
├── docs/                    # Detailed documentation
│   ├── 0_coding_standards.md
│   ├── 1_competition_instructions.md
│   ├── 2_eda_and_environment.md
│   ├── 3_agent_strategy.md
│   ├── 4_evaluation_and_submissions.md
│   ├── 5_kaggle_runbook.md
│   ├── 6_experiment_log.md
│   ├── 7_competition_author_references.md
│   ├── experiments/          (45+ detailed experiment reports)
│   └── submissions/          (submission history & scores)
│
├── data/                    # Downloaded competition data (ignored)
├── scratch/                 # Runtime outputs (ignored)
└── requirements.txt
```

---

## 🤖 How It Works

### 1. **Core Agent Architecture**

The agent follows a **deterministic decision-making pipeline**:

```python
agent(obs_dict: dict) → list[int]
```

**Input**: Game observation (JSON dict with game state)
**Output**: Legal action indices to take

#### Key Components:

**a) Deck Loading** (`read_deck_csv()`)
- Locates deck.csv from multiple possible paths
- Validates exactly 60 cards
- Handles both local and Kaggle runtime environments

**b) Option Selection** (`_choose_indices()`)
- Receives list of legal options for current game state
- Applies priority-based sorting:
  - Primary: Action type priority (EVOLVE → ABILITY → ATTACH → PLAY → ATTACK → RETREAT → DISCARD → END)
  - Secondary: Stable tie-breaking using card properties (number, area, index, attackId, etc.)
- Returns selected option indices respecting min/max constraints

**c) Error Handling**
- Graceful fallback on invalid observations
- Returns deck on initial setup phase
- Falls back to safe defaults if parsing fails

### 2. **Decision Strategies**

Different candidate agents implement different strategic approaches:

#### **Kojimar Simple Baseline v1-v25** (Best: 861.4 score)
- Complex scoring system for prize value, damage, threat level
- Opponent archetype detection (Water deck, Crustle wall, etc.)
- Attack planning with damage calculation
- Context-aware energy attachment
- Evolution sequencing

**Key Methods**:
- `target_score()`: Evaluates prize value + damage potential
- `prize_count()`: Accounts for Pokémon type effects
- `_base_attack()`: Calculates damage with weakness/resistance
- `_plan_attack()`: Multi-turn attack sequencing

#### **Lucario Public Sample v1-v7**
- Simpler heuristic-based approach
- Focus on active threat elimination
- Balanced aggression vs defense

#### **Abomasnow Planner**
- Attack-planning focused
- Resource management emphasis

#### **Conservative Switch** variants
- Risk-averse switching logic
- Defensive positioning

#### **Development-First Baseline** (Current agent/)
- Priority-based action selection
- Simpler, more general strategy
- Used as stable baseline for experiments

### 3. **Game Loop**

```
1. Kaggle loads tarball → extracts main.py + deck.csv + cg/
2. Competition starts → calls agent(initial_obs)
3. Agent returns deck card IDs (60 cards)
4. Game initializes both players' hands and boards
5. During match:
   - Game state → agent(observation)
   - Agent returns legal action indices
   - Game executes action
   - Repeat until win/loss/draw
6. Rating updates based on outcome
```

---

## 📊 Project Assets

### Agents: 50+ Variants
Each in `candidates/` with its own `main.py` and `deck.csv`:
- Tunable decision logic (attack plans, scoring weights)
- Different deck compositions (card pool, energy ratios)
- Meta-game specific (Abomasnow pressure, Lucario tempo, etc.)

### Notebooks: 12 Kaggle-Runnable
- **EDA**: Card database analysis (1,267 cards, type distributions)
- **Evaluation**: Baseline vs random agent (775 win rate)
- **Packaging**: Tarball creation + validation
- **Experiments**: Isolated testing of policy & deck changes
- **Analysis**: Loss taxonomy, matchup patterns, first-player advantage

### Documentation: 45+ Reports
- **Experiment evidence**: Each candidate tested with paired games, win/loss counts, uncertainty estimates
- **Submission history**: All 45+ submissions tracked with scores and insights
- **Strategic notes**: Why each variant was kept, rejected, or promoted

---

## 🔬 Development Workflow

### Standard Process (as documented):

1. **Idea Generation** → Pick a strategic change (archetype swap, priority tuning, etc.)

2. **Create Candidate**
   - Copy `agent/` → `candidates/new_variant/`
   - Modify `main.py` (decision logic) or `deck.csv` (card pool)
   - Lock opposite component (keep deck if testing policy, keep policy if testing deck)

3. **Local Evaluation**
   - Run notebook `02_agent_baseline_and_local_evaluation.ipynb`
   - Play 10-20 paired games against control agents
   - Record win/loss/draw in experiment report

4. **Promotion Decision**
   - If results beat current best: promote to `agent/`
   - Create experiment report in `docs/experiments/`
   - Update `docs/6_experiment_log.md` and `docs/submissions/`

5. **Submission**
   - Run notebook `03_submission_packaging_and_validation.ipynb`
   - Package tarball with main.py + deck.csv + cg/ SDK
   - Submit to Kaggle
   - Record submission ID + score in `docs/submissions/`

6. **Monitoring**
   - Check ladder score daily
   - If promising: keep; if drift down: investigate + revert

### Success Criteria (from docs):
- > 0.50 win rate vs random baseline
- Improvement over previous best in local testing
- No timeout/error in validation
- Consistent performance across multiple games

---

## 📈 Current Performance

| Rank | Agent | Type | Score | Status |
|------|-------|------|-------|--------|
| 1 | Kojimar v1 | Heuristic complex | 861.4 | Active best |
| 2 | Lucario v3 | Heuristic medium | 708.3 | Previous best |
| 3 | Lucario v1 | Heuristic medium | 662.0 | Watchlist |
| 4 | Planner v1 | Plan-based | 560.3 | Validated |
| 5 | Baseline fix | Development | 496.7 | Baseline |

**Key Insight**: Complex heuristic scoring (Kojimar) outperformed simpler approaches and plan-based strategies.

---

## 🚀 How to Improve

### Short-Term (Immediate Wins)

#### 1. **Meta-Specific Scoring Refinements**
- Analyze opponent deck signatures in win/loss replays
- Add more specific counters to high-meta threats
- Example: If Crustle-wall is meta, boost water-type targeting

#### 2. **Energy Attachment Optimization**
- Current: generic attachment heuristics
- Improve: Look-ahead to plan multi-turn setups
- Add: Dynamic energy cost estimation based on remaining deck

#### 3. **Retreat/Switch Logic Enhancement**
- Current: Conservative switches based on damage
- Improve: Predict opponent's next attack + proactive switching
- Add: Switch cost optimization (minimize retreat cost wasted)

#### 4. **Deck Composition Tuning**
- Run `05_deck_consistency_experiment.ipynb` with deck variants
- Test: Different energy ratios, trainer compositions
- Lock current policy, swap 3-5 cards at a time
- Example: More draw trainers vs more disruption

---

### Medium-Term (2-3 Weeks)

#### 5. **Opponent Modeling**
- Track card names/types drawn in replays
- Build per-opponent deck probability models
- Adjust strategy based on likely opponent deck
- Example: If opponent plays Water Pokémon → prepare electric counters

#### 6. **Hybrid Decision Trees**
- Move beyond flat priority scoring
- Create context-dependent policies (opening vs midgame vs endgame)
- Example:
  - Early game: Prioritize setup (evolve, attach energy)
  - Mid game: Attack high-threat targets
  - Late game: Finish regardless of damage

#### 7. **Lookahead Search (Limited Depth)**
- Current: Greedy single-action selection
- Improve: 2-3 move lookahead with simple simulator
- Use: `cg.api.search_begin()` + `search_step()` (already available in SDK)
- Benefit: Catch multi-turn tactical errors

#### 8. **Multi-Archetype Support**
- Current: Single best agent (Kojimar)
- Create: Archetype-specific variants (aggressive, defensive, balanced)
- Use: Lightweight deck type detection to pick best counter

---

### Long-Term (1+ Month)

#### 9. **Machine Learning Integration**
- Current: Hand-crafted heuristics
- Next: Train lightweight neural network on replay data
- Approach:
  - Input: Game state (card types, HP, energy, etc.)
  - Output: Action probabilities
  - Train on: Kaggle competition replays + self-play
- Benefit: Learn non-obvious patterns humans miss

#### 10. **Self-Play Training Loop**
- Generate 1000+ games between candidate variants
- Use results to evolve hyperparameters (scoring weights, priorities)
- Evolutionary algorithms: Genetic algorithms or CMA-ES for weight tuning
- Example: Adjust `MAIN_ACTION_PRIORITY` values via gradient descent

#### 11. **Monte Carlo Tree Search (MCTS)**
- Current: Greedy policies
- Improve: MCTS with rollouts for key decisions
- Benefit: Deeper strategic planning (especially late-game finishes)
- Cost: Higher latency (must stay within time budget)

#### 12. **Ensemble Voting**
- Keep top 3 agents (Kojimar, Lucario, Abomasnow)
- Predict each agent's action for current state
- Majority vote or weighted ensemble
- Benefit: Reduces individual agent weaknesses

---

## 🎯 Quick Wins (By Priority)

### Priority 1 (Highest ROI)
1. **Crustle Wall Detection** — Add specific counter if meta says Crustle is common
2. **Energy Attachment Lookahead** — Avoid wasting energy on dead-end setups
3. **Deck Variant Testing** — Try 5-card swaps (more draw vs more disruption)

### Priority 2 (Medium ROI)
4. **Endgame Planning** — Special logic when ≤3 prizes remain (be aggressive)
5. **First-Player Bias** — Notebook #6 showed 1st player advantage; exploit it
6. **Replay Analysis** — Manually review top losses; find systematic errors

### Priority 3 (Long-term)
7. **Opponent Modeling** — Requires replay data collection
8. **MCTS Integration** — Requires time budget analysis
9. **ML Training** — Requires training infrastructure

---

## 🔍 Debug & Analysis Tools

### Available Notebooks:
- **01**: Card stats → find synergies
- **02**: Baseline evaluation → smoke test new agents
- **04**: Action ordering → test if priority changes help
- **05**: Deck changes → isolated deck testing
- **06**: Replay analysis → find first-player patterns
- **10**: Loss taxonomy → understand failure modes

### Key Metrics to Track:
- Win rate vs random (should be > 0.60)
- Win rate vs current best (should be > 0.50 to promote)
- Average game length (turnsIndicates strategy aggression)
- Specific loss patterns (e.g., always loses to Water decks)

---

## 📝 Best Practices (from Project)

1. **Experiment Isolation**: Lock deck when testing policy; lock policy when testing deck
2. **Evidence Trail**: Document every experiment report + decision rationale
3. **Stable Baselines**: Keep `agent/` unchanged during experiments
4. **Reproducibility**: Use fixed seeds, multiple game samples (80+ games)
5. **Versioning**: Name candidates with strategy + version number
6. **Submission Discipline**: Only promote if local eval beats current best
7. **Post-Mortem**: Check ladder drift; if score drops, review what changed

---

## 🚨 Known Limitations

1. **Deterministic Only**: No randomness allowed; strategy must handle any valid state
2. **Time Budget**: Agent must respond in <1ms per decision (typically runs in <100μs)
3. **No Search Yet**: Current agents are greedy (single action lookahead only)
4. **Limited Opponent Info**: Can't see opponent's hand, deck, or discard pile details
5. **Meta Dependency**: Best strategy shifts as meta changes (new decks emerge)
6. **No Multi-Agent Coordination**: Doesn't learn from other team agents' submitted variants

---

## 💡 Strategic Insights (from Results)

- **Kojimar outperformed Lucario**: Complex scoring + opponent archetype detection beats simplicity
- **Planner approach underperformed**: Planning-based strategies harder to tune than heuristics
- **First-player advantage**: Documented in notebook #6; exploit with early aggression
- **Archetype-specific tactics work**: Crustle-guard, Phantump targeting showed promise in experiments
- **Deck tuning matters less than policy**: Small policy tweaks > major deck swaps (in experiments 04-05)

---

## 📊 Competition Context

- **Card Pool**: 1,267 unique cards (from official Pokémon TCG)
- **Game Rules**: Standard TCG rules (60-card decks, 6 prize cards, etc.)
- **Participants**: Global competitive players (some posted 900+ scores)
- **Observation Space**: Game state includes:
  - Both players' boards (active Pokémon + bench)
  - Hand status (opponent hand count, not cards)
  - Discard piles
  - Prize cards
  - Stadium + special conditions
  - Available actions + constraints

---

## 🎓 Learning Outcomes

Running this project teaches:
- **Game AI**: Decision-making under uncertainty with incomplete info
- **Hyperparameter Tuning**: Balancing exploration vs exploitation
- **Reproducible Research**: Documentation, versioning, evidence trails
- **Competition Strategy**: Meta analysis, deck building, matchup theory
- **Software Engineering**: Modular design, experiment isolation, CI/CD concepts

---

## 📚 References

- **Kaggle Page**: https://www.kaggle.com/competitions/pokemon-tcg-ai-battle
- **Official Notebooks**: Links in `docs/README.md` (vipeen-kumar's Kaggle profile)
- **Competition Rules**: See `docs/1_competition_instructions.md`
- **Detailed Strategy**: See `docs/3_agent_strategy.md`

---

**Last Updated**: 2026-08-14  
**Best Score**: 861.4 (Kojimar simple baseline v1)  
**Next Action**: Either implement Priority 1 improvements or submit as-is for baseline score.
