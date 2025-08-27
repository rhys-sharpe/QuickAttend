DELETE FROM Section;
DELETE FROM Category;
DELETE FROM Student;
DELETE FROM Attended;

INSERT INTO Section (label) VALUES('A'), ('B');

INSERT INTO Category (category, score) VALUES
    ('PRESENT', 2),
    ('EXCUSED', 2),
    ('TARDY', 1),
    ('ABSENT', 0);

INSERT INTO Student (id, student_name, section) VALUES
    (0, 'Allamaraine Johnson', 'A'),
    (1, 'Michael Phillips', 'B'),
    (2, 'Whosiwhatsit Anonymous', 'A'),
    (3, 'Thingamajig Anonymous', 'B');