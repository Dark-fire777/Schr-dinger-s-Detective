## P(correct accusation) vs tests used, 8 suspects (chance 0.125), greedy information-gain detective
| Evidence copies | K=1 | K=2 | K=3 | K=4 | K=5 | K=6 |
|---|---|---|---|---|---|---|
| 1 | 0.25 | 0.33 | 0.34 | 0.36 | 0.35 | 0.33 |
| 2 | 0.24 | 0.35 | 0.43 | 0.51 | 0.52 | 0.54 |
| 3 | 0.23 | 0.32 | 0.39 | 0.53 | 0.67 | 0.75 |
| 5 | 0.26 | 0.34 | 0.42 | 0.54 | 0.68 | 0.78 |
| inf (classical lab) | 0.26 | 0.29 | 0.43 | 0.52 | 0.67 | 0.76 |
| random tests, 1 copy | 0.19 | 0.22 | 0.26 | 0.26 | 0.29 | 0.29 |
| random tests, inf copies | 0.14 | 0.20 | 0.29 | 0.32 | 0.38 | 0.40 |

## Difficulty levels (greedy detective, final accuracy within budget)
| Level | Suspects | Copies | Tests | Accuracy |
|---|---|---|---|---|
| easy | 4 | 3 | 4 | 0.87 |
| medium | 8 | 3 | 5 | 0.65 |
| hard | 8 | 1 | 3 | 0.34 |

## Noise (2 copies, 4 tests)
| Readout flip prob | Accuracy |
|---|---|
| 0 | 0.55 |
| 0.02 | 0.50 |
| 0.05 | 0.44 |
| 0.1 | 0.43 |
| 0.2 | 0.27 |

| Depolarising p | Accuracy |
|---|---|
| 0 | 0.55 |
| 0.1 | 0.45 |
| 0.2 | 0.42 |
| 0.4 | 0.28 |
| 0.6 | 0.27 |