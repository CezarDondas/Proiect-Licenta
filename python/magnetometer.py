import smbus
import time
# MPU9250 address and registers
MPU9250_ADDRESS = 0x68
AK8963_ADDRESS=0X0C
MAG_XOUT_L = 0x03
MAG_XOUT_H = 0x04
MAG_YOUT_L = 0x05
MAG_YOUT_H = 0x06
MAG_ZOUT_L = 0x07
MAG_ZOUT_H = 0x08
MAG_SENS = 4900.0

# Initialize I2C bus
bus = smbus.SMBus(1)

# Configure MPU9250 to enable magnetometer
bus.write_byte_data(MPU9250_ADDRESS, 0x6B, 0x00)
bus.write_byte_data(AK8963_ADDRESS, 0x0A, 0x16)

# Read magnetometer data
x_low = bus.read_byte_data(MPU9250_ADDRESS, MAG_XOUT_L)
x_high = bus.read_byte_data(MPU9250_ADDRESS, MAG_XOUT_H)
y_low = bus.read_byte_data(MPU9250_ADDRESS, MAG_YOUT_L)
y_high = bus.read_byte_data(MPU9250_ADDRESS, MAG_YOUT_H)
z_low = bus.read_byte_data(MPU9250_ADDRESS, MAG_ZOUT_L)
z_high = bus.read_byte_data(MPU9250_ADDRESS, MAG_ZOUT_H)

# Convert magnetometer data to meaningful units
while(True):
    x = (x_high << 8) | x_low
    y = (y_high << 8) | y_low
    z = (z_high << 8) | z_low
    x = x if x < 32768 else x - 65536
    y = y if y < 32768 else y - 65536
    z = z if z < 32768 else z - 65536
    print("Magnetometer data (uT): X=%d, Y=%d, Z=%d" % (x, y, z))
    time.sleep(1)
