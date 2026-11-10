//> using scala 2.13.12
//> using dep io.github.pityka::saddle-core:4.0.0-M14
// Sample HOT questions, Module 4: Saddle answers (patient records and loan records)
import org.saddle._
import org.saddle.ops.BinOps._

object S4HotSaddle extends App {
  println("--- Q2 Saddle: Series and Frame for the patient records ---")
  val ids = Index("P101", "P102", "P103", "P104")
  val age = Series(Vec(45.0, 32.0, 58.0, 29.0), ids)
  val bp = Series(Vec(130.0, 120.0, 145.0, 118.0), ids)
  val diabetes = Series(Vec(1.0, 0.0, 1.0, 0.0), ids)                      // Yes = 1, No = 0
  val frame = Frame("Age" -> age, "BP" -> bp, "Diabetes" -> diabetes)
  println(frame)
  println("shape: " + frame.numRows + " rows x " + frame.numCols + " columns | row labels are the patient ids: " + frame.rowIx.toVec.toSeq.mkString(","))
  println("BP of P103 by label: " + bp.first("P103").get + " | Age of the second patient by position: " + age.values.raw(1))

  println("--- Q2 detect abnormal records ---")
  val abnormal = bp.filter(_ >= 140)
  println("systolic BP >= 140 -> " + abnormal.index.toVec.toSeq.mkString(",") + " (" + abnormal.values.toSeq.mkString(",") + ")")
  val m = bp.values.mean; val sd = bp.values.stdev
  val z = bp.mapValues(v => (v - m) / sd)
  println(f"mean BP $m%.2f, std $sd%.2f | z-scores " + z.values.toSeq.map(v => f"$v%.2f").mkString(", "))
  println("older than 55: " + age.filter(_ >= 55).index.toVec.toSeq.mkString(","))
  val withFlag = frame.addCol(bp.mapValues(v => if (v >= 140) 1.0 else 0.0), "HighBP")
  println("flag added as a new column: columns = " + withFlag.colIx.toVec.toSeq.mkString(","))
  println("mean BP, diabetic: " + bp.filterAt(i => diabetes.values.raw(i) == 1.0).values.mean + " | non-diabetic: " + bp.filterAt(i => diabetes.values.raw(i) == 0.0).values.mean)

  println("--- Q2 missing values are first-class ---")
  val withNA = Series(Vec(130.0, Double.NaN, 145.0), Index("P101", "P102", "P103"))
  println("hasNA = " + withNA.hasNA + " | mean ignores NA: " + withNA.values.mean + " | dropNA keeps " + withNA.dropNA.index.toVec.toSeq.mkString(",") + " | fillNA(mean) -> " + withNA.fillNA(_ => 137.5).values.toSeq.mkString(","))

  println("--- Q5 Saddle: structure and pre-process the loan records ---")
  val cid = Index("L101", "L102", "L103", "L104")
  val income = Series(Vec(650000.0, 350000.0, 800000.0, 250000.0), cid)
  val loan = Series(Vec(300000.0, 400000.0, 500000.0, 350000.0), cid)
  val status = Series(Vec("Approved", "Rejected", "Approved", "Rejected"), cid)
  val lti = loan / income                                                   // aligned on the customer id, no loop
  val loans = Frame("Income" -> income, "Loan" -> loan, "LTI" -> lti)
  println(loans)
  println("approved: mean LTI " + f"${lti.filterAt(i => status.values.raw(i) == "Approved").values.mean}%.3f" + " | rejected: mean LTI " + f"${lti.filterAt(i => status.values.raw(i) == "Rejected").values.mean}%.3f")
  println("loans above 100% of income: " + lti.filter(_ > 1.0).index.toVec.toSeq.mkString(",") + " | riskiest first: " + lti.sorted.index.toVec.toSeq.reverse.mkString(" > "))
}
