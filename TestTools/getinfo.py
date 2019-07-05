import time


# 当前时间
def get_time():
    now_time = time.strftime("%Y-%m-%d_%H%M%S", time.localtime(time.time()))
    return now_time


# 当前日期
def get_date():
    now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    return now_date


# 根据传参显示对应日期
def get_dates(days=0):
    any_date = time.strftime("%Y-%m-%d", time.localtime(time.time()-60*60*24*int(days)))
    return any_date
