import sys
import zmq
import cv2
import numpy as np
import cProfile

host = "172.17.0.2"
port = "5556"
src_addr = "tcp://172.17.0.2:5556"

topic = "inference"
if len(sys.argv) > 1:
    topic = sys.argv[1]

def subscribe():
    global socket, context, topic
    socket = context.socket(zmq.SUB)
    socket.connect(src_addr)
    socket.setsockopt(zmq.SUBSCRIBE, topic.encode())

context = zmq.Context()
subscribe()

cv2.namedWindow(topic, cv2.WINDOW_AUTOSIZE|cv2.WINDOW_KEEPRATIO)
while True:
    try:
        topic = socket.recv().decode()
        md = socket.recv_json()
        msg = socket.recv()
        A = np.frombuffer(msg, dtype=md['dtype'])
        frame_num, frame = (md['frameId'], A.reshape(md['shape']))
        sys.stdout.write("\r {} received frame {}".format(topic, frame_num))
        cv2.putText(frame, "{}x{}".format(md['shape'][1], md['shape'][0]), (10, 65),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow(topic, frame)
        key = cv2.waitKey(md["timeout"])
        if key == ord('q'):
            break
        
        socket.close()
        subscribe()

    except KeyboardInterrupt:
        break

cv2.destroyAllWindows()
