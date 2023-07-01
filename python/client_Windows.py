
###RULEZ DOAR PE WINDOWS, CHIAR DACA EXISTA SI IN REPO-UL CARE ESTE SI PE RASPBERRY PI!!!
import socket
import time
import math
import json

IP_HOME='192.168.0.59'
IP_AC='192.168.89.37'
PORT=5005

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP_HOME, PORT))

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
threshold=1.2 #pragul care ne ajuta sa detectam pasii, acesta poate fi setat in functie de cum dorim
move=False
thresholder_accel=10

while True:
    try:
        #Primul for este pentru a prelua datele de la server si a crea listele pentru cele 3 axe pentru accelerometru si gyroscop
        #la finalul acestuia vor exista 5 seturi de valori(x,y,z) pe baza carora se vor efectua calculele in al doilea for
        for i in range(5):
            print('Iteratie:',i)

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
                print('\nxyzAccel: ', xyzAccel)
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

        print('Valori afisate in afara buclelor i si j---------------------\n')
        print('xAccel: ',xAccel)
        print('yAccel: ',yAccel)
        print('zAccel: ',zAccel)
        print('xGyro: ',xGyro)
        print('yGyro: ',yGyro)
        print('zGyro: ',zGyro)
        print('-------------------------------------------------------------------------\n')

        #In acest for vom prelucra cele 5 seturi de date (x,y,z), adica vor exista 5 valori pentru fiecare lista a axei
        for j in range(len(xAccel)):
            print(len(xAccel))
            if len(xAccel)==0:
                break
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


        # dupa ce se parcurg ambele for-uri, se vor sterge toate elementele listelor si se va relua procedeul si vom calcula pe baza altor
        # 5 seturi de valori numarul de pasi
        print('Aici se golesc listele pentru alte 5 seturi de valori')
        xAccel.clear()
        yAccel.clear()
        zAccel.clear()
        xGyro.clear()
        yGyro.clear()
        zGyro.clear()

        """
        
                for value in received_from_server.split("[ ]"):
            new_value=value.replace('[','').replace(']','')
            #print('new_value: \n',new_value)
            values=new_value.split(",")
            #print(len(values))
            #print('values: ',values)
            float_accel=([float(n) for n in values])
        """

        #time.sleep(1)
    except socket.error:
        print('Connection abort by server')
    except KeyboardInterrupt:
        print("\nDone for now to continue editing....\n")
        raise

client_socket.close()










    