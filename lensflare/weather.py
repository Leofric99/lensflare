import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

def open_meteo_hourly_forecast_7days(latitude, longitude):

    latitude = round(latitude, 3)
    longitude = round(longitude, 3)

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["sunrise", "sunset"],
        "hourly": ["temperature_2m", "dew_point_2m", "relative_humidity_2m", "rain", "showers", "snowfall", "snow_depth", "surface_pressure", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility", "wind_speed_10m", "wind_gusts_10m", "precipitation", "precipitation_probability"],
        "timezone": "Europe/London",
        "wind_speed_unit": "kn"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_rain = hourly.Variables(3).ValuesAsNumpy()
    hourly_showers = hourly.Variables(4).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(5).ValuesAsNumpy()
    hourly_snow_depth = hourly.Variables(6).ValuesAsNumpy()
    hourly_surface_pressure = hourly.Variables(7).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(8).ValuesAsNumpy()
    hourly_cloud_cover_low = hourly.Variables(9).ValuesAsNumpy()
    hourly_cloud_cover_mid = hourly.Variables(10).ValuesAsNumpy()
    hourly_cloud_cover_high = hourly.Variables(11).ValuesAsNumpy()
    hourly_visibility = hourly.Variables(12).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(13).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(14).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(15).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(16).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["dew_point_2m"] = hourly_dew_point_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["rain"] = hourly_rain
    hourly_data["showers"] = hourly_showers
    hourly_data["snowfall"] = hourly_snowfall
    hourly_data["snow_depth"] = hourly_snow_depth
    hourly_data["surface_pressure"] = hourly_surface_pressure
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
    hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
    hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
    hourly_data["visibility"] = hourly_visibility
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["precipitation_probability"] = hourly_precipitation_probability

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    # Convert DataFrame to list of dicts with date and hour split
    hourly_list = []
    for _, row in hourly_dataframe.iterrows():
        dt = row["date"]
        entry = {
            "date": dt.strftime("%Y-%m-%d"),
            "time": dt.strftime("%H")
        }
        for col in hourly_dataframe.columns:
            if col != "date":
                entry[col] = row[col]
        hourly_list.append(entry)

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_sunrise = daily.Variables(0).ValuesInt64AsNumpy()
    daily_sunset = daily.Variables(1).ValuesInt64AsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}

    daily_data["sunrise"] = daily_sunrise
    daily_data["sunset"] = daily_sunset

    daily_dataframe = pd.DataFrame(data = daily_data)

    # Convert the DataFrame to a list of dicts with formatted values
    daily_list = []
    for _, row in daily_dataframe.iterrows():
        date_str = row["date"].strftime("%Y-%m-%d")
        sunrise_str = pd.to_datetime(row["sunrise"], unit="s", utc=True).strftime("%H:%M")
        sunset_str = pd.to_datetime(row["sunset"], unit="s", utc=True).strftime("%H:%M")
        daily_list.append({
            "date": date_str,
            "sunrise": sunrise_str,
            "sunset": sunset_str
        })

    return hourly_list, daily_list


