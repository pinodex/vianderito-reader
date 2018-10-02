from threading import Thread
import threading

import time
import serial
import requests

import config

headers = {
  'Authorization': 'Bearer %s' % config.KIOSK_KEY
}

ser = serial.Serial(
  port = 'COM5',
  baudrate = 9600,
  parity = serial.PARITY_NONE,
  stopbits = serial.STOPBITS_ONE,
  bytesize = serial.EIGHTBITS,
  timeout = 0.1
)

tags = []

def clear_epcs():
  global tags
  
  tags = []
  
  threading.Timer(5.0, clear_epcs).start()

def send_epcs():
  url = '%s/cart' % config.BASE_URL

  if (tags):
    try:
      requests.post(url, json={ 'epcs': tags }, headers=headers)
    except:
      print "Error sending EPCS to server"

  threading.Timer(0.5, send_epcs).start()

def serial_read():
  global tags

  while True:
    try:
      raw_line = ser.readline()

      if raw_line:
        line = raw_line.encode('hex')

        head = line[:2]
        lsb = line[2:4]
        msb = line[4:6]
        cid1 = line[6:8]
        cid2 = line[8:10]

        tag_count = int(line[10:12], 16)
        tag_length = int(line[12:14], 16)

        data_start = 14

        print 'Count: %s' % tag_count

        tags = []

        for x in range(1, tag_count + 1):
            antenna_number = line[data_start : data_start + 2]

            epc_start = data_start + 2
            epc_end = (epc_start + (tag_length * 2)) - 4

            epc = line[epc_start:epc_end]
            
            data_start = epc_end + 2

            if (epc not in tags):
              tags.append(epc)

            print 'Tag %d: %s' % (x, epc)
    except:
      print "Error occurred decoding tag"

serial_read_thread = Thread(target=serial_read)
serial_read_thread.start()

clear_epcs()
send_epcs()
