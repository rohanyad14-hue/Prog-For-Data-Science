//> using scala 2.13.12
// Sample answer M3-Q2: library resources (inheritance, abstract class, field overriding, polymorphism, final)
abstract class LibraryResource(val id: Int, val title: String, initialStatus: String) {
  private var status: String = initialStatus        // "Available" or "Issued"
  val kind: String                                  // abstract field, every subclass gives its own value
  def loanDays: Int                                 // abstract method
  val lateFeePerDay: Double = 1.0                   // concrete field with a default that subclasses may override

  def isAvailable: Boolean = status == "Available"

  final def issue(): String =                       // final: the issuing rule is the same for every resource and cannot be changed
    if (isAvailable) { status = "Issued"; s"$kind '$title' issued for $loanDays days" }
    else s"$kind '$title' is not available"

  final def giveBack(daysLate: Int): String =
    if (!isAvailable) { status = "Available"; f"$kind '$title' returned, late fee Rs. ${daysLate * lateFeePerDay}%.2f" }
    else s"$kind '$title' was not issued"

  override def toString: String = s"$kind($id, $title, $status)"
}

class Book(id: Int, title: String, status: String) extends LibraryResource(id, title, status) {
  val kind = "Book"
  def loanDays = 14
}

class Journal(id: Int, title: String, status: String) extends LibraryResource(id, title, status) {
  val kind = "Journal"
  def loanDays = 7
  override val lateFeePerDay = 5.0                  // field overriding
}

final class Magazine(id: Int, title: String, status: String) extends LibraryResource(id, title, status) {
  val kind = "Magazine"                             // final class: nobody extends it further
  def loanDays = 3
  override val lateFeePerDay = 0.5
}

object Library {
  def main(args: Array[String]): Unit = {
    val shelf: List[LibraryResource] = List(
      new Book(101, "Scala Programming", "Available"),
      new Journal(201, "Data Science Journal", "Issued"),
      new Magazine(301, "Tech Today", "Available"))

    println("--- the catalogue ---")
    shelf.foreach(println)
    println("--- issue every resource: one call, three behaviours (polymorphism) ---")
    shelf.foreach(r => println(r.issue()))
    println("--- return every resource, 2 days late ---")
    shelf.foreach(r => println(r.giveBack(2)))
    println("--- state after the round ---")
    shelf.foreach(println)
    println(shelf.map(r => r.kind -> r.loanDays))
  }
}
