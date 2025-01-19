import io
import cv2
import numpy as np
import picamera

def generate_frames():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 24
        stream = io.BytesIO()

        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            # Rewind the stream to the beginning
            stream.seek(0)
            
            # Convert the stream to a NumPy array
            frame = np.frombuffer(stream.getvalue(), dtype=np.uint8)
            
            # Decode the frame into an OpenCV image
            image = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            
            yield image

            # Clear the stream for the next frame
            stream.seek(0)
            stream.truncate()

if __name__ == "__main__":
    for frame in generate_frames():
        # Display the frame in an OpenCV window
        cv2.imshow("Video Feed", frame)
        
        # Break the loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources and close the window
    cv2.destroyAllWindows()
