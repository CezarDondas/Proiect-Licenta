from mpu9250 import mpu9250
import time
import socket



mpu = mpu9250(0x68) #Adresa pentru senzorul mpu9dof care este mereu 0x68, dar daca nu este aceasta,
#ea poate fi gasita scriind comanda sudo i2cdetect -y 1 in terminal!!
datenow=time.ctime()
#Initializari variabile pentru configurarea socket-urilor

IP_HOME='x.x.x.x'
IP_AC='x.x.x.x'
PORT='xxxx'

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((IP_HOME,PORT))
server_socket.listen(1)
while True:
        print('Wait for client...\n')
        client_socket,client_address=server_socket.accept()
        print('Client connected: ',client_address)
        try:
            while True:
                try:
                    accel_data = mpu.get_accel_data()
                    xAccel=(accel_data['x'])
                    yAccel=(accel_data['y']) 
                    zAccel=(accel_data['z']) 

                    gyro_data = mpu.get_gyro_data()
                    xGyro=(gyro_data['x'])
                    yGyro=(gyro_data['y'])
                    zGyro=(gyro_data['z'])
                    print("Acc X: {:.5f} m/s^2".format(xAccel))
                    print("Acc Y: {:.5f} m/s^2".format(yAccel))
                    print("Acc Z: {:.5f} m/s^2".format(zAccel))
                    print('{}'.format('-'*30))
                    print("Gyro X: {:.5f}rad/s".format(xGyro))
                    print("Gyro Y: {:.5f}rad/s".format(yGyro))
                    print("Gyro Z: {:.5f}rad/s".format(zGyro))
                    print("")


                    xyzAccelGyro=[xAccel,yAccel,zAccel,xGyro,yGyro,zGyro]
                    client_socket.send(str(xyzAccelGyro).encode()) 
                    time.sleep(1) 
                except KeyboardInterrupt:
                    print("\nDone for now to continue editing....\n")
                    raise
        except socket.error:
            print('Connection abort by client')

        client_socket.close()



        

    


    
