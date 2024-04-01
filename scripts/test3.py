from datetime import datetime

date_str = "2024-04-22"
date_obj = datetime.strptime(date_str, "%Y-%m-%d")

if date_obj < datetime.now():
    print("The date is valid and earlier than today.")
else:
    print("The date is not valid or later than today.")