def check_num(num):
    if num == 0:
        return "000"
    if 10 <= num < 100:
        return "0" + str(num)
    if num < 10:
        return "00" + str(num)
    return str(num)