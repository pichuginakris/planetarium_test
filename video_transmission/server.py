import cv2
import zmq
import logging
import logging.config

Video_path = 'shrek-best-life.mp4'
logging.basicConfig(filename='errors_log.log', filemode='a',
                        format='%(process)s - %(asctime)s - %(levelname)s - %(message)s')

context = zmq.Context()
socket = context.socket(zmq.PUB)
try:
    socket.bind("tcp://127.0.0.1:5688")
except zmq.ZMQError as connection_error:
    logging.error(
        'SERVER ERROR: Exception of type {!s} : {!s}'.format(type(connection_error).__name__, str(connection_error)))


while True:
    vid_capture = cv2.VideoCapture(Video_path)
    if not vid_capture.isOpened():
        logging.warning('SERVER: Opening video warning')
    while vid_capture.isOpened():
        ret, frame = vid_capture.read()
        if ret:
            cv2.imshow('Server', frame)
            socket.send_pyobj(frame)
            key = cv2.waitKey(30)
        else:
            break
    vid_capture.release()
else:
    cv2.destroyAllWindows()

