from mpu6050 import mpu6050
import time
import math
mpu = mpu6050(0x68)


steps=0
prevVector=0
while True:
    try:
        print("Temp : "+str(mpu.get_temp()))
        print()

        accel_data = mpu.get_accel_data()
        xAccel=accel_data['x']
        yAccel=accel_data['y']
        zAccel=accel_data['z']
        modulVector=math.sqrt(xAccel*xAccel+yAccel*yAccel+zAccel*zAccel)
        print('Modul vector: {} '.format(modulVector))
        print('-----------------------------')

        vect=modulVector-prevVector
        print('Diferenta dintre valoarea curenta si cea anterioara : {} '.format(vect))
        print('-----------------------------')
        if(vect>4):
            steps+=1
        
        prevVector=modulVector
        print('Prevvector : {} '.format(prevVector))
        print('-----------------------------')


        print("Acc X : "+str(xAccel))
        print("Acc Y : "+str(yAccel))
        print("Acc Z : "+str(zAccel))
        print('-----------------------------')
        print('Steps: {}'.format(steps))
        
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
    