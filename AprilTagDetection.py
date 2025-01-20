import cv2
from pupil_apriltags import Detector
from picamera2 import Picamera2

# Initialize the camera
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(camera_config)
picam2.start()

# Initialize AprilTag detector
at_detector = Detector(families="tag36h11")  # Default tag family

print("Press 'q' to quit.")

try:
    while True:
        # Capture a frame from the camera
        frame = picam2.capture_array()

        # Convert to grayscale (required for AprilTag detection)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Detect AprilTags
        tags = at_detector.detect(gray_frame)

        # Draw detections on the frame
        for tag in tags:
            (ptA, ptB, ptC, ptD) = tag.corners
            ptA = tuple(map(int, ptA))
            ptB = tuple(map(int, ptB))
            ptC = tuple(map(int, ptC))
            ptD = tuple(map(int, ptD))

            # Draw bounding box
            cv2.line(frame, ptA, ptB, (0, 255, 0), 2)
            cv2.line(frame, ptB, ptC, (0, 255, 0), 2)
            cv2.line(frame, ptC, ptD, (0, 255, 0), 2)
            cv2.line(frame, ptD, ptA, (0, 255, 0), 2)

            # Add the tag ID near the top-left corner
            cv2.putText(frame, f"ID: {tag.tag_id}", (ptA[0], ptA[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("AprilTag Detection", frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()
