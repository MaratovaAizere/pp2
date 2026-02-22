#Task 1
from datetime import datetime, timedelta

today = datetime.now()
new_date = today - timedelta(days=5)

print("Bugin:", today)
print("5 kun buryn:", new_date)

#Task 2
from datetime import datetime, timedelta

today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Keshe:", yesterday)
print("Bugin:", today)
print("Erten:", tomorrow)

#Task 3
from datetime import datetime

now = datetime.now()
without_microseconds = now.replace(microsecond=0)

print("Original:", now)
print("Without microseconds:", without_microseconds)


#Task 4
from datetime import datetime

date1 = datetime(2026, 2, 20, 10, 0, 0)
date2 = datetime(2026, 2, 21, 10, 0, 0)

difference = date2 - date1

print("Difference in seconds:", difference.total_seconds())

