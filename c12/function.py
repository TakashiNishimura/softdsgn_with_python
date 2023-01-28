from typing import List


def mean(values: List[int]) -> float:
    return sum(values) / len(values)


def std(values: List[int]) -> float:
    total = 0
    m = mean(values)
    for i in values:
        total = i - m
    return total / len(values)
