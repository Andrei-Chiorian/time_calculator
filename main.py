def switch_half_day(start_half_day, count_days):
    """
    Switch from AM to PM, or PM to AM and increment count_days if necessary

    Args:
        start_half_day (str): Either 'AM' or 'PM'
        count_days (int): Number of days to increment if switching from PM to AM

    Returns:
        tuple: (str, int) A tuple containing the new half day and the updated count of days
    """
    # Switch from AM to PM
    if start_half_day == 'AM':
        start_half_day = 'PM'
    else:
        # Switch from PM to AM
        start_half_day = 'AM'
        # Increment the count of days
        count_days += 1

    return start_half_day, count_days


def count_minutes(start_minutes, duration_minutes, duration_hours):
    """
    Count the minutes in the new time by adding the start minutes and duration minutes.
    If the result is greater than or equal to 60, subtract 60 from the result and increment the duration hours.
    This is because we want to count hours in the duration hours, but want the minutes to wrap around to 0-59.

    Args:
        start_minutes (int): The minutes in the start time
        duration_minutes (int): The minutes in the duration
        duration_hours (int): The hours in the duration

    Returns:
        tuple: (int, int) A tuple containing the new minutes and the updated duration hours
    """
    # Add the start minutes and the duration minutes
    result_minutes = start_minutes + duration_minutes
    # If the minutes are greater than or equal to 60, subtract 60 from the result and increment the duration hours
    if result_minutes >= 60:
        result_minutes -= 60
        duration_hours += 1
    # Return the result
    return result_minutes, duration_hours


def count_hours(start_hours, duration_hours, start_half_day):
    """
    Count the hours in the new time by adding the start hours and duration hours.
    If the result is greater than or equal to 12, switch from AM to PM or PM to AM as necessary and count the days.
    This is because we want to count days and want the hours to wrap around to 0-11.

    Args:
        start_hours (int): The hours in the start time
        duration_hours (int): The hours in the duration
        start_half_day (str): The half day of the start time, either 'AM' or 'PM'

    Returns:
        tuple: (int, str, int) A tuple containing the new hours, the new half day, and the count of days
    """
    # Initialize the result hours and the count of days
    result_hours = start_hours + duration_hours
    count_days = 0

    # Loop until the hours are less than 12
    while result_hours >= 12:
        # Switch from AM to PM or PM to AM and increment the count of days if necessary
        start_half_day, count_days = switch_half_day(start_half_day, count_days)
        # Subtract 12 from the hours to wrap them around to 0-11
        result_hours -= 12

    # Return the result
    return result_hours, start_half_day, count_days


def add_time(start, duration, start_day=None):
    """
    Add a duration of time to a start time and return the new time.
    If the start time has a day, the new time will have the same day.
    If the duration is greater than 24 hours, the new time will have the correct day.
    """
    # List of days of the week
    days_of_week = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
    ]

    # Store the index of the start day in the list of days of the week
    start_day_index = None

    # If the start time has a day, store the index of the day in the list of days of the week
    if start_day is not None:
        start_day = start_day.lower()
        start_day_index = days_of_week.index(start_day)

    # Parse the start time into hours, minutes, and half day
    start_hours = int(start.split(' ')[0].split(':')[0])
    start_minutes = int(start.split(' ')[0].split(':')[1])
    start_half_day = start.split(' ')[1]

    # Parse the duration into hours and minutes
    duration_hours = int(duration.split(':')[0])
    duration_minutes = int(duration.split(':')[1])

    # Count minutes and hours
    # result_minutes is the sum of the start minutes and the duration minutes
    # duration_hours is the sum of the start hours and the duration hours minus the number of hours that the minutes exceeded 60
    result_minutes, duration_hours = count_minutes(start_minutes, duration_minutes, duration_hours)
    # result_hours is the sum of the start hours and the duration hours minus the number of hours that the minutes exceeded 60
    # result_half_day is the new half day after switching from AM to PM or PM to AM if the hours exceeded 12
    # count_days is the number of days that the hours exceeded 12
    result_hours, result_half_day, count_days = count_hours(start_hours, duration_hours, start_half_day)

    # Correct formatting for hours
    # If the result hours is 0, convert it to 12 for AM
    if result_hours == 0:
        result_hours = 12

    # Checking the current day
    # If the start time has a day, store the index of the day in the list of days of the week
    result_day_index = start_day_index
    if count_days > 0 and start_day is not None:
        # If the duration is greater than 24 hours, the new time will have the correct day
        result_day_index = (start_day_index + count_days) % len(days_of_week)

    # Format new time
    # Use string formatting to create the new time string
    # Include the day if the start time has a day
    new_time = f"{result_hours}:{str(result_minutes).zfill(2)} {result_half_day}{', ' + days_of_week[result_day_index].capitalize() if start_day is not None else ''}"

    # Determine new day
    # If the duration is greater than 24 hours, the new time will have the correct day
    if count_days > 0:
        # If the duration is greater than 24 hours, the new time will have the correct day
        total_days_later = f" ({count_days} days later)" if count_days > 1 else " (next day)"
        return new_time + total_days_later

    return new_time


# Test the function
result = add_time('3:30 PM', '2:12')  # should return '5:42 PM
result1 = add_time('11:55 AM', '3:12')  # should return '3:07 PM'
result2 = add_time('2:59 AM', '24:00')  # should return '2:59 AM (next day)'
result3 = add_time('11:59 PM', '24:05')  # should return '12:04 AM (2 days later)'
result4 = add_time('8:16 PM', '466:02')  # should return '6:18 AM (20 days later)'
result5 = add_time('3:30 PM', '2:12', 'Monday')  # should return '5:42 PM, Monday'
result6 = add_time('2:59 AM', '24:00', 'saturDay')  # should return '2:59 AM, Sunday (next day)'
result7 = add_time('11:59 PM', '24:05', 'Wednesday')  # should return '12:04 AM, Friday (2 days later)'
result8 = add_time('8:16 PM', '466:02', 'tuesday')  # should return '6:18 AM, Monday (20 days later)'

print(result)
print(result1)
print(result2)
print(result3)
print(result4)
print(result5)
print(result6)
print(result7)
print(result8)