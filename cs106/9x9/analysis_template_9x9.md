# Analysis Template for Killer Sudoku 9x9

## 0. Puzzle Information

- Grid size: 9x9
- Digits allowed: 1–9
- Box shape: 3x3
- Row sum: 45
- Column sum: 45
- Box sum: 45
- Cage rule: digits in each cage cannot repeat and must sum to the cage clue.

---

## 1. Equation System View

Treat the puzzle as a constraint system with 81 variables:

```text
r1c1, r1c2, ..., r9c9
```

Each variable must satisfy:

```text
r[x]c[y] ∈ {1,2,3,4,5,6,7,8,9}
```

The full constraint system contains:

```text
9 row equations
9 column equations
9 box equations
N cage equations
```

where:

```text
N = number of cages in the current puzzle JSON
```

Therefore:

```text
Total equations = 27 + N
```

Each equation has two constraints:

1. The values must sum to the target.
2. The values inside the same equation must be distinct.

---

## 1.1 State Update and Constraint Propagation

After every committed placement, update all equations that contain that cell.

For a filled cell:

```text
rXcY = v
```

Update these related equations:

1. The row containing rXcY
2. The column containing rXcY
3. The 3x3 box containing rXcY
4. The cage containing rXcY

For each affected equation, compute:

```text
remaining_sum = target_sum - sum(known_values)
remaining_cells = cells that are still 0
used_digits = digits already placed in this equation
allowed_digits = {1,2,3,4,5,6,7,8,9} - used_digits
```

Then restrict candidates of remaining cells using:

1. Row restriction
2. Column restriction
3. Box restriction
4. Cage sum restriction
5. Non-repeating restriction

If a cell has only one candidate left, it is a forced placement.

If a digit can appear in only one cell of a row, column, box, or cage, it is a hidden single.

Do not stop after updating only one equation. Propagate the effects through all related equations.

---

## 2. Row Equations

Each row contains digits 1–9 exactly once, so each row sums to 45.

```text
R1: r1c1 + r1c2 + r1c3 + r1c4 + r1c5 + r1c6 + r1c7 + r1c8 + r1c9 = 45
R2: r2c1 + r2c2 + r2c3 + r2c4 + r2c5 + r2c6 + r2c7 + r2c8 + r2c9 = 45
R3: r3c1 + r3c2 + r3c3 + r3c4 + r3c5 + r3c6 + r3c7 + r3c8 + r3c9 = 45
R4: r4c1 + r4c2 + r4c3 + r4c4 + r4c5 + r4c6 + r4c7 + r4c8 + r4c9 = 45
R5: r5c1 + r5c2 + r5c3 + r5c4 + r5c5 + r5c6 + r5c7 + r5c8 + r5c9 = 45
R6: r6c1 + r6c2 + r6c3 + r6c4 + r6c5 + r6c6 + r6c7 + r6c8 + r6c9 = 45
R7: r7c1 + r7c2 + r7c3 + r7c4 + r7c5 + r7c6 + r7c7 + r7c8 + r7c9 = 45
R8: r8c1 + r8c2 + r8c3 + r8c4 + r8c5 + r8c6 + r8c7 + r8c8 + r8c9 = 45
R9: r9c1 + r9c2 + r9c3 + r9c4 + r9c5 + r9c6 + r9c7 + r9c8 + r9c9 = 45
```

---

## 3. Column Equations

Each column contains digits 1–9 exactly once, so each column sums to 45.

```text
C1: r1c1 + r2c1 + r3c1 + r4c1 + r5c1 + r6c1 + r7c1 + r8c1 + r9c1 = 45
C2: r1c2 + r2c2 + r3c2 + r4c2 + r5c2 + r6c2 + r7c2 + r8c2 + r9c2 = 45
C3: r1c3 + r2c3 + r3c3 + r4c3 + r5c3 + r6c3 + r7c3 + r8c3 + r9c3 = 45
C4: r1c4 + r2c4 + r3c4 + r4c4 + r5c4 + r6c4 + r7c4 + r8c4 + r9c4 = 45
C5: r1c5 + r2c5 + r3c5 + r4c5 + r5c5 + r6c5 + r7c5 + r8c5 + r9c5 = 45
C6: r1c6 + r2c6 + r3c6 + r4c6 + r5c6 + r6c6 + r7c6 + r8c6 + r9c6 = 45
C7: r1c7 + r2c7 + r3c7 + r4c7 + r5c7 + r6c7 + r7c7 + r8c7 + r9c7 = 45
C8: r1c8 + r2c8 + r3c8 + r4c8 + r5c8 + r6c8 + r7c8 + r8c8 + r9c8 = 45
C9: r1c9 + r2c9 + r3c9 + r4c9 + r5c9 + r6c9 + r7c9 + r8c9 + r9c9 = 45
```

---

## 4. Box Equations

Each 3x3 box contains digits 1–9 exactly once, so each box sums to 45.

```text
B1: r1c1 + r1c2 + r1c3 + r2c1 + r2c2 + r2c3 + r3c1 + r3c2 + r3c3 = 45
B2: r1c4 + r1c5 + r1c6 + r2c4 + r2c5 + r2c6 + r3c4 + r3c5 + r3c6 = 45
B3: r1c7 + r1c8 + r1c9 + r2c7 + r2c8 + r2c9 + r3c7 + r3c8 + r3c9 = 45

B4: r4c1 + r4c2 + r4c3 + r5c1 + r5c2 + r5c3 + r6c1 + r6c2 + r6c3 = 45
B5: r4c4 + r4c5 + r4c6 + r5c4 + r5c5 + r5c6 + r6c4 + r6c5 + r6c6 = 45
B6: r4c7 + r4c8 + r4c9 + r5c7 + r5c8 + r5c9 + r6c7 + r6c8 + r6c9 = 45

B7: r7c1 + r7c2 + r7c3 + r8c1 + r8c2 + r8c3 + r9c1 + r9c2 + r9c3 = 45
B8: r7c4 + r7c5 + r7c6 + r8c4 + r8c5 + r8c6 + r9c4 + r9c5 + r9c6 = 45
B9: r7c7 + r7c8 + r7c9 + r8c7 + r8c8 + r8c9 + r9c7 + r9c8 + r9c9 = 45
```

---

## 5. Cage Equations

Read the cage definitions dynamically from the current puzzle JSON.

Let:

```text
N = total number of cages
```

Then create:

```text
K1, K2, ..., KN
```

For each cage:

```text
sum(cells in cage) = cage_sum
all cells in that cage must be distinct
```

Example format:

```text
K1: r1c1 + r2c1 + r3c1 = 10
K2: r1c2 + r1c3 + r2c2 = 21
...
KN: ...
```

Do NOT assume a fixed number of cages.
When analyzing a cage, use `killer_sudoku_cheat_sheet_9x9.md` to find possible combinations.

Example:

```text
K2: r1c2 + r1c3 + r2c2 = 21
Possible 3-cell combinations:
489, 579, 678
```

Then combine with row, column, and box restrictions.

---

## 6. Cage Domain Analysis

For each important cage, write:

```text
Cage name:
Cells:
Sum:
Possible combinations:
Candidate digits per cell:
Reason for elimination:
```

Example:

```text
K6:
Cells: r1c9, r2c9
Sum: 16
Possible combinations: 79
Therefore:
r1c9 ∈ {7,9}
r2c9 ∈ {7,9}
```

---

## 7. Equation Interaction Analysis

Look for interactions between:

- Row equation and cage equation
- Column equation and cage equation
- Box equation and cage equation
- Multiple cages inside the same row/column/box
- Cage cells that share the same row, column, or box

Useful reasoning patterns:

### Pattern 1: Single Combination Cage

If a cage has only one possible combination, restrict all cells to that digit set.

Example:

```text
2-cell cage sum 16 → only 79
```

### Pattern 2: Missing Sum

If a row, column, or box has known digits, compute the remaining sum.

Example:

```text
Row total = 45
Known digits sum = 30
Remaining cells must sum to 15
```

### Pattern 3: Cage-Region Overlap

If part of a cage lies inside one row/column/box, compare its sum with the region total.

Example:

```text
Box total = 45
Known cages inside box contribute 32
Remaining cells in box must sum to 13
```

### Pattern 4: Distinctness

Inside every row, column, box, and cage:

```text
No repeated digits are allowed.
```

---

## 8. Candidate Elimination

For restricted cells, list candidates like this:

```text
r[x]c[y]: {candidates}
Reason:
- row restriction:
- column restriction:
- box restriction:
- cage restriction:
```

Example:

```text
r1c9: {7,9}
Reason:
- It belongs to a 2-cell cage with sum 16.
- The only valid combination is 79.
```

---

## 9. Forced Placement

Only place a digit if it is logically certain.

Valid reasons include:

- Naked single: a cell has only one candidate.
- Hidden single: a digit appears in only one possible cell in a row/column/box/cage.
- Cage completion: all but one cell in a cage are known.
- Equation completion: remaining cells have only one possible combination.
- Contradiction elimination: all other candidates lead to invalid sums or repeated digits.

Output format:

```json
{
  "placements": [
    {
      "cell": "r1c1",
      "value": 3,
      "reason": "Explain why this value is forced."
    }
  ]
}
```

---

## 10. No Guessing Rule

Do not guess.

If no certain move can be found, output:

```json
{
  "placements": [],
  "status": "NO_CERTAIN_MOVE",
  "reason": "No logically forced placement was found from the current constraints."
}
```

---

## 11. Final Check

A completed solution is valid only if:

- Every row contains digits 1–9 exactly once.
- Every column contains digits 1–9 exactly once.
- Every 3x3 box contains digits 1–9 exactly once.
- Every cage sums to its clue.
- No cage contains repeated digits.