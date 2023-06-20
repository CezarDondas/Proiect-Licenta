from mpu9250 import mpu9250
import time
import math
import socket
import threading

mpu = mpu9250(0x68)  # Adresa pentru senzorul mpu9dof care este mereu 0x68, dar daca nu este aceasta,
    # ea poate fi gasita scriind comanda sudo i2cdetect -y 1 in terminal!!

datenow = time.ctime()
steps=0
 # numarul de pasi detectati    
threshold = 1.2  # pragul care ne ajuta sa detectam pasii, acesta poate fi setat in functie de cum dorim

move = False

    # Am initializat variabilele ce vor fi acceleratiile pentru fiecare axa
xAccel = 0
yAccel = 0
zAccel = 0

xGyro = 0
yGyro = 0
zGyro = 0

thresholder_accel = 10  # am setat acest prag deoarece g=9.80 si am considerat ca intre 9.81 si 9.99 sa fie o marja de eroare pentru a evita
    # detectarea unei miscari eronate.
    # thresholder_gyro=50.00

modulVector = [0.0] * 100
diff_mod = [0.0] * 100

v_xAccel = []
v_yAccel = []
v_zAccel = []

v_xGyro = []
v_yGyro = []
v_zGyro = []

absxAcc = [0.0] * 100
absyAcc = [0.0] * 100
abszAcc = [0.0] * 100


IP = '192.168.0.59'
PORT = 5005

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(1)

def step_function(client_socket):
    global steps
    while True:
        try:
            for i in range(100):
                accel_data = mpu.get_accel_data()
                xAccel = accel_data['x']
                v_xAccel.append(xAccel)
                yAccel = accel_data['y']
                v_yAccel.append(yAccel)
                zAccel = accel_data['z']
                v_zAccel.append(zAccel)

                gyro_data = mpu.get_gyro_data()
                xGyro = gyro_data['x']
                v_xGyro.append(xGyro)
                yGyro = gyro_data['y']
                v_yGyro.append(yGyro)
                zGyro = gyro_data['z']
                v_zGyro.append(zGyro)

                modulVector[i] = math.sqrt(v_xAccel[i] * v_xAccel[i] + v_yAccel[i] * v_yAccel[i] + v_zAccel[i] * v_zAccel[i])
                diff_mod[i] = modulVector[i] - modulVector[i - 1]

                absxAcc[i] = abs(v_xAccel[i]) - abs(v_xAccel[i - 1])
                absyAcc[i] = abs(v_yAccel[i]) - abs(v_yAccel[i - 1])
                abszAcc[i] = abs(v_zAccel[i]) - abs(v_zAccel[i - 1])

                if (abs(v_xAccel[i]) > thresholder_accel and absxAcc[i] != 0) or (abs(v_yAccel[i]) > thresholder_accel and absyAcc[i] != 0) or (abs(v_zAccel[i]) > thresholder_accel and abszAcc[i] != 0):
                    move = True
                else:
                    move = False

                if move and diff_mod[i] > threshold:
                    steps += 1
                
                print("Acc X: {:.5f} m/s^2".format(v_xAccel[i]))
                print("Acc Y: {:.5f} m/s^2".format(v_yAccel[i]))
                print("Acc Z: {:.5f} m/s^2".format(v_zAccel[i]))
                print('{}'.format('-'*30))

                        
                        
                print("Gyro X: {:.5f}rad/s".format(v_xGyro[i]))
                print("Gyro Y: {:.5f}rad/s".format(v_yGyro[i]))
                print("Gyro Z: {:.5f}rad/s".format(v_zGyro[i]))
                print("")

                

                

                time.sleep(0.000125)
                steps_to_send_to_client = str(steps)
                client_socket.send(steps_to_send_to_client.encode())
                
                
                    
        except KeyboardInterrupt:
            print("\nDone for now to continue editing....\n")
            raise
        
        client_socket.close()
        
                        
                    
                

        

print('Wait for client...\n')
while True:
    try:
        client_socket, client_address = server_socket.accept()
        print('Client connected: ', client_address)
        client_thread_1 = threading.Thread(target=step_function, args=(client_socket,))
        client_thread_2 = threading.Thread(target=step_function, args=(client_socket,))
        client_thread_1.start()
        client_thread_2.start()
        client_thread_1.join()
        client_thread_2.join()


    except socket.error:
        print('Connection abort by client')

