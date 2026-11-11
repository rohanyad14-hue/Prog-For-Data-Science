//> using scala 2.13.12
//> using dep io.github.pityka::saddle-core:4.0.0-M14
// Sample answer M4-Q2 (Saddle part): organise the patient records on one machine with Series and Frames
import org.saddle._
import org.saddle.ops.BinOps._

object HospitalSaddle {
  def main(args: Array[String]): Unit = {
    val ids = Index("P101", "P102", "P103", "P104")
    val age = Vec(45.0, 32.0, 58.0, 29.0)
    val bp = Vec(130.0, 120.0, 145.0, 118.0)
    val diabetes = Vec(1.0, 0.0, 1.0, 0.0)                            // Yes = 1, No = 0

    println("--- a Series is one labelled column, a Frame is a table of them ---")
    val bpSeries = Series(bp, ids)
    println(bpSeries)
    val frame = Frame("Age" -> Series(age, ids), "BP" -> Series(bp, ids), "Diabetes" -> Series(diabetes, ids))
    println(frame)
    println(frame.numRows + " rows x " + frame.numCols + " columns, columns: " + frame.colIx.toVec.toSeq)

    println("--- summary statistics (a Series has no mean, so go through .values) ---")
    println(f"mean BP ${bpSeries.values.mean}%.1f, max BP ${bpSeries.values.max.get}%.0f, mean age ${age.mean}%.1f")

    println("--- abnormal records ---")
    println("BP >= 140 (stage 2 hypertension range): " + bpSeries.filter(_ >= 140.0).index.toVec.toSeq)
    val highRisk = bp.find(_ >= 130.0).toSeq.intersect(diabetes.find(_ == 1.0).toSeq).toArray     // positions that satisfy both conditions
    println("diabetes and BP >= 130: " + ids.take(highRisk).toVec.toSeq)
    println(f"mean BP with diabetes ${bp.take(diabetes.find(_ == 1.0).toArray).mean}%.1f, without ${bp.take(diabetes.find(_ == 0.0).toArray).mean}%.1f")
    println("sorted by BP: " + bpSeries.sorted.index.toVec.toSeq)
  }
}
