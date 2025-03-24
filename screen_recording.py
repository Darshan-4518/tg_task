import cv2
import requests
import numpy as np
import time

# Set the broadcast URL
BROADCAST_URL = "http://192.168.0.244/device_broadcast_39005/"

# Video output settings
output_file = "recorded_video.mp4"
frame_width = 1280  # Adjust based on the source stream
frame_height = 720  # Adjust based on the source stream
fps = 10  # Adjust FPS as needed

# OpenCV VideoWriter to save the video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

print("Recording started... Press Ctrl+C to stop.")

try:
    while True:
        response = requests.get(BROADCAST_URL, stream=True)
        if response.status_code == 200:
            print(type(response.content))
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if frame is not None:

                # Resize the frame to ensure consistent size
                frame = cv2.resize(frame, (frame_width, frame_height))

                out.write(frame)


        time.sleep(1 / fps)  # Control frame rate

except KeyboardInterrupt:
    print("Recording stopped.")
    out.release()
    cv2.destroyAllWindows()