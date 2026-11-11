//> using scala 2.13.12
// Deliberately wrong code: this file must NOT compile. It shows what private and protected protect.
class Account(val owner: String, private var balance: Int) {
  protected val bank = "VITB"
}

object Wrong {
  def main(args: Array[String]): Unit = {
    val acc = new Account("Asha", 1000)
    println(acc.balance)        // error: balance is private
    println(acc.bank)           // error: bank is protected
  }
}
