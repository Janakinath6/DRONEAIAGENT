from assignment_engine import match_pilot_to_mission, urgent_reassign
from sheets_service import get_sheet_data

def process_query(user_input: str):
    
    user_input = user_input.lower()

    # 🔹 Assign pilot
    if "assign pilot" in user_input:
        missions = get_sheet_data("Missions")
        mission = missions.iloc[0]   # testing with first mission
        pilots = match_pilot_to_mission(mission)

        if pilots.empty:
            return "No available pilot found."

        return f"Suggested Pilot: {pilots.iloc[0]['name']}"

    # 🔹 Urgent reassignment
    if "urgent" in user_input:
        return "Urgent reassignment logic triggered."

    return "Command not recognized."
