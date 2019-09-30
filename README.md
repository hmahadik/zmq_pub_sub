# Python ZMQ pub/sub pattern sample

## Installation
```bash
# clone git repo
git clone https://github.com/hmahadik/zmq_pub_sub.git
cd zmq_pub_sub

# set up virtualenv
python3 -m virtualenv .zmqvenv
source .zmqvenv/bin/activate

# install dependencies
pip3 install -r requirements.txt
```

## Run Publisher
Starts streaming frames from your local webcam (device 0) to tcp port 5556 on two topics: `inference` and `postprocess`.
```
python3 stream_pub.py
```

## Run Subscribers
Inference topic subscriber receives and displays frames that have been resized to 300x300.
```
python3 stream_sub.py inference
```

Postprocess topic subscriber receives and displays a video stream where each frame is 1280x720.
```
python3 stream_sub.py postprocess
```

## To-do
* inference subscriber performs inference on frames
* inference subscriber publishes a metadata stream (bounding boxes, classes, confidences)
* postprocess subscriber subscribes to the metadata stream published by inference subscriber
* postprocess subscriber overlays the metadata on the 1280x720 video stream before displaying it
