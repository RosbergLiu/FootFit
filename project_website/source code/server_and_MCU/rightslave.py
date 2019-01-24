"""Test for nrf24l01 module.  Portable between MicroPython targets."""

import sys
import ustruct as struct
import utime
import urequests
from machine import Pin, SPI,ADC
from nrf24l01 import NRF24L01
from micropython import const
import socket
import json
import network
def do_connect():
    
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Columbia University','')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
do_connect()
addr = '184.72.70.209'
port = 8003

# slaveserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

iot_headers = {
'Content-Type': 'application/json'
}


# Slave pause between receiving data and checking for further packets.
# _RX_POLL_DELAY = const(15)
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

foot_r = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
foot_rcount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
printcount = 1
def slave():
    csn = Pin(cfg['csn'], mode=Pin.OUT, value=1)
    ce = Pin(cfg['ce'], mode=Pin.OUT, value=0)
    if cfg['spi'] == -1:
        spi = SPI(-1, sck=Pin(cfg['sck']), mosi=Pin(cfg['mosi']), miso=Pin(cfg['miso']))
        nrf = NRF24L01(spi, csn, ce, payload_size=32 ,channel =50)
    else:
        nrf = NRF24L01(SPI(cfg['spi']), csn, ce, payload_size=32,channel = 50)

    nrf.open_tx_pipe(pipes[1])
    nrf.open_rx_pipe(1, pipes[0])
    nrf.start_listening()


    print('NRF24L01 slave mode, waiting for packets... (ctrl-C to stop)')
    
    while True:
        global printcount
        global foot_r
        global foot_rcount
        if nrf.any():
            while nrf.any():
                buf = nrf.recv()
                lorr, datasend,count = struct.unpack('iii', buf)
                if lorr == 0:
                    foot_r[count] = datasend
                    foot_rcount[count] += 1 
                printcount  = (printcount+1)%16
                
                utime.sleep_ms(_RX_POLL_DELAY)

                nrf.stop_listening()

            if printcount == 0:
                print('ready to send to server')
                foot_r = foot_r[1:] + [foot_r[0]]
                print('foot',foot_r)
                dictsend = {'sign':'r','data':foot_r}
                sent = json.dumps(dictsend)
                try:
                    print('stat send')
                    # slaveserver.sendto(sent.encode('utf-8'),(addr,port))
                    r = urequests.post('http://184.72.70.209:5000/rightdata', data=sent, headers=iot_headers)
                    print('send finish')
                except:
                    print('send failed')
                utime.sleep(0.01)
            nrf.start_listening()
print('NRF24L01 test module loaded')
print('NRF24L01 pinout for test:')
print('    CE on', cfg['ce'])
print('    CSN on', cfg['csn'])
print('    SCK on', cfg['sck'])
print('    MISO on', cfg['miso'])
print('    MOSI on', cfg['mosi'])
print('run nrf24l01test.slave() on slave, then nrf24l01test.master() on master')
slave()
