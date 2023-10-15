import cv2
import os

files = "test_images"
saved_images = f"{files}/blurred"

images = os.listdir(files)

def blur_faces(path:str, file_name:str) -> cv2.imread:
    # Load the image
    image = cv2.imread(f"{path}/{file_name}")

    # Load the face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(5, 5))
    print(file_name)
    print(len(faces))
    if len(faces) == 0:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
        print("PROFILE")
        print(len(faces))
    # faces = faces if len(faces) == 1 else faces[0]

    # Increase the size of the detected face regions
    margin = 30  # Adjust this value to control the size of the blurred area

    for (x, y, w, h) in faces:
        x -= margin
        y -= margin
        w += 2 * margin
        h += 2 * margin

        # Ensure the new coordinates are within the image boundaries
        x = max(x, 0)
        y = max(y, 0)
        w = min(w, image.shape[1])
        h = min(h, image.shape[0])

        face = image[y:y + h, x:x + w]
        blurred_face = cv2.GaussianBlur(face, (0, 0), 30)
        image[y:y + h, x:x + w] = blurred_face
    return image

# Display or save the modified image
# cv2.imshow("Blurred Faces", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

for file in images:
    image = blur_faces(path=files, file_name=file)

    # To save the modified image:
    if not os.path.exists(saved_images):
        os.makedirs(saved_images)
    cv2.imwrite(f"{saved_images}/blur_{file}", image)
