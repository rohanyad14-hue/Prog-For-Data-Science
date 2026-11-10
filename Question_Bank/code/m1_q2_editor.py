"""M1-Q2  Text editor with undo / redo using two stacks.
Topics: OOP, stack (list), string slicing, exceptions, file handling.
"""


class EditorError(Exception):
    """Any editor-level problem (bad delete length, nothing to undo, file issue)."""


class TextEditor:
    def __init__(self):
        self._text = ""
        self._undo = []     # stack of operations already done
        self._redo = []     # stack of operations that were undone

    @property
    def text(self):
        return self._text

    # ---- primitive actions (also used by undo / redo) ----
    def _apply(self, op, data):
        if op == "T":                      # type
            self._text += data
        else:                              # "D": delete -> data is the removed text
            self._text = self._text[: len(self._text) - len(data)]

    def _reverse(self, op, data):
        if op == "T":
            self._text = self._text[: len(self._text) - len(data)]
        else:
            self._text += data

    # ---- public operations ----
    def type_text(self, s):
        self._apply("T", s)
        self._undo.append(("T", s))
        self._redo.clear()                 # a new edit invalidates the redo history

    def delete(self, n):
        if n < 0 or n > len(self._text):
            raise EditorError(f"cannot delete {n} characters from a text of length {len(self._text)}")
        removed = self._text[len(self._text) - n:] if n else ""
        self._apply("D", removed)
        self._undo.append(("D", removed))
        self._redo.clear()

    def undo(self):
        if not self._undo:
            raise EditorError("nothing to undo")
        op, data = self._undo.pop()
        self._reverse(op, data)
        self._redo.append((op, data))

    def redo(self):
        if not self._redo:
            raise EditorError("nothing to redo")
        op, data = self._redo.pop()
        self._apply(op, data)
        self._undo.append((op, data))

    # ---- file handling ----
    def save(self, path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self._text)
        except OSError as err:
            raise EditorError(f"could not save '{path}': {err.strerror}") from err

    def load(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                self._text = f.read()
        except FileNotFoundError as err:
            raise EditorError(f"file '{path}' not found") from err
        self._undo.clear()
        self._redo.clear()

    def snapshot(self):
        return repr(self._text), self._undo[:], self._redo[:]


if __name__ == "__main__":
    ed = TextEditor()
    steps = [
        ('type("Hello")', lambda: ed.type_text("Hello")),
        ('type(" World")', lambda: ed.type_text(" World")),
        ("delete(5)", lambda: ed.delete(5)),
        ("undo()", ed.undo),
        ("undo()", ed.undo),
        ("redo()", ed.redo),
    ]
    print(f"{'step':<16}{'text':<16}undo stack / redo stack")
    for label, action in steps:
        action()
        text, undo, redo = ed.snapshot()
        print(f"{label:<16}{text:<16}{undo}  /  {redo}")

    print("\nException handling")
    for label, action in [("delete(50)", lambda: ed.delete(50)),
                          ("load('missing.txt')", lambda: ed.load("missing.txt"))]:
        try:
            action()
        except EditorError as err:
            print(f"  {label}: EditorError - {err}")

    ed.save("note.txt")
    ed2 = TextEditor()
    ed2.load("note.txt")
    print("\nsaved and reloaded:", repr(ed2.text))
