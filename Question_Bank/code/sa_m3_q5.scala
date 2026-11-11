//> using scala 2.13.12
// Sample answer M3-Q5: vehicle monitoring with traits and mixins, driven by an Array of (name, speed) pairs
abstract class Vehicle(val name: String, val speed: Int) {
  def limit: Int = 60                               // city speed limit, km/h
  def status: String = if (speed > limit) "OVERSPEED" else "ok"
}

trait PassengerVehicle {                            // reusable behaviour no. 1
  def seats: Int
  def boarding: String = s"$seats seats"
}

trait EmergencyService extends Vehicle {            // reusable behaviour no. 2
  def siren: String = s"$name: siren ON, right of way"
}

trait HighSpeedVehicle extends Vehicle {            // reusable behaviour no. 3: overrides the limit
  override def limit: Int = 100
}

class Bus(speed: Int) extends Vehicle("Bus", speed) with PassengerVehicle { def seats = 50 }
class Car(speed: Int) extends Vehicle("Car", speed) with PassengerVehicle { def seats = 4 }
class Ambulance(speed: Int) extends Vehicle("Ambulance", speed) with EmergencyService with HighSpeedVehicle
class FireEngine(speed: Int) extends Vehicle("FireEngine", speed) with EmergencyService with HighSpeedVehicle
class Bike(speed: Int) extends Vehicle("Bike", speed)

object Monitor {
  def build(name: String, speed: Int): Vehicle = name match {
    case "Bus" => new Bus(speed)
    case "Car" => new Car(speed)
    case "Ambulance" => new Ambulance(speed)
    case "FireEngine" => new FireEngine(speed)
    case _ => new Bike(speed)
  }

  def main(args: Array[String]): Unit = {
    val data = Array(("Bus", 45), ("Car", 70), ("Ambulance", 90), ("FireEngine", 85), ("Bike", 60))
    val fleet: Array[Vehicle] = data.map { case (n, s) => build(n, s) }

    println("--- real-time check of the whole fleet ---")
    fleet.foreach(v => println(f"${v.name}%-10s ${v.speed}%3d km/h  limit ${v.limit}%3d  ${v.status}"))
    println("overspeeding: " + fleet.filter(_.status == "OVERSPEED").map(_.name).toList)
    println("fastest     : " + fleet.maxBy(_.speed).name)
    println("average     : " + fleet.map(_.speed).sum.toDouble / fleet.length)

    println("--- what each mixin adds ---")
    fleet.foreach {
      case v: EmergencyService => println(v.siren)
      case v: PassengerVehicle => println(v.name + ": " + v.boarding)
      case v => println(v.name + ": no special trait")
    }
    println("emergency vehicles: " + fleet.collect { case v: EmergencyService => v.name }.toList)

    println("--- mixing a trait into one object at creation time ---")
    val police = new Car(80) with EmergencyService with HighSpeedVehicle
    println(police.siren + " | limit " + police.limit + " | " + police.status + " | " + police.boarding)
  }
}
