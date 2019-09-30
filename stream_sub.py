import sys
import zmq
import cv2
import numpy as np
import cProfile

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

topic = "inference"
if len(sys.argv) > 2:
    topic = sys.argv[2]

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:%s" % port)

# Subscribe to topic
socket.setsockopt(zmq.SUBSCRIBE, topic.encode())

profile = cProfile.Profile()

while True:
    try:
        topic = socket.recv()
        md = socket.recv_json()
        msg = socket.recv()
        A = np.frombuffer(msg, dtype=md['dtype'])
        frame_num, frame = (md['frameId'], A.reshape(md['shape']))
        sys.stdout.write("\r {} received frame {}".format(topic, frame_num))
        cv2.imshow("Inference", frame)
        key = cv2.waitKey(md["timeout"])
        if key == ord('q'):
            break

        #profile.enable()
        socket.close()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://localhost:%s" % port)
        socket.setsockopt(zmq.SUBSCRIBE, topic)
        #profile.disable()

    except KeyboardInterrupt:
        break

profile.print_stats(sort="cumtime")
cv2.destroyAllWindows()
