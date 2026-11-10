// Notes M3: evaluation strategies, folds, equality, collections and pattern-matching traps (Scala 2.13)
import scala.collection.mutable.{ArrayBuffer, ListBuffer}

object N3Traps extends App {
  println("--- val, var, def, lazy val, call-by-name ---")
  var calls = 0
  def next(): Int = { calls += 1; calls }
  val v = next()                         // evaluated once, now
  def d = next()                         // evaluated at every use
  lazy val l = next()                    // evaluated once, at first use
  println(s"after definitions: calls=$calls")
  println(s"v twice: $v $v | d twice: $d $d | l twice: $l $l | calls=$calls")
  def byValue(x: Int): Int = { println("  byValue body"); x + x }
  def byName(x: => Int): Int = { println("  byName body"); x + x }
  calls = 0; println("byValue(next()) = " + byValue(next()) + " (argument evaluated once, before the body); calls=" + calls)
  calls = 0; println("byName(next())  = " + byName(next()) + " (argument evaluated at each use); calls=" + calls)

  println("\n--- folds: direction matters for non-commutative operations ---")
  val xs = List(1, 2, 3, 4)
  println("foldLeft(0)(_ - _)  = " + xs.foldLeft(0)(_ - _) + "   ((((0-1)-2)-3)-4)")
  println("foldRight(0)(_ - _) = " + xs.foldRight(0)(_ - _) + "    (1-(2-(3-(4-0))))")
  println("reverse via foldLeft  : " + xs.foldLeft(List.empty[Int])((acc, x) => x :: acc))
  println("copy via foldRight    : " + xs.foldRight(List.empty[Int])((x, acc) => x :: acc))
  println("reduce(_ - _) = " + xs.reduce(_ - _) + " | scanLeft(0)(_ + _) = " + xs.scanLeft(0)(_ + _))
  println("reduce on empty list: " + scala.util.Try(List.empty[Int].reduce(_ + _)).failed.get.getClass.getSimpleName + " | fold(0) on empty: " + List.empty[Int].fold(0)(_ + _))

  println("\n--- lists: :: is right-associative, immutability ---")
  println("1 :: 2 :: Nil = " + (1 :: 2 :: Nil) + " | List(1,2) ::: List(3) = " + (List(1, 2) ::: List(3)) + " | List(1,2) :+ 3 = " + (List(1, 2) :+ 3) + " | 0 +: List(1) = " + (0 +: List(1)))
  val ys = List(3, 1, 2)
  println("sorted returns a new list: " + ys.sorted + ", original still " + ys + " | head/tail: " + ys.head + "/" + ys.tail + " | last: " + ys.last)
  val buf = ListBuffer(1, 2); buf += 3; buf.prepend(0)
  println("ListBuffer is mutable: " + buf + " | toList: " + buf.toList)

  println("\n--- equality: == vs eq, arrays ---")
  println("List(1,2) == List(1,2): " + (List(1, 2) == List(1, 2)) + " | Array(1,2) == Array(1,2): " + (Array(1, 2) == Array(1, 2)) + " (arrays compare by reference!)")
  println("Array(1,2).sameElements(Array(1,2)): " + Array(1, 2).sameElements(Array(1, 2)) + " | Array(1,2).toList == Array(1,2).toList: " + (Array(1, 2).toList == Array(1, 2).toList))
  val s1 = new String("hi"); val s2 = new String("hi")
  println(s"strings: s1 == s2 is ${s1 == s2}, s1 eq s2 is ${s1 eq s2}")
  println("Set(1,2) == Set(2,1): " + (Set(1, 2) == Set(2, 1)) + " | Map(1->2) == Map(1->2): " + (Map(1 -> 2) == Map(1 -> 2)) + " | (1,2) == (1,2): " + ((1, 2) == (1, 2)))

  println("\n--- Char vs String conversion trap ---")
  println("\"5\".toInt = " + "5".toInt + " | '5'.toInt = " + '5'.toInt + " (the character code!) | '5'.asDigit = " + '5'.asDigit + " | '5' - '0' = " + ('5' - '0'))
  println("scala.util.Try(\"abc\".toInt).isFailure = " + scala.util.Try("abc".toInt).isFailure + " | \"abc\".toIntOption = " + "abc".toIntOption)
  println("7 / 2 = " + 7 / 2 + " | 7 / 2.0 = " + 7 / 2.0 + " | 7 % 3 = " + 7 % 3 + " | -7 % 3 = " + -7 % 3 + " | Int.MaxValue + 1 = " + (Int.MaxValue + 1) + " | 0.1 + 0.2 = " + (0.1 + 0.2))

  println("\n--- Option instead of null ---")
  val m = Map("a" -> 1)
  println("m.get(\"a\") = " + m.get("a") + " | m.get(\"z\") = " + m.get("z") + " | m(\"a\") = " + m("a") + " | m(\"z\") throws " + scala.util.Try(m("z")).failed.get.getClass.getSimpleName)
  println("chain: Some(4).map(_ * 2).filter(_ > 5) = " + Some(4).map(_ * 2).filter(_ > 5) + " | Some(1).flatMap(x => None: Option[Int]) = " + Some(1).flatMap(x => None: Option[Int]) + " | None.getOrElse(0) = " + None.getOrElse(0))
  val pairs = for { a <- Some(2); b <- Some(3) } yield a * b
  println("for-comprehension over Options: " + pairs + " | with a None inside: " + (for { a <- Some(2); b <- Option.empty[Int] } yield a * b))
  println("for over lists: " + (for { i <- 1 to 3; j <- 1 to 2 if i != j } yield (i, j)).toList)

  println("\n--- pattern matching ---")
  def describe(x: Any): String = x match {
    case 0                       => "zero"
    case n: Int if n < 0         => s"negative int $n"
    case n: Int                  => s"int $n"
    case s: String               => s"string of length ${s.length}"
    case (a, b)                  => s"pair $a,$b"
    case Nil                     => "empty list"
    case head :: tail            => s"list head=$head tail=$tail"
    case Some(inner)             => s"some($inner)"
    case _                       => "something else"
  }
  List(0, -5, 7, "scala", (1, 2), Nil, List(1, 2, 3), Some("x"), 3.5).foreach(x => println("  " + describe(x)))
  val whole @ List(first, _*) = List(9, 8, 7)
  println("binder @ and varargs pattern: whole=" + whole + " first=" + first)
  val (q, r) = (17 / 5, 17 % 5)
  println("tuple destructuring: q=" + q + " r=" + r)

  println("\n--- more collection operations ---")
  val nums = (1 to 10).toList
  println("partition: " + nums.partition(_ % 3 == 0) + " | groupBy(_ % 3): " + nums.groupBy(_ % 3).toList.sortBy(_._1))
  println("zip: " + List(1, 2, 3).zip(List("a", "b")) + " | zipWithIndex: " + List("a", "b").zipWithIndex + " | sliding: " + List(1, 2, 3, 4).sliding(2).toList)
  println("take/drop/takeWhile: " + nums.take(2) + nums.drop(8) + nums.takeWhile(_ < 4) + " | distinct: " + List(1, 1, 2).distinct + " | sortWith: " + List(3, 1, 2).sortWith(_ > _))
  println("1 to 5 = " + (1 to 5) + " | 1 until 5 = " + (1 until 5) + " | by 2: " + (1 to 9 by 4).toList)
  println("mapValues-free word count: " + "to be or not to be".split(" ").groupBy(identity).map { case (w, ws) => w -> ws.length }.toList.sorted)
  println("Set(1,2,2,3) = " + Set(1, 2, 2, 3) + " | & : " + (Set(1, 2, 3) & Set(2, 3, 4)) + " | | : " + (Set(1, 2) | Set(5)) + " | -- : " + (Set(1, 2, 3) -- Set(1)))
  println("Map + new pair, then + same key again (overwrites): " + (Map("a" -> 1) + ("b" -> 2) + ("a" -> 9)))
  println("Array elements are mutable, indexed with (): " + { val a = Array(1, 2, 3); a(0) = 10; a.toList } + " | ArrayBuffer can grow: " + ArrayBuffer(1, 2).+=(3))

  println("\n--- functions: default/named args, varargs, currying, closures ---")
  def greet(name: String, greeting: String = "Hello", punct: String = "!") = s"$greeting, $name$punct"
  println(greet("Asha") + " | " + greet("Ravi", punct = "?") + " | " + greet(greeting = "Hi", name = "Meena"))
  def total(xs: Int*) = xs.sum
  println("varargs: " + total() + " " + total(1, 2, 3) + " " + total(List(4, 5): _*))
  def add(a: Int)(b: Int) = a + b
  val add5 = add(5) _
  println("curried: add(2)(3) = " + add(2)(3) + " | add5(10) = " + add5(10))
  var factor = 2
  val times = (x: Int) => x * factor
  factor = 10
  println("closure sees the variable, not a copy: times(3) = " + times(3))
  val compose = ((_: Int) + 1) andThen ((_: Int) * 2)
  println("andThen composes functions left to right: (5 + 1) * 2 = " + compose(5))
  println("Unit value: " + (()) + " | Any holds anything: " + List[Any](1, "a", 2.0, true) + " | Nothing: throw has type Nothing: " + scala.util.Try(throw new Exception("x")).isFailure)
}
