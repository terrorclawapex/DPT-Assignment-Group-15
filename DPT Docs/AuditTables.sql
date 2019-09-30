

create table Documents
(
	DocumentID int Primary Key identity (1,1),
	RawData varbinary,

);

create table AuditDocuments
(
	AuditID int Identity (1,1) primary key,
	DocumentID int ,
	RawData varbinary,
	UpdatedOn date,
	UpdatedBy varchar(128)

);


create table ApplicantAudit
(
	AuditID int Identity (1,1) primary key,
	IDNumber numeric (11),
	Firstname varchar(25),
	Lastname varchar(25),
	DateOfBirth date,
	UpdatedOn date,
	UpdatedBy varchar(128)
);

create table CoordinatorAudit
(
	AuditID int Identity (1,1) primary key,
	CoordinatorID numeric(5),
	StaffNumber numeric (10),
	UpdatedOn date,
	UpdatedBy varchar(128)
);

create table LecturerAudit
(
	AuditID int Identity (1,1) primary key,
	StaffNumber numeric (10),
	IDNumber numeric(11),
	UpdatedOn date,
	UpdatedBy varchar(128)
);
