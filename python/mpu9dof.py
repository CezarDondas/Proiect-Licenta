from mpu6050 import mpu6050
from datetime import datetime, timedelta
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
datenow=datetime.today()



x=0 #numarul de iteratii ale programului
steps=0 #numarul de pasi detectati
modulVector=0
prev1Vector=0 #variabila din program care stocheaza distanta vectorului celor 3 axe pentru iteratia curenta
threshold=1.5 #pragul care ne ajuta sa detectam pasii, acesta poate fi setat in functie de cum dorim

#Am initializat variabilele ce vor fi acceleratiile pentru fiecare axa
xAccel=0
yAccel=0
zAccel=0

xGyro=0
yGyro=0
zGyro=0
while True:
    try:
        x+=1
        print('//////////{} ITERATION!!//////////'.format(x))
        print('\n--------------------')
        temp=mpu.get_temp()
        print("Temp: {:.3f}".format(temp))
        print('--------------------')

        accel_data = mpu.get_accel_data()
        xAccel=(accel_data['x']) 
        yAccel=(accel_data['y']) 
        zAccel=(accel_data['z'])
        #accel_vec=[xAccel,yAccel,zAccel]
        modulVector=math.sqrt(xAccel**2+yAccel**2+zAccel**2)
        print('Modul vector: {:.5f} '.format(modulVector))
        print('--------------------')
        vect1=modulVector-prev1Vector
        print('Diferenta dintre valoarea distantei vectoriale curente si celei anterioara - vect1: {:.5f} '.format(vect1))
        print('--------------------')
        if(vect1>threshold):
            steps+=1
        if(x==1):
            steps=0
        
        prev1Vector=modulVector
        
        print('Prev1vector : {:.5f} '.format(prev1Vector))
        print('--------------------')


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
        print("Gyro X: {:.5f}".format(xGyro))
        print("Gyro Y: {:.5f}".format(yGyro))
        print("Gyro Z: {:.5f}".format(zGyro))
        print()
        print("-------------------------------")
        time.sleep(1)

        
        
        


        

    except KeyboardInterrupt:
        print("\nDone for now to continue editing....\n")
        raise


    