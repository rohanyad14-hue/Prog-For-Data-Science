// M3-Q3  Case classes, pattern matching, traits and mixins (Lab 17, FAT top-10 questions 5, 6, 9)
case class Person(name: String, age: Int, city: String)

case class Transaction(id: String, amount: Double, status: String)

trait Logger { def log(msg: String): Unit = println(s"  [LOG] $msg") }
trait Auditor { def audit(msg: String): Unit = println(s"  [AUDIT] $msg") }
trait Notifier { def notifyUser(msg: String): Unit = println(s"  [NOTIFY] $msg") }

// Linearization demo: each trait calls super, so the call order shows the chain
trait A { def who: String = "A" }
trait B extends A { override def who: String = "B > " + super.who }
trait C extends A { override def who: String = "C > " + super.who }
class D extends B with C { override def who: String = "D > " + super.who }

class Worker(val name: String) extends Logger with Auditor {          // mixin composition
  def work(): Unit = { log(s"$name started"); audit(s"$name finished") }
}

object M3Q3 extends App {
  // ---- case class: what the compiler generates ----
  val p1 = Person("Asha", 22, "Chennai")
  val p2 = Person("Asha", 22, "Chennai")
  println(s"toString : $p1")
  println(s"equals   : ${p1 == p2}  (structural)   eq: ${p1 eq p2}  (reference)")
  println(s"hashCode : ${p1.hashCode == p2.hashCode}")
  println(s"copy     : ${p1.copy(city = "Pune")}")
  val Person(n, a, _) = p1                                             // unapply -> deconstruction
  println(s"unapply  : name=$n age=$a")

  // ---- Lab 17 style operations ----
  val people = List(Person("Asha", 22, "Chennai"), Person("Ravi", 34, "Delhi"),
                    Person("Meena", 41, "Chennai"), Person("Kabir", 29, "Pune"), Person("Sneha", 33, "Delhi"))
  println("older than 30  : " + people.filter(_.age > 30).map(_.name))
  println("grouped by city: " + people.groupBy(_.city).map { case (c, ps) => c -> ps.map(_.name) }.toList.sortBy(_._1))
  println("as strings     : " + people.take(2).map(p => s"${p.name} is ${p.age} years old and lives in ${p.city}"))
  println("sorted by age  : " + people.sortBy(_.age).map(_.name))

  // ---- pattern matching on a case class ----
  def process(tx: Transaction): String = tx match {
    case Transaction(id, amt, "SUCCESS") if amt > 10000 => s"Large transaction $id logged"
    case Transaction(id, _, "SUCCESS")                   => s"Standard transaction $id approved"
    case Transaction(id, _, "FAILED")                    => s"Alert: Transaction $id failed"
    case _                                               => "Unknown transaction state"
  }
  List(Transaction("T1", 25000, "SUCCESS"), Transaction("T2", 900, "SUCCESS"),
       Transaction("T3", 50, "FAILED"), Transaction("T4", 10, "PENDING")).foreach(t => println("  " + process(t)))

  // ---- traits, mixins and linearization ----
  new Worker("Asha").work()
  println("linearization of D extends B with C: " + (new D).who)
  val adHoc = new Worker("Kabir") with Notifier                        // mix a trait in at instantiation time
  adHoc.work()
  adHoc.notifyUser("shift over")
}
