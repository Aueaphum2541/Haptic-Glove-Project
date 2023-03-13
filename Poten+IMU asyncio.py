import imu
import utime
from machine import Pin, ADC
import uasyncio as asyncio

potentiometer_pin = ADC(Pin(25))

async def read_potentiometer():
    last_value = potentiometer_pin.read_u16()
    last_time = utime.ticks_ms()
    while True:
        value = potentiometer_pin.read_u16()
        time_diff = utime.ticks_ms() - last_time
        if value != last_value:
            print('Poten P0 =', value, 'Time between changes =', time_diff, 'ms')
        last_value = value
        last_time = utime.ticks_ms()
        await asyncio.sleep_ms(50)
        
async def read_imu():
    while True:
        start_time = utime.ticks_ms()
        acc_z = imu.acc[2]
        end_time = utime.ticks_ms()
        imu_rate = 1000 / (end_time - start_time)
        print('Z =', acc_z, 'Rate =', imu_rate, 'Hz')
        await asyncio.sleep_ms(100)

async def main():
    tasks = [read_potentiometer(), read_imu()]
    while True:
        for task in tasks:
            await task

asyncio.run(main())

