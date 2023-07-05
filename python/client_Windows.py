
###RULEZ DOAR PE WINDOWS, CHIAR DACA EXISTA SI IN REPO-UL CARE ESTE SI PE RASPBERRY PI!!!
import socket
import time
import math
import json
from collections import deque
import statistics
import numpy as np
import matplotlib.pyplot as plt

IP_HOME='192.168.0.59'
IP_AC='192.168.89.37'
PORT=5005

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP_AC, PORT))

#Lista cu acceleratiile de pe x,y,z
xyzAccel=[]
#Lista cu valorile giroscoape de pe x,y,z
xyzGyro=[]

#3 liste diferite cu valori pentru fiecare axa a accelerometrului
xAccel=[]
yAccel=[]
zAccel=[]

#3 liste diferite cu valori pentru fiecare axa a giroscopului
xGyro=[]
yGyro=[]
zGyro=[]

xA=0
yA=0
zA=0

xG=0
yG=0
zG=0

modulVector=[0.0]*5
diff_mod=[0.0]*5



absxAcc=[0.0]*5
absyAcc=[0.0]*5
abszAcc=[0.0]*5

steps=0 #numarul de pasi detectati
sleep_quality=""
threshold=1.2 #pragul care ne ajuta sa detectam pasii, acesta poate fi setat in functie de cum dorim
move=False
thresholder_accel=10

agitation_threshold_g = 5  # pragul pentru deviația standard
agitation_threshold_a = 6.5 #prag determinat experimental in functie de cat este dispersia cand nu exista miscare
rotation_history_g = deque(maxlen=10)
rotation_history_a = deque(maxlen=10)


fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
plt.gcf().canvas.manager.set_window_title('Step detection and sleep quality')
fig.set_size_inches(10,7)


# Creează un vector de timp pentru a reprezenta valorile pe axa x
t = np.arange(0)

# Plotează accelerațiile inițiale
line_xAccel, = ax1.plot(t, xAccel, label='xAccel')
line_yAccel, = ax1.plot(t, yAccel, label='yAccel')
line_zAccel, = ax1.plot(t, zAccel, label='zAccel')
ax1.set_ylabel('Accelerație')

# Plotează valorile giroscopului inițiale
line_xGyro, = ax2.plot(t, xGyro, label='xGyro')
line_yGyro, = ax2.plot(t, yGyro, label='yGyro')
line_zGyro, = ax2.plot(t, zGyro, label='zGyro')
ax2.set_xlabel('Timp')
ax2.set_ylabel('Giroscop')

# Adaugă legenda statică
ax1.legend(loc='upper left')
ax2.legend(loc='upper left')

# Adaugă variabilele x și y cu etichete deasupra fiecărui grafic
ax1.set_title('Accelerometru')
x_text = ax1.text(0.1, 1.1, '', transform=ax1.transAxes, fontsize=7, horizontalalignment='center')
ax2.set_title('Giroscop')
y_text = ax2.text(0.1, 1.1, '', transform=ax2.transAxes, fontsize=7, horizontalalignment='center')

# Afișează graficul rezultat
plt.show(block=False)

# Funcția de gestionare a evenimentelor de închidere a ferestrei
def on_close(event):
    plt.gcf().canvas.mpl_disconnect(cid)  # Deconectează funcția de închidere a ferestrei
    plt.close()  # Închide fereastra graficului
    exit(0)  # Închide programul

# Conectează funcția de gestionare a evenimentelor de închidere a ferestrei
cid = plt.gcf().canvas.mpl_connect('close_event', on_close)


def determine_sleep_quality(xyz_gyro,xyz_accel):

    deviations_gyro = []
    deviations_accel = []



    for _ in range(60):
        #Se adauga in lista de mai jos 60 de valori care reprezinta deviatia standard
        #Pentru cele 3 axe ale giroscopului(vreau sa vad cum difera setul de valori de la o iteratie la alta)
        #Pe aceasta baza putem deduce ca valorile s-au schimbat brusc, adica putem concluziona
        #Ca si miscarile de rotatie au fost efectuate brusc
        deviation_g = statistics.stdev(xyz_gyro)
        deviation_a = statistics.stdev(xyz_accel)

        #Facem acelasi lucru si pentru accelerometru pentru a vedea daca exista miscare transversala in acelasi timp cu cea de rotatie
        deviations_gyro.append(deviation_g)
        deviations_accel.append(deviation_a)


    #Cu aceste valori vom realiza o medie aritmetica
    #Media aritmetica va fi adaugata in lista de mai jos
    avg_deviation_g = statistics.mean(deviations_gyro)
    avg_deviation_a = statistics.mean(deviations_accel)

    print('avg dev gyro: ',avg_deviation_g)
    print('avg dev accel: ',avg_deviation_a)

    #Cea mai mare medie aritmetica fiecarui set de 60 de valori din for-ul de mai sus
    #Va fi luata in calcul si daca va depasi pragul setat inainte de bucla while, vom concluziona ca somnul este agitat/linistit
    #In lista rotation_history se vor adauga maxim 10 elemente, iar cand se ajunge la aceasta dimensiune a listei, cand se va adauga
    #In lista, ultimul element adaugat va suprascrie elementul deja existent.
    #Somnul va fi considerat agitat pana cand acea valoare de maxim care exista in lista, va disparea
    #Adica sa spunem ca max_value_rotation e pe pozitia [9] din lista, trebuie sa se efectueze 10 append-uri pana cand aceasta va disparea.
    #Echivalentul a 10 secunde.
    rotation_history_g.append(avg_deviation_g)
    rotation_history_a.append(avg_deviation_a)
    print('Rotation history gyro: ',rotation_history_g)
    print('Rotation history accel : ',rotation_history_a)


    if (len(rotation_history_g) == rotation_history_g.maxlen and len(rotation_history_a) == rotation_history_a.maxlen)and (max(rotation_history_g) >= agitation_threshold_g and max(rotation_history_g) >= agitation_threshold_a):
        print('max rot hist accel:  ', max(rotation_history_a))
        print('max rot hist gyro: ', max(rotation_history_g))
        return "Somn agitat"

    else:
        print('max rot hist accel:  ', max(rotation_history_a))
        print('max rot hist gyro: ', max(rotation_history_g))
        return "Somn linistit/nu s-a ajuns la numarul maxim de valori!"

while True:
    try:



        #Primul for este pentru a prelua datele de la server si a crea listele pentru cele 3 axe pentru accelerometru si gyroscop
        #la finalul acestuia vor exista 5 seturi de valori(x,y,z) pe baza carora se vor efectua calculele in al doilea for
        for i in range(5):
            print('Iteratie i :',i)

            received_from_server = client_socket.recv(1024).decode()

            if not received_from_server:
                break
            float_list_values = json.loads(received_from_server)

            if len(float_list_values) != 6:
                print("String-ul decodatat nu contine valori care pot fi transformate in float!!\n")
            else:
                for index in range(len(float_list_values)):
                    xyzAccel = float_list_values[:3]
                    xyzGyro = float_list_values[3:]
                #print('\nxyzAccel: ', xyzAccel)
                #print('\nxyzGyro: ', xyzGyro)
            xA = xyzAccel[0]
            yA = xyzAccel[1]
            zA = xyzAccel[2]

            xG = xyzGyro[0]
            yG = xyzGyro[1]
            zG = xyzGyro[2]
            #Liste accelerometru pentru fiecare axa
            xAccel.append(xA)
            yAccel.append(yA)
            zAccel.append(zA)
            #Liste giroscop pentru fiecare axa
            xGyro.append(xG)
            yGyro.append(yG)
            zGyro.append(zG)
        print('\nxyzGyro: ', xyzGyro)
        print('Valori afisate in afara buclelor i si j---------------------\n')
        print('xAccel: ',xAccel)
        print('yAccel: ',yAccel)
        print('zAccel: ',zAccel)
        print('xGyro: ',xGyro)
        print('yGyro: ',yGyro)
        print('zGyro: ',zGyro)
        print('-------------------------------------------------------------------------\n')

        t = np.arange(len(xAccel))
        line_xAccel.set_data(t, xAccel)
        line_yAccel.set_data(t, yAccel)
        line_zAccel.set_data(t, zAccel)
        line_xGyro.set_data(t, xGyro)
        line_yGyro.set_data(t, yGyro)
        line_zGyro.set_data(t, zGyro)

        # Actualizează variabilele x, y și z
        x_text.set_text(f'Numar pasi: {steps}')
        y_text.set_text(f'Calitate somn:\n {sleep_quality}')

        # Ajustează limitele axelor y în funcție de valorile actuale
        ax1.relim()
        ax1.autoscale_view()
        ax2.relim()
        ax2.autoscale_view()

        # Redesenază graficul
        plt.draw()
        plt.pause(0.1)  # Pauză pentru a permite actualizarea graficului


        #In acest for vom prelucra cele 5 seturi de date (x,y,z), adica vor exista 5 valori pentru fiecare lista a axei
        for j in range(len(xAccel)):
            print(len(xAccel))
            modulVector[j]=math.sqrt(xAccel[j]*xAccel[j]+yAccel[j]*yAccel[j]+zAccel[j]*zAccel[j])
            print('modul vector: ',modulVector)
            print('modul_vector[j]: ',modulVector[j])
            print('modul vector [j-1]: ',modulVector[j - 1])
            diff_mod[j] = modulVector[j] - modulVector[j - 1]
            print('Diff_mod[j]: ',diff_mod[j])


            """
            Ceea ce se regaseste mai jos, reprezinta verificarea daca senzorul MPU este intr-adevar in miscare sau nu.
            Daca el este in aceeasi pozitie, desi are valori ale accelerometrului care ar putea determina ca diff_mod[i]>1.2,
            s-ar detecta un pas in mod eronat. Aici verificam daca modulul acceleratiei anterioare si cu cea actuala sunt egale.
            Daca sunt egale, inseamna ca nu exista miscare a senzorului. In cele mai multe cazuri ele vor fi diferite.
            """
            absxAcc[j] = abs(xAccel[j]) - abs(xAccel[j - 1])

            print("absxacc: \n", absxAcc[j])

            absyAcc[j] = abs(yAccel[j]) - abs(yAccel[j-1])

            print("absyacc: \n", absyAcc[j])

            abszAcc[j] = abs(zAccel[j]) - abs(zAccel[j - 1])

            print("abszacc: \n", abszAcc[j])

            print("\n")

            print('Valori citite si afisate in bucla FOR J IN ...**************\n')
            print('xAccel: ', xAccel)
            print('yAccel: ', yAccel)
            print('zAccel: ', zAccel)
            print("*******\n")
            print('xGyro: ', xGyro)
            print('yGyro: ', yGyro)
            print('zGyro: ', zGyro)
            print('*********************************\n')
            #Ca sa se detecteze un pas efectuat, mai intai trebuie sa existe miscare, pentru a exista miscare verificam daca pe oricare dintre axe
            #acceleratia este mai mare decat 9.8(ACC GRAVITATIONALA), pentru a nu crea confuzii, am setat acel prag ca fiind peste 10.
            #am verificat si daca acceleratia de pe fiecare axa in modul este diferita fata de cea anteriora, deoarece sa nu existe riscul de calcul eronat
            #
            if (abs(xAccel[j]) > thresholder_accel and absxAcc[j] != 0) or (abs(yAccel[j]) > thresholder_accel and absyAcc[j] != 0) or (abs(zAccel[j]) > thresholder_accel and abszAcc[j] != 0):
                print('\nMiscare detectata!!!!!!\n')
                move = True
                print(move)
            else:
                print('\nNu s-a detectat nimic.\n')
                move = False
                print(move)
            # am considerat teoria care spune ca pentru a detecta eficient numarul de pasi, trebuie sa ne gandim la tot procesul care exista
            # adica atunci cand se efectueaza un pas, exista o miscare pe verticala(interpretarea prin acceleratia pe axa Y atunci cand talpa piciorului
            # se ridica de la sol si dupa ajunge din nou pe sol)
            # vect1>threshold nu inseamna nimic altceva decat verificarea daca acceleratiile de pe axe s-au modificat de la o iteratie la alta
            # iar variabila move reprezinta confirmarea ca intr-adevar a existat o miscare, dar care nu poate fi catalogata ca un pas
            # pentru moment un algortim mai eficient nu am gasit pentru a detecta in mod corect un pas.
            # as putea imbunatati acest algoritm prin introducerea giroscopului care poate verifica si a doua parte a procesului din mers.
            # interpretarea miscarii tip pendul a picioarelor.

            if (move and diff_mod[j] > threshold):  # aici verificam daca diferenta celor 2 > un prag care va fi stabilit in functie de sensivitatea de detectie a pasilor
                steps += 1
                print("Pas detectat!! \n", steps)
            else:
                print("Numar de pasi actuali: \n", steps)

        if len(xAccel) == 0:
            print("Valori invalide, BREAK!!(Posibil sa fi iesit vreun cablu de la masa sau chiar firele de SCL/SDA\n")
            break
        sleep_quality = determine_sleep_quality(xyzGyro,xyzAccel)
        print(sleep_quality)
        # dupa ce se parcurg ambele for-uri, se vor sterge toate elementele listelor si se va relua procedeul si vom calcula pe baza altor
        # 5 seturi de valori numarul de pasi
        print('Aici se golesc listele pentru alte 5 seturi de valori')
        xAccel.clear()
        yAccel.clear()
        zAccel.clear()
        xGyro.clear()
        yGyro.clear()
        zGyro.clear()
        #time.sleep(1)
    except socket.error:
        print('Connection abort by server')
    except KeyboardInterrupt:
        print("\nDone for now to continue editing....\n")
        raise

client_socket.close()










    