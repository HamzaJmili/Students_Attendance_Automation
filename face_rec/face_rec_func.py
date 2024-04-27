import face_recognition
import cv2 
import os
import GUI.gui as gui

def load_known_faces(students_dir):
    known_face_encodings = []
    students = []  # Initialize students list

    for filename in os.listdir(students_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(students_dir, filename)
            student_name = os.path.splitext(filename)[0]
            student_image = face_recognition.load_image_file(image_path)
            student_face_encoding = face_recognition.face_encodings(student_image)[0]
            known_face_encodings.append(student_face_encoding)
            students.append((student_name, "Absent"))  # Initially, mark all students as absent

    return known_face_encodings, students  # Return students list

def recognize_faces(frame, known_face_encodings, students):
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_location, face_encoding in zip(face_locations, face_encodings):
        top, right, bottom, left = face_location
        name = "Unknown"

        for i, known_encoding in enumerate(known_face_encodings):
            match = face_recognition.compare_faces([face_encoding], known_encoding, tolerance=0.6)[0]
            if match:
               
                name = students[i][0]  # Get student name
                
                if students[i][1]== "Absent" :
                     students[i] = (name, "Present")
                     gui._update_students_gui(students,i)
                 
                break
                
                 
                
                

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Update GUI with the updated student list
    

    return frame


def face_recognition_loop(known_face_encodings, students):
    # Initialize camera
    video_capture = cv2.VideoCapture(0)


    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Recognize faces
        frame = recognize_faces(frame, known_face_encodings, students)

        # Display the resulting image
        cv2.imshow('Video', frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    video_capture.release()
    cv2.destroyAllWindows()
