// Sample HOT questions, Module 3: five Scala design problems (Scala 2.13)
import scala.collection.mutable
import scala.util.Try

// ======================================================================== Q1 course registration
abstract class Student(val id: Int, val name: String, val dept: String, val courses: List[String]) {
  def level: String
  def maxCourses: Int
  protected def withCourses(cs: List[String]): Student
  def addCourse(c: String): Either[String, Student] =
    if (courses.contains(c)) Left(s"$name is already registered for $c")
    else if (courses.size >= maxCourses) Left(s"$name has reached the $level limit of $maxCourses courses")
    else Right(withCourses(courses :+ c))
  def removeCourse(c: String): Student = withCourses(courses.filterNot(_ == c))
  def has(c: String): Boolean = courses.contains(c)
  override def toString = s"$level($id, $name, $dept, ${courses.mkString("[", ", ", "]")})"
}
class UndergraduateStudent(id: Int, name: String, dept: String, courses: List[String]) extends Student(id, name, dept, courses) {
  def this(id: Int, name: String, dept: String) = this(id, name, dept, Nil)          // auxiliary constructor
  val level = "UG"; val maxCourses = 5
  protected def withCourses(cs: List[String]) = new UndergraduateStudent(id, name, dept, cs)
}
class PostgraduateStudent(id: Int, name: String, dept: String, courses: List[String], val thesis: String = "TBD") extends Student(id, name, dept, courses) {
  val level = "PG"; val maxCourses = 4
  protected def withCourses(cs: List[String]) = new PostgraduateStudent(id, name, dept, cs, thesis)
  override def toString = super.toString + s" thesis=$thesis"
}
object Registry {                                            // singleton holding the data
  private val students = mutable.LinkedHashMap.empty[Int, Student]       // Map: O(1) lookup by id
  def register(s: Student): Unit = students(s.id) = s
  def find(id: Int): Option[Student] = students.get(id)
  def search(course: String): List[Student] = students.values.filter(_.has(course)).toList                  // overloaded
  def search(dept: String, course: String): List[Student] = students.values.filter(s => s.dept == dept && s.has(course)).toList
  def update(id: Int)(f: Student => Either[String, Student]): String = find(id) match {
    case None    => s"no student with id $id"
    case Some(s) => f(s).fold(err => s"rejected: $err", ns => { students(id) = ns; s"ok: $ns" })
  }
}

// ======================================================================== Q2 library hierarchy
abstract class Resource(val id: Int, val title: String, initial: String) {
  val kind: String                                          // abstract fields, overridden below
  val loanDays: Int
  private var state = initial
  final def status: String = state                          // final: nobody may change how status is read
  final def issue(): String =                               // final: the availability rule must hold for every resource type
    if (state == "Available") { state = "Issued"; s"$kind '$title' issued for $loanDays days" } else s"$kind '$title' cannot be issued (status: $state)"
  final def giveBack(): String =
    if (state == "Issued") { state = "Available"; s"$kind '$title' returned" } else s"$kind '$title' was not issued"
  def describe: String = s"$kind #$id '$title' [$state], loan period $loanDays days"        // open for overriding
}
class Book(id: Int, title: String, st: String) extends Resource(id, title, st) { override val kind = "Book"; override val loanDays = 14 }
class Journal(id: Int, title: String, st: String) extends Resource(id, title, st) {
  override val kind = "Journal"; override val loanDays = 7
  override def describe = super.describe + " (reference copy, in-library reading preferred)"
}
final class Magazine(id: Int, title: String, st: String) extends Resource(id, title, st) { override val kind = "Magazine"; override val loanDays = 3 }

// ======================================================================== Q4 employees
case class Employee(id: Int, name: String, role: String, private val salary: Int) {
  def band: String = if (salary >= 90000) "A" else if (salary >= 60000) "B" else "C"
  def safeView: String = s"$id $name ($role) band $band"                                // exposes the band, never the figure
}
object Employee {                                           // companion: utilities + factories, may read the private salary
  private var nextId = 104
  def apply(name: String, role: String, salary: Int): Employee = { val e = new Employee(nextId, name, role, salary); nextId += 1; e }   // overloaded apply
  def totalPayroll(es: Seq[Employee]): Int = es.map(_.salary).sum
  def highestPaid(es: Seq[Employee]): Employee = es.maxBy(_.salary)
  def raise(e: Employee, pct: Int): Employee = e.copy(salary = e.salary + e.salary * pct / 100)
  def fromCsv(line: String): Either[String, Employee] = line.split(",").map(_.trim) match {
    case Array(i, n, r, s) => Try(new Employee(i.toInt, n, r, s.toInt)).toEither.left.map(_ => s"bad number in '$line'")
    case _                 => Left(s"expected 4 fields in '$line'")
  }
  def averageSalary(es: Seq[Employee]): Double = totalPayroll(es).toDouble / es.size
}
object ReportGenerator {                                    // singleton: one report generator for the whole application
  def report(es: Seq[Employee]): String = {
    val lines = es.sortBy(_.safeView).map(e => "  " + e.safeView)
    ("Employee report" +: lines :+ f"  total payroll ${Employee.totalPayroll(es)}, average ${Employee.averageSalary(es)}%.1f, highest paid ${Employee.highestPaid(es).name}").mkString("\n")
  }
}

// ======================================================================== Q5 transportation traits
abstract class Vehicle(val name: String, val speed: Int) { def describe = s"$name at $speed km/h" }
trait PassengerVehicle { this: Vehicle => def capacity: Int = 40; def board(n: Int): String = s"$name boards $n of $capacity passengers" }
trait EmergencyService { this: Vehicle => def priority: Int = 1; def siren(): String = s"$name: siren on, priority $priority" }
trait HighSpeedVehicle { this: Vehicle => def overLimit(limit: Int): Boolean = speed > limit }
class Bus(s: Int) extends Vehicle("Bus", s) with PassengerVehicle
class Car(s: Int) extends Vehicle("Car", s) with PassengerVehicle { override def capacity = 4 }
class Ambulance(s: Int) extends Vehicle("Ambulance", s) with EmergencyService with HighSpeedVehicle
class FireEngine(s: Int) extends Vehicle("FireEngine", s) with EmergencyService with HighSpeedVehicle
class Bike(s: Int) extends Vehicle("Bike", s)

object S3Hot extends App {
  println("--- Q1 course registration: classes, constructors, lists, overloading, inheritance ---")
  Registry.register(new UndergraduateStudent(101, "Arun", "CSE", List("Scala", "DBMS")))
  Registry.register(new UndergraduateStudent(102, "Priya", "ECE", List("Python", "ML")))
  Registry.register(new PostgraduateStudent(103, "Rahul", "CSE", List("Scala", "AI"), "Graph analytics"))
  Registry.register(new UndergraduateStudent(104, "Kavya", "IT"))                                    // auxiliary constructor: no courses yet
  println("all students: " + List(101, 102, 103, 104).flatMap(Registry.find).mkString("\n              "))
  println("add AI to Arun        : " + Registry.update(101)(_.addCourse("AI")))
  println("add Scala to Arun again: " + Registry.update(101)(_.addCourse("Scala")))
  println("remove DBMS from Arun : " + Registry.update(101)(s => Right(s.removeCourse("DBMS"))))
  println("search(\"Scala\")        : " + Registry.search("Scala").map(_.name))
  println("search(\"CSE\", \"Scala\") : " + Registry.search("CSE", "Scala").map(_.name) + "   (overloaded method, two parameter lists of different length)")
  println("PG limit is 4         : " + List("ML", "DBMS", "Python").map(c => Registry.update(103)(_.addCourse(c))).last)
  println("unknown id            : " + Registry.update(999)(_.addCourse("X")))

  println("\n--- Q2 library: abstract class, field overriding, polymorphism, final ---")
  val items: List[Resource] = List(new Book(101, "Scala Programming", "Available"), new Journal(201, "Data Science Journal", "Issued"), new Magazine(301, "Tech Today", "Available"))
  items.foreach(r => println("  " + r.describe))
  println("issue every resource through the same call:")
  items.foreach(r => println("  " + r.issue()))
  println("return them all:")
  items.foreach(r => println("  " + r.giveBack()))
  println("status after the round trip: " + items.map(r => r.kind + "=" + r.status).mkString(", "))

  println("\n--- Q3 shopping cart: Map and combinators versus an imperative loop ---")
  val cart = Map("Laptop" -> 65000, "Mobile" -> 25000, "Tablet" -> 18000, "Headphone" -> 3000)
  val discounted = cart.map { case (k, v) => k -> v * 90 / 100 }                    // integer arithmetic avoids floating-point noise
  val premium = cart.filter { case (_, v) => v > 20000 }.keys.toList.sorted
  val total = cart.values.reduce(_ + _)
  println("10% discount : " + discounted.toList.sortBy(-_._2))
  println("above 20,000 : " + premium + " | total inventory value (one unit each): " + total + " | after discount: " + discounted.values.sum)
  var tmpTotal = 0; val tmpDisc = mutable.Map[String, Int](); val tmpPrem = mutable.ListBuffer[String]()       // imperative version
  for ((k, v) <- cart) { tmpTotal += v; tmpDisc(k) = v * 90 / 100; if (v > 20000) tmpPrem += k }
  println("imperative gives the same: " + (tmpTotal == total && tmpDisc.toMap == discounted && tmpPrem.sorted.toList == premium) + " (but with 3 mutable variables and one loop doing three jobs)")
  println("chained pipeline : " + cart.filter(_._2 > 20000).map { case (k, v) => k -> v * 90 / 100 }.values.sum + " = discounted total of the premium items")

  println("\n--- Q4 employees: case class, companion object, access modifiers, singleton ---")
  val staff = List(Employee(101, "Ravi", "Developer", 75000), Employee(102, "Anu", "Tester", 55000), Employee(103, "Kiran", "Manager", 95000))
  val e4 = Employee("Dev", "Analyst", 65000)                                          // companion apply with an auto-generated id
  println("case class toString / equality / copy: " + staff.head + " | " + (staff.head == Employee(101, "Ravi", "Developer", 75000)) + " | " + staff.head.copy(role = "Lead").role)
  println("auto id from companion: " + e4.safeView)
  println("band only, never the salary: " + staff.map(_.band))
  println("companion utilities: total " + Employee.totalPayroll(staff) + ", highest " + Employee.highestPaid(staff).name + ", Ravi after a 10% raise has band " + Employee.raise(staff.head, 10).band)
  println("parsing: " + List("104,Dev,Analyst,65000", "105,Zed,Tester,abc", "106,Only,Three").map(Employee.fromCsv(_).fold(identity, _.safeView)))
  println(ReportGenerator.report(staff ++ List(e4)))

  println("\n--- Q5 transport: traits, mixins, arrays, real-time rules ---")
  val feed = Array(("Bus", 45), ("Car", 70), ("Ambulance", 90), ("FireEngine", 85), ("Bike", 60))
  def make(n: String, s: Int): Vehicle = n match {
    case "Bus" => new Bus(s); case "Car" => new Car(s); case "Ambulance" => new Ambulance(s); case "FireEngine" => new FireEngine(s); case _ => new Bike(s)
  }
  val fleet = feed.map { case (n, s) => make(n, s) }
  println("fleet: " + fleet.map(_.describe).mkString("; "))
  println("emergency vehicles : " + fleet.collect { case e: Vehicle with EmergencyService => e.siren() }.toList)
  println("high-speed capable : " + fleet.collect { case v: Vehicle with HighSpeedVehicle => v.name }.toList)
  println("ordinary vehicles over the 60 km/h city limit: " + fleet.filterNot(_.isInstanceOf[EmergencyService]).filter(_.speed > 60).map(_.name).toList + " (emergency vehicles are exempt)")
  println("passenger loading  : " + fleet.collect { case p: Vehicle with PassengerVehicle => p.board(3) }.toList)
  val ad = new Bike(60) with HighSpeedVehicle                                       // mixin chosen at instantiation
  println("ad-hoc mixin on one object: " + ad.name + " overLimit(50) = " + ad.overLimit(50))
  println("sorted by speed    : " + fleet.sortBy(-_.speed).map(v => v.name + ":" + v.speed).toList)
  println("average speed      : " + fleet.map(_.speed).sum / fleet.length.toDouble)
}
