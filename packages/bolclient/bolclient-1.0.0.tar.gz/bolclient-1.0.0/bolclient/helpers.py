from datetime import datetime, timedelta


def get_last_month_period():
    today = datetime.now().today()
    first_of_month = today.replace(day=1)
    last_month = first_of_month - timedelta(days=1)
    last_month_days = int(last_month.strftime("%d"))
    first_of_previous_month = first_of_month - timedelta(days=last_month_days)
    return first_of_previous_month, last_month
