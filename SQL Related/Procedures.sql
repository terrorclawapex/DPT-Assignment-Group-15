
create PROCEDURE IDSearch		-- Find a Applicant by searching for their ID number
    @ID numeric(11)
AS
BEGIN
    SELECT *
    FROM Applicant, Lecturer, Coordinator
    WHERE IDnumber = @ID;
END
GO


create PROCEDURE FindFirstAndSecondName		-- Find a person by searching for their First Name and Surname
    @Firstname varchar(25),
    @Lastname varchar(25)
AS
BEGIN
    SELECT *
    FROM Applicant, Lecturer, Coordinator
    WHERE Firstname = @Firstname AND Lastname = LastName;
END
GO


create Procedure FindFirstName		-- Search for Person's first name
    @SearchString varchar
AS
BEGIN
    SELECT Firstname, Lastname, IDNumber	
    from Applicant, Lecturer, Coordinator
    where Firstname like @SearchString;
END
Go


create Procedure FindLastName		-- Search for Person's last name
    @SearchString varchar
AS
BEGIN
    SELECT Firstname, Lastname, IDNumber
    from Applicant, Lecturer, Coordinator
    where Lastname like @SearchString;
END
Go


create Procedure FindAllFirstNames		-- Get all First names
AS
BEGIN
    SELECT Firstname
    FROM Applicant, Lecturer, Coordinator;
END
Go


create Procedure FindAllLastNames		-- Get all Last names
AS
BEGIN
    SELECT Lastname
    FROM Applicant, Lecturer, Coordinator;
END
GO


create Procedure FindAllIDNumbers		-- Get all ID Numbers
AS
BEGIN
    Select IDNumber
    from Applicant, Lecturer, Coordinator;
END
GO


create Procedure GetAllDatesOfBirth		-- Get all Dates of Birth
As
BEGIN
    Select DateOfBirth
    from Applicant, Lecturer, Coordinator;
END
Go


create PROCEDURE GetIDNumber		-- Find Applicant with specific ID Number
    @IDNumber numeric(11)
AS
BEGIN
    SELECT *
    FROM Applicant
    WHERE IDNumber = @IDNumber;
END
GO

