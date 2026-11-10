package lab.exercises

import scala.collection.mutable

/**
 * Exercise 15: Handling Collisions and Resolving Conflicts in HashMaps
 * 
 * Objectives:
 * 1. Create HashMap with student grades, insert duplicate key with different grade.
 * 2. Function to merge two HashMaps taking the higher grade.
 * 3. Function to handle collisions by chaining, using lists to store multiple values.
 */
object Exercise15_HashMap_Collisions {

  // Function to merge two maps and resolve conflicts by taking the max grade
  def mergeResolvingHigherGrade(map1: Map[String, Int], map2: Map[String, Int]): Map[String, Int] = {
    val allKeys = map1.keySet ++ map2.keySet
    allKeys.map { key =>
      val resolved = (map1.get(key), map2.get(key)) match {
        case (Some(g1), Some(g2)) => math.max(g1, g2)
        case (Some(g1), None)     => g1
        case (None, Some(g2))     => g2
        case _                    => 0
      }
      key -> resolved
    }.toMap
  }

  // Function to insert a grade using separate chaining via List[Int]
  def insertWithChaining(map: Map[String, List[Int]], student: String, grade: Int): Map[String, List[Int]] = {
    val existing = map.getOrElse(student, List.empty[Int])
    map + (student -> (existing :+ grade))
  }

  def main(args: Array[String]): Unit = {
    println("==================================================")
    println("   EXERCISE 15: HASHMAP COLLISIONS & CONFLICTS")
    println("==================================================")

    // 1. Basic mutable HashMap showing duplicate overwrite
    val grades = mutable.HashMap[String, Int]("Alice" -> 85, "Bob" -> 78, "Charlie" -> 92)
    println(s"1. Original Grades: $grades")
    grades.put("Alice", 95) // Overwrites previous 85
    println(s"   After inserting duplicate 'Alice' -> 95: $grades")

    // 2. Conflict resolution via higher grade
    val examA = Map("Alice" -> 85, "Bob" -> 90, "David" -> 70)
    val examB = Map("Alice" -> 92, "Bob" -> 80, "Emma" -> 88)
    val merged = mergeResolvingHigherGrade(examA, examB)
    println(s"\n2. Exam A: $examA")
    println(s"   Exam B: $examB")
    println(s"   Merged (Higher Grade): $merged")

    // 3. Chaining with Lists for duplicate keys
    val submissions = Seq(
      ("Alice", 85), ("Bob", 78), ("Charlie", 92),
      ("Alice", 95), ("Bob", 88), ("Alice", 90)
    )
    val chained = submissions.foldLeft(Map.empty[String, List[Int]]) { (acc, item) =>
      insertWithChaining(acc, item._1, item._2)
    }

    println("\n3. Chained Hash Table (All attempts retained):")
    chained.foreach { case (student, scores) =>
      println(s"   -> $student: ${scores.mkString("[", ", ", "]")}")
    }

    println("==================================================")
  }
}
