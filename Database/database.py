from datetime import date
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

def desconnect(cursor,connection) :
    cursor.close()
    connection.close()

def insertAbsence( cursor, connection , students) :
    
   for i,student in students :
        if student[i][1]==False :
             cursor.execute("INSERT INTO Absence VALUES (:1, :2)", (student[0], "Module122") ,date.now())
             connection.commit()
             
   desconnect(cursor,connection)