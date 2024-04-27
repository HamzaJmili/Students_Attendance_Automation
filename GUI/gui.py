import customtkinter as ctk
from CTkTable import *

class MainWindow(ctk.CTk ): 
    global tree #no need
  
    def __init__(self,students):
        super().__init__()
        self.title("Main Window")
        self.geometry("900x600")
        #self.iconbitmap(r"assets\icons\faceIA.ico")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme('green')
        my_font= ctk.CTkFont(family="Calibri" , weight="bold" ,size=15) 
        self.students=students
        self.frame1 = ctk.CTkFrame(master=self)
        self.frame1.pack( fill ="both" ,expand=True)

        self.label1 = ctk.CTkLabel(self.frame1, text="Séléctionner le module enseigné : ", font=my_font)
        self.label1.pack(pady=40)

        self.optionmenu=ctk.CTkOptionMenu(self.frame1,values=['Python pour AI','Traitement d\'image','JEE','Anglais','Français'] , width=260,font=my_font)
        # self.optionmenu.get()
        self.optionmenu.pack(pady=30)

        self.inputEmail = ctk.CTkEntry(self.frame1,placeholder_text="Entrez votre adresse mail", width=300)
        self.inputEmail.pack(pady=30)

        checkbox_2 = ctk.CTkCheckBox(self.frame1, text="Envoyer moi feuille d'absence : fichier Excel sur l'addresse mail ", font=my_font)
        checkbox_2.pack(pady=30)


        # Create Button to switch to Page 2
        self.btn_start = ctk.CTkButton(self.frame1, text="Start", corner_radius=10, command=self.switch_to_page2,font=my_font)
        self.btn_start.pack(pady=10)

        self.frame2 = ctk.CTkFrame(master=self)
        self.frame2.pack(fill ="both" ,expand=True)

          # Create Label for Page 2
        self.label2 = ctk.CTkLabel(self.frame2, text="Feuille d'absence", font=my_font)
        self.label2.pack(pady=40)


        studentstest = [("Alice", True),("Bob", False),("Charlie", True),("David", False),("Eve", True)]
        global my_table
        my_table = CTkTable(self.frame2, values=students , width=220) 
       
        my_table.pack(pady=10)
        # https://pypi.org/project/CTkTable/
       
    
        # Create Button to switch to Page 1
        self.btn_close = ctk.CTkButton(self.frame2, text="Fermer et Envoyer", command=self.switch_to_page1, font=my_font)
        self.btn_close.pack(pady=10)

        # Initially show Page 1
        self.show_page1()


    


    def show_page1(self):
        # Show Frame 1 and hide Frame 2
        self.frame1.pack(fill ="both" ,expand=True)
        self.frame2.pack_forget()

    def switch_to_page1(self):
        self.show_page1()

    def switch_to_page2(self):
        # Show Frame 2 and hide Frame 1
        self.frame2.pack(fill ="both" ,expand=True)
        self.frame1.pack_forget()


        

      

def _update_students_gui(students,i):
       #my_table.delete_row(index=i)
       my_table.update_values(values=students)
        
    
def create_main_window(students):
    window = MainWindow(students)
    window.mainloop()

