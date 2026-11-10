package lab.exercises

import org.saddle._
import vegas._
import vegas.render.HTML5._

/**
 * Exercise 18: Saddle and Vegas
 * 
 * Objectives:
 * 1. Use Saddle to load and manipulate fruit dataset (Date, Fruit, Price, Quantity).
 * 2. Filter for apples and calculate average price.
 * 3. Visualize price trend over time using Vegas.
 */
object Exercise18_Saddle_Vegas {

  def main(args: Array[String]): Unit = {
    println("==================================================")
    println("       EXERCISE 18: SADDLE AND VEGAS")
    println("==================================================")

    // 1. Load / Construct Dataset in Saddle
    val dates      = Vec("2023-10-01", "2023-10-02", "2023-10-03", "2023-10-04", "2023-10-05", "2023-10-01", "2023-10-02")
    val fruitNames = Vec("Apple", "Apple", "Apple", "Apple", "Apple", "Banana", "Orange")
    val prices     = Vec(2.40, 2.65, 2.50, 2.90, 3.10, 1.20, 1.80)
    val quantities = Vec(120.0, 110.0, 140.0, 95.0, 130.0, 250.0, 180.0)

    val frame: Frame[Int, String, Any] = Frame(
      "Date"     -> dates,
      "Fruit"    -> fruitNames,
      "Price"    -> prices,
      "Quantity" -> quantities
    )

    println("Original Saddle Frame:")
    println(frame)

    // 2. Filter for Apples and compute average price
    val isApple = frame.col("Fruit").toVec.map(_ == "Apple")
    val appleFrame = frame.filterRows(r => isApple.at(r))
    val applePrices = appleFrame.col("Price").mapValues(_.asInstanceOf[Double]).toVec
    val avgPrice = applePrices.mean

    println("\nFiltered Apple Frame:")
    println(appleFrame)
    println(f"Calculated Average Apple Price: $$${avgPrice}%.2f")

    // 3. Visualize Price Trend Over Time with Vegas
    val applePlotData = Seq(
      Map("Date" -> "2023-10-01", "Price" -> 2.40),
      Map("Date" -> "2023-10-02", "Price" -> 2.65),
      Map("Date" -> "2023-10-03", "Price" -> 2.50),
      Map("Date" -> "2023-10-04", "Price" -> 2.90),
      Map("Date" -> "2023-10-05", "Price" -> 3.10)
    )

    val plot = Vegas("Apple Price Trend Over Time")
      .withData(applePlotData)
      .encodeX("Date", Nom)
      .encodeY("Price", Quant)
      .mark(Line)

    println("\nVegas Plot Specification Successfully Built.")
    println("==================================================")
  }
}
