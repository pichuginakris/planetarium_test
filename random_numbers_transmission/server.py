import zmq
import time
import numpy
import logging
import logging.config

logging.basicConfig(filename='errors_log.log', filemode='a',
                        format='%(process)s - %(asctime)s - %(levelname)s - %(message)s')

context = zmq.Context()
socket = context.socket(zmq.PUB)
try:
    socket.bind("tcp://127.0.0.1:5687")
except zmq.ZMQError as connection_error:
    logging.error(
        'SERVER ERROR: Exception of type {!s} : {!s}'.format(type(connection_error).__name__, str(connection_error)))


def sending_messages(lower: int = 0, upper: int = 10000, count: int = 6):
    while True:
        messages = numpy.random.uniform(lower, upper, count)
        print(messages)
        time.sleep(1)
        try:
            socket.send_pyobj(messages)
        except Exception as ex:
            logging.error(
                'SERVER ERROR: Exception of type {!s} : {!s}'.format(type(ex).__name__, str(ex)))


if __name__ == "__main__":
    sending_messages()
