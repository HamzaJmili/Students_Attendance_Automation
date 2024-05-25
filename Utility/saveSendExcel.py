import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import xlsxwriter
from datetime import datetime

def create_excel_file(students):
    # Créer un nouveau fichier Excel
    title = "Absence " + datetime.now().strftime('%d-%m-%Y')
    
    workbook = xlsxwriter.Workbook(title+'.xlsx')
    file_name =title+'.xlsx'
    
    # Ajouter une feuille de calcul
    worksheet = workbook.add_worksheet()
    
    # Définir le style pour le titre
    title_format = workbook.add_format({'bold': True, 'font_size': 14})
    
    # Écrire le titre dans la cellule A1
    worksheet.write('A1', title, title_format)
    
    # Définir le style pour le header
    header_format = workbook.add_format({'bold': True})
    
    # Définir le header
    header = ['CNE', 'NOM', 'PRENOM', 'EMAIL', 'ABSENT']
    
    # Écrire le header dans les cellules A3:E3
    for col, value in enumerate(header):
        worksheet.write(2, col, value, header_format)
    
    # Définir le style pour les cellules "Absent" dans la colonne "Status"
    absent_format = workbook.add_format({'color': 'red','bold': True})
    
    # Écrire les informations des étudiants
    for row, student in enumerate(students, start=3):
        for col, value in enumerate(student):
            
            if col == 4 and value == "Absent":
                worksheet.write(row, col, value, absent_format)  # Appliquer le style si la colonne est "Status" et la valeur est "Absent"
            else:
                worksheet.write(row, col, value)
    
    # Fermer le fichier Excel
    workbook.close()
    return file_name



def send_email_with_excel(receiver_email, attachment_path):
    # Paramètres de connexion au serveur SMTP Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Port SMTP pour Gmail (TLS)
    smtp_username = 'umi.fsm.noreply@gmail.com'
    smtp_password='wpnk mufk twze mach'
 
      # Votre mot de passe Gmail
    
    # Créer un objet MIMEMultipart
    msg = MIMEMultipart()
    
    # Définir les détails de l'email
    msg['From'] = smtp_username
    msg['To'] = receiver_email
    msg['Subject'] = "Absence Report " + datetime.now().strftime('%d-%m-%Y')  # Sujet avec la date actuelle
    
    # Attacher le fichier Excel à l'email
    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename=students.xlsx')
        msg.attach(part)
    
    # Connexion et envoi de l'email via le serveur SMTP Gmail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Activer le mode TLS
        server.login(smtp_username, smtp_password)  # Connexion au serveur SMTP Gmail
        server.sendmail(smtp_username, receiver_email, msg.as_string())  # Envoi de l'email
        print("Email sent successfully")



