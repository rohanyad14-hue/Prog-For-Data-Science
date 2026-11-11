//> using scala 2.13.12
// Deliberately wrong code: this file must NOT compile. A final class cannot be extended.
final class Leaf {
  def bonus: String = "leaf bonus"
}

class Twig extends Leaf                                     // error

object Wrong {
  def main(args: Array[String]): Unit = println(new Twig().bonus)
}
