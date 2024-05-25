from datetime import datetime
import cx_Oracle

# database connection

def connect() :
    try :   
        connection = cx_Oracle.connect(
           user="face_recog_usr",
           password="pswd",
           dsn="localhost:1521/orcl")  
        cursor = connection.cursor()
        print("Connected to Oracle Database")
        return cursor,connection
        
    except  cx_Oracle.DatabaseError as e:
              print("Error:", e)
              return None,None

# Close cursor and connection

def disconnect(cursor , connection) :
    cursor.close()
    connection.close()
   
def insertAbsence(students, module_id):
    cursor , connection = connect()
    for student in students:
        cne, _, _, _, status = student
        if status == "Absent":
            print("Student",cne,"is absent")
            current_datetime = datetime.now().strftime('%d-%b-%y')  # Format the date
            cursor.execute("INSERT INTO Absence (cne, id_mod, date_abs) VALUES (:1, :2, TO_DATE(:3, 'DD-MON-YY'))",
                           (cne, module_id, current_datetime))
            connection.commit()
            print("Data Inserted")
    disconnect(cursor, connection)

def getModules(id_prof):
    cursor , connection = connect()
    query="SELECT * FROM Module where id_prof=:id_prof"
    cursor.execute(query,id_prof=id_prof)
    modules = cursor.fetchall()
    return modules

def getStudents(): 
    cursor , connection = connect()
    cursor.execute("SELECT * FROM Etudiant")
    students = cursor.fetchall()
    #Ajouter a chaque etudiant colonne absent 
    students_with_status = []

    for tuple_donnees in students:
   
        tuple_avec_age = tuple_donnees + ("Absent",) 

        students_with_status.append(tuple_avec_age)
    return students_with_status


def verify_login(email, password):
     cursor, connection = connect()
     query = "SELECT id_prof, nom, prenom, email FROM Professeur WHERE email = :email AND password = :password"
     cursor.execute(query, email=email, password=password)    
     prof = cursor.fetchone()
     if prof : 
      return prof[0] 
     else : 
         return None


def get_students_and_filiere_name(module_name, prof_id):
    cursor, connection = connect()

    cursor.execute("SELECT id_fil FROM Module  WHERE Nom_mod = :module_name AND id_prof = :prof_id", module_name=module_name, prof_id=prof_id)
    result = cursor.fetchone()

    if result is None:
        return None 

    id_fil = result[0]

    cursor.execute("SELECT e.cne, e.nom, e.prenom, e.email FROM Etudiant e WHERE e.id_fil = :id_fil ", id_fil=id_fil)
    students = cursor.fetchall()

    cursor.execute(" SELECT nom_fil FROM Filiere WHERE id_fil = :id_fil ", id_fil=id_fil)
    filiere_result = cursor.fetchone()
    filiere_name = filiere_result[0] if filiere_result else None

    students_with_status = [(s[0], s[1], s[2], s[3], 'Absent') for s in students]

    return students_with_status, filiere_name

