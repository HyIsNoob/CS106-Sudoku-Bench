## arXiv:2505.16135v1 [cs.AI] 22 May 2025

```
21 May 2025
```
# Sudoku-Bench: Evaluating creative reasoning

# with Sudoku variants

```
Jeffrey Seely^1 , Yuki Imajuku^1 , Tianyu Zhao^1 , Edoardo Cetin^1 and Llion Jones^1
```
(^1) Sakana AI
Existing reasoning benchmarks for large language models (LLMs) frequently fail to capture authentic
creativity, often rewarding memorization of previously observed patterns. We address this shortcoming with
S u d oku - Be nc h, a curated benchmark of challenging and unconventional Sudoku variants specifically
selected to evaluate creative, multi-step logical reasoning. Sudoku variants form an unusually effective domain
for reasoning research: each puzzle introduces unique or subtly interacting constraints, making memorization
infeasible and requiring solvers to identify novel logical breakthroughs (“break-ins”). Despite their diversity,
Sudoku variants maintain a common and compact structure, enabling clear and consistent evaluation.
S u d oku - Be nc hincludes a carefully chosen puzzle set, a standardized text-based puzzle representation, and
flexible tools compatible with thousands of publicly available puzzles—making it easy to extend into a general
research environment. Baseline experiments show that state-of-the-art LLMs solve fewer than 15% of puzzles
unaided, highlighting significant opportunities to advance long-horizon, strategic reasoning capabilities.
Alongside this report, we release the Sudoku-Bench repository.

## Contents

```
1 Introduction 2
```
```
2 Background: Sudoku Variants 3
```
```
3 Sudoku-Bench: Dataset and Benchmark Design 6
```
```
4 Baseline Performance and Analysis 9
```
```
5 Related Work 10
```
```
6 Discussion 11
```
```
Corresponding author(s): Jeffrey Seely (jeffrey@sakana.ai)
```

```
Matty Didn't Call You Back Because He Had The Wrogn Number
by Lake
Normal sudoku rules apply.
Every clue in the puzzle is wrogn. A clue is wrogn if it is not completely correct.
```
```
Parity Paradoxby Marty Sears
Normal sudoku rules apply. Each line within a 3x3 box has the same total, which is
displayed in yellow in that box. (2-digit yellow totals read from left to right.) The digit in the
purple square indicates how many of the yellow totals have the same parity
(oddness/evenness) as itself (ie the purple square digit).
```
```
Reticuleby Skeptical Mario
Killer cages - Digits in a cage cannot repeat and sum to the clue in the upper left corner
of the cage
Thermometers - Digits along a gray thermometer line increase moving away from
the bulb
```
```
Modsby Marty Sears & ThePedallingPianist
Normal sudoku rules apply. Yellow lines are 'Same Difference' lines. Each pair of
adjacent digits on one of these lines has the same difference. However, this 'difference
value' may be different for different lines. A digit in a circle indicates exactly how many
circles contain that digit.
```
```
RAT RUN 7: Multiple Choiceby Marty Sears
Normal sudoku rules apply.
AIM OF EXPERIMENT: Finkz the rat must reach the cupcake by finding a path through the maze. The path
must not visit any cell more than once, cross itself, or pass through any thick maze walls.
As well as moving orthogonally, Finkz may move diagonally if there's a 2x2 space in which to do so, but
may never pass diagonally through a round wall-spot on the corner of a cell.
TELEPORTS: Entering a teleport will cause Finkz to be instantly transported to the matching coloured teleport.
From there she can continue her journey. Matching teleports always have identical digits, but teleports that
don't match always have different digits.
ONE-WAY DOORS: Finkz may only pass directly through a purple arrow if moving in the direction the
arrow is pointing. An arrow always points to the smaller of the two values it sits between.
TEST CONSTRAINT: In this experiment, for any two adjacent digits along the correct path, one can be
divided by the other to give an exact integer (ie; one is a multiple of the other.)
```
Figure 1|Each Sudoku variant has a unique set of constraints explicitly described in the puzzle rules.
Puzzles may feature whimsical rules such as in _Rat Run_ , or meta-level constraints, such as requiring
all standard Sudoku rules to be intentionally violated.

## 1. Introduction

Large-scale language models excel at short-form deduction (Long, 2023; Wei et al., 2022), yet
genuinely _creative_ reasoning remains elusive. Many standard benchmarks, where current models
already rival or surpass human performance (Glazer et al., 2024; Hendrycks et al., 2021; Phan et al.,
2025), often reward the memorization of solution templates (Bubeck et al., 2023). Once these
templates are implicitly memorized, incremental accuracy gains offer limited insight into a model’s
capacity for novel reasoning. Benchmarks such as ARC (Chollet, 2019) effectively resist memorization;
however, their solutions, while novel to models, remain straightforward for humans, insufficiently
capturing the depth of human creative reasoning.

We propose Sudoku variants (Fig. 1) as a unique domain addressing this gap. A Sudoku variant is a
logical puzzle defined by a partially filled𝑛×𝑛grid, accompanied by visual constraints and even a
problem-specific set of rules that can only be described in natural language. Yet, each puzzle still
admits a unique solution—an𝑛×𝑛grid fulfilling its constraints. Puzzle creators introduce original
rules or combine common constraints in novel ways. Hundreds of user-submitted Sudoku variants
are published daily on platforms like Logic Masters Germany (Log), deliberately designed to require
_creative_ insights and subtle logical breakthroughs. Such puzzles precisely target the type of novel,
multi-step reasoning that memorization-focused and even popular reasoning benchmarks fail to
consistently measure (Zhang et al., 2024).

This paper’s contribution is twofold. First, we introduce open-source tools interfacing directly with
the popular puzzle application **SudokuPad** (Neumann, 2021), facilitating both agentic tool-use
interaction and standardized textual puzzle representations. The agentic interaction provides an
API to fetch images of the current board state and access to all the annotation tools available in
**SudokuPad** that human solvers usually rely on. Our textual format isolates logical reasoning from
visual processing, enabling effective evaluation with current language models. Second, we present
S u d oku - Be nc h, a carefully curated benchmark of 100 Sudoku variants, selected in collaboration


with hosts from the _Cracking the Cryptic_ YouTube channel. These puzzles span a wide range of
difficulties and reasoning styles, deliberately chosen to test model performance across diverse logical
pathways and puzzle-specific “break-ins.”

Our experiments showcaseS u d oku - Be nc hposes a striking challenge for current state-of-the-art
models. Without tool assistance, even the strongest publicly available LLM evaluated solves fewer
than 15% of the benchmark. Notably, most of the successful completions come from the simplest
subset of 4 × 4 puzzles, with performance rapidly collapsing with larger and less conventional grids.
This is observed in both the one-shot configuration (prompt a model to solve a puzzle in one response)
and a multi-step configuration (multi-turn interaction between the model providing at least one digit
and the user providing the updated board state).

Beyond benchmarking, Sudoku variants offer a fertile _laboratory_ for reasoning research. An extensive,
ever-growing supply of human-generated puzzles allows scalable difficulty progression, from simpler
4 × 4 puzzles suitable for small models to highly intricate 9 × 9 puzzles, the hardest of which can
stump all but the best expert human solvers. Rich auxiliary data, including detailed expert solution
transcripts and interaction traces, facilitate imitation learning. We include, as part of S u d oku -
Be nc hthousands of hours of reasoning transcripts and actions taken when solving from _Cracking the
Cryptic_ , a popular YouTube channel dedicated to detailed demonstrations of solving Sudoku variants
with over 250M views. This data is entirely available for researchers who wish to explore supervised
approaches to learn and fine-tune models from human reasoning – qualitatively far beyond the depth
and diversity of synthetic reasoning datasets with current state-of-the-art language models (Li et al.,
2025; Muennighoff et al., 2025).

The remainder of this paper proceeds as follows: Section 2 surveys Sudoku variants and their reasoning
demands. Section 3 details theS u d oku - Be nc hdataset, text interface, and evaluation framework.
Section 4 presents baseline results and analyses of model failure modes. We review related work in
Section 5, and conclude with open research directions in Section 6.

## 2. Background: Sudoku Variants

Traditional Sudoku involves completing a 9 × 9 grid such that each digit from 1 to 9 appears exactly
once in every row, column, and 3 × 3 subgrid. This structure provides a foundation for numerous
variants that introduce additional constraints. For instance, _Killer Sudoku_ combines elements of
Sudoku and Kakuro, requiring digits within outlined cages to sum to specified totals without repeats.
_Thermometers_ are paths of adjacent cells where digits must increase monotonically. Digits along
_arrows_ must sum to the digit in the circled cell at the base. _Kropki_ dots between cells indicate specific
relationships, such as consecutive numbers or a 1:2 ratio.

The availability of web-based puzzle-making tools allowed puzzle authors to invent their own variants.
In early 2020, the puzzle-hosting site Logic Masters saw a surge in the number of puzzles posted. As
of May 2025, more than 27,000 user-submitted variants are published on the site (Log).

Puzzle creators frequently combine multiple constraints in unique ways. Often, these combined
constraints result in puzzles starting with minimal or no digits, necessitating extensive logical reasoning
to determine the initial placement, termed a “break-in.” Such puzzles require solvers to meticulously
explore the interaction of constraints, significantly diverging from the eager guessing often observed
in reasoning LLMs (Section 4).

Beyond these standard constraint types, puzzle setters often employ meta-constraints, which involve
deducing puzzle-specific parameters (e.g., “digits in a cage sum to an unknown value to be determined
by solving,” or “the line must be identified as either a palindrome or a renban sequence”). These
meta-constraints add another layer of complexity and creative reasoning.


```
Ascension
by Florian Wortmann
Normal sudoku rules apply. Identical digits cannot be a knight's move apart. Digits along an arrow sum to the digit in the corresponding circle.
```
Example of a logical break-in from the puzzle _Ascension_. Despite the initial grid being empty, the puzzle
constraints collectively enforce a strict sequence of increasing digits from the lower left to the upper right
shaded circles. Identifying and leveraging this subtle interplay forms the puzzle’s essential insight. Though
rated at an easy difficulty (2-star), current LLMs consistently fail to identify this logical entry point.

```
reasoning trace by gemini-2.5-pro-preview-03-
```
1. Identify Constraints: Standard Sudoku, Anti-Knight, Arrows (sum along arrow equals circle
value).2. Arrow Analysis: All circles must be >= 3 (sum of two distinct digits >= 1+2=3). Arrow digits are
distinct from circle digit. Digits on an arrow are distinct.
3. Shared Circle Analysis:
* C(4,3) = C(4,1)+C(4,2) = C(5,4)+C(6,5). C(4,3) != C(4,1), C(4,2). C(4,3) != C(5,4), C(6,5). * C(4,6) = C(5,6)+C(6,6) = C(3,5)+C(2,4). C(4,6) != C(5,6), C(6,6). C(4,6) != C(3,5), C(2,4).
* C(1,6) = C(1,5)+C(1,4) = C(2,7)+C(3,8). C(1,6) != C(1,5), C(1,4). C(1,6) != C(2,7), C(3,8).
4. * C(4,3) is knight move from C(2,4) & C(3,5). Since C(4,6) = C(2,4)+C(3,5), C(4,6) > C(2,4) and Anti-Knight + Arrow Interactions:
C(4,6) > C(3,5). This means C(4,3) cannot be C(2,4) or C(3,5). Thus, C(4,3) != C(4,6).
* [...]
5. * Digits on arrows cannot be 9.Digit 9 Analysis:
* C(1,9) cannot be 9: If C(1,9)=9, then C(2,7)!=9, C(3,8)!=9 (knight moves).
C(1,6)=C(2,7)+C(3,8). C(1,6)!=9 (same box). C(2,9)+C(3,9)=9. This doesn't lead to the previous contradiction. Let's re-evaluate. C(1,9)=9 -> C(2,7)!=9, C(3,8)!=9. C(1,6) = C(2,7)+C(3,8). C(1,6)
!= C(1,9)=9 because they are in the same box. This means C(2,7)+C(3,8) != 9. This is possible.
Where did the earlier contradiction come from? Ah, I misinterpreted C(1,6)!=9.
* C(4,3) cannot be 9: If C(4,3)=9, [...] * [...]
6. C(4,6)=5Digit 1 Analysis (, C(3,5)=4, C(2,4)=1. Check anti-knight 1: C(4,1)=1, C(5,4)=1, C(2,4)=1. These are Attempt C(4,3)=3): Led to C(4,1)=1, C(4,2)=2, C(5,4)=1, C(6,5)=2. Then
allowed. This led to {C(5,6), C(6,6)}={1,4} or {2,3}. {1,4} fails (row 5 conflict: C(5,4)=1, C(5,6)=1).
{2,3} means C(5,6)=2, C(6,6)=3 or C(5,6)=3, C(6,6)=2. Subcase C(5,6)=2, C(6,6)=3. Grid:
C(4,1)=1, C(4,2)=2, C(4,3)=3, C(5,4)=1, C(6,5)=2. C(2,4)=1, C(3,5)=4. C(4,6)=5. C(5,6)=2, C(6,6)=3. Column 4 has C(2,4)=1 and C(5,4)=1. Impossible. So C(4,3)=3 is impossible.
7. C(4,6)=5Digit 1 Analysis (, C(3,5)=2, C(2,4)=3. Then {C(5,6), C(6,6)}={1,4} or {2,3}. {1,4} means C(5,6)=1, Attempt C(4,3)=4): Led to C(4,1)=1, C(4,2)=3, C(5,4)=1, C(6,5)=3. Then
C(6,6)=4. Fails (row 5 conflict: C(5,4)=1, C(5,6)=1). {2,3} requires C(5,6)=3, C(6,6)=2 (C(5,6)=
impossible by AK C(3,5)=2, C(6,6)=2 impossible by AK C(3,5)=2). Grid: C(4,1)=1, C(4,2)=3,
C(4,3)=4, C(5,4)=1, C(6,5)=3. C(2,4)=3, C(3,5)=2. C(4,6)=5. C(5,6)=3, C(6,6)=2. Check AK 3: C(4,2)=3, C(6,5)=3, C(2,4)=3, C(5,6)=3. C(4,2) vs C(2,4): OK. C(4,2) vs C(5,6): OK. C(6,5) vs
C(2,4): OK. C(6,5) vs C(5,6): OK. C(2,4) vs C(5,6): OK. Looks OK. Let's write partial grid:
... |... |.. .... 3.....
.... 2....
1 3 4 |.. 5 |...
... 1. 3.. ..... 3 2...
Row 6 has C(6,5)=3, C(5,6)=3. Impossible. So C(4,3)=4 is impossible.
8. Conclusion so far: C(4,3) >= 5. C(1,9)!=9. C(4,6)!=9.
9. Consider C(7,3)=8. [...]
[...]

```
Analysis
Confirmation of the puzzle rule of arrow and circle
```
```
Analysis
Confirmation of the puzzle rule of knight’s move
```
```
(Strange) Analysis
The model tries to exclude the possibility of some
cells being 9, but the intuition is unclear, and this
step of analysis does not effectively narrow the
candidate space.
```
```
Search
With the temporary information of “circles>=3”, the
model starts “guessing” until contradiction.
Firstly it tries circle cell r4c3=3, r4c6=5, which
finally leads to a contradiction. While the search
strategy is brutal, the model also makes mistakes
of missing potential placements (e.g. when r4c3=3,
it can also have r4c1=2, r4c2=1).
Then it tries circle cell r4c3=4, r4c6=5, etc. This
search attempt finally leads to a contradiction
again.
```
```
More Search
The above attempts of search provide a bit more
information but the model continues to rely on
search to solve the puzzle and reached a wrong
solution.
```
Gemini 2.5 Pro Preview’s attempt to solve the puzzle _Ascension_. In contrast to the break-in by a human
solver, the model failed to effectively narrow its search space and had to rely on a more brute-force search
strategy, which did not lead to the correct solution.

Figure 2| _Ascension_ example.


```
Puzzle authors are ultimately limited only by imagination, often developing whimsical and novel
rulesets (e.g., puzzles themed around rats in mazes (Fig. 1)). Crucially, all Sudoku variants maintain
a structured format: an𝑛×𝑛grid, natural-language puzzle rules, visual elements easily encoded as
text, and a single unique solution. This structured yet flexible framework makes Sudoku variants
exceptionally suitable for systematically investigating creative reasoning capabilities, meaning that
the puzzles are very diverse and challenging but grounded and easy to verify if correct.
```
```
Puzzle example: Ascension We illustrate some of these features with an example. Figure 2a
highlights the novel interaction between a knight’s move restriction and arrow constraints.
To find the puzzle’s break-in, the solver must make three observations.
```
### First, whatever the digit highlighted in green (r4c6, box 5), it must occur somewhere in box 2, but

```
not in column 6 (by standard Sudoku rules), or along its arrow tip, or a knight’s move away, thus
```
### can only occur in one of the two half-shaded cellsr1c4orr1c5. This same pattern applies to the

```
other cell groups highlighted by the other colors shown in the middle panel. The second observation
is that since digits on the arrow must be smaller than the corresponding circled base, this creates a
long-range chain dependency across the highlighted cells, namely, the circled cells shaded yellow,
purple, green, blue, then red, must be monotonically increasing. This is a key insight but not enough
to determine an exact digit yet.
The third observation is that the purple cell must be the sum of three Sudoku digits, the two in its
```
### arrow tipr4c1andr4c2, but one of which is equal to the yellow cell ofr7c3, which itself is the

```
sum of two Sudoku digits by arrow rules. The only digit that can be the sum of three Sudoku digits
```
### and leave enough room for the monotonic chain along green, blue and red, is six. Thereforer4c

```
must be six and the subsequent digits in the monotonic chain are forced (right panel).
In a video demonstrating this puzzle solve, an expert solver discovered this break-in in about 4.
minutes, and a full puzzle solve taking about 35 minutes.^1 In all LLMs we tested, no model was able
```
### to make progress. For example, we show the reasoning summary ofGemini 2.5 Pro Preview

(Fig. 2b), which was able to successfully parse and identify the puzzle constraints, but quickly resorts
to guesswork and search. This highlights that there is still a gap between how LLMs reason and how
humans prefer to reason; LLMs can rely on brute-force but humans will prefer to save time and energy
by using precise logic to find shortcuts to correct digits. We hope to see this benchmark encouraging
work on creating LLMs that reason in a more “human-like” manner.
The _Ascension_ example highlights two facets of Sudoku variants. First, although both knight-move
and arrow constraints are commonplace, this specific interaction is unique to this particular puzzle.
Therefore, the memorization-resistance of Sudoku variants is not exclusively due to the inclusion of
novel rulesets; familiar constraints can induce a solving tactic never seen before. Indeed, some of the
most difficult puzzles adopt deceptively simple rulesets. The second point is that for puzzles with few
or no given digits (as is common in variants), the search space is too large for initial guesswork to be
effective. This also often necessitates a kind of meta-reasoning where one must decide at the outset
what reasoning techniques should be applied, e.g. the use of coloring, set theory or looking at digit
parity.
This pattern of needing to spend time at the beginning to understand how the constraints interact
in a new manner is normal when humans tackle these puzzles. This also means that some of these
initial deductions remain pertinent throughout the solve, meaning that in order to robustly solve
some of these puzzles over 100s of steps will either require a form of memory, like a scratchpad, or a
very long context window.

(^1) https://www.youtube.com/watch?v=-7OR_IK4Th


## 3. Sudoku-Bench: Dataset and Benchmark Design

We sought to select 100 puzzles that are representative of the breadth of Sudoku variants. To establish
a graded evaluation curve, we selected 15 4 × 4 puzzles, 15 6 × 6 puzzles, and 70 9 × 9 puzzles.
The 15 4 × 4 puzzles are included, in part, to measure progress in even modestly sized language
models. Fifty of the 9 × 9 puzzles were curated by the hosts of _Cracking the Cryptic_ exclusively for this
benchmark. The selected puzzles evenly span difficulty ratings from novice-friendly “1-star” puzzles
to expert-level “5-star” challenges that may require hours of careful analysis before any digits can be
confidently placed. Twenty of the puzzles are difficult vanilla Sudokus, which were supplied by the
puzzle company Nikoli, which popularized Sudoku in the 1980s. We aimed to create a smooth ramp
in complexity such that an initial attempt at tackling the benchmark can yield some early success, but
fully solving it will be very challenging, and we hope that this benchmark will resist being solved for
a significant time span.

**Text descriptions** Each puzzle is given a pure text representation. For instance, Fig 3 shows a simple

### 4 × 4 puzzle whose line paths are represented as a sequence ofrxcy(row x column y) coordinates,

and the location of the dot is described as the two cells it lies between. The rules, visual elements,
grid size, and initial board state (if any digits are given) are sufficient to unambiguously specify the
puzzle and converted into a prompt.

While some of the most recent reasoning models have shifted toward multimodal inputs, we found
that most, including OpenAI o3 (OpenAI, 2025), struggle in converting 9 × 9 puzzles into accurate
coordinates. Puzzle benchmarks such as Enigma (Wang et al., 2025) and VGRP (Ren et al., 2025)
emphasize the visual aspect of puzzles and require multimodal models. Given that current frontier
models still struggle in exact specification of the visual elements of Sudoku puzzles, we opted to
specify all elements precisely in text to isolate the creative reasoning process itself from visual
understanding.

Each puzzle’s text representation has been precomputed for puzzles onS u d oku - Be nc h. We provide
the code for extracting text descriptions from a puzzle specified in SudokuPad, allowing researchers
to utilize this harness in other puzzles.

Note that many of the puzzles would benefit from visual reasoning, some even potentially requiring
it, since many of the break-ins are geometric and use symmetry, or have some rules that reference the
shapes in the puzzle. Some puzzles can be very visually dense (See Bottom-Right in Fig 1) and current
vision model we tested are not powerful enough to extract all the features, like the small numbers.
We suspect that solving this benchmark using vision would represent a significant improvement over
current multimodal LLMs.

**3.1. Expert reasoning traces**
A core question is whether advancing reasoning capabilities in LLMs can benefit from adopting
more “human-like” thinking. In reinforcement learning models, pretraining on human supervision is
common, while other work has shown that RL from scratch yields better performance in contained
environments (Hester et al., 2018; Lowe et al., 2017; Ouyang et al., 2022; Silver et al., 2016).
Vanilla Sudoku is an interesting domain in that the strategies that humans use differ so significantly
from search-based solvers (Pelánek, 2011), and this effect is especially pronounced in Sudoku
variants.

The YouTube channel _Cracking the Cryptic_ offers a particularly unique opportunity to explore the
benefits of imitation learning. The channel contains over 3,000 published videos demonstrating the
solving process of Sudoku variants. Notably, the hosts must verbally describe their thinking process,
explaining to the viewer each logical deduction. A typical puzzle takes the hosts around 60 minutes


```
Rules:
Normal 4x4 sudoku rules apply.
Digits separated by a black dot are in a 1:2 ratio.
The difference between two adjacent digits on a coloured
line indicates exactly how many pairs of adjacent digits
along that line have that exact difference.
```
```
Initial grid:
```
....
....
....
....

```
Differences Count - part 1
by Sujoyku and Marty Sears
```
```
Visual elements:
```
- line, color: pale green, coords: r1c1 r2c2 r4c
- line, color: plum, coords: r2c2 r2c3 r3c4 r4c
- circle, color: black, location: between r4c1 and r4c

Figure 3|A text representation of a puzzle. The rules, initial grid, and a text description of visual
elements are sufficient to unambiguously specify the puzzle.

to solve, while some of the more difficult puzzles featured on the channel are over 3 hours in length.
We developed a dataset consisting of the audio transcripts of each solve, together with a sequence of
SudokuPad actions extracted from the video. The actions were extracted using a machine learning
model trained on ground truth actions simulated on SudokuPad and then applied to video frames.
This dataset is hosted on HuggingFace^2 under an MIT license in agreement with the hosts of the
channel.

**3.2. Dataset format**

### TheS u d oku - Be nc hpuzzle dataset^3 contains three subsets,challenge_100,nikoli_100, and

### ctc. Thechallenge_100is described above and represents the core benchmark. Additional

### puzzle data includenikoli_100, a collection of hand-made vanilla Sudokus supplied by Nikoli for

### this benchmark (20 of which are featured inchallenge_100). Thenikoli_100are designed to

highlight creative or human-like reasoning in their solution paths, and may be applicable to many of

### the research approaches that use vanilla Sudoku as a testbed (Section 5). Thectcincludes 2,

Sudoku variants that have been solved on _Cracking the Cryptic_. Due to the breadth and variety of

### Sudoku variants, the text representation of each puzzle inctchas not undergone manual checking,

and an unambiguous representation of the board would require a screenshot in some cases.

**3.3. SudokuPad environment**

We also provide tools for interacting with SudokuPad in an agentic environment. SudokuPad enables
common note-taking strategies used by human solvers, including color-coding cells (as in Fig. 2a)
or providing candidate digits or pencil marks to cells. Our simple harness allows models to directly
interface with the application to make use of these tools. Using SudokuPad in-the-loop may fit well
with related benchmarks that evaluate reasoning models (including vision language models) in simple
game environments (Paglieri et al., 2024; Ren et al., 2025). Our evaluation in this paper (Section 4)
uses text interaction (relying only on SudokuPad for the initial puzzle data extraction). We make all

(^2) huggingface.co/datasets/SakanaAI/Sudoku-CTC-Reasoning
(^3) huggingface.co/datasets/SakanaAI/Sudoku-Bench


```
Model Multi-step correct placements Multi-step solve rate (%) Single-shot solve rate (%)
4 ×4 6×6 9× 9 All 4 ×4 6×6 9× 9 All 4 ×4 6×6 9× 9 All
O3 Mini High 9.7 0.7 – – 60.0 0.0 – – 73.3 6.7 2.9 14.
Gemini 2.5 Pro 11.6 0.6 1.8 3.1 73.3 0.0 0.0 11.0 60.0 13.3 0.0 11.
Qwen 3.235B A22B 6.5 1.1 0.7 1.7 40.0 0.0 0.0 6.0 53.3 0.0 0.0 8.
Qwen 3.30B A3B 1.3 0.0 0.3 0.4 6.7 0.0 0.0 1.0 46.7 0.0 0.0 7.
DeepSeek R1 9.5 0.8 1.1 2.3 60.0 0.0 0.0 9.0 40.0 0.0 0.0 6.
Grok 3 Mini 8.5 0.7 0.9 2.0 53.3 0.0 0.0 8.0 40.0 0.0 0.0 6.
Qwen QwQ 32B 5.0 0.7 0.6 1.3 26.7 0.0 0.0 4.0 40.0 0.0 0.0 6.
Qwen 3 32B 4.3 0.5 0.5 1.0 26.7 0.0 0.0 4.0 40.0 0.0 0.0 6.
Claude 3.7 Sonnet (Thinking) 8.1 1.1 – – 40.0 0.0 – – 33.3 0.0 0.0 5.
GPT 4.1 2.3 0.2 0.3 0.6 13.3 0.0 0.0 2.0 13.3 0.0 0.0 2.
Gemini 2.0 Flash 0.5 0.1 0.2 0.2 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.
Gemma 3 27B IT 0.1 0.1 0.5 0.3 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.
Llama 4 Maverick 0.2 0.5 0.4 0.4 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.
```
Table 1| **Sudoku-Bench leaderboard.** Performance comparison of various LLMs on Sudoku-Bench.
Percentage of puzzles completely solved for each evaluation mode (multi-step vs. single-shot), stratified
by grid size. The right-most **All** columns aggregate across grid sizes (15 puzzles for 4×4 and 6×6,
70 for 9×9). In the multi-step setting, a model is prompted to provide any number of digits in its
response, with the user providing an updated board state at each turn. Interaction is terminated if
the model makes an incorrect placement. The average number of correct placements are presented in
the first column set. In the single-shot setting the model is prompted to solve the entire puzzle in a
single response. “–” indicates that fewer than the required number of responses were available due to
cost limitations, so an aggregate could not be computed.

### of these SudokuPad tools available for researchers on our repositoryhttps://github.com/Sakan

### aAI/Sudoku-Bench.

**3.4. Evaluation Framework**

**Multi-step and single-shot** We evaluate models in both multi-round and single-shot configurations.
In a multi-round setup, we prompt the model to analyze the board and give at least one valid digit
placement per response. We clarify that this is a committed digit(s) that cannot be undone (in the
model’s reasoning trace, any amount of internal backtracking is possible in order to deduce the digit).
Once the digit is placed, the user displays the updated board state. We continue until the puzzle
is solved or the LLM misplaces any digit. In the multi-round setting, we track both the solve rate
and correct digit placements per puzzle. To keep the context window manageable, we keep the most
recent 5 responses from the LLM in context, while always keeping the first user message with the
puzzle specification and instructions. We report the averages as **average solve rate** and **average
correct digits**. In our evaluation, we run a single evaluation per model and per puzzle, so the average
is across the 100 puzzles in the set.

In the single-shot configuration, we prompt the model to provide a solution in a single response. A
single-shot configuration is appropriate for evaluating models with sufficiently large context, or for a
more straightforward evaluation of the smaller 4 × 4 puzzles. In the single-shot setting, we report
only the **average solve rate**.


```
Figure 4|Response categorization for the single-shot setting.
```
## 4. Baseline Performance and Analysis

```
We evaluated the current generation of state-of-the-art large language models onS u d oku - Be nc h,
revealing substantial difficulty posed by these Sudoku variants. Table 1 summarizes model perfor-
```
### mance across puzzle sizes and interaction modes on benchmark. Even leading models such aso

### mini highandGemini 2.5 pro previewdemonstrated solve rates below 15% for the complete

```
set. Notably, performance varied significantly by puzzle size: models generally solved smaller 4 × 4
puzzles at rates between 40% to 73%, but performance sharply declined for 6 × 6 grids and dropped
nearly to zero on 9 × 9 puzzles, underscoring the rapid escalation in complexity.
Comparing single-shot to multi-step evaluation modes, allowing iterative feedback slightly improved
outcomes for smaller puzzles but did not meaningfully impact results for larger puzzles. The minimal
difference between modes suggests that the fundamental difficulty for these models lies not merely
in incremental reasoning but in effectively identifying initial logical breakthroughs.
```
**Categorizing model failures** Analyzing model failures indicated several recurring patterns which
we categorize in Fig. 4. The most common failure mode was presenting with confidence an _Incorrect
Solution_. Other failure modes included _Surrender_ (model explicitly gives up), _Missing Information_
(model incorrectly claims puzzle information or given constraints are incomplete), and _Claimed
Contradiction_ (model mistakenly identifies contradictions in the puzzle rules). Of note is _Missing
Information_. Since variants are not as densely represented in the training set of foundation models
compared to vanilla Sudoku, it appears the new rules and variants throw them off, most notably due
to the fact that variants typically have fewer starting digits (often none) compared to the minimum of
17 in a vanilla 9 × 9 Sudoku. In addition, a part of model responses contain _No Reasoning Trace_ so we

### cannot make a fine-grained categorization of its error type, otherwise we useClaude-3.5-Haiku

```
to classify a wrong solution response into one of the other four error types.
```

```
Sumthings
by Kennet's Dad
Place the digits 1-6, once each, in every row, column,
and region. Region borders divide the blue line into
segments with the same sum.
```
```
Description of the puzzle Sumthings.
```
```
reasoning trace by gemini-2.5-pro-preview-03-
```
1. Understand the Rules and Setup* [...]
2. Analyze the Blue Lines and Segments
* [...]
* * Segments: {r3c4, r2c4} (R4), {r3c3, r4c3} (R2), {r3c2, r4c2, r3c1, r2c1} (R1).Line 2: r3c4, r2c4, r3c3, r4c3, r3c2, r4c2, r3c1, r2c
* Constraint: Sums are equal. Let this sum be S2.
* `S2 = r3c4 + r2c4` * `S2 = r3c3 + r4c3`
* `S2 = r3c2 + r4c2 + r3c1 + r2c1`
* The minimum sum for 4 distinct digits is 1+2+3+4=10. The maximum sum for 2 distinct digits
is 5+6=11. Therefore, * [...] S2 must be 10 or 11.
* The minimum sum for 4 distinct digits is 10. The maximum sum for 2 distinct digits is 11.
Therefore, S3 must be 10 or 11.
3. Determine the Line Sums (S2 and S3)
* [...]
* Let A = digits in {r2c4, r3c4}. Let B = digits in {r4c4, r5c4, r6c4, r6c5}. A and B are disjoint sets of digits.
    * If S2=10, A={4, 6}. If S2=11, A={5, 6}.
    * If S3=10, B={1, 2, 3, 4}. If S3=11, B={1, 2, 3, 5}.
* Test combinations:* S2=10, S3=10: A={4,6}, B={1,2,3,4}. Union = {1,2,3,4,6}. Missing 5. Impossible.
    * S2=10, S3=11: A={4,6}, B={1,2,3,5}. Union = {1,2,3,4,5,6}. Possible.
    * S2=11, S3=10: A={5,6}, B={1,2,3,4}. Union = {1,2,3,4,5,6}. Possible.* S2=11, S3=11: A={5,6}, B={1,2,3,5}. Union = {1,2,3,5,6}. Missing 4. Impossible.
* So, either (S2=10, S3=11) or (S2=11, S3=10).
4. Use the r1c4 = r6c5 Relationship [...]
5. Test the Two Possible Scenarios for S2 and S
* Scenario 1: S2=10, S3=11 [...]
* Scenario 2: S2=11, S3=
[...]
[...]

```
Analysis
Understanding the rules.
```
```
Analysis
The model effectively reduces the possible cases of
two blue lines’ segment sum (S2 and S3) to two
candidates (10 or 11).
```
```
Analysis
From the 2 x 2 = 4 combinations of S2 and S3, it
further reduces it to 2 possible cases, which forms
a small constrained space for latter search.
```
```
Search
The model starts to search by starting from (S2=10,
S3=11) or (S2=11, S3=10) and guessing other
numbers on the lines until a contradiction.
Due to the small search space, the model can find
the only correct placements of the lines and reach a
correct global solution in the end.
```
```
Gemini 2.5 Pro’s solution to the puzzle Sumthings.
```
```
Figure 5| Sumthings example.
```
```
A successful solve While models often struggle with complex break-ins, they can sometimes succeed
on moderately complex puzzles by effectively narrowing the search space. For instance, Figure 5
```
### illustrates a 6×6 puzzle, Sumthings, whichGemini 2.5 Pro Previewsolved. The model adopted

a strategy of reducing the search space to a manageable size, then employing search to find the
correct solution. This approach, however, proves less effective as puzzle complexity increases, where
identifying specific "break-in" insights becomes crucial, as demonstrated by the Ascension example
(Figure 2).

## 5. Related Work

```
S u d oku - Be nc hcomplements existing benchmarks designed to evaluate advanced reasoning in
artificial intelligence, with a particular focus on Sudoku variants as a structured domain for assessing
creative and logical deduction.
```

**Benchmarks targeting creative deductive insight** Benchmarks such as the Abstraction and Reason-
ing Corpus (A R C; Chollet, 2019) present diverse tasks to test reasoning and generalization beyond
pattern memorization.S u d oku - Be nc hsimilarly introduces novel constraints for each puzzle, re-
sisting memorization through a continuous influx of unique puzzles. UnlikeA R C, which emphasizes
tasks simple for humans but challenging for AI, Sudoku variants span a broader difficulty spectrum,
including puzzles challenging even for expert human solvers. Nonetheless, Sudoku puzzles offer rec-
ognizable logical breakthroughs readily appreciated by human novices, makingS u d oku - Be nc ha
valuable resource for precise evaluation of creative reasoning.

**Puzzle-centric reasoning datasets** Several benchmarks focus on puzzle-solving for evaluating
reasoning skills (Giadikiaroglou et al., 2024). For instance, PU Z Z L E S(Estermann et al., 2024)
compiles canonical logic puzzles; Tyagi et al. (2024) systematically analyze grid puzzle-solving
by LLMs; andE n igma E val(Wang et al., 2025) evaluates a large suite of problems from puzzle
competitions. Recent additions includeVG R P- Be nc h(Ren et al., 2025) for visual-grid reasoning,
L og ic Gam e(Gui et al., 2024) for rule-based reasoning, andP u z z l e P l e x(Long et al., 2024) for
evaluating conversational agents’ reasoning. BALROG (Paglieri et al., 2024) evaluates LLM and VLM
reasoning in complex game environments and could be extended using tools fromS u d oku - Be nc hto
include SudokuPad as an environment.

**Sudoku as a reasoning testbed** The standard Sudoku puzzle has been extensively utilized in
machine learning research. Models include Recurrent Relational Networks (Palm et al., 2018)
employing message-passing, differentiable SATNet consistency layers (Wang et al., 2019), masked-
denoising and diffusion methods (Kim et al., 2025; Ye et al., 2024), and Kuramoto-inspired oscillator
dynamics (Miyato et al., 2024). Further, large language models have achieved human-level accuracy
through structured prompting and reasoning decomposition (Long, 2023). Shah et al. (2024) showed
a high solve rate on vanilla Sudokus by training on a sequence of steps from a solver.S u d oku -
Be nc hextends this research tradition by incorporating diverse and novel puzzle constraints, enabling
evaluations that specifically target multi-step, strategic, and creative reasoning.

## 6. Discussion

**The role of tool use** Evaluating model reasoning can be distinguished by whether external tools,
such as constraint solvers or code execution environments, are available. Without tool use, the
evaluation specifically assesses the model’s intrinsic reasoning capabilities, including logical deduction,
maintaining global consistency, and internally generating creative insights, akin to solving puzzles by
hand. This approach emphasizes pure cognitive reasoning skills and has been the primary evaluation
mode presented in our baselines (Section 4).

Conversely, allowing tool use tests the model’s ability to translate a given puzzle into a formal
representation suitable for external solvers, effectively interact with these tools, and interpret solver
results correctly. Standard Sudoku puzzles become straightforward when a solver is employed.
Variants that only employ standard constraints such as arrows, cages, etc, are also easily solved
by code execution. A third category of puzzles require natural language understanding and are
not straightforward to interpret as a constraint satisfaction problem. This third category is itself
a meaningful test for reasoning models with tool-use enabled. However, our current intention is
to assess the reasoning required to find a puzzle’s “break-in,” and many puzzles such as _Ascension_
from Fig. 2a are easily solved by tool-use, but the solution path would be substantially different than
that intended by the puzzle setter. Therefore we selected the 100 puzzles ofS u d oku - Be nc hfor
evaluating models without tool-use. Future work could consider a separate tool-use track, potentially
with a different collection of puzzles.


**Conclusion** We introducedS u d oku - Be nc h, a unified benchmark built around modern Sudoku
variants that systematically stress long-horizon deduction, rule-interpretation, and strategic planning.
In addition, the benchmark is uniquely suited for evaluating creative reasoning via the rich and varied
collection of break-ins featured in most puzzles. The benchmark includes a curated puzzle corpora
with textual representations, providing a controlled substrate for measuring how well language
models cope with novel, tightly coupled constraints. Baseline experiments show that frontier LLMs
solve fewer than 15% of instances without external tools, and performance falls sharply on 9 × 9
variants—evidence that substantial headroom remains for improvements.

## Acknowledgments

We thank Sven Neumann, author of SudokuPad, for help with the development of tooling used in
S u d oku - Be nc h, and for permission in using SudokuPad as part of this project.S u d oku - Be nc his
developed in partnership with _Cracking the Cryptic_ , with an agreement to provide content from the
channel for use in the AI research community. The puzzles provided in the benchmark are featured
on the channel. We acknowledge all puzzle creators and provide a list of setter acknowledgments
in our repository. We thank the hosts of _Cracking the Cryptic_ , Simon Anthony and Mark Goodliffe,
for various help in the development of this benchmark, including the curated selection of puzzles in
S u d oku - Be nc h, and for providing SudokuPad replay files for the reasoning traces described in
3.1. The handmade vanilla Sudoku puzzles were provided by Nikoli. We thank Nikoli for graciously
agreeing to provide their puzzles for this benchmark.

## References

### Logic masters germany.https://logic-masters.de. Accessed: 2025-05-13.

S. Bubeck, V. Chandrasekaran, R. Eldan, J. A. Gehrke, E. Horvitz, E. Kamar, P. Lee, Y. T. Lee, Y.-
F. Li, S. M. Lundberg, H. Nori, H. Palangi, M. T. Ribeiro, and Y. Zhang. Sparks of artificial

### general intelligence: Early experiments with gpt-4. ArXiv , abs/2303.12712, 2023. URLhttps:

### //api.semanticscholar.org/CorpusID:257663729.

### F. Chollet. On the measure of intelligence, 2019. URLhttps://arxiv.org/abs/1911.01547.

B. Estermann, L. A. Lanzendörfer, Y. Niedermayr, and R. Wattenhofer. Puzzles: A benchmark for neural
algorithmic reasoning. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and
C. Zhang, editors, _Advances in Neural Information Processing Systems_ , volume 37, pages 127059–

### 127098. Curran Associates, Inc., 2024. URLhttps://proceedings.neurips.cc/paper_fil

### es/paper/2024/file/e5d1eaadeed651ba1021c09149db4b92-Paper-Datasets_and_

### Benchmarks_Track.pdf.

P. Giadikiaroglou, M. Lymperaiou, G. Filandrianos, and G. Stamou. Puzzle solving using reasoning of
large language models: A survey. _arXiv preprint arXiv:2402.11291_ , 2024.

E. Glazer, E. Erdil, T. Besiroglu, D. Chicharro, E. Chen, A. Gunning, C. F. Olsson, J.-S. Denain,
A. Ho, E. de Oliveira Santos, O. JĂ¤rviniemi, M. Barnett, R. Sandler, M. Vrzala, J. Sevilla, Q. Ren,
E. Pratt, L. Levine, G. Barkley, N. Stewart, B. Grechuk, T. Grechuk, S. V. Enugandla, and M. Wildon.
Frontiermath: A benchmark for evaluating advanced mathematical reasoning in ai, 2024. URL

### https://arxiv.org/abs/2411.04872.

J. Gui, Y. Liu, J. Cheng, X. Gu, X. Liu, H. Wang, Y. Dong, J. Tang, and M. Huang. Logicgame: Bench-
marking rule-based reasoning abilities of large language models. _arXiv preprint arXiv:2408.15778_ ,
2024.


D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt. Measuring
mathematical problem solving with the math dataset. _NeurIPS_ , 2021.

T. Hester, M. Vecerik, O. Pietquin, M. Lanctot, T. Schaul, B. Piot, D. Horgan, J. Quan, A. Sendonaris,
I. Osband, G. Dulac-Arnold, J. Agapiou, J. Z. Leibo, and A. Gruslys. Deep q-learning from demon-
strations. In _Proceedings of the Thirty-Second AAAI Conference on Artificial Intelligence and Thirtieth
Innovative Applications of Artificial Intelligence Conference and Eighth AAAI Symposium on Edu-
cational Advances in Artificial Intelligence_ , AAAI’18/IAAI’18/EAAI’18. AAAI Press, 2018. ISBN
978-1-57735-800-8.

J. Kim, K. Shah, V. Kontonis, S. Kakade, and S. Chen. Train for the worst, plan for the best: Under-
standing token ordering in masked diffusions. _arXiv preprint arXiv:2502.06768_ , 2025.

D. Li, S. Cao, T. Griggs, S. Liu, X. Mo, E. Tang, S. Hegde, K. Hakhamaneshi, S. G. Patil, M. Zaharia,
et al. Llms can easily learn to reason from demonstrations structure, not content, is what matters!
_arXiv preprint arXiv:2502.07374_ , 2025.

J. Long. Large language model guided tree-of-thought. _arXiv preprint arXiv:2305.08291_ , 2023.

Y. Long, T. Jiang, Y. Zhao, A. Cohan, and D. Shasha. PuzzlePlex: A benchmark to evaluate the
reasoning and planning of large language models on puzzles. 2024.

R. Lowe, Y. Wu, A. Tamar, J. Harb, P. Abbeel, and I. Mordatch. Multi-agent actor-critic for mixed
cooperative-competitive environments. In _Proceedings of the 31st International Conference on Neural
Information Processing Systems_ , NIPS’17, page 6382â€“6393, Red Hook, NY, USA, 2017. Curran
Associates Inc. ISBN 9781510860964.

T. Miyato, S. Löwe, A. Geiger, and M. Welling. Artificial kuramoto oscillatory neurons. _arXiv preprint
arXiv:2410.13821_ , 2024.

N. Muennighoff, Z. Yang, W. Shi, X. L. Li, L. Fei-Fei, H. Hajishirzi, L. Zettlemoyer, P. Liang, E. Candès,
and T. Hashimoto. s1: Simple test-time scaling. _arXiv preprint arXiv:2501.19393_ , 2025.

### S. Neumann. Sudokupad, 2021. URLhttps://sudokupad.app/.

### OpenAI. OpenAI o3 and o4-mini System Card.https://openai.com/index/o3-o4-mini-sys

### tem-card/, 2025.

L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama,
A. Ray, J. Schulman, J. Hilton, F. Kelton, L. Miller, M. Simens, A. Askell, P. Welinder, P. Christiano,
J. Leike, and R. Lowe. Training language models to follow instructions with human feedback. In
_Proceedings of the 36th International Conference on Neural Information Processing Systems_ , NIPS ’22,
Red Hook, NY, USA, 2022. Curran Associates Inc. ISBN 9781713871088.

D. Paglieri, B. Cupiał, S. Coward, U. Piterbarg, M. Wolczyk, A. Khan, E. Pignatelli, Ł. Kuciński, L. Pinto,
R. Fergus, et al. Balrog: Benchmarking agentic llm and vlm reasoning on games. _arXiv preprint
arXiv:2411.13543_ , 2024.

R. Palm, U. Paquet, and O. Winther. Recurrent relational networks. _Advances in neural information
processing systems_ , 31, 2018.

R. Pelánek. Difficulty rating of sudoku puzzles by a computational model. In _The Florida AI Research_

### Society , 2011. URLhttps://api.semanticscholar.org/CorpusID:6431985.


L. Phan, A. Gatti, Z. Han, N. Li, J. Hu, H. Zhang, C. B. C. Zhang, M. Shaaban, J. Ling, S. Shi, et al.

### Humanity’s last exam, 2025. URLhttps://arxiv.org/abs/2501.14249.

Y. Ren, K. Tertikas, S. Maiti, J. Han, T. Zhang, S. Süsstrunk, and F. Kokkinos. Vgrp-bench: Visual grid
reasoning puzzle benchmark for large vision-language models. _arXiv preprint arXiv:2503.23064_ ,
2025.

K. Shah, N. Dikkala, X. Wang, and R. Panigrahy. Causal language modeling can elicit search and
reasoning capabilities on logic puzzles. _arXiv preprint arXiv:2409.10502_ , 2024.

D. Silver, A. Huang, C. J. Maddison, A. Guez, L. Sifre, G. van den Driessche, J. Schrittwieser,
I. Antonoglou, V. Panneershelvam, M. Lanctot, S. Dieleman, D. Grewe, J. Nham, N. Kalchbrenner,
I. Sutskever, T. Lillicrap, M. Leach, K. Kavukcuoglu, T. Graepel, and D. Hassabis. Mastering the
game of Go with deep neural networks and tree search. _Nature_ , 529(7587):484–489, Jan. 2016.
doi: 10.1038/nature16961.

N. Tyagi, M. Parmar, M. Kulkarni, A. Rrv, N. Patel, M. Nakamura, A. Mitra, and C. Baral. Step-by-step
reasoning to solve grid puzzles: Where do LLMs falter? In Y. Al-Onaizan, M. Bansal, and Y.-N. Chen,
editors, _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ ,
pages 19898–19915, Miami, Florida, USA, Nov. 2024. Association for Computational Linguistics.

### doi: 10.18653/v1/2024.emnlp-main.1111. URLhttps://aclanthology.org/2024.emnl

### p-main.1111/.

C. J. Wang, D. Lee, C. Menghini, J. Mols, J. Doughty, A. Khoja, J. Lynch, S. Hendryx, S. Yue, and
D. Hendrycks. Enigmaeval: A benchmark of long multimodal reasoning challenges, 2025. URL

### https://arxiv.org/abs/2502.08859.

P.-W. Wang, P. Donti, B. Wilder, and Z. Kolter. Satnet: Bridging deep learning and logical reasoning
using a differentiable satisfiability solver. pages 6545–6554, 2019.

J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi, Q. V. Le, and D. Zhou.
Chain-of-thought prompting elicits reasoning in large language models. In _NeurIPS_ , 2022. URL

### https://arxiv.org/abs/2201.11903.

J. Ye, J. Gao, S. Gong, L. Zheng, X. Jiang, Z. Li, and L. Kong. Beyond autoregression: Discrete diffusion
for complex reasoning and planning. _arXiv preprint arXiv:2410.14157_ , 2024.

H. Zhang, J. Da, D. Lee, V. Robinson, C. Wu, W. Song, T. Zhao, P. Raja, C. Zhuang, D. Slack, et al. A
careful examination of large language model performance on grade school arithmetic. _Advances in
Neural Information Processing Systems_ , 37:46819–46836, 2024.


You are the Execution Engine of an advanced Sudoku solver. Your task is to evaluate the provided 
logical analysis and commit EXACTLY ONE valid digit to the board.
[KNOWLEDGE RECAP]
1. The Grid & Core Rules:
- The grid is 6x6, containing 6 rows and 6 columns.
- Notation: "r1c1" indicates the cell at row 1 and column 1.
- The grid consists of 6 rectangular 2x3 subgrids (2 rows tall, 3 columns wide).
- Standard Sudoku Rule: Each row, each column, and each 2x3 subgrid must contain the numbers 1 
through 6 exactly once.
- Killer Sudoku Rule: The grid is divided into "Cages" (contiguous groups of cells). The sum of 
the numbers in each cage must perfectly match its provided target sum.
- Non-Repeating Rule: Numbers cannot repeat within a single cage.
2. Mathematical Facts & Solving Strategies:
- Sum to 21: Since the numbers 1 through 6 add up to 21, every completely filled row, column, and 
2x3 subgrid must sum exactly to 21.
- A 6-cell cage must also have a target sum of 21.
- Deduction Tip: For any subset of cells (row, column, or subgrid), if all but one cell are filled, 
the final cell's value must be 21 minus the sum of the known cells.
3. Reference Material: The Cheat-Sheet
Important Interpretation Rules for the cheat-sheet:
- Combinations are written as sequences of individual digits without separators.
- Each digit in the sequence represents one distinct number in the combination.
- Example: "12" means the combination {{1, 2}}. "135" means the combination {{1, 3, 5}}.
Here is your cheat-sheet for cage combinations: {cheat_sheet}
[CURRENT STATE]
Current board: {current_board}
Cages: {cages}
[LOGICAL ANALYSIS] {current_analysis}
INSTRUCTIONS:
1. Review the "3. Deductions & Bottlenecks" section of the Logical Analysis carefully.
2. Identify ONE cell where a digit is mathematically forced. You can ONLY modify cells that currently contain 0.
3. If there is NO forced cell, review the "2. Candidate Elimination" section and make your best educated guess 
for the cell with the fewest candidates.
4. You MUST output your decision for exactly ONE cell. Abstaining is strictly prohibited.
5. Output your response STRICTLY as a valid JSON object.




You are an expert Sudoku reasoning engine. Your current task is strictly limited to ANALYSIS and NOTE-TAKING. 
Do NOT attempt to solve the puzzle completely. Do NOT output a final grid. Do NOT make eager guesses.
Your objective is to carefully scan the current board state, apply standard Sudoku rules along with the specific variant constraints, and generate a logical scratchpad. This scratchpad will be used in the next step to confidently commit digits.
[KNOWLEDGE RECAP]
1. The Grid & Core Rules:
- The grid is 6x6, containing 6 rows and 6 columns.
- Notation: "r1c1" indicates the cell at row 1 and column 1.
- The grid consists of 6 rectangular 2x3 subgrids (2 rows tall, 3 columns wide).
- Standard Sudoku Rule: Each row, each column, and each 2x3 subgrid must contain the numbers 1 through 6 exactly once.
- Killer Sudoku Rule: The grid is divided into "Cages" (contiguous groups of cells). The sum of the numbers in each cage must perfectly match its provided target sum.
- Non-Repeating Rule: Numbers cannot repeat within a single cage.
2. Mathematical Facts & Solving Strategies:
- Sum to 21: Since the numbers 1 through 6 add up to 21, every completely filled row, column, and 2x3 subgrid must sum exactly to 21.
- A 6-cell cage must also have a target sum of 21.
- Deduction Tip: For any subset of cells (row, column, or subgrid), if all but one cell are filled, the final cell's value must be 21 minus the sum of the known cells.
3. Reference Material: The Cheat-Sheet
Important Interpretation Rules for the cheat-sheet:
- Combinations are written as sequences of individual digits without separators.
- Each digit in the sequence represents one distinct number in the combination.
- Example: "12" means the combination {{1, 2}}. "135" means the combination {{1, 3, 5}}.
Here is your cheat-sheet for cage combinations:
{cheat_sheet}
[LAST MOVE LOG]
- Cell Modified: {last_cell} (Value: {last_value})
- AI's Reasoning: "{last_reasoning}"
- Confidence: {last_is_certain}
[CURRENT STATE]
Current board:
{current_board}
Cages:
{cages}
[PREVIOUS ANALYSIS]
{previous_analysis}
INSTRUCTIONS:
1. Scan the board for the most constrained areas (cells, rows, columns, or variant shapes with the fewest empty spaces).
2. Eliminate candidate digits for these empty cells based on the active rules.
3. If a cell is reduced to a single valid digit, explicitly highlight it in the "Deductions" section with irrefutable logical proof.
4. Output your analysis EXACTLY matching the Markdown template below. Do not add conversational filler.
{analysis_template}