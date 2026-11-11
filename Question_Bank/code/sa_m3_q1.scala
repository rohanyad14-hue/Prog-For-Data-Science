//> using scala 2.13.12
// Sample answer M3-Q1: course registration system (classes, objects, constructors, lists, method overloading, inheritance)
import scala.collection.mutable.ListBuffer

abstract class Student(val id: Int, val name: String, val dept: String, initialCourses: List[String]) {
  private var registered: List[String] = initialCourses.distinct   // an immutable List behind a private var

  def maxCourses: Int                                              // the rule comes from the subclass (def, not val)
  def level: String

  def courses: List[String] = registered                           // callers receive the immutable list, they cannot change ours
  def hasCourse(course: String): Boolean = registered.contains(course)

  def addCourse(course: String): Boolean =                         // overloaded: one course
    if (hasCourse(course) || registered.size >= maxCourses) false
    else { registered = registered :+ course; true }

  def addCourse(newCourses: List[String]): Int =                   // overloaded: several courses, returns how many were added
    newCourses.count(c => addCourse(c))

  def removeCourse(course: String): Boolean =
    if (hasCourse(course)) { registered = registered.filterNot(_ == course); true } else false
}

class UGStudent(id: Int, name: String, dept: String, initial: List[String]) extends Student(id, name, dept, initial) {
  def this(id: Int, name: String, dept: String) = this(id, name, dept, Nil)    // auxiliary constructor
  def maxCourses = 6
  def level = "UG"
}

class PGStudent(id: Int, name: String, dept: String, initial: List[String], val thesisTopic: String = "to be decided")
    extends Student(id, name, dept, initial) {
  def maxCourses = 4
  def level = "PG"
}

object Registry {                                                  // singleton: one registry for the whole application
  private val students = ListBuffer[Student]()
  def register(s: Student): Unit = students += s
  def find(id: Int): Option[Student] = students.find(_.id == id)                       // overloaded search: by id
  def find(name: String): Option[Student] = students.find(_.name.equalsIgnoreCase(name)) // overloaded search: by name
  def enrolledIn(course: String): List[String] = students.filter(_.hasCourse(course)).map(_.name).toList
  def report(): Unit = students.foreach { s =>
    println(s.id + " " + s.name + " (" + s.dept + ", " + s.level + ", max " + s.maxCourses + "): " + s.courses.mkString("[", ", ", "]"))
  }
}

object CourseRegistration {
  def main(args: Array[String]): Unit = {
    Registry.register(new UGStudent(101, "Arun", "CSE", List("Scala", "DBMS")))
    Registry.register(new PGStudent(102, "Priya", "ECE", List("Python", "ML"), "speech models"))
    Registry.register(new UGStudent(103, "Rahul", "CSE", List("Scala", "AI")))
    println("--- registered students ---")
    Registry.report()

    println("--- searching (two overloaded find methods) ---")
    println(Registry.find(101).map(_.name))
    println(Registry.find("priya").map(_.id))
    println(Registry.find(999))
    println(Registry.enrolledIn("Scala"))

    println("--- adding and removing courses ---")
    val arun = Registry.find(101).get
    println("add Statistics     : " + arun.addCourse("Statistics"))
    println("add Scala again    : " + arun.addCourse("Scala"))
    println("add four more      : " + arun.addCourse(List("OS", "CN", "Maths", "Physics")) + " added (UG limit is 6)")
    println("remove DBMS        : " + arun.removeCourse("DBMS") + ", remove Chemistry: " + arun.removeCourse("Chemistry"))
    println("Arun now           : " + arun.courses)
    val priya = Registry.find(102).get
    println("Priya adds three   : " + priya.addCourse(List("Stats", "NLP", "Vision")) + " added (PG limit is 4)")
    println("Priya now          : " + priya.courses)
  }
}
