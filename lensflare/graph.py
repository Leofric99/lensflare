from datetime import datetime
import matplotlib.pyplot as plt


def rain(predicted):
    # Extract weekday and hour labels, precipitation, and probability
    times = []
    for item in predicted:
        date_str = f"{item['date']} {item['time']}"
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H")
        times.append(dt.strftime("%A %H:%M"))
    precipitation = [item.get('precipitation', 0.0) for item in predicted]
    probability = [item.get('precipitation_probability', 0.0) for item in predicted]

    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Day and Hour')
    ax1.set_ylabel('Precipitation (mm)', color=color)
    ax1.bar(times, precipitation, color=color, alpha=0.6, label='Precipitation')
    ax1.tick_params(axis='y', labelcolor=color)

    # Show only a subset of x-ticks for readability
    step = max(1, len(times)//12)
    ax1.set_xticks(times[::step])
    ax1.set_xticklabels(times[::step], rotation=45, ha='right')

    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Probability (%)', color=color)
    ax2.plot(times, probability, color=color, marker='o', label='Probability')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(0, 100)

    plt.title('Predicted Precipitation and Probability')
    fig.tight_layout()
    plt.show()