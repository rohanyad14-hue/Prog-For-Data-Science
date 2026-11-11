//> using scala 2.13.12
// Deliberately wrong code: this file must NOT compile. Replacing a concrete method needs the word override.
class Person {
  def describe: String = "a person"
}

class Employee extends Person {
  def describe: String = "an employee"                     // error: override is missing
}

object Wrong {
  def main(args: Array[String]): Unit = println(new Employee().describe)
}
