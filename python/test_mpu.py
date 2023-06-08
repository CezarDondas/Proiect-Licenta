from mpu9250 import mpu9250
import time
import math


#Aici am incercat sa detecteze miscare doar atunci cand acceleratia in modul depaseste acel prag setat mai sus cu 10
#dar acea acceleratie de pe fiecare coordonata sa fie diferita in urmatoare iteratie ptr ca daca acceleratia ar fi aceeasi
#fara sa se miste senzorul, aceasta ar detecta miscare desi nu s-a miscat.
"""
    Aici voi scrie observatii descoperite legate de librarie, proiect s.a



    raw values = valori brute
    Libraria mpu6050 are deja in metodele ei calibrate valorile pentru temperatura si pentru acceleratiile pe axele x,y,z.
    Pentru moment vreau sa calculez algoritmul potrivit pentru calcularea numarului de pasi si sa functioneze normal.
    As fi vrut sa implementez resetarea numarului de pasi la 0 in momentul cand intram intr-o noua zi(adica la ora: 00:00), dar inca nu stiu.


"""


mpu = mpu9250(0x68) #Adresa pentru senzorul mpu9dof care este mereu 0x68, dar daca nu este aceasta,
#ea poate fi gasita scriind comanda sudo i2cdetect -y 1 in terminal!!

datenow=time.ctime()

steps=0 #numarul de pasi detectati
threshold=1.2 #pragul care ne ajuta sa detectam pasii, acesta poate fi setat in functie de cum dorim


move=False


#Am initializat variabilele ce vor fi acceleratiile pentru fiecare axa
xAccel=0
yAccel=0
zAccel=0

xGyro=0
yGyro=0
zGyro=0

thresholder_accel=10 #am setat acest prag deoarece g=9.80 si am considerat ca intre 9.81 si 9.99 sa fie o marja de eroare pentru a evita 
#detectarea unei miscari eronate.
#thresholder_gyro=50.00

modulVector=[0.0]*100
diff_mod=[0.0]*100

#v_xAccel=[0.0]*100
v_xAccel=[]
#v_yAccel=[0.0]*100
v_yAccel=[]
#v_zAccel=[0.0]*100
v_zAccel=[]


#v_xGyro=[0.0]*100
v_xGyro=[]
#v_yGyro=[0.0]*100
v_yGyro=[]
#v_zGyro=[0.0]*100
v_zGyro=[]


absxAcc=[0.0]*100
absyAcc=[0.0]*100
abszAcc=[0.0]*100

while True:
    try:
        #x+=1
        #print('//////////{} ITERATION!!//////////'.format(x))
        #print('{}'.format('-'*30))
        for i in range(100):
            print("Iteratie : ", i)
            accel_data = mpu.get_accel_data()
            xAccel=(accel_data['x'])
            v_xAccel.append(xAccel) 
            yAccel=(accel_data['y'])
            v_yAccel.append(yAccel) 
            zAccel=(accel_data['z'])
            v_zAccel.append(zAccel)  

            gyro_data = mpu.get_gyro_data()
            xGyro=(gyro_data['x'])
            v_xGyro.append(xGyro)
            yGyro=(gyro_data['y'])
            v_yGyro.append(yGyro)
            zGyro=(gyro_data['z'])
            v_zGyro.append(zGyro)
            #Odata ce am actualizat codul si am creat un for cu 100 de iteratii, as putea sa calculez numarul de pasi pentru fiecare 100 de valori dinn cele 3 axe si pe baza celor 100
            #sa fac calculele necesare detectarii unui pas si a numarului de rotatii ptr starea somnului.
            #sa ma ajut de functia zip cand creez for, de retinut !!

            modulVector[i]=math.sqrt(v_xAccel[i]*v_xAccel[i]+v_yAccel[i]*v_yAccel[i]+v_zAccel[i]*v_zAccel[i])
            print(modulVector[i])
            diff_mod[i]=modulVector[i]-modulVector[i-1]
            print("diff_mod: \n", diff_mod[i]) 
            


            #Aici am incercat sa detecteze miscare doar atunci cand acceleratia in modul depaseste acel prag setat mai sus cu 10
            #dar acea acceleratie de pe fiecare coordonata sa fie diferita in urmatoare iteratie ptr ca daca acceleratia ar fi aceeasi
            #fara sa se miste senzorul, aceasta ar detecta miscare desi nu s-a miscat.

            absxAcc[i]=abs(v_xAccel[i]) - v_xAccel[i-1]

            print("absxacc: \n",absxAcc[i-1])
            

            absyAcc[i]=abs(v_yAccel[i]) - v_yAccel[i-1]

            print("absyacc: \n",absyAcc[i-1])
            

            abszAcc[i]=abs(v_zAccel[i]) - v_zAccel[i-1]

            print("abszacc: \n",abszAcc[i-1])
            

            print("\n")
            
            

            if (abs(v_xAccel[i])>thresholder_accel and absxAcc[i]!=0) or (abs(v_yAccel[i])>thresholder_accel and absyAcc[i]!=0) or (abs(v_zAccel[i])>thresholder_accel and abszAcc[i]!=0):
                print('\nMiscare detectata!!!!!!\n')
                move=True
                print(move)
            else:
                print('\nNu s-a detectat nimic.\n')
                move=False
                print(move)

            
            

            #am considerat teoria care spune ca pentru a detecta eficient numarul de pasi, trebuie sa ne gandim la tot procesul care exista
            #adica atunci cand se efectueaza un pas, exista o miscare pe verticala(interpretarea prin acceleratia pe axa Y atunci cand talpa piciorului
            # se ridica de la sol si dupa ajunge din nou pe sol)
            #vect1>threshold nu inseamna nimic altceva decat verificarea daca acceleratiile de pe axe s-au modificat de la o iteratie la alta
            #iar variabila move reprezinta confirmarea ca intr-adevar a existat o miscare, dar care nu poate fi catalogata ca un pas
            #pentru moment un algortim mai eficient nu am gasit pentru a detecta in mod corect un pas.
            #as putea imbunatati acest algoritm prin introducerea giroscopului care poate verifica si a doua parte a procesului din mers.
            #interpretarea miscarii tip pendul a picioarelor.
            if(move and diff_mod[i]>threshold): #aici verificam daca diferenta celor 2 > un prag care va fi stabilit in functie de sensivitatea de detectie a pasilor
                steps+=1
                print("Pas detectat!!: \n",steps)
            else:
                print("Numar de pasi actuali: \n",steps)
            
        
            print("Acc X: {:.5f} m/s^2".format(v_xAccel[i]))
            print("Acc Y: {:.5f} m/s^2".format(v_yAccel[i]))
            print("Acc Z: {:.5f} m/s^2".format(v_zAccel[i]))
            print('{}'.format('-'*30))

            
            
            print("Gyro X: {:.5f}rad/s".format(v_xGyro[i]))
            print("Gyro Y: {:.5f}rad/s".format(v_yGyro[i]))
            print("Gyro Z: {:.5f}rad/s".format(v_zGyro[i]))
            print("")

            if i==5:
                for loop in v_xAccel, v_yAccel,v_zAccel:
                    print(loop)
        
            
            
            #print('Steps: {}'.format(steps))
            print()
            if(i%125==0):
                with open("/home/cezar/Desktop/Cezar_Licenta/RPI_MPU9DOF_AN4/python/steps.txt","a")as f:
                    f.write('Steps {}\n'.format(steps))
                    f.write('Datenow: {}\n'.format(datenow))
                    f.write('Iteratie: {}\n'.format(i))
                    f.write('--------------------\n')
                

    
        

        


        #O iteratie efectuata la fiecare 0.000125 secunde
        # (adica o frecventa de 8000Hz precum este mentionat si in documentatia oficiala a senzorului pentru accelerometru si giroscop)
            #time.sleep(0.000125)
            time.sleep(1) #pentru o mai buna observare a citirii datelor senzorului

    except KeyboardInterrupt:
        print("\nDone for now to continue editing....\n")
        raise


    