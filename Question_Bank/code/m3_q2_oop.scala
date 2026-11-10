// M3-Q2  Classes, constructors, overloading, inheritance, access modifiers, singleton, companion
class Account(val owner: String, private var balance: Double) {       // primary constructor
  def this(owner: String) = this(owner, 0.0)                          // auxiliary constructor (uses this(...))

  def deposit(amount: Double): Unit = { balance += amount }
  def deposit(amount: Double, note: String): Unit = {                 // method overloading: different parameters
    balance += amount
    println(s"  note: $note")
  }
  def current: Double = balance                                       // private var exposed read-only
  override def toString: String = f"Account($owner, $balance%.2f)"
}

// ---- inheritance, field overriding, final ----
class Animal {
  val sound: String = "..."
  def describe(): String = s"makes the sound '$sound'"
  final def kind(): String = "animal"                                 // final -> cannot be overridden
}
class Dog extends Animal {
  override val sound: String = "woof"                                 // field overriding needs `override`
  override def describe(): String = "A dog " + super.describe()
}

// ---- abstract class ----
abstract class Shape {
  def area: Double                                                    // abstract member
  def show(): String = f"${getClass.getSimpleName} area = $area%.2f"  // concrete member
}
class Circle(r: Double) extends Shape { def area: Double = math.Pi * r * r }
class Rect(w: Double, h: Double) extends Shape { def area: Double = w * h }

// ---- access modifiers ----
class Base {
  private val secret = "private"             // visible only inside Base
  protected val shared = "protected"         // Base and subclasses
  val open = "public"                        // everywhere (default)
  def reveal: String = secret
}
class Child extends Base { def peek: String = shared }

// ---- singleton object and companion object with apply ----
object Config { val appName = "PDS Demo"; def hello(): String = s"Welcome to $appName" }  // singleton

class Student private (val name: String, val id: Int)                 // private constructor
object Student {                                                      // companion: same name, same file
  private var count = 0
  def apply(name: String, id: Int): Student = { count += 1; new Student(name, id) }  // factory
  def created: Int = count
}

object M3Q2 extends App {
  val a = new Account("Asha")                  // auxiliary constructor
  a.deposit(500)
  a.deposit(250, "salary")                     // overloaded version
  println(a)

  val d = new Dog
  println(d.describe() + " | kind = " + d.kind())

  val shapes: List[Shape] = List(new Circle(1.5), new Rect(2, 3))
  shapes.foreach(s => println(s.show()))

  val c = new Child
  println(s"${c.peek}, ${c.open}, ${c.reveal}")
  // c.secret  // would not compile: value secret in class Base cannot be accessed

  println(Config.hello())                      // singleton: no `new`, one instance
  val s1 = Student("Rohan", 101)               // companion apply: no `new`
  val s2 = Student("Meena", 102)
  println(s"${s1.name}, ${s2.name}, created = ${Student.created}")

  // anonymous class: an instance of a one-off subclass
  val cat = new Animal { override val sound = "meow" }
  println("anonymous: " + cat.describe())
}
