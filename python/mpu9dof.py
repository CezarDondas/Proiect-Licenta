from mpu6050 import mpu6050
import time
import math
mpu = mpu6050(0x68)

x=0
steps=0
prev1Vector=0
prev2Vector=0
threshold=1.2
datenow=time.ctime()
while True:
    try:
        x+=1
        print('//////////{} iteration//////////'.format(x))
        print('\n--------------------')
        print("Temp : "+str(mpu.get_temp()))
        print('--------------------')

        accel_data = mpu.get_accel_data()
        xAccel=accel_data['x']
        yAccel=accel_data['y']
        zAccel=accel_data['z']
        modulVector=math.sqrt(xAccel**2+yAccel**2+zAccel**2)
        print('Modul vector: {} '.format(modulVector))
        print('--------------------')

        vect1=modulVector-prev1Vector
        vect2=modulVector-prev2Vector
        print('Diferenta dintre valoarea distantei vectoriale curente si celei anterioara - vect1: {} '.format(vect1))
        print('Diferenta dintre valoarea distantei vectoriale curente si celei anterioara - vect2: {} '.format(vect2))
        print('--------------------')
        if(threshold<vect1 and threshold<vect2):
            steps+=1
        
        prev1Vector=modulVector
        prev2Vector=prev1Vector
        print('Prev1vector : {} '.format(prev1Vector))
        print('Prev2vector : {} '.format(prev2Vector))
        print('--------------------')


        print("Acc X : "+str(xAccel))
        print("Acc Y : "+str(yAccel))
        print("Acc Z : "+str(zAccel))
        print('--------------------')
        print('Steps: {}'.format(steps))
        print()
        if(x%5==0):
            with open("steps.txt","a")as f:
                f.write('Steps {}\n'.format(steps))
                f.write('Datenow: {}\n'.format(datenow))
                f.write('Iteratie: {}\n'.format(x))
                f.write('--------------------\n')
                

    
        time.sleep(1)

        #gyro_data = mpu.get_gyro_data()
        #print("Gyro X : "+str(gyro_data['x']))
        #print("Gyro Y : "+str(gyro_data['y']))
        #print("Gyro Z : "+str(gyro_data['z']))
        #print()
        #print("-------------------------------")
        #time.sleep(1)
    except KeyboardInterrupt:
        print("\nDone")
        raise


    