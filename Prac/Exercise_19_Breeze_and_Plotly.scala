package lab.exercises

import breeze.linalg._
import plotly._
import plotly.element._
import plotly.layout._
import plotly.Plotly._

/**
 * Exercise 19: Breeze and Plotly.Scala
 * 
 * Objectives:
 * 1. Use Breeze to calculate total revenue for each fruit type (Price * Quantity).
 * 2. Create a bar chart using Plotly.Scala to visualize revenues.
 */
object Exercise19_Breeze_Plotly {

  def main(args: Array[String]): Unit = {
    println("==================================================")
    println("      EXERCISE 19: BREEZE AND PLOTLY.SCALA")
    println("==================================================")

    // 1. Data vectors
    val fruits = Seq("Apple", "Banana", "Cherry", "Mango", "Orange")
    val prices = DenseVector(2.50, 1.20, 4.00, 3.50, 2.00)
    val quantities = DenseVector(150.0, 300.0, 80.0, 110.0, 200.0)

    // Breeze vectorized element-wise multiplication:
    val revenues: DenseVector[Double] = prices *:* quantities

    println("Breeze Revenue Calculations:")
    for (i <- fruits.indices) {
      println(f"  ${fruits(i)}%-8s: $$${prices(i)}%.2f * ${quantities(i)}%.0f = $$${revenues(i)}%.2f")
    }

    // 2. Bar Chart with Plotly.Scala
    val trace = Bar(
      x = fruits,
      y = revenues.toArray.toSeq,
      name = "Revenue"
    )

    val layout = Layout(
      title = "Total Fruit Revenue",
      xaxis = Axis(title = "Fruit"),
      yaxis = Axis(title = "Total Revenue ($)")
    )

    Plotly.plot("fruit_revenues.html", Seq(trace), layout)
    println("\nSaved Plotly visualization to 'fruit_revenues.html'.")
    println("==================================================")
  }
}
