
create table Etudiant (   
    cne varchar(10) PRIMARY KEY  , 
    Nom varchar(40) NOT NULL, 
    Prenom varchar(40) NOT NULL ,
    Email varchar(50) NOT NULL ) ;

create table Module ( 
    id_mod int PRIMARY KEY , 
    Nom_mod varchar(50) NOT NULL);

create table Absence (
    cne varchar(10) ,
    id_mod int , 
    date_abs date NOT NULL,
    PRIMARY KEY (cne,id_mod,date_abs),
    foreign key cne references Etudiant(cne), 
    foreign key id_mod references Module(id_mod)); 