import xlsxwriter
from datetime import datetime

def create_excel_file(students):
    # Créer un nouveau fichier Excel
    title = "Absence " + datetime.now().strftime('%d-%m-%Y')
    
    workbook = xlsxwriter.Workbook(title+'.xlsx')
    
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


