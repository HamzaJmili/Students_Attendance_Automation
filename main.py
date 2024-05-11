import threading
import GUI.gui as gui
import face_rec.face_rec_func as frf
from Utility.database import getStudents

def main():

    students = getStudents()
    students_dir = r"students_images\\"
    known_face_encodings = frf.load_known_faces(students_dir)

    # Create the main window in the main thread
    gui_thread = threading.Thread(target=gui.create_main_window, args=(students,))
    gui_thread.start()

    # Start face recognition loop in the main thread
    frf.face_recognition_loop(known_face_encodings, students)
    


if __name__ == "__main__":
    main()
