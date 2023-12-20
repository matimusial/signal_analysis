import math
import matplotlib.pyplot as plt
import numpy as np
from functions import *



def no_disturbes(int_array):

    print("kod przed wizytą w cyrku:")
    print(int_array)

    segmenty = podziel_na_4(int_array)          # dzieli tablice na segmenty po 4

    siodemki_a = []     
    siodemki = []
    for i in range(len(segmenty)-1):
        siodemki_a.append(hamming74(segmenty[i][:]))        #dodaje do tablicy tablice po hammingu

    for i in range(len(siodemki_a)):
        for j in range(len(siodemki_a[0])):
            siodemki.append(siodemki_a[i][j])       #skleja wszystko w jedna tablice

    mod = modulacja(siodemki)           # moduluje ciag bitow
    ask = mod[0]
    psk = mod[1]
    fsk = mod[2]
    fn = mod[3]
    fn1 = mod[4]
    fn2 = mod[5]
    time = mod[6]
    tbp = mod[7]

    demodulacja = demodulator_ask(ask, fn, time, tbp)       #demoduluje sygnal ask
    #demodulacja = demodulator_psk(psk, fn, time, tbp)       #demoduluje sygnal psk
    #demodulacja = demodulator_fsk(fsk, fn1, fn2, time, tbp)       #demoduluje sygnal fsk

    kod_wyjsciowy = to_bit(demodulacja, tbp)        #przeksztalca probki na kod binarny

    czworki_a = podziel_na_7(kod_wyjsciowy)     #dzieli na segmenty 7 bitow
    czworki = []
    kod = []

    for i in range(len(czworki_a)-1):
        czworki.append(dekoder74(czworki_a[i][:]))      #dekoduje z 7 bitow na 4 bity

    for i in range(len(czworki)):
        for j in range(len(czworki[0])):
            kod.append(czworki[i][j])       #skleja wszystko


    print("kod po wizycie w cyrku:")
    print(kod)


def disturbes_sep(int_array):

    segmenty = podziel_na_4(int_array)          # dzieli tablice na segmenty po 4

    siodemki_a = []     
    siodemki = []
    for i in range(len(segmenty)-1):
        siodemki_a.append(hamming74(segmenty[i][:]))        #dodaje do tablicy tablice po hammingu

    for i in range(len(siodemki_a)):
        for j in range(len(siodemki_a[0])):
            siodemki.append(siodemki_a[i][j])       #skleja wszystko w jedna tablice

    mod = modulacja(siodemki)           # moduluje ciag bitow
    ask = mod[0]
    psk = mod[1]
    fsk = mod[2]
    fn = mod[3]
    fn1 = mod[4]
    fn2 = mod[5]
    time = mod[6]
    tbp = mod[7]

    zaklocenia = np.random.uniform(-1, 1, size=len(mod[0]))

    #alfa

    alfa = np.arange(0,2.1,0.1)
    ber_a_ask = []
    ber_a_psk = []
    ber_a_fsk = []


    for i in range(0,21):

        disturbed_ask = zaklocenia_alfa(ask, list(alfa)[i],list(zaklocenia))
        disturbed_psk = zaklocenia_alfa(psk, list(alfa)[i],list(zaklocenia))
        disturbed_fsk = zaklocenia_alfa(fsk, list(alfa)[i],list(zaklocenia))

        demodulacja_ask = demodulator_ask(disturbed_ask, fn, time, tbp)
        demodulacja_psk = demodulator_psk(disturbed_psk, fn, time, tbp)
        demodulacja_fsk = demodulator_fsk(disturbed_fsk, fn1,fn2, time, tbp)

        final_ask = to_bit(demodulacja_ask, tbp)        #przeksztalca probki na kod binarny
        final_psk = to_bit(demodulacja_psk, tbp)
        final_fsk = to_bit(demodulacja_fsk, tbp)

        
        #dla ask

        czworki_a = podziel_na_7(final_ask)     #dzieli na segmenty 7 bitow
        czworki = []
        kod_ask = []

        for i in range(len(czworki_a)-1):
            czworki.append(dekoder74(czworki_a[i][:]))      #dekoduje z 7 bitow na 4 bity

        for i in range(len(czworki)):
            for j in range(len(czworki[0])):
                kod_ask.append(czworki[i][j])       #skleja wszystko

        #dla psk

        czworki_a = podziel_na_7(final_psk)     
        czworki = []
        kod_psk = []

        for i in range(len(czworki_a)-1):
            czworki.append(dekoder74(czworki_a[i][:]))      

        for i in range(len(czworki)):
            for j in range(len(czworki[0])):
                kod_psk.append(czworki[i][j])       


        #dla fsk

        czworki_a = podziel_na_7(final_fsk)     
        czworki = []
        kod_fsk = []

        for i in range(len(czworki_a)-1):
            czworki.append(dekoder74(czworki_a[i][:]))      

        for i in range(len(czworki)):
            for j in range(len(czworki[0])):
                kod_fsk.append(czworki[i][j])       

        ber_a_ask.append(fun_ber(int_array,kod_ask))
        ber_a_psk.append(fun_ber(int_array,kod_psk))
        ber_a_fsk.append(fun_ber(int_array,kod_fsk))

    plt.title('Zaklocenia alfa')
    plt.plot(alfa,ber_a_ask, c='red', label="ASK")
    plt.plot(alfa,ber_a_psk, c='blue', label="PSK")
    plt.plot(alfa,ber_a_fsk, c='green', label="FSK")
    plt.legend()
    plt.show()


    mod = modulacja(siodemki)
    ask = mod[0]
    psk = mod[1]
    fsk = mod[2]
    fn = mod[3]
    fn1 = mod[4]
    fn2 = mod[5]
    time = mod[6]
    tbp = mod[7]


    #beta

    beta = np.arange(0,21,1)

    ber_b_ask = []
    ber_b_psk = []
    ber_b_fsk = []


    for i in range(0,21):

        disturbed_ask = zaklocenia_beta(ask, list(beta)[i],time)
        disturbed_psk = zaklocenia_beta(psk, list(beta)[i],time)
        disturbed_fsk = zaklocenia_beta(fsk, list(beta)[i],time)

        demodulacja_ask = demodulator_ask(disturbed_ask, fn, time, tbp)
        demodulacja_psk = demodulator_psk(disturbed_psk, fn, time, tbp)
        demodulacja_fsk = demodulator_fsk(disturbed_fsk, fn1,fn2, time, tbp)

        final_ask = to_bit(demodulacja_ask, tbp)        #przeksztalca probki na kod binarny
        final_psk = to_bit(demodulacja_psk, tbp)
        final_fsk = to_bit(demodulacja_fsk, tbp)



        #dla ask

        czworki_a = podziel_na_7(final_ask)     #dzieli na segmenty 7 bitow
        czworki = []
        kod_ask = []

        for i in range(len(czworki_a)-1):
            czworki.append(dekoder74(czworki_a[i][:]))      #dekoduje z 7 bitow na 4 bity

        for i in range(len(czworki)):
            for j in range(len(czworki[0])):
                kod_ask.append(czworki[i][j])       #skleja wszystko



        #dla psk

        czworki_a = podziel_na_7(final_psk)     
        czworki = []
        kod_psk = []

        for i in range(len(czworki_a)-1):
            czworki.append(dekoder74(czworki_a[i][:]))      

        for i in range(len(czworki)):
            for j in range(len(czworki[0])):
                kod_psk.append(czworki[i][j])       


        #dla fsk

        czworki_a = podziel_na_7(final_fsk)     
        czworki = []
        kod_fsk = []

        for i in range(len(czworki_a)-1):
            czworki.append(dekoder74(czworki_a[i][:]))      

        for i in range(len(czworki)):
            for j in range(len(czworki[0])):
                kod_fsk.append(czworki[i][j])       

        ber_b_ask.append(fun_ber(int_array,kod_ask))
        ber_b_psk.append(fun_ber(int_array,kod_psk))
        ber_b_fsk.append(fun_ber(int_array,kod_fsk))

    plt.title('Zaklocenia beta')
    plt.plot(alfa,ber_b_ask, c='red', label="ASK")
    plt.plot(alfa,ber_b_psk, c='blue', label="PSK")
    plt.plot(alfa,ber_b_fsk, c='green', label="FSK")
    plt.legend()
    plt.show()


def disturbes_mult(int_array):

    segmenty = podziel_na_4(int_array)          # dzieli tablice na segmenty po 4

    siodemki_a = []     
    siodemki = []
    for i in range(len(segmenty)-1):
        siodemki_a.append(hamming74(segmenty[i][:]))        #dodaje do tablicy tablice po hammingu

    for i in range(len(siodemki_a)):
        for j in range(len(siodemki_a[0])):
            siodemki.append(siodemki_a[i][j])       #skleja wszystko w jedna tablice

    mod = modulacja(siodemki)           # moduluje ciag bitow
    ask = mod[0]
    psk = mod[1]
    fsk = mod[2]
    fn = mod[3]
    fn1 = mod[4]
    fn2 = mod[5]
    time = mod[6]
    tbp = mod[7]

    zaklocenia = np.random.uniform(-1, 1, size=len(mod[0]))

    

    alfa = np.arange(0,2.1,0.1)
    beta = np.arange(0,21,1)

    ber_ask_a = []
    ber_psk_a = []
    ber_fsk_a = []

    ber_ask_b = []
    ber_psk_b = []
    ber_fsk_b = []

    # alfa + beta

    for i in range(0,21):
        for j in range(0,21):

            disturbed_ask_a = zaklocenia_alfa(ask, list(alfa)[i],list(zaklocenia))
            disturbed_psk_a = zaklocenia_alfa(psk, list(alfa)[i],list(zaklocenia))
            disturbed_fsk_a = zaklocenia_alfa(fsk, list(alfa)[i],list(zaklocenia))

            disturbed_ask = zaklocenia_beta(disturbed_ask_a, list(beta)[j], time)
            disturbed_psk = zaklocenia_beta(disturbed_psk_a, list(beta)[j],time)
            disturbed_fsk = zaklocenia_beta(disturbed_fsk_a, list(beta)[j],time)

            demodulacja_ask = demodulator_ask(disturbed_ask, fn, time, tbp)
            demodulacja_psk = demodulator_psk(disturbed_psk, fn, time, tbp)
            demodulacja_fsk = demodulator_fsk(disturbed_fsk, fn1,fn2, time, tbp)

            final_ask = to_bit(demodulacja_ask, tbp)        #przeksztalca probki na kod binarny
            final_psk = to_bit(demodulacja_psk, tbp)
            final_fsk = to_bit(demodulacja_fsk, tbp)

        
            #dla ask

            czworki_a = podziel_na_7(final_ask)     #dzieli na segmenty 7 bitow
            czworki = []
            kod_ask = []

            for i in range(len(czworki_a)-1):
                czworki.append(dekoder74(czworki_a[i][:]))      #dekoduje z 7 bitow na 4 bity

            for i in range(len(czworki)):
                for j in range(len(czworki[0])):
                    kod_ask.append(czworki[i][j])       #skleja wszystko

            #dla psk

            czworki_a = podziel_na_7(final_psk)     
            czworki = []
            kod_psk = []

            for i in range(len(czworki_a)-1):
                czworki.append(dekoder74(czworki_a[i][:]))      

            for i in range(len(czworki)):
                for j in range(len(czworki[0])):
                    kod_psk.append(czworki[i][j])       


            #dla fsk

            czworki_a = podziel_na_7(final_fsk)     
            czworki = []
            kod_fsk = []

            for i in range(len(czworki_a)-1):
                czworki.append(dekoder74(czworki_a[i][:]))      

            for i in range(len(czworki)):
                for j in range(len(czworki[0])):
                    kod_fsk.append(czworki[i][j])       

            ber_ask_a.append(fun_ber(int_array,kod_ask))
            ber_psk_a.append(fun_ber(int_array,kod_psk))
            ber_fsk_a.append(fun_ber(int_array,kod_fsk))

    alfa_g, beta_g = np.meshgrid(alfa, beta)

    # Plot for ASK
    fig_ask = plt.figure(figsize=(8, 6))
    ax_ask = fig_ask.add_subplot(111, projection='3d')
    surf_ask = ax_ask.plot_surface(alfa_g, beta_g, np.array(ber_ask_a).reshape(alfa_g.shape), cmap='viridis')
    ax_ask.set_xlabel('Alpha', fontsize=12)
    ax_ask.set_ylabel('Beta', fontsize=12)
    ax_ask.set_zlabel('BER ASK', fontsize=12)
    ax_ask.set_title('ASK I+II', fontsize=14)

    # Plot for PSK
    fig_psk = plt.figure(figsize=(8, 6))
    ax_psk = fig_psk.add_subplot(111, projection='3d')
    surf_psk = ax_psk.plot_surface(alfa_g, beta_g, np.array(ber_psk_a).reshape(alfa_g.shape), cmap='viridis')
    ax_psk.set_xlabel('Alpha', fontsize=12)
    ax_psk.set_ylabel('Beta', fontsize=12)
    ax_psk.set_zlabel('BER PSK', fontsize=12)
    ax_psk.set_title('PSK I+II', fontsize=14)

    # Plot for FSK
    fig_fsk = plt.figure(figsize=(8, 6))
    ax_fsk = fig_fsk.add_subplot(111, projection='3d')
    surf_fsk = ax_fsk.plot_surface(alfa_g, beta_g, np.array(ber_fsk_a).reshape(alfa_g.shape), cmap='viridis')
    ax_fsk.set_xlabel('Alpha', fontsize=12)
    ax_fsk.set_ylabel('Beta', fontsize=12)
    ax_fsk.set_zlabel('BER FSK', fontsize=12)
    ax_fsk.set_title('FSK I+II', fontsize=14)

    plt.show()



    # beta + alfa

    mod = modulacja(siodemki)           # moduluje ciag bitow
    ask = mod[0]
    psk = mod[1]
    fsk = mod[2]
    fn = mod[3]
    fn1 = mod[4]
    fn2 = mod[5]
    time = mod[6]
    tbp = mod[7]

    for i in range(0,21):

        for j in range(0,21):

            disturbed_ask_a = zaklocenia_beta(ask, list(alfa)[i], time)
            disturbed_psk_a = zaklocenia_beta(psk, list(alfa)[i], time)
            disturbed_fsk_a = zaklocenia_beta(fsk, list(alfa)[i], time)

            disturbed_ask = zaklocenia_alfa(disturbed_ask_a, list(beta)[j],list(zaklocenia))
            disturbed_psk = zaklocenia_alfa(disturbed_psk_a, list(beta)[j],list(zaklocenia))
            disturbed_fsk = zaklocenia_alfa(disturbed_fsk_a, list(beta)[j],list(zaklocenia))

            demodulacja_ask = demodulator_ask(disturbed_ask, fn, time, tbp)
            demodulacja_psk = demodulator_psk(disturbed_psk, fn, time, tbp)
            demodulacja_fsk = demodulator_fsk(disturbed_fsk, fn1,fn2, time, tbp)

            final_ask = to_bit(demodulacja_ask, tbp)        #przeksztalca probki na kod binarny
            final_psk = to_bit(demodulacja_psk, tbp)
            final_fsk = to_bit(demodulacja_fsk, tbp)

        
            #dla ask

            czworki_a = podziel_na_7(final_ask)     #dzieli na segmenty 7 bitow
            czworki = []
            kod_ask = []

            for i in range(len(czworki_a)-1):
                czworki.append(dekoder74(czworki_a[i][:]))      #dekoduje z 7 bitow na 4 bity

            for i in range(len(czworki)):
                for j in range(len(czworki[0])):
                    kod_ask.append(czworki[i][j])       #skleja wszystko

            #dla psk

            czworki_a = podziel_na_7(final_psk)     
            czworki = []
            kod_psk = []

            for i in range(len(czworki_a)-1):
                czworki.append(dekoder74(czworki_a[i][:]))      

            for i in range(len(czworki)):
                for j in range(len(czworki[0])):
                    kod_psk.append(czworki[i][j])       


            #dla fsk

            czworki_a = podziel_na_7(final_fsk)     
            czworki = []
            kod_fsk = []

            for i in range(len(czworki_a)-1):
                czworki.append(dekoder74(czworki_a[i][:]))      

            for i in range(len(czworki)):
                for j in range(len(czworki[0])):
                    kod_fsk.append(czworki[i][j])       

            ber_ask_b.append(fun_ber(int_array,kod_ask))
            ber_psk_b.append(fun_ber(int_array,kod_psk))
            ber_fsk_b.append(fun_ber(int_array,kod_fsk))

    alfa_g, beta_g = np.meshgrid(alfa, beta)

    # Plot for ASK
    fig_ask = plt.figure(figsize=(8, 6))
    ax_ask = fig_ask.add_subplot(111, projection='3d')
    surf_ask = ax_ask.plot_surface(alfa_g, beta_g, np.array(ber_ask_b).reshape(alfa_g.shape), cmap='viridis')
    ax_ask.set_xlabel('Alpha', fontsize=12)
    ax_ask.set_ylabel('Beta', fontsize=12)
    ax_ask.set_zlabel('BER ASK', fontsize=12)
    ax_ask.set_title('ASK II+I', fontsize=14)

    # Plot for PSK
    fig_psk = plt.figure(figsize=(8, 6))
    ax_psk = fig_psk.add_subplot(111, projection='3d')
    surf_psk = ax_psk.plot_surface(alfa_g, beta_g, np.array(ber_psk_b).reshape(alfa_g.shape), cmap='viridis')
    ax_psk.set_xlabel('Alpha', fontsize=12)
    ax_psk.set_ylabel('Beta', fontsize=12)
    ax_psk.set_zlabel('BER PSK', fontsize=12)
    ax_psk.set_title('PSK II+I', fontsize=14)

    # Plot for FSK
    fig_fsk = plt.figure(figsize=(8, 6))
    ax_fsk = fig_fsk.add_subplot(111, projection='3d')
    surf_fsk = ax_fsk.plot_surface(alfa_g, beta_g, np.array(ber_fsk_b).reshape(alfa_g.shape), cmap='viridis')
    ax_fsk.set_xlabel('Alpha', fontsize=12)
    ax_fsk.set_ylabel('Beta', fontsize=12)
    ax_fsk.set_zlabel('BER FSK', fontsize=12)
    ax_fsk.set_title('FSK II+I', fontsize=14)

    plt.show()  

    #wykresy przy pomocy bota gpt

int_array = ASCII("VSDgeeg")
disturbes_mult(int_array)