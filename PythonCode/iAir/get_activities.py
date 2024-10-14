import db_service
import json

activities = db_service.get_activities()

print(activities)
