package lab.exercises

/**
 * Exercise 17: Case Classes
 * 
 * Objectives:
 * 1. Define case class Person(name, age, city).
 * 2. List of 5 Person objects.
 * 3. Filter out people older than 30.
 * 4. Group people by city.
 * 5. Format each Person into "Name is Age years old and lives in City".
 * 6. Sort people by age ascending.
 */
case class Person(name: String, age: Int, city: String)

object Exercise17_Case_Classes {

  def filterOutOlderThan30(list: List[Person]): List[Person] = list.filter(_.age <= 30)

  def groupByCity(list: List[Person]): Map[String, List[Person]] = list.groupBy(_.city)

  def formatPeople(list: List[Person]): List[String] = 
    list.map(p => s"${p.name} is ${p.age} years old and lives in ${p.city}")

  def sortByAge(list: List[Person]): List[Person] = list.sortBy(_.age)

  def main(args: Array[String]): Unit = {
    println("==================================================")
    println("          EXERCISE 17: CASE CLASSES")
    println("==================================================")

    val people: List[Person] = List(
      Person("Alice", 25, "New York"),
      Person("Bob", 35, "San Francisco"),
      Person("Charlie", 28, "New York"),
      Person("Diana", 42, "London"),
      Person("Edward", 30, "London")
    )

    println("Original People List:")
    people.foreach(println)

    println("\n1. Filtered (Age <= 30):")
    filterOutOlderThan30(people).foreach(println)

    println("\n2. Grouped by City:")
    groupByCity(people).foreach { case (city, group) =>
      println(s"   $city: ${group.map(_.name).mkString(", ")}")
    }

    println("\n3. Formatted Descriptions:")
    formatPeople(people).foreach(println)

    println("\n4. Sorted by Age:")
    sortByAge(people).foreach(p => println(s"   ${p.name} (${p.age})"))

    println("==================================================")
  }
}
