# Final deadline hold: keep Kojimar v1, reject v26 retreat experiment

## Date

2026-08-16

## Current final submission state

- Keep `submission_kojimar.tar.gz` as the final working submission package.
- This corresponds to `kojimar_simple_baseline_v1`, the safe live baseline.
- Latest user-tracked live rating at the deadline check: about `695`.

## Latest two active submissions

A live Kaggle submissions-page confirmation was not available from this
workspace on 2026-08-16 because the local environment does not have the
`kaggle` CLI module installed, so the final-state check fell back to tracked
repo records and local packaged artifacts.

Based on those records, the latest two active submissions still appear to be:

| Slot | Package | Candidate / description | Evidence |
| --- | --- | --- | --- |
| 1 | `submission_kojimar.tar.gz` | `kojimar_simple_baseline_v1` | current safe baseline tracked throughout the repo as the active best; latest user-tracked live rating about `695` |
| 2 | `submission.tar.gz` | older basic/planner baseline | historical submission log shows the old `submission.tar.gz` branch drifting around the high `400s` and remaining clearly weaker than v1 |

No local record in the repo indicates a newer Kaggle submission after the
Kojimar v1 package that would displace this pair, but this statement is based on
tracked local history rather than a live Kaggle page refresh.

## v26 outcome

`kojimar_simple_baseline_v26` tested a retreat-priority idea twice:

1. first with a guessed weakness multiplier, which produced a misleading small
   sample result;
2. then with corrected weakness/resistance handling and a later rebuild using
   generic SDK attack metadata for opponent threat estimation.

Both corrected 30-game seat-balanced checks versus `kojimar_simple_baseline_v1`
finished at `11-19` (`36.7%` win rate), which is a clear rejection signal for a
deadline-day submission decision.

Decision:

- revert v26 safely to the original v1 retreat behavior;
- keep the experimental threat estimators only as dead-code reference;
- do not package or submit v26.

## Final decision

No other candidate in `candidates/` is documented in the repo as both:

- already validated with a real 30+ game win over `kojimar_simple_baseline_v1`;
- and ready to package as a better final deadline submission.

Therefore no further action is needed before the deadline. Keep
`kojimar_simple_baseline_v1` as the final working submission.
