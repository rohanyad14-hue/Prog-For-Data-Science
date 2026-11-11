//> using scala 2.13.12
// Sample answer M3-Q4: employees with case classes, a companion object, access modifiers and a singleton report generator
case class Employee(id: Int, name: String, role: String, salary: Double)

object Employee {                                   // companion: same name, same file; holds the utility methods
  val MinSalary = 30000.0
  def fromCsv(line: String): Option[Employee] = line.split(",").map(_.trim) match {
    case Array(id, name, role, salary) =>
      scala.util.Try(Employee(id.toInt, name, role, salary.toDouble)).toOption.filter(_.salary >= MinSalary)
    case _ => None
  }
  def raise(e: Employee, percent: Double): Employee = {          // money: round to paise, 55000 * 1.1 alone gives 60500.00000000001
    val raised = BigDecimal(e.salary * (1 + percent / 100)).setScale(2, BigDecimal.RoundingMode.HALF_UP).toDouble
    e.copy(salary = raised)
  }
  def totalPayroll(es: Seq[Employee]): Double = es.map(_.salary).sum
}

object PayrollReport {                              // singleton object: the one and only report generator
  private val taxRate = 0.10                        // private: not visible outside this object
  private def net(e: Employee): Double = e.salary * (1 - taxRate)
  def generate(es: List[Employee]): String = {
    val lines = es.map(e => f"${e.id}%d ${e.name}%-5s ${e.role}%-9s gross ${e.salary}%9.1f net ${net(e)}%9.1f")
    val top = es.maxBy(_.salary)
    (lines :+ f"payroll ${Employee.totalPayroll(es)}%.1f, average ${Employee.totalPayroll(es) / es.size}%.1f, highest paid ${top.name}").mkString("\n")
  }
}

object EmployeeApp {
  def main(args: Array[String]): Unit = {
    val staff = List(Employee(101, "Ravi", "Developer", 75000), Employee(102, "Anu", "Tester", 55000), Employee(103, "Kiran", "Manager", 95000))

    println("--- what a case class gives for free ---")
    println(staff.head)                                                       // readable toString
    println(Employee(101, "Ravi", "Developer", 75000) == staff.head)         // equality by value
    println(staff.head.copy(salary = 80000))                                  // immutable update
    staff(2) match {                                                          // pattern matching on the fields
      case Employee(_, n, "Manager", s) if s > 90000 => println(n + " is a senior manager")
      case _ => println("other")
    }

    println("--- companion object utilities ---")
    println(Employee.fromCsv("104, Meena, Analyst, 62000"))
    println(Employee.fromCsv("105, Bad, Intern, 12000") + " (below the minimum of " + Employee.MinSalary + ")")
    println(Employee.fromCsv("106, Oops, Tester") + " and " + Employee.fromCsv("x, Y, Z, abc") + " (malformed lines are rejected)")
    println(Employee.raise(staff(1), 10))

    println("--- singleton report ---")
    println(PayrollReport.generate(staff))
  }
}
