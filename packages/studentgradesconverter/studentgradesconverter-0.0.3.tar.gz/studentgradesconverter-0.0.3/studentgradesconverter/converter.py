def getGrade(percentage):
    percentage = round(percentage)
    if percentage >= 93:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    elif percentage >= 35:
        return "E"
    else:
        return "F"

def overallPercentage(arr):
    l = len(arr)
    total = 0
    for i in arr:
        total = total + i
    return (round(total)/l)
