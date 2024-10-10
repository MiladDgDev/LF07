import mysql.connector as db_connector
import types_enums

db_server_config = {
'host': 'localhost',
'user': 'root'
}

db_config = {
'host': 'localhost',
'user': 'root',
'database': 'iair'
}


def setup_database():
    my_db_connection = db_connector.connect(**db_server_config)

    try:
        cursor = my_db_connection.cursor()

        cursor.execute('DROP DATABASE IF EXISTS iAir; ')
        cursor.execute('CREATE DATABASE IF NOT EXISTS iAir; ')

        my_db_connection.commit()

    except Exception as e:
        print(e.args)

    finally:
        if my_db_connection.is_connected():
            cursor.close()
            my_db_connection.close()
            print("MySQL connection is closed.")


def check_db_existence() -> bool:
    my_db_connection = db_connector.connect(**db_server_config)

    try:
        cursor = my_db_connection.cursor()

        check_query: str = "SHOW DATABASES;";

        cursor.execute(check_query)

        databases = cursor.fetchall()

        print(databases)

        if ('iair',) in databases:
            print("Database created successfully.")
            return True
        else:
            print("Database creation failed.")
            return False

    except Exception as e:
        print(e.args)
        return False

    finally:
        if my_db_connection.is_connected():
            cursor.close()
            my_db_connection.close()
            print("MySQL connection is closed.")


def setup_tables():
    my_db_connection = db_connector.connect(**db_config)

    try:
        cursor = my_db_connection.cursor()

        create_air_condition_table: str =(
            'CREATE TABLE Air_Condition ( '
            'Condition_ID 			INT AUTO_INCREMENT PRIMARY KEY, '
            'Condition_Name			VARCHAR(50), '
            'Enum_Index				INT '
            '); '
        )

        create_command_table: str = (
            'CREATE TABLE Command ( '
            'Command_ID 			INT AUTO_INCREMENT PRIMARY KEY, '
            'Command_Name		VARCHAR(50), '
            'Enum_Index			INT '
            '); '
        )

        create_activity_log_table: str = (
            'CREATE TABLE Activity_Log ( '
            'Activity_ID					INT AUTO_INCREMENT PRIMARY KEY, '
            'Condition_ID					INT NOT NULL, '
            'Temperature					DECIMAL (5, 2) NOT NULL, '
            'Humidity						DECIMAL (5, 2) NOT NULL, '
            'Carbon_Dioxide_Level			DECIMAL (6, 2) NOT NULL, '
            'Command_ID					INT NOT NULL, '
            'Activity_Time					TIMESTAMP DEFAULT CURRENT_TIMESTAMP, '
            'CONSTRAINT `fk_condition` '
            '    FOREIGN KEY (Condition_ID) REFERENCES Air_Condition (Condition_ID) '
            '    ON DELETE CASCADE '
            '    ON UPDATE RESTRICT, '
            'CONSTRAINT `fk_command` '
            '    FOREIGN KEY (Command_ID) REFERENCES Command (Command_ID) '
            '    ON DELETE CASCADE '
            '    ON UPDATE RESTRICT '
            ');'
        )

        cursor.execute(create_air_condition_table)
        cursor.execute(create_command_table)
        cursor.execute(create_activity_log_table)

        my_db_connection.commit()

    except Exception as e:
        print(e.args)

    finally:
        if my_db_connection.is_connected():
            cursor.close()
            my_db_connection.close()
            print("MySQL connection is closed.")


def check_tables_existence() -> bool:
    my_db_connection = db_connector.connect(**db_config)

    try:
        cursor = my_db_connection.cursor()

        check_query: str = ("SHOW TABLES;");

        cursor.execute(check_query)

        tables = cursor.fetchall()

        print(tables)

        if tables.__len__() == 3:
            print("Tables created successfully.")
            return True
        else:
            print("Database creation failed.")
            return False

    except Exception as e:
        print(e.args)
        return False

    finally:
        if my_db_connection.is_connected():
            cursor.close()
            my_db_connection.close()
            print("MySQL connection is closed.")


def add_condition(condition: types_enums.conditions) -> bool:
    my_db_connection = db_connector.connect(**db_config)

    try:

        cursor = my_db_connection.cursor()

        insert_command: str = 'INSERT INTO air_condition (condition_name, enum_index) VALUES (%s, %s)'
        params = (condition.name, condition.value)

        cursor.execute(insert_command, params)
        rows_affected: int = cursor.rowcount

        print(f"rows affected: {rows_affected}")

        if rows_affected == 0:
            my_db_connection.rollback()
            my_db_connection.close()
            return False
        else:
            my_db_connection.commit()
            my_db_connection.close()
            return True
    except db_connector.Error as error:
        print(f"Error while connecting to MySQL: {error}")
        my_db_connection.close()
        return False
    finally:
        if my_db_connection.is_connected():
            cursor.close()
            my_db_connection.close()
            print("MySQL connection is closed.")


def get_condition_id(condition: types_enums.conditions) -> int:
    my_db_connection = db_connector.connect(**db_config)

    try:

        cursor = my_db_connection.cursor()

        query: str = 'SELECT Condition_ID FROM air_condition WHERE Enum_Index = %s'

        params = (condition.value,)
        cursor.execute(query, params)

        result = cursor.fetchone()

        if result is None:
            return 0

        return result[0]
    except Exception as error:
        print(f"Error while connecting to MySQL: {error}")
    finally:
        if my_db_connection.is_connected():
            cursor.close()
            my_db_connection.close()
            print("MySQL connection is closed.")


def add_command(command: types_enums.commands) -> bool:
    my_db_connection = db_connector.connect(**db_config)

    try:

        cursor = my_db_connection.cursor()

        insert_query: str = 'INSERT INTO command (Command_Name, enum_index) VALUES (%s, %s)'
        params = (command.name, command.value)

        cursor.execute(insert_query, params)
        rows_affected: int = cursor.rowcount

        print(f"rows affected: {rows_affected}")

        if rows_affected == 0:
            my_db_connection.rollback()
            my_db_connection.close()
            return False
        else:
            my_db_connection.commit()
            my_db_connection.close()
            return True
    except db_connector.Error as error:
        print(f"Error while connecting to MySQL: {error}")
        my_db_connection.close()
        return False
    finally:
        if my_db_connection.is_connected():
            cursor.close()
            my_db_connection.close()
            print("MySQL connection is closed.")


def get_command_id(condition: types_enums.conditions) -> int:
    my_db_connection = db_connector.connect(**db_config)

    try:

        cursor = my_db_connection.cursor()

        query: str = 'SELECT Command_ID FROM command WHERE Enum_Index = %s'

        params = (condition.value,)

        cursor.execute(query, params)
        result = cursor.fetchone()

        if result is None:
            return 0

        return result[0]
    except Exception as error:
        print(f"Error while connecting to MySQL: {error}")
    finally:
        if my_db_connection.is_connected():
            cursor.close()
            my_db_connection.close()
            print("MySQL connection is closed.")


def get_activities() -> [dict]:
    activities: [types_enums.Activity] = []
    my_db_connection = db_connector.connect(**db_config)

    try:
        cursor = my_db_connection.cursor()

        select_query = ('SELECT '
                        'Activity_ID, '
                        'air_condition.enum_index, '
                        'Temperature, '
                        'Humidity, '
                        'Carbon_Dioxide_Level, '
                        'command.enum_index, '
                        'Activity_Time '
                        'FROM activity_log '
                        'JOIN air_condition ON activity_log.Condition_ID = air_condition.Condition_ID '
                        'JOIN command ON command.Command_ID = activity_log.Command_ID ')
        cursor.execute(select_query)

        result = cursor.fetchall()

        for row in result:
            activities.append(
                types_enums.Activity(
                    activity_id=row[0],
                    air_condition=types_enums.get_condition(row[1]),
                    temperature=row[3],
                    humidity=row[4],
                    carbon_dioxide_level=row[5],
                    command=types_enums.get_command(row[6]),
                    activity_time=row[7]
                )
            )
            my_db_connection.close()
        return activities
    except Exception as e:
        print(e.args)
    finally:
        if my_db_connection.is_connected():
            cursor.close()
            my_db_connection.close()
            print("MySQL connection is closed.")


def add_activity(condition: types_enums.conditions,
                 temperature: float,
                 humidity: float,
                 carbon_dioxide_level: float,
                 command: types_enums.commands) -> bool:
    condition_id: int = 0
    command_id = 0

    try:
        queried_condition_id = get_condition_id(condition)

        if queried_condition_id == 0:
            raise Exception("Condition ID not found!")
        condition_id = queried_condition_id

        queried_command_id = get_command_id(command)
        if queried_command_id == 0:
            raise Exception("Command ID not found!")
        command_id = queried_command_id

    except Exception as e:
        print(e.args)

    my_db_connection = db_connector.connect(**db_config)

    try:

        cursor = my_db_connection.cursor()

        insert_command: str = ('INSERT INTO activity_log '
                               '(condition_id, temperature, humidity, carbon_dioxide_level, command_id) '
                               'VALUES (%s, %s, %s, %s, %s)')
        params = (condition_id, temperature, humidity, carbon_dioxide_level, command_id)

        cursor.execute(insert_command, params)

        rows_affected = cursor.rowcount

        if rows_affected == 1:
            my_db_connection.commit()
            return True
        else:
            return False
    except Exception as e:
        print(e.args)
    finally:
        if my_db_connection.is_connected():
            cursor.close()
            my_db_connection.close()
            print("MySQL connection is closed.")
