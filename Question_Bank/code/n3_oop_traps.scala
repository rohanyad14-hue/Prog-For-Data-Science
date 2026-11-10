// Notes M3: object-oriented Scala - initialisation order, overriding, sealed hierarchies, extractors, companions (Scala 2.13)

// ---- initialisation order trap: a superclass constructor calls an overridden val ----
class Base {
  val name: String = "base"
  println(s"  Base constructor sees name = $name | name.length -> " +
    scala.util.Try(name.length).fold(e => e.getClass.getSimpleName, n => n.toString))
}
class Derived extends Base {
  override val name: String = "derived"
}
class SafeBase {
  def name: String = "base"                       // def instead of val: resolved at call time
  println(s"  SafeBase constructor sees name = $name")
}
class SafeDerived extends SafeBase { override def name: String = "derived" }

// ---- constructors, val/var parameters, auxiliary constructors, this ----
class Point(val x: Int, var y: Int, tag: String) {   // x: read-only field, y: read/write field, tag: plain parameter (private[this] if used)
  def this(x: Int) = this(x, 0, "aux")               // auxiliary: first statement must call another constructor
  def describe = s"Point($x,$y,$tag)"
  def moveTo(nx: Int, ny: Int): this.type = { this.y = ny; this }   // returning this enables chaining
}

// ---- sealed hierarchy gives exhaustive matching; case object as an enumeration ----
sealed trait Shape
case class Circle(r: Double) extends Shape
case class Rect(w: Double, h: Double) extends Shape
case object Dot extends Shape

// ---- custom extractor (unapply) and companion with private constructor ----
object Even { def unapply(n: Int): Option[Int] = if (n % 2 == 0) Some(n / 2) else None }
class Secret private (val code: Int)
object Secret { def apply(c: Int): Secret = new Secret(c * 2); def peek(s: Secret): Int = s.code }

// ---- override / super / abstract members ----
abstract class Animal(val name: String) {
  def sound: String                                        // abstract
  def intro: String = s"$name says $sound"                  // concrete, uses the abstract member
}
class Dog(n: String) extends Animal(n) { def sound = "woof" }
class Puppy(n: String) extends Dog(n) { override def sound = super.sound + " (squeaky)" }

// ---- stackable traits ----
trait Greeter { def greet(s: String): String = "Hello " + s }
trait Loud extends Greeter { override def greet(s: String): String = super.greet(s).toUpperCase }
trait Polite extends Greeter { override def greet(s: String): String = super.greet(s) + ", please" }

case class Team(name: String, members: Array[String])

object N3Oop extends App {
  println("--- initialisation order ---")
  val d = new Derived
  println("  after construction: d.name = " + d.name)
  new SafeDerived

  println("\n--- constructors ---")
  val p = new Point(1, 2, "t")
  p.y = 5
  println("  " + p.describe + " | aux constructor: " + new Point(7).describe + " | chaining: " + p.moveTo(0, 0).moveTo(1, 1).describe)
  println("  p.x = " + p.x + " (val is a read-only field); p.tag does not compile: tag is just a constructor parameter")

  println("\n--- sealed + case classes ---")
  def area(s: Shape): Double = s match {
    case Circle(r)  => math.Pi * r * r
    case Rect(w, h) => w * h
    case Dot        => 0.0
  }
  println("  areas: " + List(Circle(1), Rect(2, 3), Dot).map(area(_)).map(a => f"$a%.2f"))
  println("  case object equality: " + (Dot == Dot) + " | toString: " + Dot)

  println("\n--- case class: equality, copy, arrays inside ---")
  val c1 = Circle(2); val c2 = c1.copy()
  println("  c1 == c2: " + (c1 == c2) + " | c1 eq c2: " + (c1 eq c2) + " | hashCode equal: " + (c1.hashCode == c2.hashCode))
  val t1 = Team("A", Array("x", "y")); val t2 = Team("A", Array("x", "y"))
  println("  Team(A, Array(..)) == same data: " + (t1 == t2) + " (the Array field is compared by reference)")
  val shallow = t1.copy(name = "B")
  println("  copy is shallow, shares the array: " + (shallow.members eq t1.members))

  println("\n--- extractors and companions ---")
  println("  " + List(10, 7).map { case Even(h) => s"even, half is $h"; case n => s"odd $n" })
  println("  Secret(21) code = " + Secret.peek(Secret(21)) + " (companion may call the private constructor; `new Secret(1)` outside does not compile)")

  println("\n--- overriding and super ---")
  println("  " + new Dog("Rex").intro + " | " + new Puppy("Bit").intro)
  val a: Animal = new Puppy("Bit")
  println("  static type Animal, dynamic dispatch picks Puppy.sound: " + a.sound + " | isInstanceOf[Dog]: " + a.isInstanceOf[Dog])

  println("\n--- trait mixin order changes behaviour ---")
  val g1 = new Greeter with Loud with Polite
  val g2 = new Greeter with Polite with Loud
  println("  Loud with Polite : " + g1.greet("asha") + "   (Polite is outermost: Loud upper-cases first, then Polite appends)")
  println("  Polite with Loud : " + g2.greet("asha") + "   (Loud is outermost: it upper-cases everything Polite produced)")
}
