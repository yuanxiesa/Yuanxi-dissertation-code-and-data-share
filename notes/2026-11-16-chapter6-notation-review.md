# Chapter 6 notation review — November 16, 2026

Target: `dissertation/6-contribution-3.tex`. Line numbers below refer to the file at the time of this review.

## Source findings

Checked both papers in `resources/`:

- Modgil and Prakken (2014), *The ASPIC+ framework for structured argumentation: a tutorial*: printed p. 35 (PDF p. 5), Definition 3.2, defines `n` as a partial naming function from defeasible rules to formulas in the object language. It does not mean rule instantiation. Printed p. 38, Definition 3.10, defines undercutting using a conclusion contrary to the name of a defeasible rule.
- Section 4.3 of that tutorial, printed p. 50 (PDF p. 20), uses parameterized rule names such as `d_m(x, phi)` directly. Instantiating the parameters gives names for particular ground instances. Its example undercutter concludes the negation of that name, without displaying `n`.
- Prakken (2010), *An abstract framework for argumentation with structured arguments*: printed p. 101 (PDF p. 9), Section 3.3.1 and Definition 3.12, leaves the naming convention implicit rather than introducing the 2014 tutorial's explicit `n` function.

## Revisions to make

1. **Introduce the simpler convention (line 12).** Define `x` as the cited resource and `y` as the citing publication. Explain that parameterized rule names follow Section 4.3 of Modgil and Prakken (2014).
2. **Parameterize the initial rule labels (lines 16, 25, 27).** Use `r_{1a}(y,x)`, `r_{2a}(y,x)`, and `r_{2b}(y,x)`.
3. **Replace the incorrect explanation of `n` (line 34).** Explain that the parameterized expression names the rule instance for the particular publications, and that an argument concluding its negation undercuts an argument applying that instance. Do not say that `n` represents an instance.
4. **Simplify the undercutter conclusions (lines 40, 53, 62).** Replace `\neg n(r_{1a}^{y,x})` with `\neg r_{1a}(y,x)` and `\neg n(r_{2a}^{y,x})` with `\neg r_{2a}(y,x)`. The awareness target may change if the two-step account below is adopted.
5. **Parameterize the remaining rule labels (lines 38, 41, 52, 61).** Use `u_1(y,x)`, `r_3(y,x)`, `u_2(y,x)`, and `u_3(y,x)` consistently. Naming the introduction-only rule also identifies the inference that further evidence could undercut.
6. **Correct the introduction-only explanation (line 57).** The rule does not conclude non-use. It provides a defeasible reason to block the inference from citation to use. Use that plain-language explanation instead of “inference from citation location to non-use.”
7. **Update assessment-card diagrams.** Ensure the notation and attack targets in the images referenced at lines 94–126 agree with the final chapter formulation. Updating the TeX alone will not update text embedded in PNGs.

## Defeasible arrows: agreed and already changed

The user chose defeasible rules for both awareness and review status. Changed the arrows in `u_1` (line 40) and `u_2` (rule starts at line 52; arrow at line 53) from `\to` to `\Rightarrow`. All three undercutter rules now use defeasible arrows. Preserve these changes when revising the notation.

The notation and prose revisions in items 1–6 above have now been applied to the TeX file, including parameterized rule names, removal of the explicit `n` layer, and correction of the introduction-only explanation. The review-status sentence was also corrected to describe a defeasible reason to block the inference. The three template PNGs in `img/` and the five assessment-card examples have now been regenerated with the simplified notation and defeasible arrows. Editable template sources are in `img/diagram-sources/`; run `python3 scripts/generate_reasoning_diagrams.py` before regenerating cards. The output aliases and copies in `output/five-assessment-examples/` were refreshed. Diagram attack targets are unchanged. The direct-rule/two-step modeling question below remains unresolved; awareness still targets `r_{1a}(y,x)`.

## Direct rule versus two-step representation

The review identified an ambiguity at lines 21 and 89: if the direct citation-to-UP rule and the two-step citation-to-use-to-UP route are all active, blocking one route can leave the other available.

The user wants an explanation accessible to the chapter's audience, without a theoretical discussion. A proposed sentence is:

> We use this two-step representation in place of the initial rule when distinguishing where defeaters intervene.

The assistant also proposed placing awareness at the use-to-UP step, `r_{2b}(y,x)`, while review status and introduction-only citations challenge `r_{2a}(y,x)`. That would require updating the awareness paragraph, undercutter conclusion, results explanation, and corresponding diagrams/captions. This is a substantive modeling proposal, not a consequence of changing notation, and has not been settled or implemented. It assumes awareness provides a defeasible reason to expect authors to correct or avoid the known problem when using the protocol.

Do not silently treat this proposed change of target as an agreed decision. Keep the explanation short when resolving it.
