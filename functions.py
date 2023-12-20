import math
import matplotlib.pyplot as plt
import numpy as np


def ASCII(string):
    binary_string = ''.join(format(ord(char), '08b') for char in string) # linia z internetu
    int_array = []
    for char in binary_string:
        int_array.append(int(char))
    return int_array

def podziel_na_4(tablica):

    dlugosc = len(tablica)
    

    liczba_segmentow = dlugosc // 4
    

    reszta = dlugosc % 4
    

    segmenty = []
    

    for i in range(liczba_segmentow): 
        segmenty.append(tablica[i * 4 : (i + 1) * 4]) #pobiera wycinek z tablicy
    

    ostatni_segment = tablica[liczba_segmentow * 4 :]   #bierze wycinek do konca
    if reszta > 0:
        ostatni_segment += [0] * (4 - reszta)
    
    segmenty.append(ostatni_segment)
    
    return segmenty

def podziel_na_7(tablica):

    dlugosc = len(tablica)
    

    liczba_segmentow = dlugosc // 7
    

    reszta = dlugosc % 7
    

    segmenty = []
    

    for i in range(liczba_segmentow):
        segmenty.append(tablica[i * 7 : (i + 1) * 7])
    

    ostatni_segment = tablica[liczba_segmentow * 7 :]
    if reszta > 0:
        ostatni_segment += [0] * (7 - reszta)
    
    segmenty.append(ostatni_segment)
    
    return segmenty

def hamming74(input):
    bity = input

    if len(bity)!=4:return

    kod = [0]*7
    kod[2]=bity[0]
    kod[4]=bity[1]
    kod[5]=bity[2]
    kod[6]=bity[3]
    
    #x1
    x = (kod[2]+kod[4])%2
    kod[0] = (x+kod[6])%2
    #x2
    x = (kod[2]+kod[5])%2
    kod[1]=(x+kod[6])%2
    #x3
    x = (kod[4]+kod[5])%2
    kod[3]=(x+kod[6])%2

    return kod

def dekoder74(kod):

    #wybierz bit do zamiany
    bit = 0
    if (bit > 7 and bit <1):
        if kod[bit-1]==0:
            kod[bit-1]=1
        elif kod[bit-1]==1:
            kod[bit-1]=0



    #x1
    x = (kod[2]+kod[4])%2
    x1p = (x+kod[6])%2
    #x2
    x = (kod[2]+kod[5])%2
    x2p=(x+kod[6])%2
    #x4
    x = (kod[4]+kod[5])%2
    x4p=(x+kod[6])%2
    #x1d
    x1d = (kod[0]+x1p)%2
    #x2d
    x2d = (kod[1]+x2p)%2
    #x4d
    x4d = (kod[3]+x4p)%2
    oszukany_bit = x1d*1+x2d*2+x4d*4
    if oszukany_bit != 0:
        if kod[oszukany_bit-1]==0:
            kod[oszukany_bit-1]=1
        elif kod[oszukany_bit-1]==1:
            kod[oszukany_bit-1]=0

    result = [0]*4
    result[0] = kod[2]
    result[1] = kod[4]
    result[2] = kod[5]
    result[3] = kod[6]

    return result

def modulacja(int_array):
    A1 = 0.5
    A2 = 1
    w = 2
    m = len(int_array)
    tc = 1
    fs = 2500
    N = round(tc*fs)
    tb = tc/m
    fn = w*(1/tb)
    fn1 = (w+1)/tb
    fn2 = (w+2)/tb
    tbp = round(fs*tb)
    
    za, zp, zf, time = [],[],[],[]
    
    for n in range(m):
        for i in range(tbp):
            t = i/fs
            time.append(n*tb+t)
            if int_array[n] == 0: 
                za.append(A1*math.sin(2*math.pi*fn*t))
                zp.append(math.sin(2*math.pi*t*fn))
                zf.append(math.sin(2*math.pi*fn1*t))
                
            elif int_array[n]==1:
                za.append(A2*math.sin(2*math.pi*fn*t))
                zp.append(math.sin(2*math.pi*fn*t+math.pi))
                zf.append(math.sin(2*math.pi*fn2*t))
    
    #plt.plot(time,za)
    #plt.show()
    return (za, zp, zf, fn, fn1, fn2, time, tbp)

def to_bit(ct, tbp):
    bity = []
    znaki_ascii = []
    for i in range(0, len(ct), tbp):
        segment = ct[i:i+tbp]
        zeros = segment.count(0)    #liczy zera w liscie
        ones = segment.count(1)     #liczy jedynki w liscie
        if zeros > ones:
            bity.append(0)
        else:
            bity.append(1)

    return bity

def demodulator_ask(za, fn, time, tbp): #dziala
    xt = []
    a = 0
    pt = []
    ct = []
    for n in range(0,len(za)): xt.append(za[n]*math.sin(2*math.pi*fn*time[n]))
        
    for n in range(0,len(xt)):
        a += xt[n]
        pt.append(a)
        if n%tbp == 0:a = 0
   
    x = 0
    for i in range(len(pt)):
        x+=pt[i]

    h = x/len(pt)

    for n in range(0,len(pt)):
        if (float(pt[n])>h):ct.append(1)
        else:ct.append(0)
    
    #plt.plot(time,ct)
    #plt.show()
    return ct

def demodulator_psk(zp, fn, time, tbp):

    xt = []
    a = 0
    pt = []
    ct = []
    for n in range(0,len(zp)): xt.append(zp[n]*math.sin(2*math.pi*fn*time[n]))
        
    for n in range(0,len(xt)):
        a += xt[n]
        pt.append(a)
        if n%tbp == 0:a = 0
    
    for n in range(0,len(pt)):
        if (float(pt[n])<0):ct.append(1)
        else:ct.append(0)
    
    #plt.plot(time,ct)
    #plt.show()
    return ct

def demodulator_fsk(zf, fn1, fn2, time, tbp):

    x1t = []
    x2t = []
    a1 = 0
    a2 = 0
    pt1 = []
    pt2 = []
    ct = []
    pt = []
    for n in range(0,len(zf)): x1t.append(zf[n]*math.sin(2*math.pi*fn1*time[n]))
    for n in range(0,len(zf)): x2t.append(zf[n]*math.sin(2*math.pi*fn2*time[n]))
        
    for n in range(0,len(x1t)):
        a1 += x1t[n]
        pt1.append(a1)
        if n%tbp == 0:a1 = 0
        a2 += x2t[n]
        pt2.append(a2)
        if n%tbp == 0:a2 = 0
   
    for n in range(0,len(pt1)):
        pt.append(pt2[n]-pt1[n])
    
    for n in range(0,len(pt)):
        if (float(pt[n])>0):ct.append(1)        #zmienilem znak 
        else:ct.append(0)
    
    
    #plt.plot(time,ct)
    #plt.show()
    return ct

def fun_ber(array1,array2):
    blad = 0
    for i in range(len(array1)):
        if (array1[i]!=array2[i]):
            blad = blad + 1
    
    stopa = blad/len(array1) * 100

    return stopa

def zaklocenia_alfa(array, alfa, zaklocenia):

    for i in range(len(array)):
        array[i] = array[i]+zaklocenia[i] * alfa

    return array

def zaklocenia_beta(array, beta, time):

    for i in range(len(array)):
        array[i] = array[i]*math.exp(-beta*time[i]*50)  #podkrecilem

    return array