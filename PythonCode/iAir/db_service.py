import datetime

import mysql.connector as db_connector
import types_enums

db_server_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'test-123'
}

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'test-123',
    'database': 'iAir'
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

        if ('iAir',) in databases:
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

        create_air_condition_table: str = (
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


def add_condition(condition: types_enums.Conditions) -> bool:
    my_db_connection = db_connector.connect(**db_config)

    try:

        cursor = my_db_connection.cursor()

        insert_command: str = 'INSERT INTO Air_Condition (condition_name, enum_index) VALUES (%s, %s)'
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


def get_condition_id(condition: types_enums.Conditions) -> int:
    my_db_connection = db_connector.connect(**db_config)

    try:

        cursor = my_db_connection.cursor()

        query: str = 'SELECT Condition_ID FROM Air_Condition WHERE Enum_Index = %s'

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


def add_command(command: types_enums.Commands) -> bool:
    my_db_connection = db_connector.connect(**db_config)

    try:

        cursor = my_db_connection.cursor()

        insert_query: str = 'INSERT INTO Command (Command_Name, Enum_Index) VALUES (%s, %s)'
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


def get_command_id(condition: types_enums.Conditions) -> int:
    my_db_connection = db_connector.connect(**db_config)

    try:

        cursor = my_db_connection.cursor()

        query: str = 'SELECT Command_ID FROM Command WHERE Enum_Index = %s'

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
                        'Air_Condition.Enum_Index, '
                        'Temperature, '
                        'Humidity, '
                        'Carbon_Dioxide_Level, '
                        'Command.Enum_Index, '
                        'Activity_Time '
                        'FROM Activity_Log '
                        'JOIN Air_Condition ON Activity_Log.Condition_ID = Air_Condition.Condition_ID '
                        'JOIN Command ON Command.Command_ID = Activity_Log.Command_ID ')
        cursor.execute(select_query)

        result = cursor.fetchall()
        print(result)
        my_db_connection.close()
        print(len(result))
        for i in range(len(result)):
            row = result[i]
            activity = types_enums.Activity(
                activity_id=row[0],
                air_condition=types_enums.get_condition(row[1]),
                temperature=str(row[2]),
                humidity=str(row[3]),
                carbon_dioxide_level=str(row[4]),
                command=types_enums.get_command(row[5]),
                activity_time=row[6].strftime("%Y-%m-%d %H:%M:%S")
            )
            print(activity)
            activities.append(activity)

        return activities
    except Exception as e:
        print(e.args)
    finally:
        if my_db_connection.is_connected():
            cursor.close()
            my_db_connection.close()
            print("MySQL connection is closed.")


def add_activity(condition: types_enums.Conditions,
                 temperature: float,
                 humidity: float,
                 carbon_dioxide_level: float,
                 command: types_enums.Commands) -> bool:
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

        insert_command: str = ('INSERT INTO Activity_Log '
                               '(Condition_ID, Temperature, Humidity, Carbon_Dioxide_Level, Command_ID) '
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


def clear_activity_log():
    my_db_connection = db_connector.connect(**db_config)

    try:

        cursor = my_db_connection.cursor()

        delete_query = 'DELETE FROM Activity_Log'

        cursor.execute(delete_query)

        my_db_connection.commit()

        rows_affected = cursor.rowcount

        if rows_affected > 0:
            print(f"Deleted {rows_affected} rows from activity log.")

    except Exception as e:
        print(e.args)
    finally:
        if my_db_connection.is_connected():
            cursor.close()
            my_db_connection.close()
            print("MySQL connection is closed.")
