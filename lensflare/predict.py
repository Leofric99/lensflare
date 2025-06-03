import json
from datetime import datetime

def mist(open_meteo_forecast_7days):
    result = []
    for entry in open_meteo_forecast_7days:
        rh = entry.get("relative_humidity_2m", 0)
        temp = entry.get("temperature_2m", 0)
        dew = entry.get("dew_point_2m", 0)
        wind = entry.get("wind_speed_10m", 0)
        precipitation = entry.get("precipitation", 1)  # default to 1 to exclude if missing
        precipitation_probability = entry.get("precipitation_probability", 100)  # default to 100 to exclude if missing

        mist_predicted = (
            rh > 80 and
            (temp - dew) <= 3 and
            wind < 8 and
            precipitation < 0.4 and
            precipitation_probability < 20
        )
        if mist_predicted:
            result.append({
                "date": entry.get("date"),
                "time": entry.get("time")
            })

    return result


def fog(open_meteo_forecast_7days):
    result = []
    for entry in open_meteo_forecast_7days:
        rh = entry.get("relative_humidity_2m", 0)
        temp = entry.get("temperature_2m", 0)
        dew = entry.get("dew_point_2m", 0)
        wind = entry.get("wind_speed_10m", 0)
        precipitation = entry.get("precipitation", 1)  # default to 1 to exclude if missing
        precipitation_probability = entry.get("precipitation_probability", 100)  # default to 100 to exclude if missing

        fog_predicted = (
            rh > 90 and
            (temp - dew) <= 2 and
            wind < 5 and
            precipitation < 0.4 and
            precipitation_probability < 20
        )
        if fog_predicted:
            result.append({
                "date": entry.get("date"),
                "time": entry.get("time")
            })

    return result


def sunset_sunrise(hourly_forecast, daily_forecast):

    good_entries = []

    for entry in hourly_forecast:
        cloud_cover = entry.get("cloud_cover", 0)
        cloud_low = entry.get("cloud_cover_low", 0)
        cloud_mid = entry.get("cloud_cover_mid", 0)
        cloud_high = entry.get("cloud_cover_high", 0)
        humidity = entry.get("relative_humidity_2m", 0)
        visibility = entry.get("visibility", 0)
        rain = entry.get("rain", 0)
        showers = entry.get("showers", 0)
        precipitation = entry.get("precipitation", 0)
        temperature = entry.get("temperature_2m", 0)
        dew_point = entry.get("dew_point_2m", 0)
        wind_speed = entry.get("wind_speed_10m", 0)

        # Apply ideal conditions for photo-worthy sky
        if not (30 <= cloud_cover <= 70 or (cloud_low >= 50 and cloud_cover <= 85)):
            continue
        if cloud_high > 30:
            continue
        if humidity > 85:
            continue
        if visibility < 10000:
            continue
        if rain > 0 or showers > 0 or precipitation > 0:
            continue
        if wind_speed > 25:
            continue
        if (temperature - dew_point) < 2:
            continue

        good_entries.append(entry)

    return good_entries
