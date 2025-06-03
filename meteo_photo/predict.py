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

    formatted = []
    for item in result:
        date_str = item["date"]
        hour_str = item["time"].zfill(2)
        dt = datetime.strptime(f"{date_str} {hour_str}", "%Y-%m-%d %H")
        day = dt.strftime("%A")
        day_num = dt.day
        # Suffix for day
        if 4 <= day_num <= 20 or 24 <= day_num <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day_num % 10 - 1]
        month = dt.strftime("%B")
        year = dt.year
        time_str = dt.strftime("%H:00")
        formatted.append(f"{day} {day_num}{suffix} {month} at {time_str}")
    readable_result = formatted

    return result, readable_result


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