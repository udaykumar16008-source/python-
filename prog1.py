import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime

# ================================
# STEP 1: Load Images
# ================================
path = 'ImagesAttendance'
images = []
classNames = []

myList = os.listdir(path)

print("Images Found:", myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

print("Student Names:", classNames)

# ================================
# STEP 2: Encode Faces
# ================================
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:
            encodeList.append(encodes[0])
    return encodeList

encodeListKnown = findEncodings(images)
print("Encoding Complete")

# ================================
# STEP 3: Mark Attendance
# ================================
def markAttendance(name):
    with open('Attendance.csv', 'a+') as f:
        f.seek(0)
        myDataList = f.readlines()
        nameList = []

        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

# ================================
# STEP 4: Start Webcam
# ================================
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    if not success:
        break

    # Resize image for faster processing
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect faces
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()

            # Scale back face location
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4

            # Draw rectangle
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)

            # Put name
            cv2.putText(img, name, (x1+6, y2-6),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Mark attendance
            markAttendance(name)

    cv2.imshow('AI Attendance System', img)

    # Press ENTER to exit
    if cv2.waitKey(1) & 0xFF == 13:
        break

cap.release()
cv2.destroyAllWindows()