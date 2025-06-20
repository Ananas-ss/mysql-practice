CREATE DATABASE student;
USE student;
CREATE TABLE students (
    id INT COMMENT '编号',
    name VARCHAR(10) COMMENT '姓名',
    height INT COMMENT '身高'
) COMMENT='学生表';
ALTER TABLE students ADD age TINYINT COMMENT '年龄';
ALTER TABLE students ADD gender CHAR(1) COMMENT '性别';
ALTER TABLE students DROP COLUMN gender;
INSERT INTO students (name, height) VALUES
('Lucy', 160),
('Mike', 172),
('Charlie', 168);
SELECT * FROM students;
UPDATE students SET height = 175 WHERE name = 'Mike';
DELETE FROM students WHERE name = 'Charlie';
SELECT * FROM students;
