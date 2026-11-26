# Chapter 7 strengtheners

November 24, 2026

## Current status

The strengtheners subsection is in [7-contribution-4.tex](../../yuanxi-dissertation/chapters/7-contribution-4.tex#L34). The draft below was shared for review. The dissertation chapter and its figure directory have not been edited this session.

## Modeling decisions

- Use a green support arrow from each evidence predicate to the claim it supports. The current figures introduce no inference rule for either evidence predicate and assign no numerical strength.
- **Boltzmann-weighted averaging.** \(\mathrm{StepScopedToBoltzmann}(y,x)\) supports \(\mathrm{Use}(y,z)\), where \(y\) is the citing publication, \(x\) the WJH protocol, and \(z\) the averaging step. The default route is \(\mathrm{Use}(y,x)\land\mathrm{Use}(x,z)\Rightarrow\mathrm{Use}(y,z)\) via \(r_4(y,x,z)\). The next inference is \(\mathrm{Use}(y,z)\Rightarrow\mathrm{UP}(z,y)\) via \(r_{2b}(y,z)\).
- **Protocol-level citation.** \(\mathrm{ProtocolLevelCitation}(y,x)\) supports \(\mathrm{Use}(y,x)\). The figure uses the protocol-level chain \(\mathrm{Cite}(y,x)\Rightarrow\mathrm{Use}(y,x)\Rightarrow\mathrm{UP}(x,y)\), via \(r_{2a}(y,x)\) and \(r_{2b}(y,x)\). Protocol-level scope leaves open which individual steps the publication used.
- The earlier model treated citation reports as premises of separate defeasible rules \(r_5\) and \(r_6\). The original diagrams were kept for comparison. If we later want a formal claim that added evidence increases joint confidence, revisit argument accrual or gradual bipolar semantics and account for shared evidence.
- On a later pass, check how the preceding defeaters subsection distinguishes the averaging step from Python Script D. It also treats other-step scope as a rebuttal, while the [November 22 note](../../yuanxi-dissertation/notes/2026-11-22-chapter-7-defeaters.md) records an undercutting interpretation.

## Figures

| Version | PNG | TikZ |
| --- | --- | --- |
| Current Boltzmann | [Figure](../output/chapter-7-boltzmann.png) | [Source](../img/diagram-sources/chapter-7-boltzmann.tex) |
| Current protocol-level | [Figure](../output/chapter-7-protocol-level.png) | [Source](../img/diagram-sources/chapter-7-protocol-level.tex) |
| Original Boltzmann | [Figure](../output/chapter-7-boltzmann-original.png) | [Source](../img/diagram-sources/chapter-7-boltzmann-original.tex) |
| Original protocol-level | [Figure](../output/chapter-7-protocol-level-original.png) | [Source](../img/diagram-sources/chapter-7-protocol-level-original.tex) |
| First combined preview | [Figure](../output/chapter-7-strengtheners.png) | |

## Proposed subsection

\subsection{Defeasible reasoning schema and the placement of strengtheners}

Citation context can provide positive evidence for a claim in the defeasible reasoning schema. We call such evidence a \emph{strengthener}. We represent it with a support arrow pointing to the claim it bears on. The arrow records the evidential relationship, and the labeled inference arrows represent the defeasible rules.

\paragraph{Citation scoped to Boltzmann-weighted averaging.}
We write $\mathrm{StepScopedToBoltzmann}(y,x)$ when publication $y$ cites the WJH protocol $x$ specifically for Boltzmann-weighted averaging. This citation context supports $\mathrm{Use}(y,z)$, where $z$ is the Boltzmann-weighted averaging step. It provides evidence for the same claim that $r_4(y,x,z)$ derives from use of the protocol and the inclusion of the averaging step in it. The claim $\mathrm{Use}(y,z)$ in turn provides the premise for $r_{2b}(y,z)$, the defeasible inference to unreliability propagation $\mathrm{UP}(z,y)$.

\paragraph{Protocol-level citation.}
We write $\mathrm{ProtocolLevelCitation}(y,x)$ when publication $y$ cites $x$ as a methodological resource at the level of the protocol as a whole. This citation context supports $\mathrm{Use}(y,x)$, the claim that $y$ used the protocol. The support thus attaches to the conclusion of $r_{2a}(y,x)$, which in turn provides the premise for the defeasible inference to $\mathrm{UP}(x,y)$ by $r_{2b}(y,x)$. The protocol-level citation leaves open which individual steps the publication used.
