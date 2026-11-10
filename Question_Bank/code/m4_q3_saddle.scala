//> using scala 2.13.12
//> using dep io.github.pityka::saddle-core:4.0.0-M14
// M4-Q3  Saddle (maintained Scala 2.13 fork; the original org.scala-saddle artifacts on Maven Central stop at Scala 2.11): indexed Vec / Series / Frame (Lab experiments 18 and 20, data part only)
// (the Vegas chart in Lab 18 needs a notebook / browser and is not run here)
import org.saddle._
import org.saddle.ops.BinOps._                          // operator instances (Vec * Vec, ...) in Saddle 4.x

object M4Q3 extends App {
  val fruit = Vec("Apple", "Apple", "Apple", "Banana", "Orange", "Apple")
  val price = Vec(2.40, 2.65, 2.50, 1.20, 1.80, 3.10)
  val qty = Vec(120.0, 110.0, 140.0, 250.0, 180.0, 130.0)
  val date = Index("2023-10-01", "2023-10-02", "2023-10-03", "2023-10-01", "2023-10-02", "2023-10-04")

  val isApple = fruit.map(_ == "Apple")                 // boolean mask
  val appleLocs = isApple.find(identity).toArray        // positions where the mask is true
  val applePrice = price.take(appleLocs)
  println("apple prices     : " + applePrice.toSeq.mkString(", "))
  println(f"average apple    : ${applePrice.mean}%.4f")

  // Series = values + an index (labels); here the index is the date
  val s = Series(price, date)
  println("Series at 2023-10-02:\n" + s.filterAt(i => i == 1 || i == 4))

  // Frame = table of aligned columns
  val frame = Frame("Price" -> price, "Qty" -> qty)
  val revenue = frame.firstCol("Price").toVec * frame.firstCol("Qty").toVec   // vectorised column arithmetic
  println("frame shape      : " + frame.numRows + " rows x " + frame.numCols + " cols")
  println("revenue column   : " + revenue.toSeq.map(v => f"$v%.1f").mkString(", "))

  // missing values are first-class (NA), and statistics skip them
  val withNA = Vec(2.0, Double.NaN, 4.0)                // NaN is Saddle's NA for Double
  println(s"mean with NA     : ${withNA.mean}  (NA skipped), count = ${withNA.count}")
}
