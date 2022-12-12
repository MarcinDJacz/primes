import datetime
def is_prime(p):
    time1 = datetime.datetime.now()#czas
    if p % 2 == 0:
        print("Nonprime number, divided by %s" % (2))
        return False
    else:
        x = 1
        counter = 0
        square = int(p**(1/2))
        while x <= square:
                x += 2
                counter += 1
                if p % x == 0:
                        print("Nonprime number, divided by %s" % (x))
                        print("Calculate in ", (datetime.datetime.now()-time1))
                        return False                                
        else:
                print("Prime number!")
                print("Calculate in ", (datetime.datetime.now()-time1))
                return True

def Read(file_name):
    f = open(file_name)
    text = f.readline()
    text2 = text.split()
    for x in range(len(text2)):
        text2[x] = int(text2[x])
    f.close()
    return text2

def More_Legible(number):
    real_range = str(number)
    dl = len(real_range) - 3
    while dl > 0:
        real_range = real_range[:dl] + '_' + real_range[dl:]
        dl -= 3
    return real_range

def Order_of_magnitude(number):
    str_number = str(number)
    long = len(str_number)
    what = ''
    if long > 30:
        what = 'Quintilions or more!'
    elif long > 27:
        what = 'Quadrilliards'
    elif long > 24:
        what = 'Quadrillions'
    elif long > 21:
        what = 'Trylliards'
    elif long > 18:
        what = 'Tryllions'
    elif long > 15:
        what = 'Billiards'
    elif long > 12:
        what = 'Bilions'
    else:
        what = 'Miliards or less. Weakly...'
    return what
