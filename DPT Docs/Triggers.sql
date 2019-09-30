create trigger ApplicantAuditTrigger on Applicant after update,
insert as begin insert into ApplicantAudit (IDNumber, Firstname, Lastname, DateOfBirth, UpdatedBy, UpdatedOn)
 select i.IDNumber, i.Firstname, i.Lastname, i.DateOfBirth, SUSER_SNAME(),
 getdate() from Applicant t inner join inserted i on t.IDNumber=i.IDNumber;
end
go

create trigger CoordinatorAuditTrigger on Coordinator after update,
insert as begin insert into CoordinatorAudit (CoordinatorID, StaffNumber, UpdatedBy, UpdatedOn)
 select i.CoordinatorID, i.StaffNumber, SUSER_SNAME(),
 getdate() from Coordinator t inner join inserted i on t.OrderID=i.OrderID;
end
go

create trigger LecturerAuditTrigger on Lecturer after update,
insert as begin insert into LecturerAudit (StaffNumber, IDNumber, UpdatedBy, UpdatedOn)
select i.StaffNumber, i.IDNumber, SUSER_SNAME(),
 getdate() from Lecturer t inner join inserted i on t.OrderID=i.OrderID;
end
go

create trigger DocumentAuditTrigger on Documents after update,
insert as begin insert into AuditDocuments (DocumentID, RawDate, UpdatedBy, UpdatedOn)
select i.DocumentID, i.RawData, SUSER_SNAME(),
 getdate() from Documents t inner join inserted i on t.OrderID=i.OrderID;
end
go