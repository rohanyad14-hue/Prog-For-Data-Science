"""Sample answer M1-Q2: a weather collector that survives network failures and invalid API answers.
The service is a local stand-in (sa_m1_q2_stub.py); with a real service only BASE_URL (and an API key) changes."""
import json
import os
import statistics
import tempfile
import time

import requests

from sa_m1_q2_stub import start_stub

BASE_URL = start_stub()                       # real life: "https://api.<weather-provider>/v1" and the API key in params or headers


class WeatherError(Exception):
    """Base class: anything that went wrong while collecting weather data."""


class NetworkError(WeatherError):
    """Transient problem (timeout, connection lost, HTTP 5xx): worth retrying."""


class InvalidResponse(WeatherError):
    """The server answered, but the answer cannot be used."""


REQUIRED = {"city": str, "temp_c": (int, float), "humidity": (int, float)}


def validate(data):
    if not isinstance(data, dict):
        raise InvalidResponse("the answer is not a JSON object")
    for key, kind in REQUIRED.items():
        if key not in data:
            raise InvalidResponse(f"missing field '{key}'")
        if not isinstance(data[key], kind):
            raise InvalidResponse(f"field '{key}' has the wrong type")
    if not -60 <= data["temp_c"] <= 60:
        raise InvalidResponse(f"temperature {data['temp_c']} C is impossible")
    return data


def fetch(session, city, retries=2, timeout=1.0):
    """GET one city. Returns (data, number of attempts). Retries only transient problems, with a growing pause."""
    last = None
    for attempt in range(1, retries + 2):
        try:
            resp = session.get(f"{BASE_URL}/weather", params={"city": city}, timeout=timeout)
            if resp.status_code >= 500:
                raise NetworkError(f"server error {resp.status_code}")
            resp.raise_for_status()                         # 4xx: our request is wrong, retrying would not help
            try:
                data = resp.json()
            except ValueError:
                raise InvalidResponse("the answer is not JSON") from None
            return validate(data), attempt
        except (requests.ConnectionError, requests.Timeout) as e:
            last = NetworkError(type(e).__name__)
        except NetworkError as e:
            last = e
        except requests.HTTPError as e:
            raise WeatherError(f"HTTP {e.response.status_code}") from e
        time.sleep(0.2 * attempt)                           # back-off before the next attempt
    raise last


cities = ["Chennai", "Mumbai", "Delhi", "Bengaluru", "Atlantis", "Brokenville", "Nulltown", "Hotville", "Slowtown"]
results, failures = {}, {}                                  # dictionaries: city -> reading, city -> reason
with requests.Session() as session:
    for city in cities:
        try:
            data, attempts = fetch(session, city)
            results[city] = data
            print(f"{city:<12} ok after {attempts} attempt(s): {data['temp_c']} C, humidity {data['humidity']}%")
        except InvalidResponse as e:
            failures[city] = f"invalid response: {e}"
        except NetworkError as e:
            failures[city] = f"network problem: {e}"
        except WeatherError as e:
            failures[city] = f"request rejected: {e}"
        if city in failures:
            print(f"{city:<12} FAILED, {failures[city]}")

temps = {c: d["temp_c"] for c, d in results.items()}
lines = [f"Cities requested : {len(cities)}", f"Successful       : {len(results)}", f"Failed           : {len(failures)}",
         f"Average temp     : {statistics.mean(temps.values()):.1f} C",
         f"Hottest / coldest: {max(temps, key=temps.get)} {max(temps.values())} C / {min(temps, key=temps.get)} {min(temps.values())} C",
         f"Average humidity : {statistics.mean(d['humidity'] for d in results.values()):.1f} %", "Problems:"]
lines += [f"  {c}: {why}" for c, why in failures.items()]

folder = tempfile.mkdtemp(prefix="weather_")
with open(os.path.join(folder, "summary.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
with open(os.path.join(folder, "readings.json"), "w", encoding="utf-8") as f:
    json.dump({"readings": results, "failures": failures}, f, indent=2)
print("\n--- summary.txt, read back from the file ---")
with open(os.path.join(folder, "summary.txt"), encoding="utf-8") as f:
    print(f.read().strip())
print("files written:", sorted(os.listdir(folder)))
