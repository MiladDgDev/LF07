import db_service
import types_enums

database_setup_successful = db_service.setup_database()

print(f'Database initialization successful: {database_setup_successful}')

# for condition in types_enums.conditions:
#     success = db_service.add_condition(condition)
#     if success is True:
#         print(f'Condition {condition} successfully added to the database')
#     else:
#         print(f'Adding the Condition {condition} failed!')
#
# for command in types_enums.commands:
#     success = db_service.add_command(command)
#     if success is True:
#         print(f'Command {command} successfully added to the database')
#     else:
#         print(f'Adding the Command {command} failed!')


