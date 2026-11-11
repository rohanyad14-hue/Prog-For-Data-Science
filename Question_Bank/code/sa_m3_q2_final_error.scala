//> using scala 2.13.12
// Deliberately wrong code: this file must NOT compile. It shows what a final METHOD protects.
abstract class Resource {
  final def issue(): String = "issued"
}
class Magazine extends Resource {
  override def issue(): String = "issued without checking"   // error: cannot override a final member
}

object Wrong {
  def main(args: Array[String]): Unit = println(new Magazine().issue())
}
