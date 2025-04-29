# Extract timing features from raw keystroke event batch

def extract_keystroke_features(keystroke_data):
    hold_times = []
    flight_times = []
    last_release = None

    for event in keystroke_data['events']:
        hold = event.get('hold_time')
        if hold is not None:
            hold_times.append(hold)
        if last_release is not None and 'down_time' in event:
            flight = event['down_time'] - last_release
            flight_times.append(flight)
        if 'up_time' in event:
            last_release = event['up_time']

    # Filter out None values before averaging
    avg_hold = sum(hold_times) / len(hold_times) if hold_times else 0
    avg_flight = sum(flight_times) / len(flight_times) if flight_times else 0

    return [avg_hold, avg_flight]
