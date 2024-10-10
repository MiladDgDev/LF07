import db_service
import types_enums


db_service.setup_database()

database_initialization_successful = db_service.check_db_existence()
print(f'Database initialization successful: {database_initialization_successful}')

if database_initialization_successful:
    db_service.setup_tables()
    tables_are_set = db_service.check_tables_existence()
    print(f'tables are set: {tables_are_set}')


for condition in types_enums.conditions:
    success = db_service.add_condition(condition)
    if success is True:
        print(f'Condition {condition} successfully added to the database')
    else:
        print(f'Adding the Condition {condition} failed!')

for command in types_enums.Commands:
    success = db_service.add_command(command)
    if success is True:
        print(f'Command {command} successfully added to the database')
    else:
        print(f'Adding the Command {command} failed!')


