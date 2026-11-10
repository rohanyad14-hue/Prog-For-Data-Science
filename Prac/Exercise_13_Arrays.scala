package lab.exercises

/**
 * Exercise 13: Introduction to Arrays in Scala
 * 
 * Objectives:
 * 1. Create an array of integers with values 2, 5, 9, 14, 20.
 * 2. Function to compute and return the sum of its elements.
 * 3. Create an array of strings with five fruit names.
 * 4. Function to concatenate array elements separated by commas.
 * 5. Iterate over the integer array and print each element to the console.
 */
object Exercise13_Arrays {

  // Function to calculate the sum of array elements
  def sumArray(arr: Array[Int]): Int = {
    // arr.sum or arr.foldLeft(0)(_ + _)
    arr.foldLeft(0)(_ + _)
  }

  // Function to concatenate fruits with commas
  def concatenateFruits(fruits: Array[String]): String = {
    fruits.mkString(", ")
  }

  def main(args: Array[String]): Unit = {
    println("==================================================")
    println("      EXERCISE 13: ARRAYS IN SCALA")
    println("==================================================")

    // 1. Create integer array
    val numbers: Array[Int] = Array(2, 5, 9, 14, 20)
    println(s"1. Integer Array: [${numbers.mkString(", ")}]")

    // 2. Sum elements
    val sum = sumArray(numbers)
    println(s"2. Sum of array elements: $sum")

    // 3. Create fruit array
    val fruits: Array[String] = Array("Apple", "Banana", "Cherry", "Mango", "Orange")
    println(s"3. Fruits Array:  [${fruits.mkString(", ")}]")

    // 4. Concatenate fruits
    val concatenated = concatenateFruits(fruits)
    println(s"4. Concatenated String: $concatenated")

    // 5. Iterate and print
    println("5. Iterating over the integer array:")
    numbers.foreach { num =>
      println(s"   -> Element: $num")
    }

    println("==================================================")
  }
}
