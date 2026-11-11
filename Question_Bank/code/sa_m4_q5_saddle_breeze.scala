//> using scala 2.13.12
//> using dep io.github.pityka::saddle-core:4.0.0-M14
//> using dep org.scalanlp::breeze:2.1.0
// Sample answer M4-Q5 (Saddle and Breeze part): structure and preprocess the loan data, compute statistics and risk indicators
import org.saddle._
import org.saddle.ops.BinOps._
import breeze.linalg.DenseVector
import breeze.stats.{mean, stddev, variance}

object LoanRisk {
  def main(args: Array[String]): Unit = {
    val ids = Index("L101", "L102", "L103", "L104")
    val income = Vec(650000.0, 350000.0, 800000.0, 250000.0)
    val loan = Vec(300000.0, 400000.0, 500000.0, 350000.0)
    val status = Vec("Approved", "Rejected", "Approved", "Rejected")

    println("--- Saddle: labelled, typed structures and preprocessing ---")
    val numbers = Frame("Income" -> Series(income, ids), "Loan" -> Series(loan, ids))
    println(numbers)
    val gap = Vec(650000.0, Double.NaN, 800000.0, 250000.0)                      // an income that was not recorded
    println("missing income filled with the mean: " + gap.fillNA(_ => gap.mean).toSeq)
    val ratio = loan / income                                                      // element-wise division gives a new risk column
    val ratioSeries = Series(ratio, ids)
    println(ratioSeries.mapValues(r => f"$r%.3f"))
    val approved = status.find(_ == "Approved").toArray
    val rejected = status.find(_ == "Rejected").toArray
    println(f"mean loan-to-income: approved ${ratio.take(approved).mean}%.3f, rejected ${ratio.take(rejected).mean}%.3f")
    println("riskiest first: " + ratioSeries.sorted.reversed.index.toVec.toSeq)

    println("--- Breeze: statistics and risk indicators (numerical work on dense vectors) ---")
    val inc = DenseVector(income.toArray)
    val ln = DenseVector(loan.toArray)
    println(f"income: mean ${mean(inc)}%.0f, std dev ${stddev(inc)}%.0f, variance ${variance(inc)}%.3e")
    val lti = ln /:/ inc                                                            // loan-to-income ratio
    val surplus = inc - ln                                                           // income left after the loan amount
    println("loan-to-income : " + lti.toArray.map(v => f"$v%.3f").mkString(", "))
    println("income - loan  : " + surplus.toArray.map(_.toLong).mkString(", "))
    val ic = inc - mean(inc)
    val lc = ln - mean(ln)
    println(f"correlation income~loan ${(ic dot lc) / math.sqrt((ic dot ic) * (lc dot lc))}%.3f, covariance ${(ic dot lc) / (inc.length - 1)}%.3e")
    val zIncome = (inc - mean(inc)) /:/ stddev(inc)
    println("z-scores of income: " + zIncome.toArray.map(z => f"$z%.2f").mkString(", "))
    println("high-risk flag (loan above income): " + lti.toArray.map(_ > 1.0).mkString(", "))
  }
}
