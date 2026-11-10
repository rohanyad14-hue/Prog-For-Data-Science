"""Format-1 rows (Task | Code) for the Scala lab programs 18-25.
Row flags:  "" = statement inside main(), "import" = placed at the top of the file, "top" = declaration placed before the object,
            "skip" = shown in the sheet but not compiled (library unavailable for Scala 2.13).
verify_scala.py assembles each group into one program and runs it with scala-cli.
"""

SGROUPS = []


def sgroup(gid, title, labs, deps, rows, note=""):
    SGROUPS.append({"id": gid, "title": title, "labs": labs, "deps": deps, "rows": rows, "note": note})


sgroup("S1", "Scala collections: arrays, lists, sets, tuples, maps", "Programs 18, 19, 20", [], [
    ("Import for mutable collections", "import scala.collection.mutable", "import"),
    ("Entry point of every lab program", "object Experiment {\n  def main(args: Array[String]): Unit = {\n    // statements go here\n  }\n}", "wrapper"),
    ("Array of integers", "val intArr: Array[Int] = Array(2, 5, 9, 14, 20)"),
    ("Function that returns the sum", "def sumArray(arr: Array[Int]): Int = arr.sum\nval totalSum = sumArray(intArr)\nprintln(s\"Sum of integer array elements: $totalSum\")"),
    ("Array of five fruit names", "val fruitArr: Array[String] = Array(\"Apple\", \"Banana\", \"Cherry\", \"Date\", \"Elderberry\")"),
    ("Function that joins them with commas", "def concatenateFruits(arr: Array[String]): String = arr.mkString(\", \")\nprintln(concatenateFruits(fruitArr))"),
    ("Iterate and print each element", "for (x <- intArr) println(x)\nintArr.foreach(println)\nintArr.zipWithIndex.foreach { case (e, i) => println(s\"Element at index $i: $e\") }"),
    ("Access, update and length (round brackets!)", "println(intArr(0))\nintArr(0) = 99\nprintln(intArr.length)"),
    ("List of the first five primes", "val primes: List[Int] = List(2, 3, 5, 7, 11)"),
    ("Function that squares every element", "def squareList(lst: List[Int]): List[Int] = lst.map(x => x * x)\nprintln(squareList(primes))"),
    ("Set of unique characters of a string", "val charSet1: Set[Char] = \"hello world\".toSet\nval charSet2: Set[Char] = \"world wide web\".toSet"),
    ("Function returning the intersection of two sets", "def setIntersection[T](s1: Set[T], s2: Set[T]): Set[T] = s1 & s2\nprintln(setIntersection(charSet1, charSet2))"),
    ("Union and difference", "println(charSet1 | charSet2)\nprintln(charSet1 -- charSet2)"),
    ("Tuple of Int, String, Boolean", "val rec: (Int, String, Boolean) = (260020, \"Rohan Yadav\", true)\nprintln(rec._1)\nprintln(rec._2)\nprintln(rec._3)"),
    ("Destructure a tuple", "val (regId, name, active) = rec"),
    ("Two maps of grades", "val map1 = Map(\"Rohan\" -> 92, \"Vedant\" -> 88, \"Priya\" -> 84)\nval map2 = Map(\"Rohan\" -> 85, \"Vedant\" -> 95, \"Kalyan\" -> 90)"),
    ("Merge two maps, keep the higher grade", "def mergeResolveMax(m1: Map[String, Int], m2: Map[String, Int]): Map[String, Int] =\n  (m1.keySet ++ m2.keySet).map { k =>\n    k -> Math.max(m1.getOrElse(k, 0), m2.getOrElse(k, 0))\n  }.toMap\nval merged = mergeResolveMax(map1, map2)"),
    ("Print a map sorted by key", "merged.toSeq.sortBy(_._1).foreach { case (k, v) => println(s\"  - $k -> $v\") }"),
    ("Mutable HashMap: a duplicate key overwrites", "val grades = mutable.HashMap(\"Alice\" -> 85, \"Bob\" -> 78)\ngrades.put(\"Alice\", 95)\ngrades(\"Carol\") = 70"),
    ("Collision chaining: a list of values per key", "val multiGradeMap = mutable.Map[String, List[Int]]()\ndef insertChained(name: String, grade: Int): Unit = {\n  val existing = multiGradeMap.getOrElse(name, Nil)\n  multiGradeMap(name) = existing :+ grade\n}\ninsertChained(\"Vedant\", 88)\ninsertChained(\"Vedant\", 95)\nprintln(multiGradeMap)"),
    ("Look up safely", "println(map1.get(\"Rohan\"))\nprintln(map1.getOrElse(\"Zed\", 0))\nprintln(map1.contains(\"Priya\"))"),
], note="Arrays use (i) not [i]; Array/Map/Set literals need no new. A mutable collection needs the import; the default Map and Set are immutable.")

sgroup("S2", "Functional combinators and case classes", "Programs 21, 22", [], [
    ("Case class (defined outside the object)", "case class Person(name: String, age: Int, city: String)", "top"),
    ("Entry point", "object Experiment {\n  def main(args: Array[String]): Unit = {\n    // statements go here\n  }\n}", "wrapper"),
    ("List of integers 1 to 10", "val nums: List[Int] = (1 to 10).toList"),
    ("filter: keep the even numbers", "val evens = nums.filter(x => x % 2 == 0)"),
    ("map: multiply every element by 3", "val tripled = nums.map(x => x * 3)"),
    ("flatMap: pair each integer with its square", "val pairedWithSquare = nums.flatMap(x => List((x, x * x)))"),
    ("foldLeft: product of all elements", "val totalProduct = nums.foldLeft(1)((acc, elem) => acc * elem)\nprintln(totalProduct)"),
    ("More combinators", "println(nums.reduce(_ + _))\nprintln(nums.sum)\nprintln(nums.exists(_ > 9))\nprintln(nums.take(3))\nprintln(nums.partition(_ % 2 == 0))"),
    ("List of Person objects", "val people = List(\n  Person(\"Vedant Nimkar\", 24, \"Mumbai\"),\n  Person(\"Ayush Sharma\", 32, \"Delhi\"),\n  Person(\"Rohan Yadav\", 28, \"Bengaluru\"),\n  Person(\"Priya Patel\", 35, \"Mumbai\"),\n  Person(\"Sneha Reddy\", 22, \"Hyderabad\"))"),
    ("Filter people older than 30", "val olderThan30 = people.filter(_.age > 30)\nolderThan30.foreach(p => println(s\"   - ${p.name} (Age: ${p.age})\"))"),
    ("Group people by city", "val groupedByCity = people.groupBy(_.city)\ngroupedByCity.foreach { case (city, group) => println(s\"   - $city: ${group.map(_.name).mkString(\", \")}\") }"),
    ("Turn each Person into a sentence", "val formatted = people.map(p => s\"${p.name} is ${p.age} years old and lives in ${p.city}\")\nformatted.foreach(println)"),
    ("Sort by age (ascending / descending)", "val sortedByAge = people.sortBy(_.age)\nval oldestFirst = people.sortBy(-_.age)\nsortedByAge.zipWithIndex.foreach { case (p, idx) => println(s\"[Rank ${idx + 1}] ${p.name} (Age ${p.age}, ${p.city})\") }"),
    ("copy, equality and pattern matching", "val older = people.head.copy(age = 25)\nprintln(Person(\"A\", 1, \"X\") == Person(\"A\", 1, \"X\"))\nprintln(people.head match { case Person(n, a, _) if a > 18 => s\"$n is an adult\"; case _ => \"minor\" })"),
], note="Case-class fields are public vals: p.age works, p.age = 30 does not compile. Use copy to change a field.")

sgroup("S3", "Saddle: Vec, Index, Series, Frame (Program 23)", "Program 23", ["io.github.pityka::saddle-core:4.0.0-M14"], [
    ("Import Saddle", "import org.saddle._\nimport org.saddle.ops.BinOps._", "import"),
    ("Entry point", "object Experiment {\n  def main(args: Array[String]): Unit = {\n    // statements go here\n  }\n}", "wrapper"),
    ("Vec of values and an Index of labels", "val prices = Vec(120.50, 125.00, 118.75, 130.25, 128.00)\nval quantities = Vec(45.0, 50.0, 42.0, 55.0, 48.0)\nval dates = Index(\"2026-05-01\", \"2026-05-08\", \"2026-05-15\", \"2026-05-22\", \"2026-05-29\")"),
    ("Series = values + index", "val applePrice = Series(prices, dates)"),
    ("Average price", "val avgPrice = applePrice.values.mean\nprintln(f\"Average Price of Apples: INR $avgPrice%.2f\")"),
    ("Frame of aligned columns", "val frame = Frame(\"Price\" -> prices, \"Qty\" -> quantities)\nprintln(frame.numRows + \" x \" + frame.numCols)"),
    ("Take one column as a Series", "val priceCol = frame.firstCol(\"Price\")"),
    ("Filter by a condition on values", "val expensive = applePrice.filter(_ > 125.0)\nprintln(expensive.index.toVec)"),
    ("Filter rows with a Boolean mask (fruit == Apple)", "val fruit = Vec(\"Apple\", \"Apple\", \"Banana\", \"Apple\", \"Orange\")\nval mask = fruit.map(_ == \"Apple\")\nval applePrices = prices.take(mask.find(identity).toArray)\nprintln(applePrices.mean)"),
    ("Column arithmetic", "val revenue = frame.firstCol(\"Price\").toVec * frame.firstCol(\"Qty\").toVec\nprintln(revenue)"),
    ("Missing values (NaN) are skipped by statistics", "val withNA = Vec(2.0, Double.NaN, 4.0)\nprintln(withNA.mean)\nprintln(withNA.count)"),
    ("Vegas line chart (needs the Vegas library)", "import vegas._\nval plot = Vegas(\"Apple Price Trend Over Time\")\n  .withData(Seq(Map(\"date\" -> \"2026-05-01\", \"price\" -> 120.5), Map(\"date\" -> \"2026-05-08\", \"price\" -> 125.0)))\n  .mark(Line)\n  .encodeX(\"date\", Temporal)\n  .encodeY(\"price\", Quantitative)", "skip"),
], note="Saddle: Series(values, index). The original org.scala-saddle is not published for Scala 2.13 and Vegas has no Scala 2.13 build; these were verified with the maintained fork io.github.pityka (4.0.0-M14).")

sgroup("S4", "Breeze vectors and Plotly.Scala bar chart (Program 24)", "Program 24", ["org.scalanlp::breeze:2.1.0", "org.plotly-scala::plotly-render:0.8.5"], [
    ("Import Breeze", "import breeze.linalg._\nimport breeze.stats._", "import"),
    ("Entry point", "object Experiment {\n  def main(args: Array[String]): Unit = {\n    // statements go here\n  }\n}", "wrapper"),
    ("Names, prices and quantities as DenseVectors", "val fruits = Array(\"Apple\", \"Banana\", \"Orange\", \"Mango\", \"Grape\")\nval prices = DenseVector(120.0, 45.0, 80.0, 150.0, 95.0)\nval quantities = DenseVector(250.0, 600.0, 320.0, 180.0, 210.0)"),
    ("Revenue = price x quantity (element-wise *:*)", "val revenues = prices *:* quantities"),
    ("Total and mean", "val totalGross = sum(revenues)\nval meanRevenue = mean(revenues)"),
    ("Formatted output per fruit", "for (i <- 0 until fruits.length) {\n  println(f\"  ${fruits(i)}%-7s -> INR ${revenues(i)}%,10.2f\")\n}\nprintln(f\"Total Gross Revenue: INR $totalGross%,10.2f\")"),
    ("Dot product, scalar multiplication, addition", "println(prices dot quantities)\nprintln(prices * 2.0)\nprintln(prices + quantities)"),
    ("Spread: standard deviation and variance", "println(stddev(prices))\nprintln(variance(prices))"),
    ("DenseMatrix, transpose, product, solve", "val m = DenseMatrix((2.0, 1.0), (1.0, 3.0))\nprintln(m.t)\nprintln(m * m)\nprintln(m \\ DenseVector(3.0, 5.0))"),
    ("Plotly.Scala imports", "import plotly._, plotly.element._, plotly.layout._", "import"),
    ("Bar trace", "val barTrace = Bar(fruits.toSeq, revenues.toArray.toSeq, name = \"Revenue (INR)\")"),
    ("Layout with title and axis titles", "val plotLayout = Layout(\n  title = \"Total Revenue by Fruit (Breeze & Plotly.Scala)\",\n  xaxis = plotly.layout.Axis(title = \"Fruit Variety\"),\n  yaxis = plotly.layout.Axis(title = \"Total Revenue (INR)\"))"),
    ("Write the interactive HTML chart (also opens it in the browser)", "Plotly.plot(\"fruit_revenue.html\", Seq(barTrace), plotLayout)", "",
     "Plotly.plot(\"fruit_revenue.html\", Seq(barTrace), plotLayout, openInBrowser = false)"),
], note="Breeze 2.1: * and *:* between two DenseVectors are both element-wise (the old :* operator no longer exists); the inner product is dot. variance/stddev are the sample versions (n-1). Plotly.plot also opens the chart in the browser unless openInBrowser = false.")

sgroup("S5", "Spire exact arithmetic with a hand-made statistic (Program 25)", "Program 25", ["org.typelevel::spire:0.18.0"], [
    ("Import Spire", "import spire.math._\nimport spire.implicits._", "import"),
    ("Entry point", "object Experiment {\n  def main(args: Array[String]): Unit = {\n    // statements go here\n  }\n}", "wrapper"),
    ("Price lists", "val prices = Map(\"Apple\" -> List(120.50, 125.00, 118.75, 130.25, 128.00), \"Banana\" -> List(44.00, 48.00, 45.00, 49.00, 45.00))"),
    ("Exact rational numbers", "val r = Rational(1, 10) + Rational(2, 10)\nprintln(r)\nprintln(r == Rational(3, 10))\nprintln(0.1 + 0.2)"),
    ("Exact sum and mean of a price list", "val pList = prices(\"Apple\")\nval n = pList.length\nval spireSum = pList.map(Rational(_)).qsum\nval spireMean = spireSum / n\nprintln(spireMean)\nprintln(spireMean.toDouble)"),
    ("Sample variance and standard deviation", "val variance = pList.map(p => math.pow(p - spireMean.toDouble, 2)).sum / (n - 1)\nval stdDev = math.sqrt(variance)\nprintln(f\"Variance: $variance%.4f  Std dev: $stdDev%.4f\")"),
    ("Table row per fruit", "for ((f, ps) <- prices) {\n  val m = ps.map(Rational(_)).qsum / ps.length\n  println(f\"  $f%-8s ${ps.length}%2d ${m.toDouble}%10.4f\")\n}"),
], note="Rational(1/3) is Rational(0) because 1/3 is integer division; write Rational(1, 3).")
