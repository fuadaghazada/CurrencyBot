from crontab import CronTab
from crontab import CronSlices


# Cron

cron = CronTab(user=True)


# Set cron

def schedule_cron(currency, chat_id, sch_data):

    job = cron.new(command='/usr/bin/python3 /root/CurrencyBot/CurrencyBot/src/send_scheduled_message.py {} {}'.format(chat_id, currency))

    hours = sch_data["hour"]
    minutes = sch_data["minute"]
    month = sch_data["month"]
    m_day = sch_data["month-day"]
    w_day = sch_data["week-day"]

    if month:
        month = month[:3]

    if w_day:
        w_day = w_day[:3]

    # Cron string
    crn_str = "{} {} {} {} {}".format(minutes, hours, m_day, month, w_day)

    # Validity check
    if CronSlices.is_valid(crn_str):
        job.setall(crn_str)
        cron.write()
        return True
    else:
        return False



# List the schedules for user

def list_schedules(chat_id):

    sch_list = []

    for sch in cron:
        if str(chat_id) in str(sch):
            result = str(sch).split(" ")
            sch_list.append("Remove schedule for " + result[len(result) - 1])

    return sch_list


# Removes the given schedule from crontab

def remove_schedule(text, chat_id):

    currency = str(text).split(" ")
    currency = currency[len(currency) - 1]

    for sch in cron:
        if str(chat_id) in str(sch) and str(currency) in str(sch):
            cron.remove(sch)

            cron.write()
            return True

    return False


# Checks if the schedule with given parameters already exists

def exist_schedule(currency, chat_id):

    for sch in cron:
        if str(chat_id) in str(sch) and str(currency) in str(sch):
            return True

    return False
