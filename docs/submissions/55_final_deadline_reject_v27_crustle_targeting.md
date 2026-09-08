# Final deadline reject: v27 Crustle targeting change

## Date

2026-08-16

## Current final submission state

- Keep `submission_kojimar.tar.gz` as the final working submission package.
- This corresponds to `kojimar_simple_baseline_v1`, the safe live baseline.
- Latest user-tracked live rating at the deadline check: about `695`.

## Candidate tested

`kojimar_simple_baseline_v27`

## Change summary

V27 tested a narrow two-part Crustle targeting change:

1. allow Mega Lucario ex attack planning to consider the opponent's active
   Crustle (`id 345`) as a valid target instead of always skipping it;
2. add a `1150` score boost for the matching attack option when the opponent is
   detected as a Crustle-wall deck and that active Crustle is the planned
   target.

The existing benched-Crustle avoidance remained intact for non-active targets.

## Validation

Direct control: `kojimar_simple_baseline_v1`

| Batch | Games | Record | Win rate |
| --- | ---: | --- | ---: |
| Batch 1 | 30 | `18-12-0` | `60.0%` |
| Batch 2 | 30 | `15-15-0` | `50.0%` |
| Combined | 60 | `33-27-0` | `55.0%` |

## Decision

Reject for deadline submission.

The first 30-game result was promising, but the second 30-game batch removed the
edge entirely. The combined `55.0%` result is too close to the noise floor to
justify a confidence-worthy deadline-day promotion over the live safe baseline.

V27 was reverted to clean v1 behavior, not packaged, and not submitted.

## Final hold

`kojimar_simple_baseline_v1` remains the final live submission at about `695`
rating. No further action is needed before the 2026-08-16 11:59 PM UTC
deadline.
