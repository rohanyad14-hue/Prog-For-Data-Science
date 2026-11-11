//> using scala 2.13.12
// Deliberately wrong code: this file must NOT compile. A concrete subclass must implement every abstract member.
abstract class Vehicle(val name: String) {
  def wheels: Int
}

class Incomplete(name: String) extends Vehicle(name)       // error: wheels is not implemented

object Wrong {
  def main(args: Array[String]): Unit = println("never runs")
}
