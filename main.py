import math
import datetime
from bitarray import bitarray
from multiprocessing import Pool
from multiprocessing import Process
'''
autor: Marcin Djaczuk
index: 2 3 4 5 ... 25
liczby: 3 5 7 9 ... 49 : liczba = (2*index-1) - tylko nieparzyste
tab = [0,0,0,0,0,0....] bitarray
'''
def Wczytaj(nazwa_pliku):
    f = open(nazwa_pliku)
    text = f.readline()
    text2 = text.split()
    for x in range(len(text2)):
        text2[x] = int(text2[x])
    return text2

pierwsze = Wczytaj('rata0.txt')#wstępne liczby pierwsze do lekko ponad 100k
pierwsze = pierwsze[1:]
print(f'Wczytano wstępnie {len(pierwsze)} liczb, ostatnia to: {pierwsze[len(pierwsze)-1]}')

#globalne; LEN, pierwsze
def ObliczProces(rata):
    czas1 = datetime.datetime.now()# czas wykonania TEST
    ile_pierwszych = 0
    #pierwszeTYM = []
    temp_tab = LEN * bitarray('0') #Tworzenie bitarray'a do wykreslanki
    if rata == 1:
        ostatni_element = int((pierwsze[-1]+1)/2) #104729 - ostatnia pierwsza we wstepnie wczytanym pliku
    elif rata > 1:
        ostatni_element = (rata-1) *(LEN)
    zakres_p = math.floor(math.sqrt((ostatni_element+LEN)*2) + 1)#pierwiastek z granicy zakresu liczb do wykreslania

    licznik_pierwszych = 0
    wykreslana_liczba = pierwsze[licznik_pierwszych]#wczytaj pierwsza l.p. do wykreslenia
    
    while wykreslana_liczba < zakres_p:
        #ile brakuje - do obliczenia, od której liczby i którego indeksu zacznie się dalszą wykreślankę
        brakuje = (ostatni_element - int((wykreslana_liczba-1)/2)) % wykreslana_liczba
        if brakuje == 0:
            temp_tab[0]=1
        index = wykreslana_liczba - brakuje
        temp_tab[index] = 1
       
        while index < LEN:
            temp_tab[index] = 1
            index += wykreslana_liczba         
        
        licznik_pierwszych += 1
        wykreslana_liczba = pierwsze[licznik_pierwszych]
        
    nazwa_pliku = 'rata' + str(rata) + '.txt'###
    file = open(nazwa_pliku, 'w')###
    #stara_ilosc_pierwszych = len(pierwsze)
    for x in range(len(temp_tab)):
        if temp_tab[x] == 0:
            ile_pierwszych += 1
            liczba = ostatni_element*2+(x*2)+1
            if rata == 1 :#prymitywne rozwiazanie
                if liczba <= (LEN*2):
                    #pierwszeTYM.append(liczba)
                    file.write(str(liczba)+' ')
            else:
                #pierwszeTYM.append(liczba)
                file.write(str(liczba)+' ')
    file.close()
    
    #nowa_ilosc_pierwszych = len(pierwsze)
    czas2 = datetime.datetime.now()#czas wykonania TEST
    print(f'Test: wielkość zmiennej /pierwsze/: {len(pierwsze)}')
    print(f"Rata nr {rata} w czasie{(czas2-czas1)}, dodano {ile_pierwszych} liczb pierwszych")
    #print(f"Pierwsza w bloku: {pierwszeTYM[0]} , ostatnia w bloku: {pierwszeTYM[-1]}")
    print('Ilosc pierwszych w tablicy: ', len(pierwsze))
    print('------------------------------------------------------')
    return 1#pierwszeTYM    

LEN = 100_000_000 #wielkość tablicy w jednym procesie
ILE_RAT = 10 #ile rat jednocześnie w multi ma liczyć
ostatni_element = int((pierwsze[-1]+1)/2) #104729
'''
############################################ test porownawczy - single
czas1 = datetime.datetime.now()#ogólny czas 
for i in range(1,ILE_RAT):
    ObliczProces(i)
czas2 = datetime.datetime.now()#ogólny czas
print(f'Single-process: Obliczenia wykonano w czasie{czas2 - czas1}. Jeden blok(10procesow)')
#print(f'Wielkosc tablicy: {len(pierwszeTEST)}')
# 10 raty PC: Single-process: Obliczenia wykonano w czasie0:02:25.613804. Jeden blok(10procesow) Ryzen 5500 6/12
############################################ koniec testu porownawczego - single
'''
if __name__ == "__main__":
    #zakres obliczen
    od_ilu = 1
    do_ilu = ILE_RAT+1
    p = Pool()
    ile_razy = 10
    plik_nr = 0
    for x in range(ile_razy):       
        czas1 = datetime.datetime.now()#ogólny czas
        p.map(ObliczProces, range(od_ilu , do_ilu))#tu cała magia       
        czas2 = datetime.datetime.now()#ogólny czas

        od_ilu = do_ilu
        do_ilu = do_ilu + ILE_RAT        
        print(f'Blok nr {x+1} - Multi-process: Obliczenia wykonano w czasie{czas2 - czas1}')
        
        #dynamiczne zwiekszanie z wyprzedzeniem listy liczb pierwszych do wykreslenia - działa
        '''
        ostatni_element = (ILE_RAT+1) *(LEN) * (x+3)
        zakres_p = math.floor(math.sqrt((ostatni_element+LEN)*2) + 1)
        if zakres_p > pierwsze[-1]:
            plik_nr += 1
            Nazwa_pliku = 'rata' + str(plik_nr) + '.txt'
            pierwsze.extend(Wczytaj(Nazwa_pliku))
            print('Rozszerzono liste liczb pierwszych do kolejnych obliczeń')
        '''
        #prostsze rozwiazanie, do testow - z kazdym blokiem zwieksz liczby pierwsze
        plik_nr += 1
        Nazwa_pliku = 'rata' + str(plik_nr) + '.txt'
        pierwsze.extend(Wczytaj(Nazwa_pliku))
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        
    # 10 raty PC: Multi-process: Obliczenia wykonano w czasie0:00:35.375089


'''
przy 53-54 racie w multi (blok nr 5) wyrzuca error:

    wykreslana_liczba = pierwsze[licznik_pierwszych]
    IndexError: list index out of range
w pliku 55 wywoluje blad
jest to zakres, przy ktorym pierwiastek z gornego zakresu jest WIEKSZY niz ostatnia liczba pierwsza.
liczby pierwsze sa rozszerzane w linii nr  122 w glownej petli, jednak p.map jakby tego nie czytał.
'''
