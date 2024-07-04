import datetime
import pickle
from twilio.rest import Client

# Twilio credentials
account_sid = 'AC7572309f88cf990986aed84455684634'
auth_token = 'b45d1d9721a3ec19b0ea05af8b1921e5'
client = Client(account_sid, auth_token)

# Load existing reminders from file
try:
    with open('reminder.dat', 'rb') as f:
        data = pickle.load(f)
except (FileNotFoundError, EOFError):
    data = []

def send_twilio_msg(to_phone, message_body):
    from_phone = '+13307526641'  # Twilio phone number

    # Sending the message
    message = client.messages.create(
        body=message_body,
        from_=from_phone,
        to=to_phone
    )
    return f"Message sent with SID: {message.sid}"

def generate_reminder_times(times_in_hhmm, days, till_date, message):
    # Ensure times are in string format
    times_in_hhmm = [str(time).zfill(4) for time in times_in_hhmm]

    # Mapping of week names to their corresponding weekday numbers
    day_name_to_weekday = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6
    }

    def parse_days(days):
        days = days.lower()
        specific_days = set()

        if days == 'everyday':
            specific_days.update(range(7))  # All days of the week
        elif ' to ' in days:
            start_day, end_day = days.split(' to ')
            start_index = day_name_to_weekday[start_day]
            end_index = day_name_to_weekday[end_day]
            if start_index <= end_index:
                specific_days.update(range(start_index, end_index + 1))
            else:
                specific_days.update(range(start_index, 7))
                specific_days.update(range(0, end_index + 1))
        elif ' and ' in days:
            parts = days.split(' and ')
            for part in parts:
                if part == 'weekends':
                    specific_days.update({5, 6})
                elif part == 'weekdays':
                    specific_days.update({0, 1, 2, 3, 4})
                else:
                    specific_days.update({day_name_to_weekday[part]})
        else:
            if days == 'weekdays':
                specific_days.update({0, 1, 2, 3, 4})
            elif days == 'weekends':
                specific_days.update({5, 6})
            else:
                specific_days.update({day_name_to_weekday[days]})

        return specific_days

    try:
        days.lower()
        days_is_str = True
    except AttributeError:
        days_is_str = False

    if days_is_str:
        specific_days = parse_days(days)
    else:
        specific_days = set()
        for day in days:
            specific_days.update(parse_days(day))

    # Parse till_date
    try:
        till_date = datetime.datetime.strptime(till_date, '%Y-%m-%d').date()
    except ValueError as e:
        print(f"Error parsing till_date: {e}")
        return

    # Start from today
    start_date = datetime.date.today()
    current_date = start_date

    reminder_times = []

    while current_date <= till_date:
        if current_date.weekday() in specific_days:
            for time_str in times_in_hhmm:
                hour = int(time_str[:2])
                minute = int(time_str[2:])
                reminder_time = datetime.datetime.combine(current_date, datetime.time(hour=hour, minute=minute))
                reminder_times.append(reminder_time)
        current_date += datetime.timedelta(days=1)

    now = datetime.datetime.now()
    while reminder_times and reminder_times[0] < now:
        reminder_times.pop(0)

    data.append((reminder_times,message))
    with open('reminder.dat','wb') as f:
        pickle.dump(data,f)
    return data[-1]

