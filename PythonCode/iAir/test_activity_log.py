import db_service
import types_enums

success = db_service.add_activity(
    condition=types_enums.Conditions.DESIRABLE,
    temperature=24.2,
    humidity=45,
    carbon_dioxide_level=500,
    command=types_enums.Commands.CLOSE
)

print(f"activity logged: {success}")

if success is True:
    activities = db_service.get_activities()
    print(f"logged activities: {activities}")
    db_service.clear_activity_log()
