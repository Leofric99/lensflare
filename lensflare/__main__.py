from . import location
from . import weather
from . import predict
from . import graph
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

    open_meteo_forecast_7days, sunrise_sunset_times_7days = weather.open_meteo_hourly_forecast_7days(latitude, longitude)

    while True:
        
        selected_condition = condition_menu()

        if selected_condition is None:
            continue
        if selected_condition == "rain":
            graph.rain(open_meteo_forecast_7days)

        elif selected_condition == "mist":
            mist, readable_result = predict.mist(open_meteo_forecast_7days)
            if mist:
                print("\nMist is predicted on:\n")
                for item in readable_result:
                    print(item)

        elif selected_condition == "fog":
            fog = predict.fog(open_meteo_forecast_7days)
            if fog:
                print(json.dumps(fog, indent=4))
        
    




if __name__ == "__main__":
    main()