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
        name, status = student
        if status == "Absent":
            print("Student",name,"is absent")
            current_datetime = datetime.now().strftime('%d-%b-%y')  # Format the date
            cursor.execute("INSERT INTO Absence (cne, id_mod, date_abs) VALUES (:1, :2, TO_DATE(:3, 'DD-MON-YY'))",
                           (name, module_id, current_datetime))
            connection.commit()
            print("Data Inserted")
    disconnect(cursor, connection)

def getModules():
    cursor , connection = connect()
    cursor.execute("SELECT * FROM Module")
    modules = cursor.fetchall()
    return modules