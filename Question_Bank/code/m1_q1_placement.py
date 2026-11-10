"""M1-Q1  Campus Placement Shortlisting
Topics: conditionals, dict/tuple/set, set operations, priority queue (heapq),
string handling, custom exception, file handling.
"""
import heapq
import re

# --- 1. Data kept in built-in structures --------------------------------
# dict keyed by roll no (fast lookup); each record is a tuple (fixed, read-only)
students = {
    "26AIM1001": ("Ananya Rao", 8.6, 0),
    "26AIM1002": ("Rahul Verma", 7.8, 1),
    "26CSE1003": ("Sneha Iyer", 9.1, 0),
    "26DSC1004": ("Kabir Shah", 7.2, 0),
    "26ECE1005": ("Meera Nair", 8.2, 0),
}
# company -> (minimum CGPA, openings)
companies = {
    "TechNova": (8.0, 2),
    "DataWorks": (7.5, 1),
    "CloudSys": (7.0, 3),
}


class CompanyNotFoundError(Exception):
    """Raised when a company is not in the dataset."""


# --- 2. Eligibility with conditionals -> sets ---------------------------
def eligible_set(company):
    if company not in companies:
        raise CompanyNotFoundError(f"'{company}' is not in the dataset")
    min_cgpa, _ = companies[company]
    result = set()
    for roll, (name, cgpa, backlogs) in students.items():
        if cgpa >= min_cgpa and backlogs == 0:   # eligibility rule
            result.add(roll)
    return result


eligible = {c: eligible_set(c) for c in companies}
print("Eligible sets")
for c, s in eligible.items():
    print(f"  {c:<10}: {sorted(s)}")

# --- 3. Set operations --------------------------------------------------
all_students = set(students)
in_all = set.intersection(*eligible.values())
in_any = set.union(*eligible.values())
in_none = all_students - in_any
cloud_only = eligible["CloudSys"] - eligible["TechNova"] - eligible["DataWorks"]
print("\nEligible for all three :", sorted(in_all))
print("Eligible for none      :", sorted(in_none))
print("CloudSys only          :", sorted(cloud_only))


# --- 4. Priority queue (highest CGPA first) -----------------------------
def shortlist(company):
    _, openings = companies[company]
    heap = []
    for roll in eligible_set(company):
        cgpa = students[roll][1]
        heapq.heappush(heap, (-cgpa, roll))      # heapq is a min-heap -> negate
    chosen = []
    while heap and len(chosen) < openings:
        neg_cgpa, roll = heapq.heappop(heap)
        chosen.append((roll, students[roll][0], -neg_cgpa))
    return chosen


shortlists = {c: shortlist(c) for c in companies}
print("\nShortlists (top CGPA, limited to openings)")
for c, rows in shortlists.items():
    print(f"  {c} ({companies[c][1]} openings):")
    for roll, name, cgpa in rows:
        print(f"     {roll}  {name:<12} {cgpa}")


# --- 5. String handling: validate roll no and extract branch ------------
def validate_roll(roll):
    """2 digits + 3 letters + 4 digits. Returns branch code or None."""
    roll = roll.strip().upper()
    if len(roll) == 9 and roll[:2].isdigit() and roll[2:5].isalpha() and roll[5:].isdigit():
        return roll[2:5]
    return None


print("\nRoll number validation")
for r in list(students) + ["2AIM1001", "26AI1001X", "26aim1006"]:
    branch = validate_roll(r)
    print(f"  {r:<10} -> {'valid, branch ' + branch if branch else 'INVALID'}")

# the same check with a regular expression
pattern = re.compile(r"^\d{2}[A-Za-z]{3}\d{4}$")
assert all(pattern.match(r) for r in students)

# --- 6. Exception handling ----------------------------------------------
print("\nQuery handling")
for query in ["TechNova", "Zoho"]:
    try:
        names = [students[r][0] for r in sorted(eligible_set(query))]
    except CompanyNotFoundError as err:
        print(f"  Error: {err}")
    else:
        print(f"  {query}: eligible = {names}")
    finally:
        print("  (query finished)")

# --- 7. File handling: write, then read back ----------------------------
with open("shortlists.txt", "w", encoding="utf-8") as f:
    for c, rows in shortlists.items():
        f.write(f"{c}\n")
        for roll, name, cgpa in rows:
            f.write(f"  {roll},{name},{cgpa}\n")

print("\nContents of shortlists.txt")
with open("shortlists.txt", "r", encoding="utf-8") as f:
    print(f.read(), end="")
