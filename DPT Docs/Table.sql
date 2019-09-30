
create table UserGeneric
(
	
	IDNumber numeric(11) PRIMARY KEY,
	
	Firstname varchar(20),
	
	Lastname varchar(20),
	
	DateOfBirth date

)


create table Lecturer

(

    StaffNumber numeric(10) primary key not null,

    IDNumber numeric(11) not null,


);



create table Coordinator

(

    CoordinatorID numeric(5) not null primary key,

    StaffNumber Numeric(10) not null,


);

create table Document

(

	DocumentID int PRIMARY KEY,
	
	RawData varbinary()

);

create table Applicant

(

    IDNumber numeric (11) not null primary key,

    Firstname varchar(25) not null,

    Lastname varchar(25),
	
	DateOfBirth date

);

