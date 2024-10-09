DROP DATABASE IF EXISTS iAir;

CREATE DATABASE IF NOT EXISTS iAir;

USE iAir;

CREATE TABLE Air_Condition (
Condition_ID 			INT AUTO_INCREMENT PRIMARY KEY,
Condition_Name			VARCHAR(50),
Enum_Index				INT
);


CREATE TABLE Command (
Command_ID 			INT AUTO_INCREMENT PRIMARY KEY,
Command_Name		VARCHAR(50),
Enum_Index			INT
);


air_conditionCREATE TABLE ActivityLog (
Activity_ID						INT AUTO_INCREMENT PRIMARY KEY,
Condition_ID					INT NOT NULL,
Temperature						DECIMAL (5, 2) NOT NULL,
Humidity							DECIMAL (5, 2) NOT NULL,
Carbon_Dioxide_Level			DECIMAL (6, 2) NOT NULL,
Command_ID						INT NOT NULL,
Activity_Time					TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
CONSTRAINT `fk_condition`
    FOREIGN KEY (Condition_ID) REFERENCES Air_Condition (Condition_ID)
    ON DELETE CASCADE
    ON UPDATE RESTRICT,
CONSTRAINT `fk_command`
    FOREIGN KEY (Command_ID) REFERENCES Command (Command_ID)
    ON DELETE CASCADE
    ON UPDATE RESTRICT
);

