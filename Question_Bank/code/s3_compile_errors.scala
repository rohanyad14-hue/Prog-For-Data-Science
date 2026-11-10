// Deliberately WRONG code: used to capture the compiler's real messages for the notes.
class A { final def f = 1; def g = 1 }
class B extends A {
  override def f = 2        // error: cannot override a final method
  def g = 2                 // error: needs `override`
}
final class Leaf
class Child extends Leaf     // error: cannot inherit from a final class
case class Emp(id: Int, private val salary: Int)
object Outside { val e = Emp(1, 5); val s = e.salary }        // error: salary is private
