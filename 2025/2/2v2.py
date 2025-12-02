from typing import Iterable

def chunks_equal(s: str, chunk_size: int) -> bool:
    """Return True if s can be split into equal chunks of size chunk_size."""
    if len(s) % chunk_size:
        return False
    first = s[:chunk_size]
    for i in range(chunk_size, len(s), chunk_size):
        if s[i:i+chunk_size] != first:
            return False
    return True

def has_half_repeat(s: str) -> bool:
    """Part 1: length even and first half equals second half."""
    L = len(s)
    if L % 2:
        return False
    half = L // 2
    return s[:half] == s[half:]

def has_any_repeat(s: str) -> bool:
    """Part 2: exists chunk size dividing length where all chunks equal.
    Try larger chunk sizes first for earlier short-circuiting."""
    L = len(s)
    # iterate chunk sizes from largest to smallest
    for size in range(L // 2, 0, -1):
        if chunks_equal(s, size):
            return True
    return False

def parse_ranges(text: str) -> Iterable[tuple[int,int]]:
    for part in text.strip().split(','):
        a, b = part.split('-')
        yield int(a), int(b)

def sum_matching(input_text: str, predicate) -> int:
    total = 0
    for a, b in parse_ranges(input_text):
        for n in range(a, b + 1):
            s = str(n)
            if predicate(s):
                total += n
    return total

if __name__ == "__main__":
    with open("input.txt") as f:
        inp = f.read()

    print(sum_matching(inp, has_half_repeat))
    print(sum_matching(inp, has_any_repeat))
