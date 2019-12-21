class IncorrectLengthException(Exception): #raises an exception when the length is not 11
    def __init__(self):
        super().__init__("The PESEL number must contain 11 symbols")


def pesel_to_date(pesel):
    try:
        if len(str(pesel)) != 11:
            print("Incorrect Length of PESEL number")
            raise IncorrectLengthException


    except ValueError:
        print("The PESEL number can only contain integer numbers!")
        exit(0)

    if pesel[2]=="2" or pesel[2]=="3":
        miesiac=int(pesel[2:4])-20
        miesiac=str(miesiac).zfill(2)
        return "{}-{}-{}".format(int(pesel[0:2]) + 2000, miesiac, pesel[4:6])

    else:
        return "{}-{}-{}".format(int(pesel[0:2]) + 1900, pesel[2:4], pesel[4:6])
