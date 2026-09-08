# Experiment and Submission Log

## Current summary

Current active best submitted agent: `kojimar_simple_baseline_v1`.

Latest tracked public score: `864.5` on 2026-07-08.

High-level progression:

| Phase | Key candidate | Outcome |
| --- | --- | --- |
| Starter/planner baseline | `planner_main_only_v1` | Valid but low public score; useful simulator learning phase |
| Public Lucario sample | `lucario_public_sample_v3` | Became first strong submitted agent; reached scores above `700` |
| Kojimar simple baseline | `kojimar_simple_baseline_v1` | Current active best; reached `864.5` |
| Public meta replay mining | v5 / v8 / v16-v22 | Found useful Metal/Cinderace and library-out signals, but no submit-ready candidate above v1 |

Recent high-value experiment reports:

- [experiments/76_v23_v24_phantump_control_results.md](experiments/76_v23_v24_phantump_control_results.md)
- [experiments/75_v8_dragapult_phantump_replay_delta.md](experiments/75_v8_dragapult_phantump_replay_delta.md)
- [experiments/74_opening_category_cross_branch_insights.md](experiments/74_opening_category_cross_branch_insights.md)
- [experiments/73_cross_submission_meta_insights.md](experiments/73_cross_submission_meta_insights.md)
- [experiments/72_v22_midgame_metal_boss_guard_results.md](experiments/72_v22_midgame_metal_boss_guard_results.md)
- [experiments/45_kojimar_simple_baseline_candidate_results.md](experiments/45_kojimar_simple_baseline_candidate_results.md)
- [experiments/44_kojimar_insights_v7_crustle_guard.md](experiments/44_kojimar_insights_v7_crustle_guard.md)
- [experiments/43_lucario_v5_v6_upgrade_attempts.md](experiments/43_lucario_v5_v6_upgrade_attempts.md)
- [experiments/41_lucario_public_v3_candidate_results.md](experiments/41_lucario_public_v3_candidate_results.md)

Chronological submission score tracking lives in
[submissions/39_lucario_public_sample_submission.md](submissions/39_lucario_public_sample_submission.md).

This ledger is intentionally factual. Add one row for every candidate that
reaches a meaningful paired evaluation or Kaggle submission.

## Offline experiments

| Date (UTC) | Candidate | Control | Deck | Seeds x seats | W-D-L | Score rate | CI | Decision |
| --- | --- | --- | --- | ---: | --- | ---: | --- | --- |
| 2026-06-21 | `baseline-deterministic-v1` | self-play | starter | 4 games | 2-0-2 by player 0 | n/a | n/a | Reliability pass; freeze as control |
| 2026-06-21 | `baseline-deterministic-v1` | official random policy | starter | 40 seat-balanced games | 5-0-35 | 0.125 | bootstrap 95%: [0.025, 0.225] | Reject for ladder; reliable but strategically weak |
| 2026-06-21 | `development-first-v2` | attack-first v1 | starter | 40 seat-balanced games | 37-0-3 | 0.925 | bootstrap 95%: [0.825, 1.000] | Promote sequencing change |
| 2026-06-21 | `development-first-v2` | official random policy | starter | 40 seat-balanced games | 32-0-8 | 0.800 | bootstrap 95%: [0.675, 0.925] | Pass control screen |
| 2026-06-21 | `development-first-v2` | official random policy, independent screen | starter | 40 seat-balanced games | 31-0-9 | 0.775 | bootstrap 95%: [0.650, 0.900] | Confirm promotion |
| 2026-06-21 | `printed-knockout-v3` | development-first v2 | starter | 40 seat-balanced games | 25-0-15 | 0.625 | bootstrap 95%: [0.475, 0.775] | Hold; interval overlaps parity |
| 2026-06-21 | `attachment-readiness-v4` | development-first v2 | starter | 40 seat-balanced games | 20-0-20 | 0.500 | bootstrap 95%: [0.350, 0.650] | Hold; readiness alone adds no value |
| 2026-06-21 | `attachment-value-v6` | development-first v2 | starter | 40 seat-balanced games | 20-0-20 | 0.500 | bootstrap 95%: [0.350, 0.650] | Hold; 31 target changes, zero failures |
| 2026-06-21 | `eight-basic-deck-v1` | starter deck | 4 Kyogre, 4 Snover, 33 Water Energy | 80 seat-balanced games | 40-0-40 | 0.500 | bootstrap 95%: [0.3875, 0.6125] | Hold; setup gain did not improve outcomes |

## Kaggle submissions

| Date (UTC) | Version | Code hash | Deck hash | Validation | `mu` | `sigma` | Episodes | Decision |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| ? | ? | ? | ? | ? | ? | ? | ? | ? |

## Experiment note template

```markdown
### YYYY-MM-DD - candidate-name

- Hypothesis:
- Single intended change:
- Frozen control and opponents:
- Seeds, seats, and game count:
- Result with uncertainty:
- Runtime/errors:
- Interpretation:
- Decision and next action:
```


## Kaggle notebook validation

| Date (UTC) | Notebook | Version | Status | Verified output |
| --- | --- | ---: | --- | --- |
| 2026-06-21 | `pokemon-tcg-card-database-eda` | 3 | Complete | 1,267 cards plus bounded 1,306-page PDF-reference audit |
| 2026-06-21 | `pokemon-tcg-agent-baseline-and-evaluation` | 5 | Complete | Promoted agent: 31-0-9, score rate 0.775 |
| 2026-06-21 | `pokemon-tcg-action-sequence-experiment` | 6 | Complete | Corrected attachment-value follow-up: 20-0-20, hold |
| 2026-06-21 | `pokemon-tcg-deck-consistency-experiment` | 1 | Complete | Eight-Basic candidate: 40-0-40 over 80 games, hold |
| 2026-06-21 | `pokemon-tcg-submission-packaging` | 6 | Complete | Promoted-agent tar.gz, staged runtime, and hashes verified |

The private Kaggle dataset
[`vipeen-kumar/pokemon-tcg-ai-battle-agent-source`](https://www.kaggle.com/datasets/vipeen-kumar/pokemon-tcg-ai-battle-agent-source)
provides the reviewed `main.py` and `deck.csv` to the execution notebooks.

### 2026-08-16 - final deadline hold on `kojimar_simple_baseline_v1`

- Hypothesis:
  A retreat-priority patch in `kojimar_simple_baseline_v26` might reduce a real
  loss mode without hurting the rest of Kojimar v1's behavior.
- Single intended change:
  Boost retreat scoring when the opponent active appears able to KO our active.
- Frozen control and opponents:
  `kojimar_simple_baseline_v1` as the live safe baseline and direct control.
- Seeds, seats, and game count:
  30 seat-balanced head-to-head games for the corrected follow-up check.
- Result with uncertainty:
  The retreat experiment failed twice in the same direction. The first attempt
  used a guessed weakness rule and produced a misleading 10-game `9-1` result.
  After correcting the weakness rule to match verified code (`2x` weakness,
  `-30` resistance), the original approach lost `11-19` over 30 games. A second
  follow-up rebuilt the opponent threat estimate through generic SDK attack
  metadata, but the 30-game seat-balanced result remained `11-19` (`36.7%`)
  versus `kojimar_simple_baseline_v1`.
- Runtime/errors:
  No packaging or submission was attempted for v26. The experimental logic was
  reverted to the v1 retreat behavior and the threat estimators were kept only
  as dead-code reference in `candidates/kojimar_simple_baseline_v26/main.py`.
- Interpretation:
  This is a negative result, not a deadline-day bug hunt. The retreat idea did
  not survive corrected rules, generic API estimation, or the required 30-game
  validation bar.
- Decision and next action:
  Keep `submission_kojimar.tar.gz` / `kojimar_simple_baseline_v1` as the final
  working submission at about `695` live rating. Do not submit v26. Do not
  package any additional candidate before the 2026-08-16 11:59 PM UTC deadline
  unless a separately validated candidate already exists, which current records
  do not show.

### 2026-08-16 - reject `kojimar_simple_baseline_v27` Crustle targeting change

- Hypothesis:
  Kojimar v1 recognized Crustle-wall decks but only used that signal
  defensively. A narrow offensive Crustle targeting rule might improve the
  matchup without disturbing the rest of the policy.
- Single intended change:
  Add a two-part active-Crustle optimization:
  1. allow Mega Lucario ex attack planning to consider the opponent's active
     Crustle (`id 345`) as a valid target instead of always skipping it;
  2. add a `1150` attack-option score for the matching planned attack when the
     opponent is a Crustle-wall deck and that active Crustle is the target.
- Frozen control and opponents:
  `kojimar_simple_baseline_v1` as the live safe baseline and direct control.
- Seeds, seats, and game count:
  60 total seat-balanced head-to-head games, run as two 30-game batches.
- Result with uncertainty:
  First batch: `18-12-0` (`60.0%`). Second batch: `15-15-0` (`50.0%`).
  Combined result: `33-27-0` (`55.0%`) versus `kojimar_simple_baseline_v1`.
- Runtime/errors:
  The change remained isolated to the Crustle-targeting path and did not touch
  retreat, setup, or energy logic. No packaging or submission was attempted.
- Interpretation:
  The code change was narrow and behaved as intended, but the 60-game combined
  result is too close to the noise floor for a confidence-worthy deadline-day
  promotion.
- Decision and next action:
  Revert `kojimar_simple_baseline_v27` back to clean v1 behavior. Do not
  package or submit v27. Keep `submission_kojimar.tar.gz` /
  `kojimar_simple_baseline_v1` as the final live submission at about `695`.

### 2026-08-16 - final day wrap-up: v26, v27, v28, v29 all held

- Hypothesis:
  A few very narrow end-of-deadline tweaks might improve `kojimar_simple_baseline_v1`
  without risking broad regressions: retreat-threat logic, active-Crustle
  targeting, and small deck-card swaps.
- Single intended change:
  Multiple isolated attempts were tested independently against frozen control
  `kojimar_simple_baseline_v1`.
- Frozen control and opponents:
  `kojimar_simple_baseline_v1` as the live safe baseline and direct control for
  every final-day experiment.
- Seeds, seats, and game count:
  All final-day claims used seat-balanced direct checks. v26 was tested twice at
  30 games each after rule correction / generic-API reconstruction. v27 used 60
  total games as two 30-game batches. v28 and v29 used 30 games each.
- Result with uncertainty:
  - `v26` retreat threat experiment:
    first small-sample run was misleading. Corrected follow-up versus v1:
    `11-19-0` (`36.7%`). Rebuilt generic-API threat estimator follow-up versus
    v1: `11-19-0` (`36.7%`) again.
  - `v27` Crustle targeting experiment:
    batch 1 `18-12-0` (`60.0%`), batch 2 `15-15-0` (`50.0%`), combined
    `33-27-0` (`55.0%`).
  - `v28` Ultra Ball for Dusk Ball deck swap:
    `15-15-0` (`50.0%`).
  - `v29` Night Stretcher for Gravity Mountain deck swap:
    `16-14-0` (`53.3%`).
- Runtime/errors:
  No final-day candidate cleared the bar for confident promotion. None was
  packaged or submitted. Experimental candidate folders were returned to clean
  v1-equivalent behavior after rejection where applicable.
- Interpretation:
  The retreat idea failed twice in the same direction and is a genuine negative
  result. The Crustle targeting tweak was directionally interesting but too
  unstable over 60 games. The deck swaps were neutral to mildly positive at
  best, but not strong enough to justify a last-day submission decision.
- Decision and next action:
  Stop experimentation. Keep `submission_kojimar.tar.gz` /
  `kojimar_simple_baseline_v1` as the sole final submission for Sunday, August
  16, 2026, with the user-tracked live rating around `695`. No further action
  is needed before the deadline.
