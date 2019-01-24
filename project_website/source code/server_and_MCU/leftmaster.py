"""Test for nrf24l01 module.  Portable between MicroPython targets."""

import sys
import ustruct as struct
import utime
import machine
from machine import Pin, SPI
from nrf24l01 import NRF24L01
from micropython import const
import random

# Slave pause between receiving data and checking for further packets.
_RX_POLL_DELAY = const(15)
# Slave pauses an additional _SLAVE_SEND_DELAY ms after receiving data and before
# transmitting to allow the (remote) master time to get into receive mode. The
# master may be a slow device. Value tested with Pyboard, ESP32 and ESP8266.
_SLAVE_SEND_DELAY = const(10)

if sys.platform == 'pyboard':
    cfg = {'spi': 2, 'miso': 'Y7', 'mosi': 'Y8', 'sck': 'Y6', 'csn': 'Y5', 'ce': 'Y4'}
elif sys.platform == 'esp8266':  # Hardware SPI
    cfg = {'spi': 1, 'miso': 12, 'mosi': 13, 'sck': 14, 'csn': 4, 'ce': 5}
elif sys.platform == 'esp32':  # Software SPI
    # cfg = {'spi': -1, 'miso': 32, 'mosi': 33, 'sck': 25, 'csn': 26, 'ce': 27}
    cfg = {'spi': -1, 'miso': 19, 'mosi': 18, 'sck': 5, 'csn': 14, 'ce':32 }
else:
    raise ValueError('Unsupported platform {}'.format(sys.platform))

pipes = (b'\xf0\xf0\xf0\xf0\xe1', b'\xf0\xf0\xf0\xf0\xd2')

def master():
    csn = Pin(cfg['csn'], mode=Pin.OUT, value=1)
    ce = Pin(cfg['ce'], mode=Pin.OUT, value=0)
    if cfg['spi'] == -1:
        spi = SPI(-1, sck=Pin(cfg['sck']), mosi=Pin(cfg['mosi']), miso=Pin(cfg['miso']))
        nrf = NRF24L01(spi, csn, ce, payload_size= 32,channel = 80)
    else:
        nrf = NRF24L01(SPI(cfg['spi']), csn, ce, payload_size=32,channel = 80)
    adc = machine.ADC(machine.Pin(39))
    adc.atten(adc.ATTN_11DB)

    row_0 = machine.Pin(13,machine.Pin.OUT)
    row_1= machine.Pin(12,machine.Pin.OUT)
    row_2 = machine.Pin(27,machine.Pin.OUT)
    column_0 = machine.Pin(33,machine.Pin.OUT)
    column_1 = machine.Pin(15,machine.Pin.OUT)
    foot_map =[(1,0,1,0,0),(1,0,1,0,1),(1,0,1,1,0),(1,0,1,1,1),(0,0,0,0,0),(0,0,0,0,1),(0,0,0,1,0),(0,0,0,1,1),(1,0,0,1,1),(0,0,1,0,1),(0,0,1,1,0),(0,0,1,1,1),(0,1,1,0,1),(0,1,1,1,0),(0,1,0,0,1),(0,1,0,1,0)]
    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.start_listening()

    lorr = 1#left sing is 1
    count = 0
    print('NRF24L01 master mode, sending ')

    while True :

        # stop listening and send packet
        nrf.stop_listening()
        row_2_val,row_1_val,row_0_val,column_1_val,column_0_val = foot_map[count]
        row_2.value(row_2_val)
        row_1.value(row_1_val)
        row_0.value(row_0_val)
        column_1.value(column_1_val)
        column_0.value(column_0_val)
        result = adc.read()
        datasend = result
        try:
            nrf.send(struct.pack('iii',lorr,datasend,count))
            print('sending:', lorr, datasend)
        except OSError:
            pass
        count = (1+count) % 16
        # start listening again
        nrf.start_listening()

        # wait for response, with 50ms timeout
        # start_time = utime.ticks_ms()
        # timeout = False
        # while not nrf.any() and not timeout:
        #     if utime.ticks_diff(utime.ticks_ms(), start_time) > 50:
        #         timeout = True
        # if timeout:
        #     print('failed, response timed out')

        # else:
        #     # recv packet
        #     got_millis = struct.unpack('i', nrf.recv())

        #     # print response and round-trip delay
        #     print('got response:', got_millis)

        # delay then loop
        utime.sleep_ms(15)

    # print('master finished sending; successes=%d, failures=%d' % (num_successes, num_failures))




print('NRF24L01 test module loaded')
print('NRF24L01 pinout for test:')
print('    CE on', cfg['ce'])
print('    CSN on', cfg['csn'])
print('    SCK on', cfg['sck'])
print('    MISO on', cfg['miso'])
print('    MOSI on', cfg['mosi'])
print('run nrf24l01test.slave() on slave, then nrf24l01test.master() on master')
master()