import datetime

def convert_long_to_datetime(timestamp_long):
    # Convert long (milliseconds) to a UTC datetime object
    timestamp_utc = datetime.datetime.fromtimestamp(timestamp_long / 1000.0)

    # Split the formatted string to include only milliseconds, ensuring only 3 digits are shown for milliseconds
    formatted_time = timestamp_utc.strftime('%d.%m.%Y %H:%M:%Ss')

    # Extract milliseconds and add it to the string in the correct format
    milliseconds = int((timestamp_long % 1000))  # Get the remaining milliseconds part
    return f"{formatted_time}.{milliseconds:03d}ms"


def convert_long_to_simple_date_format(timestamp_long):
    # Convert long (milliseconds) to a UTC datetime object
    timestamp_utc = datetime.datetime.fromtimestamp(timestamp_long / 1000.0)

    return timestamp_utc.strftime('%d.%m.%Y %Hh:%Mm')