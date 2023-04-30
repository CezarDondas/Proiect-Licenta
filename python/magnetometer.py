import smbus

# Initialize I2C communication with MPU9250
bus = smbus.SMBus(1)
mpu9250_addr = 0x68  # or 0x69 if AD0 is high

# Write "00011011" to I2CDIS register
i2cdis_val = 0b00011011
bus.write_byte_data(mpu9250_addr, 0x6B, i2cdis_val)

# End I2C communication session
bus.close()