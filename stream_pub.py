import zmq
import sys
import cv2
import numpy as np
import time

port = "5556"
video_src = 0

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

cap = cv2.VideoCapture(video_src)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
assert(cap.isOpened())

topics = {
    "postprocess": {"width": 1280, "height": 720, "timeout": 33},
    "inference": {"width": 300, "height":300, "timeout": 333}
}
frame_num = 1
while True:
    try:
        ok, frame = cap.read()
        assert(ok)
        cv2.putText(frame, "Frame {}".format(frame_num), (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        sys.stdout.write("\rpublishing frame {}".format(frame_num))
        for topic in topics:
            if (frame.shape[1] != topics[topic]["width"] or 
                frame.shape[0] != topics[topic]["height"]):
                frame = cv2.resize(frame, (topics[topic]["width"], topics[topic]["height"]))
            messagedata = np.ascontiguousarray(frame) if not frame.flags['C_CONTIGUOUS'] else frame
            md = dict(
                    frameId=frame_num,
                    timestamp=time.time(),
                    timeout=topics[topic]["timeout"],
                    dtype=str(messagedata.dtype),
                    shape=messagedata.shape,
                )
            socket.send(topic.encode(), zmq.SNDMORE)
            socket.send_json(md, zmq.SNDMORE)
            socket.send(messagedata, copy=False, track=False)
        frame_num += 1
    except KeyboardInterrupt:
        break
