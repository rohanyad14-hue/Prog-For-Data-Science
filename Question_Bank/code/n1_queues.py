"""Notes M1: stack, queue and priority queue in Python."""
import heapq
import itertools
import queue
import timeit
from collections import deque

print("--- stack (LIFO) ---")
stack = []
for x in (1, 2, 3):
    stack.append(x)                      # push
print("peek:", stack[-1], "| pop:", stack.pop(), "| now:", stack)
def balanced(text):
    pairs, st = {")": "(", "]": "[", "}": "{"}, []
    for ch in text:
        if ch in "([{":
            st.append(ch)
        elif ch in pairs:
            if not st or st.pop() != pairs[ch]:
                return False
    return not st
print("balanced:", [balanced(s) for s in ("{[()]}", "([)]", "((", "")])

print("\n--- queue (FIFO) with deque ---")
q = deque([1, 2, 3])
q.append(4)
print("popleft:", q.popleft(), "| now:", list(q))
q.rotate(1)
print("rotate(1):", list(q))
last3 = deque(maxlen=3)
for i in range(6):
    last3.append(i)
print("deque(maxlen=3) keeps the newest:", list(last3))
lst = list(range(100000)); dq = deque(lst)
t1 = timeit.timeit(lambda: lst.pop(0) if lst else None, number=20000)
t2 = timeit.timeit(lambda: dq.popleft() if dq else None, number=20000)
print(f"20000 removals from the front: list.pop(0) {t1*1000:.1f} ms, deque.popleft() {t2*1000:.2f} ms")

print("\n--- library queues ---")
fifo, lifo, pq = queue.Queue(), queue.LifoQueue(), queue.PriorityQueue()
for x in (3, 1, 2):
    fifo.put(x); lifo.put(x); pq.put(x)
print("Queue:", [fifo.get() for _ in range(3)], "| LifoQueue:", [lifo.get() for _ in range(3)],
      "| PriorityQueue:", [pq.get() for _ in range(3)], "(thread-safe versions)")

print("\n--- priority queue with heapq ---")
data = [5, 3, 8, 1, 9, 2]
heapq.heapify(data)
print("heap list is NOT sorted:", data, "| data[0] is the minimum:", data[0])
heapq.heappush(data, 0)
print("pop order:", [heapq.heappop(data) for _ in range(len(data))])
print("nlargest(2):", heapq.nlargest(2, [5, 3, 8, 1, 9, 2]), "| nsmallest(2):", heapq.nsmallest(2, [5, 3, 8, 1, 9, 2]))
mx = []
for v in (5, 3, 8):
    heapq.heappush(mx, -v)
print("max-heap by negating:", -heapq.heappop(mx))

print("\n--- tie-breaking and non-comparable items ---")
h = []
heapq.heappush(h, (1, "task A"))
heapq.heappush(h, (1, "task B"))
print("equal priority falls back to the next field:", heapq.heappop(h))
class Job:
    def __init__(self, n): self.n = n
h3 = []
try:
    heapq.heappush(h3, (1, Job(1)))
    heapq.heappush(h3, (1, Job(2)))          # tie on priority -> Python compares the Job objects
except TypeError as err:
    print("same priority + objects without ordering ->", err)
counter = itertools.count()
h2 = []
for prio, name in [(2, "routine 1"), (1, "urgent 1"), (2, "routine 2"), (1, "urgent 2")]:
    heapq.heappush(h2, (prio, next(counter), Job(name)))
print("with a counter, order is priority then arrival:", [heapq.heappop(h2)[2].n for _ in range(4)])
print("\ncost: heappush/heappop O(log n), peek O(1), heapify O(n)")


print("\n--- user-defined classes (the usual exam question) ---")
class Stack:
    def __init__(self): self._data = []
    def push(self, x): self._data.append(x)
    def pop(self):
        if not self._data:
            raise IndexError("pop from empty stack")
        return self._data.pop()
    def peek(self):
        if not self._data:
            raise IndexError("peek at empty stack")
        return self._data[-1]
    def is_empty(self): return not self._data
    def __len__(self): return len(self._data)

class Queue:
    def __init__(self): self._data = deque()
    def enqueue(self, x): self._data.append(x)
    def dequeue(self):
        if not self._data:
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()
    def is_empty(self): return not self._data
    def __len__(self): return len(self._data)

class PriorityQueue:
    """Smaller number = higher priority; the counter keeps first-come-first-served among equals."""
    def __init__(self): self._h, self._c = [], itertools.count()
    def push(self, item, priority): heapq.heappush(self._h, (priority, next(self._c), item))
    def pop(self):
        if not self._h:
            raise IndexError("pop from empty priority queue")
        return heapq.heappop(self._h)[2]
    def __len__(self): return len(self._h)

s = Stack(); [s.push(i) for i in (1, 2, 3)]
print("Stack: pop ->", s.pop(), "| peek ->", s.peek(), "| len ->", len(s))
qq = Queue(); [qq.enqueue(i) for i in "abc"]
print("Queue: dequeue ->", qq.dequeue(), "| len ->", len(qq))
pqq = PriorityQueue(); pqq.push("print report", 3); pqq.push("fix outage", 1); pqq.push("reset password", 2); pqq.push("fix leak", 1)
print("PriorityQueue pops:", [pqq.pop() for _ in range(4)])
try:
    Stack().pop()
except IndexError as err:
    print("empty stack ->", err)
