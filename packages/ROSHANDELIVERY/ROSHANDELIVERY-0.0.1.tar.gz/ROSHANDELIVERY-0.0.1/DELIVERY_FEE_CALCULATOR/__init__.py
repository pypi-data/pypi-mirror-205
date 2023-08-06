
def deilvery_fee(address,total):
    if address=="D01":
        total=total+1
    elif address=="D02":
        total=total+2
    elif address=="D03":
        total=total+3
    elif address=="D04":
        total=total+4
    elif address=="D05":
        total=total+5
    else:
        total=total+10 
    return total