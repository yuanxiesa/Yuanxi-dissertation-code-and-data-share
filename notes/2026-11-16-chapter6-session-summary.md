# Chapter 6 notation and diagrams session — November 16, 2026

## Outcome and stopping point

The user reviewed the progress and considers the current `dissertation/6-contribution-3.tex` good. Remaining theoretical, prose, and compilation work is left for future revision. Do not treat those deferred items as blockers to the accepted stopping point.

## Completed

- Checked the two papers in `resources/`. Modgil and Prakken (2014) explicitly defines a rule-naming function `n`, but `n` does not mean instantiation. Its Section 4.3, printed p. 50 (PDF p. 20), uses parameterized rule names directly. Prakken (2010) leaves its naming convention implicit.
- Updated Chapter 6 to use parameterized names such as `r_{2a}(y,x)` and undercutter conclusions such as `\neg r_{2a}(y,x)`, removing the explicit `n(...)` layer and superscript convention.
- Defined `x` and `y`, corrected the rule-naming explanation, and clarified that introduction-only placement blocks an inference from citation to use rather than establishing non-use.
- At the user's direction, changed awareness and review undercutter rules to defeasible arrows. All three undercutter rules now use `\Rightarrow`.
- Regenerated the three standalone template PNGs in `img/`, with updated notation and defeasible arrows. The red attack labels now read “undercuts.” Awareness continues to target `r_{1a}(y,x)`; the other two target `r_{2a}(y,x)`.
- Added editable LaTeX diagram sources in `img/diagram-sources/` and the reproducible generator `scripts/generate_reasoning_diagrams.py`.
- Regenerated the five assessment cards using `scripts/generate_assessment_cards.py`, refreshed the named PNG aliases in `output/assessment-cards/`, and refreshed copies in `output/five-assessment-examples/`.
- Visually inspected rendered templates and assessment cards, including the introduction-only and multiple-justification layouts.

## Regeneration

Run from the repository root:

```sh
python3 scripts/generate_reasoning_diagrams.py
python3 scripts/generate_assessment_cards.py
```

The card generator already reads the three template filenames in `img/`. It writes DOI-named PNGs and a manifest; refreshing the friendly aliases and copies in `output/five-assessment-examples/` was performed separately during this session.

The five friendly card filenames are `awareness.png`, `review.png`, `introduction-only.png`, `default-at-risk.png`, and `multiple-justifications.png` in `output/assessment-cards/`.

## Deferred by the user

- Clarifying the relationship between the direct citation-to-UP rule and the two-step citation-to-use-to-UP representation.
- The assistant proposed moving awareness to the use-to-UP step, but this was not adopted. Do not change the target on that assumption.
- Finishing the outline and chapter summary and other prose work.
- Compiling the full chapter/dissertation to check layout and image paths. Individual diagram and card LaTeX compilations succeeded; no full dissertation compilation was performed in this session.

The detailed review is in `notes/2026-11-16-chapter6-notation-review.md`. This summary records the later user acceptance of the current state and deferral of the outstanding items. No commit or push was performed during this session.
