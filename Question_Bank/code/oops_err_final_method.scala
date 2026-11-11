//> using scala 2.13.12
// Deliberately wrong code: this file must NOT compile. A final method cannot be overridden.
class Base {
  final def pay: String = "base pay"
}

class Leaf extends Base {
  override def pay: String = "changed pay"                 // error
}

object Wrong {
  def main(args: Array[String]): Unit = println(new Leaf().pay)
}
