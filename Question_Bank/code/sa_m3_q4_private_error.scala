//> using scala 2.13.12
// Deliberately wrong code: this file must NOT compile. It shows what `private` protects.
object PayrollReport {
  private val taxRate = 0.10
  private def net(salary: Double): Double = salary * (1 - taxRate)
  def netPay(salary: Double): Double = net(salary)
}

object Wrong {
  def main(args: Array[String]): Unit = {
    println(PayrollReport.netPay(75000))   // allowed: public method
    println(PayrollReport.taxRate)         // error: private member
  }
}
