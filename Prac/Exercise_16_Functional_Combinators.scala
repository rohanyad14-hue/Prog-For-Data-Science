package lab.exercises

/**
 * Exercise 16: Exploring Advanced Functional Combinators Beyond the Basic Set
 * 
 * Objectives:
 * 1. Create a list of integers from 1 to 10.
 * 2. Use filter to get even numbers.
 * 3. Use map to multiply each element by 3.
 * 4. Use flatMap to create a list of tuples (integer, square).
 * 5. Use foldLeft to calculate the product of all elements.
 */
object Exercise16_Functional_Combinators {

  def main(args: Array[String]): Unit = {
    println("==================================================")
    println("   EXERCISE 16: ADVANCED FUNCTIONAL COMBINATORS")
    println("==================================================")

    // 1. Initial list 1 to 10
    val numbers: List[Int] = (1 to 10).toList
    println(s"Original List: $numbers")

    // 2. filter for even numbers
    val evens = numbers.filter(_ % 2 == 0)
    println(s"\n1. filter (Evens): $evens")

    // 3. map (* 3)
    val timesThree = numbers.map(_ * 3)
    println(s"2. map (* 3):     $timesThree")

    // 4. flatMap (x -> (x, x^2))
    val tuples = numbers.flatMap(x => List((x, x * x)))
    println(s"3. flatMap:       $tuples")

    // 5. foldLeft for product
    val totalProduct = numbers.foldLeft(1L)(_ * _)
    println(s"4. foldLeft (Product): $totalProduct")

    println("==================================================")
  }
}
