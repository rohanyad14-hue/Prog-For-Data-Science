"""Helpers for the notes documents: pick sections out of captured demo output."""

HEADER_STARTS = ("---", "===", "STEP", "CHECK")


def pick(*markers, drop=()):
    """Return a transform that keeps only the output sections whose header line contains one of `markers`.
    Lines that start with any string in `drop` are removed (used to hide dependency start-up noise)."""
    def f(text):
        sections, current = [], None
        for line in text.split("\n"):
            if line.startswith(HEADER_STARTS):
                current = [line]
                sections.append(current)
            elif current is not None:
                current.append(line)
        keep = ["\n".join(s).rstrip() for s in sections if any(m in s[0] for m in markers)]
        out = "\n\n".join(keep)
        return "\n".join(l for l in out.split("\n") if not l.startswith(drop)) if drop else out
    return f


NOISE = ("trying to return java", "return java 11 instance")


def between(start, end):
    """Transform: keep the lines from the first one containing `start` to the first later one containing `end`."""
    def f(text):
        lines = text.split("\n")
        a = next(i for i, l in enumerate(lines) if start in l)
        b = next(i for i, l in enumerate(lines) if end in l and i >= a)
        return "\n".join(lines[a:b + 1])
    return f
