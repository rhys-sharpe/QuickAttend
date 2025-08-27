CREATE TABLE Section (
    label VARCHAR(2),
    PRIMARY KEY (label)
);

CREATE TABLE Category (
    category VARCHAR(15),
    score INT,
    PRIMARY KEY category
);

CREATE TABLE Student (
    id INT,
    student_name VARCHAR(75),
    section VARCHAR(2),
    PRIMARY KEY (id),
    FOREIGN KEY (section) REFERENCES Section
);

CREATE TABLE Attended (
    id INT,
    class_date DATETIME,
    section VARCHAR(2),
    attended VARCHAR(15),
    PRIMARY KEY (id),
    FOREIGN KEY (section) REFERENCES Section,
    FOREIGN KEY (attended) REFERENCES Category
);