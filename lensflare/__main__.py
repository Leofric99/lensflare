from . import location
from . import weather
from . import predict
from . import graph
from . import llm
import json

def condition_menu():
    print("\nSelect a weather condition to check:")
    options = [
        ("☀️", "clear_skies"),
        ("🌧️", "rain"),
        ("🌫️", "mist"),
        ("🌁", "fog"),
        ("🌇", "good_sunset"),
        ("🌅", "good_sunrise"),
        ("🌕", "full_moon"),
        ("🌑", "new_moon"),
    ]
    for idx, (emoji, option) in enumerate(options, 1):
        print(f"{idx}. {emoji} {option}")
    print(f"{len(options) + 1}. 🚪 Exit")

    choice = input("\nEnter the number of your choice:\n> ")
    try:
        choice_num = int(choice)
        if choice_num == len(options) + 1:
            print("\nExiting. Goodbye!")
            exit(0)
        selected_condition = options[choice_num - 1][1]
        print(f"\nYou selected: {selected_condition}")
    except (IndexError, ValueError):
        print("\nInvalid selection. Please try again.")
        selected_condition = None

    return selected_condition
    

def main():


    print("=" * 40)
    print("   🌤️  Welcome to Meteo Photo!  🌤️")
    print("=" * 40)
    location_name = input("\n📍 Enter a location to get the weather for:\n> ")

    coordinates = None
    while coordinates is None:
        coordinates = location.get_coordinates(location_name)
        if coordinates is None:
            location_name = input("\n📍 Enter a location to get the weather for:\n> ")
            print()
    latitude, longitude = coordinates

    llm_query = input("\n💬 Enter your query for the weather conditions (next 7 days):\n> ")
    data_list = llm.initial_request(llm_query)

    if llm.check_list_format(data_list).lower() == "yes":

        data_list = json.loads(data_list)
        
        hourly_forecast, daily_forecast = weather.open_meteo_hourly_forecast_7days(latitude, longitude)
        
        for item in data_list:
            if item == "sunrise":
                nice_sunriseset_times = predict.sunset_sunrise(hourly_forecast, daily_forecast)
            elif item == "sunset":
                pass
            elif item == "clear":
                pass
            elif item == "rain":
                pass
            elif item == "mist":
                mist_predicted = predict.mist(hourly_forecast)
            elif item == "fog":
                fog_predicted = predict.fog(hourly_forecast)
            elif item == "snow":
                pass
            elif item == "hail":
                pass
            elif item == "sleet":
                pass
            elif item == "drizzle":
                pass
            elif item == "cloudy":
                pass
            elif item == "wind":
                pass
            elif item == "full_moon":
                pass
            elif item == "new_moon":
                pass
            else:
                pass

        





if __name__ == "__main__":
    main()