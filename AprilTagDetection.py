import cv2
import apriltag

#Initialize the camera
camera_index = 0 #Adjust as needed for setup
cap = cv2.VideoCapture(camera_index)

#Set resolution (adjust for Raspberry Pi Camera Module 3)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

#Initialize the AprilTag detector
options = apriltag.DetectorOptions(families="tag36h11")
detector = apriltag.Detector(options)

print("Press 'q' to quit")

while True:
  ret, frame = cap.read()
  if not ret:
    print("Failed to capture frame")
    break

  #Convert to grayscale
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  #Detect AprilTags
  results = detector.detect(gray)

  for result in results:
    #Draw the bounding box
    for i in range(len(result.corners)):
      start_point = tuple(map(int, result.corners[i-1]))
      end_point = tuple(map(int, result.corners[i]))
      cv2.line(frame, start_point, end_point, (0, 255, 0), 2)

    #Mark the center of the tag
    center = tuple(map(int, result.center))
    cv2.circle(frame, center, 5, (0, 0, 255), -1)

    #Display tag ID
    tag_id = result.tag_id
    cv2.putText(frame, f"ID: {tag_id}", (center[0] + 10, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

  #Display the frame
  cv2.imshow("AprilTag Detection", frame)

  #Exit on 'q' key press
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
