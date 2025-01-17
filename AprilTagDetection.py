import cv2
from pupil_apriltags import Detector

# Initialize AprilTag detector
at_detector = Detector(families="tag36h11")  # Default tag family

# Open the camera (use 0 or the appropriate index for your camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot access the camera")
    exit()

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert to grayscale (required for AprilTag detection)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect AprilTags
    tags = at_detector.detect(gray_frame)

    # Draw detections
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

cap.release()
cv2.destroyAllWindows()