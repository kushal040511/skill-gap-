CREATE DATABASE skillgapdb;

USE skillgapdb;

CREATE TABLE skill_courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(100),
    course VARCHAR(255)
);

-- Example entries
INSERT INTO skill_courses (subject, course) VALUES ('Mathematics', 'Mastering Algebra on Coursera');
INSERT INTO skill_courses (subject, course) VALUES ('Physics', 'Physics for Beginners - edX');
INSERT INTO skill_courses (subject, course) VALUES ('Computer Science', 'CS50 by Harvard - FreeCodeCamp');
INSERT INTO skill_courses (subject, course) VALUES ('English', 'Academic English on Udemy');
