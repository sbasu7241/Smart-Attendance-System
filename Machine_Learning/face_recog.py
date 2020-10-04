import face_recognition
import cv2
from openpyxl import Workbook
import datetime
from firebase import firebase


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
    
    

    
# Load images.
    
image_1 = face_recognition.load_image_file("dataset/Shreyansh.jpg")
image_1_face_encoding = face_recognition.face_encodings(image_1)[0]
    
image_5 = face_recognition.load_image_file("dataset/Soumyadeep.jpg")
image_5_face_encoding = face_recognition.face_encodings(image_5)[0]
    
image_7 = face_recognition.load_image_file("dataset/Bindu.jpg")
image_7_face_encoding = face_recognition.face_encodings(image_7)[0]
    
image_3 = face_recognition.load_image_file("dataset/Harsh.jpg")
image_3_face_encoding = face_recognition.face_encodings(image_3)[0]
    
image_4 = face_recognition.load_image_file("dataset/Mrigyen.jpg")
image_4_face_encoding = face_recognition.face_encodings(image_4)[0]
    
    
# Create arrays of known face encodings and their names
known_face_encodings = [
        
        image_1_face_encoding,
        image_5_face_encoding,
        image_7_face_encoding,
        image_3_face_encoding,
        image_4_face_encoding
        
    ]
known_face_names = [
        
        "Shreyansh",
        "Soumyadeep",
	"Jitesh",
        "Bindu",
        "Harsh",
        "Mrigyen"
       
    ]
    
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
    
# Load present date and time
now= datetime.datetime.now()
today=now.day
month=now.month
    
firebase = firebase.FirebaseApplication('https://face-attendence.firebaseio.com', None)

while True:
 # Grab a single frame of video
    ret, frame = video_capture.read()
    
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    
    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    
    face_names = []
    name = ""
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
    
         # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
         
      
    face_names.append(name)
    
    process_this_frame = not process_this_frame
    
    
    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
           # Scale back up face locations since the frame we detected in was scaled to 1/4 size
           top *= 4
           right *= 4
           bottom *= 4
           left *= 4
    
    # Draw a box around the face
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    
           # Draw a label with a name below the face
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    
    # Display the resulting image
    cv2.imshow('Video', frame)
   
    
	
    # Integrate with firebase
    
    if(firebase.get('/Harsh','IIT2018049')=='False'):
      if face_names[0] == 'Harsh':
        result = firebase.patch('/Harsh', {'IIT2018049':'True'})
    elif(firebase.get('/Mrigyen','IIT2018033')=='False'):
      if face_names[0] == 'Mrigyen':
        result = firebase.patch('/Mrigyen', {'IIT2018033':'True'})
    elif(firebase.get('/Soumyadeep','IIT2018001')=='False'):
      if face_names[0] == 'Soumyadeep':
        result = firebase.patch('/Soumyadeep', {'IIT2018001':'True'})
    elif(firebase.get('/Shreyansh','IIT2018073')=='False'):
      if face_names[0] == 'Shreyansh':
        result = firebase.patch('/Shreyansh', {'IIT2018073':'True'})
    elif(firebase.get('/Bindu','IIT2018105')=='False'):
      if face_names[0] == 'Bindu':
        result = firebase.patch('/Bindu', {'IIT2018105':'True'})
  
 
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
    
   
