"""Answers to the five Module 3 sample questions (Scala object-oriented programming and collections)."""
from dsl import B, CODE, H3, H4, KEY, NOTE, OUT, P, T, TIP, WARN

QUESTIONS = []


def question(qid, title, image, blocks):
    QUESTIONS.append(dict(id=qid, module=3, title=title, image=image, blocks=blocks))


# ------------------------------------------------------------------------------------------------ Q1
question("M3-Q1", "Student Course Registration System", "6271407831856650886.jpg", [
    H3("Answer"),
    H4("Design in one picture"),
    T(["Part", "Scala feature", "Role"], [
        ["`abstract class Student(id, name, dept, initialCourses)`", "class, primary constructor, abstract members", "common fields and the add / remove / search rules"],
        ["`UGStudent`, `PGStudent`", "inheritance, auxiliary constructor, default argument", "supply `maxCourses` and `level`; PG adds `thesisTopic`"],
        ["`addCourse(String)` and `addCourse(List[String])`", "method overloading", "add one course or several at once"],
        ["`Registry.find(Int)` and `Registry.find(String)`", "singleton object, overloading", "search by id or by name"],
        ["`private var registered: List[String]`", "encapsulation", "outsiders get the list through `courses`, they cannot change it"]], [0.38, 0.30, 0.32]),
    H4("Why this choice of data structure?"),
    T(["Structure", "Fits this problem?", "Reason"], [
        ["`Array[String]`", "no", "fixed size: adding or removing a course means building a new array; elements can be changed from outside"],
        ["<b>`List[String]` (chosen)</b>", "<b>yes</b>", "a student has at most 4 to 6 courses, so the O(n) append does not matter; it is immutable, so it can be handed out safely and gives the clean copy semantics of functional code"],
        ["`ListBuffer[String]`", "yes, for heavy editing", "fast in-place add and remove, but mutable state leaks if exposed"],
        ["`Set[String]`", "partly", "removes duplicates automatically but loses the order of registration; here `contains` plus `distinct` do the same"],
        ["`Map[Int, Student]` for the registry", "yes at scale", "O(1) lookup by id; the demo uses a `ListBuffer` scan because there are three students"]], [0.26, 0.18, 0.56]),
    H4("How does inheritance differentiate Undergraduate and Postgraduate students?"),
    B(["The base class holds everything that is the same (fields, `addCourse`, `removeCourse`, `hasCourse`) and declares what differs as <b>abstract</b> members: `maxCourses` and `level`.",
       "`UGStudent` says `maxCourses = 6`, `level = \"UG\"`. `PGStudent` says `maxCourses = 4`, `level = \"PG\"` and adds a `thesisTopic`.",
       "<b>Polymorphism</b>: the same call `student.addCourse(...)` obeys the limit of the real class. In the output Arun (UG) accepts 3 of 4 new courses because he reaches 6, Priya (PG) accepts 2 of 3 because she reaches 4.",
       "`maxCourses` is a `def`, not a `val`: a parent constructor that reads an overridden `val` sees 0 (initialisation-order trap), a `def` is always safe."]),
    NOTE("The question does not say which student is UG or PG. The code treats Arun and Rahul as undergraduates and Priya as a postgraduate."),
    H3("Code, run on the dataset of the question"),
    CODE("sa_m3_q1.scala", "Code: code/sa_m3_q1.scala"),
    OUT("sa_m3_q1.out.txt", "Real output"),
])

# ------------------------------------------------------------------------------------------------ Q2
question("M3-Q2", "Smart Library Management System", "6271407831856650919.jpg", [
    H3("Answer"),
    H4("Class hierarchy with inheritance, an abstract class and field overriding"),
    B(["`abstract class LibraryResource(id, title, initialStatus)` holds what every resource has: id, title, a private `status`, and the rules `issue()` and `giveBack()`.",
       "It declares two abstract members that each subclass must supply: the field `kind` and the method `loanDays`.",
       "It also has a concrete field with a default, `lateFeePerDay = 1.0`. <b>Field overriding</b>: `Journal` replaces it with 5.0 and `Magazine` with 0.5 using `override val`.",
       "`Book` (14 days), `Journal` (7 days), `Magazine` (3 days) extend it. Adding a `Newspaper` later means one new small class and no change to the library code."]),
    H4("How does polymorphism issue and return different resource types?"),
    P("The library keeps one `List[LibraryResource]` and calls `r.issue()` or `r.giveBack(2)` on each element. The compiler only knows the type `LibraryResource`, the JVM picks the real class at run time, so each object uses its own `kind`, `loanDays` and `lateFeePerDay`. In the output the same call prints \"issued for 14 days\" for the book and \"issued for 3 days\" for the magazine, and the same 2 days of delay costs Rs. 2.00, Rs. 10.00 and Rs. 1.00. The journal, which starts as \"Issued\" in the data, answers \"is not available\": its status is checked by the shared code."),
    H4("Where should the `final` keyword be applied?"),
    T(["Place", "Example", "Justification"], [
        ["Methods that carry a business rule", "`final def issue()`, `final def giveBack()`", "every resource must follow the same rule; a subclass must not weaken it (for example issue an item without checking its status)"],
        ["Classes not designed for extension", "`final class Magazine`", "prevents unexpected subclasses and lets the compiler optimise"],
        ["Constants", "`final val MaxRenewals = 2`", "cannot be shadowed or changed by a subclass"],
        ["<b>Not</b> on customisation points", "`loanDays`, `lateFeePerDay`, the abstract members", "they exist precisely so that subclasses can supply or override them"]], [0.26, 0.30, 0.44]),
    P("What the compiler says when the rules are broken (two small programs that are meant to fail):"),
    OUT("sa_m3_q2_final_error.out.txt", "Overriding a final method"),
    OUT("sa_m3_q2_final_class_error.out.txt", "Extending a final class"),
    TIP("Over-using `final` makes a library hard to extend and hard to test. Protect rules and invariants, leave behaviour open."),
    H3("Code, run on the dataset of the question"),
    CODE("sa_m3_q2.scala", "Code: code/sa_m3_q2.scala"),
    OUT("sa_m3_q2.out.txt", "Real output"),
])

# ------------------------------------------------------------------------------------------------ Q3
question("M3-Q3", "Online Shopping Cart Analysis", "6271407831856650920.jpg", [
    H3("Answer"),
    T(["Task", "Functional combinator", "Result"], [
        ["10% discount on all products", "`prices.map { case (item, p) => item -> p * 0.9 }`", "Laptop 58500, Mobile 22500, Tablet 16200, Headphone 2700"],
        ["Products costing more than Rs. 20,000", "`prices.filter { case (_, p) => p > 20000 }`", "Laptop, Mobile"],
        ["Total inventory value (one unit of each)", "`prices.values.reduce(_ + _)`", "111,000 (99,900 after the discount)"]], [0.28, 0.44, 0.28]),
    P("The three steps chain into one readable pipeline, for example `prices.filter(_._2 > 20000).map { case (i, p) => i -> p * 0.9 }.values.sum` (the discounted value of the expensive products, 81,000)."),
    H4("Imperative versus functional, and which is more scalable"),
    T(["", "Imperative (loop and variables)", "Functional (combinators)"], [
        ["State", "mutable `var total`, a mutable map that is filled in place", "nothing is changed; every step returns a new value"],
        ["Reading", "how to do it, step by step", "what is wanted: map, filter, reduce"],
        ["Testing", "depends on the order of the statements", "each step is a pure function and can be tested alone"],
        ["Running in parallel", "shared mutable state needs locks, otherwise race conditions", "no shared state, so the work splits into chunks safely"],
        ["Moving to a cluster", "must be rewritten", "the same `map` / `filter` / `reduce` vocabulary is the API of Spark RDDs"]], [0.16, 0.42, 0.42]),
    P("<b>Justification:</b> the functional version is more scalable. It has no shared mutable state, so the collection can be split into parts, each part processed independently and the partial results combined, which is exactly how parallel collections and Spark work. The imperative version is perfectly fine for a small local loop; it is the mutation that does not scale. Both versions give identical answers in the output (`same answers: true`)."),
    WARN("`reduce` has no starting value and throws on an empty collection (the real message is \"empty.reduceLeft\"). `foldLeft(0)(_ + _)` returns 0. Use `foldLeft` when the collection can be empty."),
    NOTE("Prices are Int and the discount is applied as `p * 0.9` (Double). For real money use `BigDecimal` and round, because Double arithmetic can give results such as 60500.00000000001."),
    H3("Code, run on the dataset of the question"),
    CODE("sa_m3_q3.scala", "Code: code/sa_m3_q3.scala"),
    OUT("sa_m3_q3.out.txt", "Real output"),
])

# ------------------------------------------------------------------------------------------------ Q4
question("M3-Q4", "Employee Management using Case Classes and Companion Objects", "6271407831856650921.jpg", [
    H3("Answer, point by point"),
    H4("Why are case classes suitable for employee records?"),
    B(["An employee record is a <b>value</b>: defined by its fields, not by identity. A case class gives value semantics for free: `equals` / `hashCode` compare the fields (`Employee(101, ...) == Employee(101, ...)` is true), `toString` prints `Employee(101,Ravi,Developer,75000.0)`.",
       "Fields are immutable `val`s, so a record cannot change under your feet; a changed copy is made with `copy(salary = 80000)`.",
       "No `new` needed (generated `apply`), and the generated `unapply` allows <b>pattern matching</b> on the fields: `case Employee(_, n, \"Manager\", s) if s > 90000 => ...`.",
       "Caution: do not put mutable fields into a case class and avoid case-class inheritance."]),
    H4("How can companion objects create utility methods?"),
    P("A companion is an `object` with the same name in the same file. It holds everything that belongs to the concept `Employee` but not to one employee: the constant `MinSalary`, the factory `fromCsv(line): Option[Employee]` that parses and validates a text line, `raise(e, percent)` and `totalPayroll(list)`. In the output `fromCsv` accepts a good line and returns `None` for a salary below the minimum and for malformed lines. The class and its companion can see each other's private members."),
    H4("How do access modifiers improve data security?"),
    T(["Modifier", "Visible to", "Use in this design"], [
        ["(none) = public", "everyone", "the case-class fields and the public methods"],
        ["`private`", "only the enclosing class or object (and its companion)", "`taxRate` and `net()` inside `PayrollReport`: the tax rule cannot be read or called from outside"],
        ["`protected`", "the class and its subclasses", "helper methods meant for subclasses"],
        ["`private[this]`", "only the same instance", "per-object internal state"]], [0.22, 0.34, 0.44]),
    P("Hiding the details means other code can only use the safe public methods, so rules (validation, rounding, tax) live in one place. Trying to touch a private member is a compile error, not a run-time surprise (this file is meant to fail):"),
    OUT("sa_m3_q4_private_error.out.txt", "Reading a private member from outside"),
    H4("How can singleton objects generate employee reports?"),
    P("`object PayrollReport` has exactly one instance, created lazily and thread-safely by the JVM, and is called as `PayrollReport.generate(staff)` without `new`. It is the right shape for a stateless service such as a report generator or a utility: no object has to be passed around, and its private helpers stay hidden. The output shows the gross and net salary of each employee, the total payroll (225,000), the average (75,000) and the highest paid employee (Kiran)."),
    H3("Code, run on the dataset of the question"),
    CODE("sa_m3_q4.scala", "Code: code/sa_m3_q4.scala"),
    OUT("sa_m3_q4.out.txt", "Real output"),
])

# ------------------------------------------------------------------------------------------------ Q5
question("M3-Q5", "Smart Transportation Monitoring System", "6271407831856650922.jpg", [
    H3("Answer, point by point"),
    H4("How do traits and mixins allow code reuse?"),
    P("A trait packages behaviour (methods, fields, abstract members) that unrelated classes can reuse without sharing a parent class. `EmergencyService` (the `siren`), `PassengerVehicle` (`seats`, `boarding`) and `HighSpeedVehicle` (a higher speed `limit`) are written once and attached to the classes that need them, instead of being copied into `Ambulance`, `FireEngine`, `Bus` and `Car`. A mixin is such an attachment: `class Ambulance(...) extends Vehicle(...) with EmergencyService with HighSpeedVehicle`, or at creation time: `new Car(80) with EmergencyService with HighSpeedVehicle`."),
    H4("How can multiple traits be combined in one class?"),
    B(["List them after the superclass with `with`: `extends Vehicle(\"Ambulance\", speed) with EmergencyService with HighSpeedVehicle`. A class has one parent class but any number of traits.",
       "When two traits define the same member, <b>linearisation</b> decides: the trait mixed in last wins. `HighSpeedVehicle` overrides `limit` (60 becomes 100), so Ambulance at 90 km/h is \"ok\" while Car at 70 km/h is \"OVERSPEED\".",
       "Traits in Scala 2 have no constructor parameters; traits can extend a class (here `Vehicle`), which restricts them to subclasses of it.",
       "Abstract class or trait? Use a trait for a reusable capability, an abstract class for the one \"is-a\" parent (`Vehicle`)."]),
    H4("How can arrays and collections be used for real-time monitoring?"),
    B(["The question's `Array((\"Bus\", 45), ...)` is turned into an `Array[Vehicle]` with one `map` and a small factory (`build`).",
       "Monitoring is then collection code: `filter(_.status == \"OVERSPEED\")`, `maxBy(_.speed)`, average speed, `collect { case v: EmergencyService => v.name }` to find the emergency vehicles. In the output only the car is overspeeding, the ambulance is the fastest, the average is 70.0 km/h.",
       "For a live feed the array is replaced each second (or the logic moves to Spark Streaming); the monitoring functions stay the same because they are written against `Vehicle`."]),
    H4("How can the REPL be used to test the solution interactively?"),
    P("Start it with `scala` (or `scala-cli repl`), type definitions and expressions and read the type and value immediately; `:quit` leaves. Below is a real session (the lines after each `scala>` prompt were typed, the others are the REPL's answers). It checks the trait in isolation, mixes it into one object, and tries the array logic before it goes into the program. Unnamed results are called `res0`, `res1`, ... and an assignment such as `fleet(0) = ...` also uses up a number although it prints nothing."),
    OUT("sa_m3_q5_repl.out.txt", "A Scala REPL session (real transcript)"),
    H3("Code, run on the dataset of the question"),
    CODE("sa_m3_q5.scala", "Code: code/sa_m3_q5.scala"),
    OUT("sa_m3_q5.out.txt", "Real output"),
])
