from mpu6050 import mpu6050
from datetime import datetime
import time
import math
#import numpy
#import matplotlib.pyplot as plt

"""
    Aici voi scrie observatii descoperite legate de librarie, proiect s.a



    raw values = valori brute
    Libraria mpu6050 are deja in metodele ei calibrate valorile pentru temperatura si pentru acceleratiile pe axele x,y,z.
    Pentru moment vreau sa calculez algoritmul potrivit pentru calcularea numarului de pasi si sa functioneze normal.
    As fi vrut sa implementez resetarea numarului de pasi la 0 in momentul cand intram intr-o noua zi(adica la ora: 00:00), dar inca nu stiu.


"""


mpu = mpu6050(0x68) #Adresa pentru senzorul mpu9dof care este mereu 0x68, dar daca nu este aceasta,
#ea poate fi gasita scriind comanda sudo i2cdetect -y 1 in terminal!!
datenow=datetime.now()



x=0 #numarul de iteratii ale programului
steps=0 #numarul de pasi detectati
modulVector=0
prev1Vector=0 #variabila din program care stocheaza distanta vectorului celor 3 axe pentru iteratia curenta
threshold=1.5 #pragul care ne ajuta sa detectam pasii, acesta poate fi setat in functie de cum dorim

prevabsxAcc=0
prevabsyAcc=0
prevabszAcc=0


#Am initializat variabilele ce vor fi acceleratiile pentru fiecare axa
xAccel=0
yAccel=0
zAccel=0

xGyro=0
yGyro=0
zGyro=0
thresholder_accel=10
thresholder_gyro=50.00
while True:
    try:
        x+=1
        print('//////////{} ITERATION!!//////////'.format(x))
        print('\n--------------------')
        try:
            temp=mpu.get_temp()
            print("Temp: {:.3f}".format(temp))
            print('--------------------')
            accel_data = mpu.get_accel_data()
            xAccel=(accel_data['x']) 
            yAccel=(accel_data['y']) 
            zAccel=(accel_data['z'])
        except :
            print('\nS-au deconectat firele de la citirea I2c si nu s-a realizat citirea senzorului!!!!!\n')

        modulVector=math.sqrt(xAccel**2+yAccel**2+zAccel**2)
        #print('Modul vector: {:.5f} '.format(modulVector))
        print('--------------------')
        vect1=modulVector-prev1Vector 
        #modulul vectorului in iteratia curenta minus modulul vectorului in cea anterioara

        #print('Diferenta dintre valoarea distantei vectoriale curente si celei anterioara - vect1: {:.5f} '.format(vect1))
        print('--------------------')
        if(vect1>threshold): #aici verificam daca diferenta celor 2 > un prag care va fi stabilit in functie de sensivitatea de detectie a pasilor
            steps+=1
        if(x==1): #in prima iteratie din while numarul de pasi sa fie 0, adica sa nu porneasca aplicatia cu 1 pas detectat(ceea ce ar fi eronat)
            steps=0
        
        prev1Vector=modulVector
        
        #print('Prev1vector : {:.5f} '.format(prev1Vector))
        print('--------------------')
        absxAcc=abs(xAccel) - prevabsxAcc
        print(absxAcc)
        absyAcc=abs(yAccel) - prevabsyAcc
        print(absyAcc)
        abszAcc=abs(zAccel) - prevabszAcc
        print(abszAcc)



        print("\n")
        prevabsxAcc=abs(xAccel)
        print(prevabsxAcc)
        prevabsyAcc=abs(yAccel)
        print(prevabsyAcc)
        prevabszAcc=abs(zAccel)
        print(prevabszAcc)

        if (abs(xAccel)>thresholder_accel and absxAcc!=0) or (abs(yAccel)>thresholder_accel and absyAcc!=0) or (abs(zAccel)>thresholder_accel and abszAcc!=0):
            print('\nMiscare detectata!!!!!!\n')
        else:
            print('\nNu s-a detectat nimic.\n')

        print("Acc X: {:.5f} m/s^2".format(xAccel))
        print("Acc Y: {:.5f} m/s^2".format(yAccel))
        print("Acc Z: {:.5f} m/s^2".format(zAccel))
        print('--------------------')
        print('Steps: {}'.format(steps))
        print()
        if(x%5==0):
            with open("/home/cezar/Desktop/Cezar_Licenta/RPI_MPU9DOF_AN4/python/steps.txt","a")as f:
                f.write('Steps {}\n'.format(steps))
                f.write('Datenow: {}\n'.format(datenow))
                f.write('Iteratie: {}\n'.format(x))
                f.write('--------------------\n')
                

    
        

        gyro_data = mpu.get_gyro_data()
        xGyro=(gyro_data['x'])
        yGyro=(gyro_data['y'])
        zGyro=(gyro_data['z'])
        #print("Gyro X: {:.5f}rad/s".format(xGyro))
        #print("Gyro Y: {:.5f}rad/s".format(yGyro))
        #print("Gyro Z: {:.5f}rad/s".format(zGyro))
        print()
        print("-------------------------------")
        time.sleep(1)

        
        
        


        

    except KeyboardInterrupt:
        print("\nDone for now to continue editing....\n")
        raise


    