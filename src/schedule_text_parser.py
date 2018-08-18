import re

def parse_sch_text(text):

    regex = re.compile("[/]schedule")
    resp = regex.sub("", text)

    # Clock
    clk_time = re.findall(r"((\d+):(\d+))", resp)

    hours = "*"
    minutes = "*"

    if len(clk_time) == 1:
        clk_time = clk_time[0]
        hours = clk_time[1]
        minutes = clk_time[2]
    else:
        clk_time = "*"

    # Month
    month = re.findall(r"((J|j)an(uary)?|(F|f)eb(ruary)?|(M|m)ar(ch)?|(A|a)pr(il)?|(M|m)ay|(J|j)un(e)?|(J|j)ul(y)?|(A|a)ug(ust)?|(S|s)ep(tember)?|(O|o)ct(ober)?|(N|n)ov(ember)?|(D|d)ec(ember)?)", resp)

    if len(month) != 0:
        month = month[0][0]
    else:
        month = "*"

    # Day of month
    m_day = re.findall(r"(\d+)\s", resp)

    if len(m_day) != 0:
        m_day = m_day[0]
    else:
        m_day = "*"

    # Day of week
    w_day = re.findall(r"((M|m)on(day)?|(T|t)ue(sday)?|(W|w)ed(nesday)?|(T|t)hu(rday)?|(F|f)ri(day)?|(S|s)un(day)?)", resp)

    if len(w_day) != 0:
        w_day = w_day[0][0]
    else:
        w_day = "*"

    return dict({ "hour" : hours, "minute" : minutes, "month" : month, "month-day" : m_day, "week-day" : w_day })
