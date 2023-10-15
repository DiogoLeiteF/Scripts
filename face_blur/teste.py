import cv2
import os

files = "test_images"
saved_images = f"{files}/blurred"

images = os.listdir(files)


# Load the image
image = cv2.imread(f"{files}/{images[1]}")
# Load the face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
nose_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_mcs_nose.xml')
mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_mcs_mouth.xml')
# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Detect faces
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
print(images[1])
print(len(faces))
print(faces)
# Increase the size of the detected face regions
margin = 30  # Adjust this value to control the size of the blurred area
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    roi_gray = gray[y:y + h, x:x + w]
    roi_color = image[y:y + h, x:x + w]
    # Detect eyes within the face
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)
    # Detect the nose within the face
    noses = nose_cascade.detectMultiScale(roi_gray)
    for (nx, ny, nw, nh) in noses:
        cv2.rectangle(roi_color, (nx, ny), (nx + nw, ny + nh), (0, 0, 255), 2)
    # Detect the mouth within the face
    mouths = mouth_cascade.detectMultiScale(roi_gray)
    for (mx, my, mw, mh) in mouths:
        cv2.rectangle(roi_color, (mx, my), (mx + mw, my + mh), (0, 255, 255), 2)
# Display the image with detected features
cv2.imshow("Face Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Display or save the modified image
# cv2.imshow("Blurred Faces", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



# for file in images:
#     image = blur_faces(path=files, file_name=file)
#
#     # To save the modified image:
#     if not os.path.exists(saved_images):
#         os.makedirs(saved_images)
#     cv2.imwrite(f"{saved_images}/blur_{file}", image)