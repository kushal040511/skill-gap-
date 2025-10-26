-- Create database
CREATE DATABASE IF NOT EXISTS skillgapdb;
USE skillgapdb;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Create skill_courses table
CREATE TABLE IF NOT EXISTS skill_courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(100) NOT NULL,
    course VARCHAR(255) NOT NULL
);

-- Insert sample subjects and their recommended courses
INSERT INTO skill_courses (subject, course) VALUES
('Mathematics', 'Advanced Mathematics Course'),
('Physics', 'Fundamentals of Physics'),
('Chemistry', 'Organic Chemistry Basics'),
('Biology', 'Human Biology Introduction'),
('History', 'World History Overview'),
('Geography', 'Understanding Earth Systems'),
('Political Science', 'Political Systems 101'),
('Economics', 'Principles of Economics'),
('Psychology', 'Introduction to Psychology'),
('Sociology', 'Understanding Human Society'),
('Computer Science', 'Basics of Programming'),
('Information Technology', 'IT Infrastructure Basics'),
('Environmental Science', 'Climate Change Awareness'),
('Physical Education', 'Fitness and Health Fundamentals'),
('Business Studies', 'Business Management Essentials'),
('Accountancy', 'Introduction to Accounting'),
('Statistics', 'Fundamentals of Statistics'),
('English', 'Mastering English Communication'),
('French', 'French Language Basics'),
('German', 'German Language for Beginners'),
('Hindi', 'Hindi Language Proficiency'),
('Telugu', 'Telugu Language Introduction'),
('Tamil', 'Tamil Language Skills'),
('Kannada', 'Kannada Language Learning'),
('Malayalam', 'Malayalam Basics'),
('Marathi', 'Marathi Language Training'),
('Gujarati', 'Gujarati Communication Skills'),
('Punjabi', 'Punjabi Language Basics'),
('Sanskrit', 'Introduction to Sanskrit'),
('Arts', 'Creative Arts Program'),
('Music', 'Fundamentals of Music'),
('Dance', 'Basics of Dance Techniques'),
('Drama', 'Theater and Drama Essentials'),
('Philosophy', 'Introduction to Philosophy'),
('Law', 'Basics of Legal Studies'),
('Engineering Drawing', 'Technical Drawing Skills'),
('Robotics', 'Introduction to Robotics'),
('Astronomy', 'Basics of Astronomy'),
('Astrophysics', 'Understanding Astrophysics'),
('Nutrition', 'Nutrition and Dietetics'),
('Fashion Studies', 'Fundamentals of Fashion Design'),
('Home Science', 'Home Science Concepts'),
('Agriculture', 'Introduction to Agricultural Science'),
('Medical Science', 'Basics of Medical Studies'),
('Zoology', 'Zoology Fundamentals'),
('Botany', 'Plant Science Basics'),
('Anthropology', 'Human Evolution and Society'),
('Photography', 'Photography Skills and Techniques'),
('Film Studies', 'Introduction to Film Production');

-- ── Notes table for rich-text user notes ──
CREATE TABLE IF NOT EXISTS notes (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  user_id    INT NOT NULL,
  content    LONGTEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
