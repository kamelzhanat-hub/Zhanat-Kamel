import datetime
from datetime import timedelta

# task 1

x = datetime.datetime.now() 
five_days = timedelta(days=5)
result_date = x - five_days
print(result_date.strftime("%c"))

# task 2

one_day = timedelta(days=1)
today = datetime.datetime.now()
tomorrow = today + one_day
yesterday = today - one_day
print(yesterday.strftime("%c"))
print(today.strftime("%c"))
print(tomorrow.strftime("%c"))

# task 3

date = datetime.datetime.now()
without_microseconds = date.replace(microsecond=0)
print(without_microseconds)

# task 4

now = datetime.datetime.now()
future_date = datetime.datetime(2027, 1, 1, 0, 0)
difference = future_date - now
seconds_diff = difference.total_seconds()
print(f"{seconds_diff}")