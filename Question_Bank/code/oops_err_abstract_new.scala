//> using scala 2.13.12
// Deliberately wrong code: this file must NOT compile. An abstract class cannot be instantiated.
abstract class Vehicle(val name: String) {
  def wheels: Int
}

object Wrong {
  def main(args: Array[String]): Unit = {
    val v = new Vehicle("x")                               // error
    println(v.name)
  }
}
