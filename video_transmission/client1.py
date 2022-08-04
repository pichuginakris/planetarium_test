import zmq
import logging
import logging.config
import cv2

logging.basicConfig(filename='errors_log.log', filemode='a',
                        format='%(process)s - %(asctime)s - %(levelname)s - %(message)s')

context = zmq.Context()
socket = context.socket(zmq.SUB)
try:
    socket.connect("tcp://127.0.0.1:5688")
except zmq.ZMQError as connection_error:
    logging.error(
        'CLIENT ERROR: Exception of type {!s} : {!s}'.format(type(connection_error).__name__, str(connection_error)))

socket.setsockopt_string(zmq.SUBSCRIBE, '')
while True:
    messages = socket.recv_pyobj()
    cv2.imshow('Client 1', messages)
    key = cv2.waitKey(30)
