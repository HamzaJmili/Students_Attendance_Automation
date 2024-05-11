import customtkinter as ctk
from CTkTable import *
from Utility.database import insertAbsence ,getModules
from Utility.saveSendExcel import create_excel_file


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
        studentss = [(t[0], t[1], t[2], t[4]) for t in students]
        self.frame1 = ctk.CTkFrame(master=self)
        self.frame1.pack( fill ="both" ,expand=True)

        self.label1 = ctk.CTkLabel(self.frame1, text="Séléctionner le module enseigné : ", font=my_font)
        self.label1.pack(pady=40)
        self.modules=getModules()
        module_names = [module[1] for module in self.modules]
        self.optionmenu=ctk.CTkOptionMenu(self.frame1,values=module_names , width=260,font=my_font)
        self.optionmenu.get()
        self.optionmenu.pack(pady=30)

        self.inputEmail = ctk.CTkEntry(self.frame1,placeholder_text="Entrez votre adresse mail", width=300)
        self.inputEmail.pack(pady=30)

        self.checkbox = ctk.CTkCheckBox(self.frame1, text="Envoyer moi feuille d'absence : fichier Excel sur l'addresse mail ", font=my_font)
        self.checkbox.pack(pady=30)


        # Create Button to switch to Page 2
        self.btn_start = ctk.CTkButton(self.frame1, text="Start", corner_radius=10, command=self.switch_to_page2,font=my_font)
        self.btn_start.pack(pady=10)

        self.frame2 = ctk.CTkFrame(master=self)
        self.frame2.pack(fill ="both" ,expand=True)

          # Create Label for Page 2
        self.label2 = ctk.CTkLabel(self.frame2, text="Feuille d'absence", font=my_font)
        self.label2.pack(pady=40)


        global my_table
        my_table = CTkTable(self.frame2, values=studentss , width=220) 
       
        my_table.pack(pady=10)
        # https://pypi.org/project/CTkTable/
       
    
        # Create Button to switch to Page 1
        self.btn_close = ctk.CTkButton(self.frame2, text="Fermer et Envoyer", command=self.close_window, font=my_font)
        self.btn_close.pack(pady=10)

        # Initially show Page 1
        self.show_page1()


    


    def show_page1(self):
        # Show Frame 1 and hide Frame 2
        self.frame1.pack(fill ="both" ,expand=True)
        self.frame2.pack_forget()


    def close_window(self):
        module_name=self.optionmenu.get()
        for module in  self.modules:
            if module[1] == module_name:  # Check if the module name matches
                module_id = module[0]
        self.btn_close.configure(text="Wait" , state = "disabled")
        if(self.checkbox.get()==1) :
            create_excel_file(self.students)
        insertAbsence(self.students , module_id)
        
        self.btn_close.configure(text="Done " , state = "disabled")

        #self.destroy()
        #self.show_page1()

    def switch_to_page2(self):
        # Show Frame 2 and hide Frame 1
        self.frame2.pack(fill ="both" ,expand=True)
        self.frame1.pack_forget()
        
    


        

      

def _update_students_gui(students):
       #my_table.delete_row(index=i)
    studentss = [(t[0], t[1], t[2], t[4]) for t in students]

    my_table.update_values(values=studentss)
        
    
def create_main_window(students):
    window = MainWindow(students)
    window.mainloop()


