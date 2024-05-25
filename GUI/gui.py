import customtkinter as ctk
from CTkTable import *
import cv2
from Utility.database import insertAbsence, getModules , verify_login , get_students_and_filiere_name
import face_rec.face_rec_func as frf
from Utility.saveSendExcel import create_excel_file, send_email_with_excel
import threading

class MainWindow(ctk.CTk):
    global tree # No need
  
    def __init__(self):
        super().__init__()
        self.title("Main Window")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        
        my_font = ctk.CTkFont(family="Calibri", weight="bold", size=15)
        
        #studentss = [(t[0], t[1], t[2], t[5]) for t in students]
        
        self.frame1 = ctk.CTkFrame(master=self)
        self.frame1.pack(fill="both", expand=True)

        self.label_login = ctk.CTkLabel(self.frame1, text="Se connecter", font=my_font)
        self.label_login.pack(pady=20)

        self.label_email = ctk.CTkLabel(self.frame1, text="Email:", font=my_font)
        self.label_email.pack(pady=10)
        self.input_email= ctk.CTkEntry(self.frame1, placeholder_text="Entrez votre adresse mail", width=300)
        self.input_email.pack(pady=10)

        self.label_password = ctk.CTkLabel(self.frame1, text="Mot de passe:", font=my_font)
        self.label_password.pack(pady=10)
        self.input_password= ctk.CTkEntry(self.frame1, placeholder_text="Entrez votre mot de passe", show="*", width=300)
        self.input_password.pack(pady=10)

        self.btn_login = ctk.CTkButton(self.frame1, text="Login", corner_radius=10, command=self.login, font=my_font)
        self.btn_login.pack(pady=20)

        self.label_incorrect = ctk.CTkLabel(self.frame1, text="Email et/ou mot de passe incorrect",text_color="red" )
        

        self.frame2 = ctk.CTkFrame(master=self)
        self.frame2.pack(fill="both", expand=True)

        self.label1 = ctk.CTkLabel(self.frame2, text="Sélectionner le module enseigné :", font=my_font)
        self.label1.pack(pady=40)
        #self.modules = getModules()
        #module_names = [module[1] for module in self.modules]
        self.optionmenu = ctk.CTkOptionMenu(self.frame2, values= ['',''], width=260 ,height=30, font=my_font)
        self.optionmenu.pack(pady=30)


        self.checkbox = ctk.CTkCheckBox(self.frame2, text="Envoyer moi feuille d'absence : fichier Excel dans l'addresse mail", font=my_font)
        self.checkbox.pack(pady=30)

        self.btn_start = ctk.CTkButton(self.frame2, text="Commencer", corner_radius=10, command=self.switch_to_page3, font=my_font)
        self.btn_start.pack(pady=10)

        
        self.frame3 = ctk.CTkFrame(master=self)
        self.frame3.pack(fill="both", expand=True)

        self.label2 = ctk.CTkLabel(self.frame3, text="Feuille d'absence", font=my_font)
        self.label2.pack(pady=40)
        default_values=[('  ', '   ', '  ', '  '), (' ', ' ', '  ', '  ')]
        global my_table
        my_table = CTkTable(self.frame3, values=default_values,width=220)
        my_table.pack(pady=10)
    
        self.btn_close = ctk.CTkButton(self.frame3, text=" Enregister et Envoyer", command=self.close_window, font=my_font)
        self.btn_close.pack(pady=10)

        self.show_page1()

    def show_page1(self):
        self.frame1.pack(fill="both", expand=True)
        self.frame2.pack_forget()
        self.frame3.pack_forget()



    def close_window(self):
        self.btn_close.configure(text="Attendez ...", state="disabled")
        module_name = self.optionmenu.get()
        for module in self.modules:
            if module[1] == module_name:
                module_id = module[0]
        insertAbsence(self.students, module_id)
        if self.checkbox.get() == 1:
            file_name = create_excel_file(self.students)
            email =self.input_email.get()
            send_email_with_excel(email, file_name)
        self.destroy()  # Fermer la fenêtre principale

        self.btn_close.configure(text="Fermer", state="disabled")


    def login(self):
        self.profId = verify_login(self.input_email.get(),self.input_password.get())
        if self.profId :
            self.frame2.pack(fill="both", expand=True)
            self.modules=getModules(self.profId)
            modules_names = [module[1] for module in self.modules] #update getmodules to get only the ones enseignés par le prof 
            self.optionmenu.configure(values=modules_names)
            self.optionmenu.set(modules_names[0])
            self.frame1.pack_forget()
            self.frame3.pack_forget()
            self.label_incorrect.pack_forget()
        else : 
             self.label_incorrect.pack(pady=10)
       




    def switch_to_page3(self):
        self.btn_start.configure(text="Attendez....", state="disabled")
        module_name = self.optionmenu.get()
        self.students,filiere=get_students_and_filiere_name(module_name, self.profId)
        studentss = [(t[0], t[1], t[2], t[4]) for t in self.students]
        my_table.configure(values=studentss)
        students_dir = r"students_images\\" + filiere + "\\"
        known_face_encodings = frf.load_known_faces(students_dir)
        face_recognition_thread = threading.Thread(target=frf.face_recognition_loop, args=(known_face_encodings, self.students))
        face_recognition_thread.start()
        self.frame3.pack(fill="both", expand=True)
        self.btn_start.configure(text="Commencer", state="enabled")
        self.frame1.pack_forget()
        self.frame2.pack_forget()

    

def _update_students_gui(students):
    studentss = [(t[0], t[1], t[2], t[4]) for t in students]
    my_table.update_values(values=studentss)

def create_main_window():
    window = MainWindow()
    window.mainloop()


