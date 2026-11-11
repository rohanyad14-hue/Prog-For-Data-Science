//> using scala 2.13.12
// Deliberately wrong code: this file must NOT compile. It shows what a final CLASS protects.
final class Magazine {
  def issue(): String = "issued"
}
class SpecialMagazine extends Magazine                       // error: illegal inheritance from a final class

object Wrong {
  def main(args: Array[String]): Unit = println(new SpecialMagazine().issue())
}
