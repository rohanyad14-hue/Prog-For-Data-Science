//> using scala 2.13.12
// OOP in Scala, one section per concept (the Python twin is oops_py.py). Run: scala-cli run oops_scala.scala
// build_oops.py cuts this file at the 'def sN()' lines, so the PDF shows exactly the code that was run.
object OopsScala {
  def section(n: Int, title: String): Unit = println(s"## $n $title")

  def s1(): Unit = {
    section(1, "Class, object, constructor, this")
    class Student(val name: String, var marks: Int) {        // primary constructor: the parameters after the class name
      def this(name: String) = this(name, 0)                 // auxiliary constructor: must start by calling another one
      def grade: String = if (marks >= 40) "pass" else "fail"
      def setMarks(m: Int): Student = { this.marks = m; this }   // this = the current object; returning it allows chaining
      override def toString: String = s"$name ($marks)"
    }
    val a = new Student("Asha", 72)
    val b = new Student("Ravi")
    println(s"$a ${a.grade} | $b ${b.grade}")
    println(b.setMarks(30).setMarks(55))
  }

  def s2(): Unit = {
    section(2, "Encapsulation and access modifiers")
    class Account(val owner: String, private var balance: Int) {
      protected val bank = "VITB"                            // visible in this class and its subclasses
      def deposit(amount: Int): Unit = { require(amount > 0, "amount must be positive"); balance += amount }
      def currentBalance: Int = balance                      // public getter for the private field
      private def audit(): String = s"audit of $owner"       // visible only inside Account
      def report: String = audit()                           // a public method may call a private one
    }
    class Savings(owner: String, start: Int) extends Account(owner, start) {
      def showBank: String = bank                            // protected: allowed here, not outside
    }
    val acc = new Account("Asha", 1000)
    acc.deposit(500)
    println(s"${acc.currentBalance} ${acc.report}")
    println(new Savings("Ravi", 10).showBank)
    try acc.deposit(-5) catch { case e: IllegalArgumentException => println(s"IllegalArgumentException: ${e.getMessage}") }
  }

  def s3(): Unit = {
    section(3, "Inheritance and super")
    class Person(val name: String) {
      def describe: String = s"$name is a person"
    }
    class Employee(name: String, val salary: Int) extends Person(name) {   // pass name up to the parent constructor
      override def describe: String = super.describe + s" earning $salary"  // override is compulsory
    }
    class Manager(name: String, salary: Int) extends Employee(name, salary)
    val m = new Manager("Meena", 90000)
    println(m.describe)
    println(m.isInstanceOf[Person])
    val chain = Iterator.iterate[Class[_]](m.getClass)(_.getSuperclass).takeWhile(_ != null)
    println(chain.map(_.getSimpleName.takeWhile(_ != '$')).mkString(" -> "))   // takeWhile drops the $1 that local classes get
  }

  def s4(): Unit = {
    section(4, "Method overloading and field overriding")
    class Calc {
      def add(a: Int, b: Int): Int = a + b
      def add(a: Int, b: Int, c: Int): Int = a + b + c       // same name, different number of parameters
      def add(a: Double, b: Double): Double = a + b          // same name, different parameter types
    }
    val k = new Calc
    println(s"${k.add(1, 2)} ${k.add(1, 2, 3)} ${k.add(1.5, 2.5)}")

    class Animal { val sound: String = "..."; def speak: String = s"makes $sound" }
    class Dog extends Animal { override val sound: String = "woof" }      // a val can be overridden by a val
    println(new Dog().speak)

    // Trap: Base runs first, so while it is being built the overriding val of Derived is still null
    class Base { val label: String = "base"; val size: Int = label.length }
    class Derived extends Base { override val label: String = "derived" }
    try new Derived() catch { case e: NullPointerException => println("NullPointerException while Derived is being built") }
    class Base2 { val label: String = "base"; lazy val size: Int = label.length }   // fix: lazy val, computed on first use
    class Derived2 extends Base2 { override val label: String = "derived" }
    println(new Derived2().size)
  }

  def s5(): Unit = {
    section(5, "Polymorphism and operator overloading")
    class Shape { def area: Double = 0.0 }
    class Circle(r: Double) extends Shape { override def area: Double = math.round(3.14159 * r * r * 100) / 100.0 }
    class Rect(w: Double, h: Double) extends Shape { override def area: Double = w * h }
    val shapes: List[Shape] = List(new Circle(2), new Rect(3, 4), new Shape)   // one type, three kinds of object
    shapes.foreach(s => println(s"${s.getClass.getSimpleName.takeWhile(_ != '$')} ${s.area}"))   // the object decides which area runs

    class Vec(val x: Int, val y: Int) {
      def +(o: Vec): Vec = new Vec(x + o.x, y + o.y)         // an operator is only a method named +
      override def toString: String = s"Vec($x, $y)"
    }
    println(new Vec(1, 2) + new Vec(3, 4))
  }

  def s6(): Unit = {
    section(6, "Abstract class")
    abstract class Vehicle(val name: String) {
      def wheels: Int                                        // abstract member: no body
      def info: String = s"$name has $wheels wheels"         // concrete member
    }
    class Car(name: String) extends Vehicle(name) {
      def wheels: Int = 4                                    // 'override' is optional when implementing an abstract member
    }
    println(new Car("Swift").info)
    val bike = new Vehicle("Hero") { def wheels: Int = 2 }   // an abstract class can be completed on the spot
    println(bike.info)
  }

  def s7(): Unit = {
    section(7, "Traits and mixins")
    trait Flyer { def name: String; def fly: String = s"$name flies" }
    trait Swimmer { def name: String; def swim: String = s"$name swims" }
    class Duck(val name: String) extends Flyer with Swimmer  // extends one, mixes in the others with 'with'
    val d = new Duck("Donald")
    println(s"${d.fly} | ${d.swim}")

    trait Logger { def log(msg: String): Unit = println(s"log: $msg") }
    class Service { def run: String = "service running" }
    val s = new Service with Logger                          // mix a trait into one object when creating it
    s.log(s.run)

    trait A { def hi: String = "A" }
    trait B extends A { override def hi: String = "B>" + super.hi }
    trait C extends A { override def hi: String = "C>" + super.hi }
    class D extends B with C                                 // linearization: D, C, B, A (the last mixin runs first)
    println(new D().hi)
  }

  def s8(): Unit = {
    section(8, "final")
    class Base {
      final def pay: String = "base pay"                     // cannot be overridden
      def bonus: String = "base bonus"
    }
    final class Leaf extends Base {                          // cannot be extended
      override def bonus: String = "leaf bonus"
    }
    val l = new Leaf
    println(s"${l.pay} | ${l.bonus}")
  }

  def s9(): Unit = {
    section(9, "Singleton and companion object")
    object Registry {                                        // a singleton: exactly one instance, no 'new'
      private var count = 0
      def next(): Int = { count += 1; count }
    }
    class Temp private (val c: Double) {                     // private constructor: only the companion may call it
      override def toString: String = f"$c%.1f C"
    }
    object Temp {                                            // companion: same name, same scope as the class
      def apply(c: Double): Temp = new Temp(c)               // Temp(21.5) calls apply
      def fromF(f: Double): Temp = new Temp((f - 32) * 5 / 9)
      val absoluteZero: Double = -273.15                     // 'static'-like member
    }
    println(s"${Registry.next()} ${Registry.next()}")
    println(s"${Temp(21.5)} ${Temp.fromF(212)} ${Temp.absoluteZero}")
  }

  def s10(): Unit = {
    section(10, "Case classes")
    case class Point(x: Int, y: Int = 0)                     // no 'new', toString, equals, hashCode, copy and unapply for free
    val p = Point(1, 2)
    println(s"$p ${p == Point(1, 2)} ${p.copy(y = 9)}")
    println(p.hashCode == Point(1, 2).hashCode)
    p match {                                                // pattern matching takes the object apart
      case Point(1, y) => println(s"x is 1, y is $y")
      case _ => println("other")
    }
  }

  def s11(): Unit = {
    section(11, "Anonymous class")
    trait Greeter { def greet(name: String): String }
    val g = new Greeter { def greet(name: String): String = s"Hello, $name" }   // a class with no name, one object
    println(g.greet("Asha"))
    val task = new Runnable { def run(): Unit = println("running an anonymous Runnable") }
    task.run()
    println(s"the class has no name: ${g.getClass.getSimpleName.isEmpty}")
  }

  def main(args: Array[String]): Unit = {
    s1(); s2(); s3(); s4(); s5(); s6(); s7(); s8(); s9(); s10(); s11()
  }
}
