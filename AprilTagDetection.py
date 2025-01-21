import cv2
from pupil_apriltags import Detector
from picamera2 import Picamera2

# Camera parameters (replace with actual calibrated values)
fx, fy = 600, 600  # Focal lengths in pixels
cx, cy = 320, 240  # Principal point (center of the image)
camera_params = [fx, fy, cx, cy]

# Tag size (meters)
tag_size = 0.1  # Example: 10 cm wide tag

# Initialize AprilTag detector
at_detector = Detector(families="tag36h11")

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration())
picam2.start()

print("Press 'q' to quit.")

while True:
    # Capture frame from the camera
    frame = picam2.capture_array()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect AprilTags with pose estimation
    tags = at_detector.detect(
        gray_frame,
        estimate_tag_pose=True,
        camera_params=camera_params,
        tag_size=tag_size,
    )

    for tag in tags:
        # Extract pose data (translation vector)
        x, y, z = tag.pose_t  # Position relative to the camera
        print(f"Tag ID: {tag.tag_id}, Position - x: {x:.2f}, y: {y:.2f}, z: {z:.2f}")

        # Draw the detected tag on the frame
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

        # Display tag ID and position
        cv2.putText(frame, f"ID: {tag.tag_id}", (ptA[0], ptA[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, f"x: {x:.2f}, y: {y:.2f}, z: {z:.2f}",
                    (ptA[0], ptA[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the camera feed
    cv2.imshow("AprilTag Detection with Pose Estimation", frame)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
picam2.stop()