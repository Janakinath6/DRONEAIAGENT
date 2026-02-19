import pandas as pd
from sheets_service import get_sheet_data
from datetime import datetime
def match_pilot_to_mission(mission):
    pilots = get_sheet_data("Pilot_Roster")
    pilots = pilots[pilots["status"] == "Available"]
    pilots = pilots[pilots["skills"].str.contains(mission["required_skills"], case=False)]
    pilots = pilots[pilots["location"] == mission["location"]]
    pilots = pilots.sort_values("daily_rate")
    return pilots
def calculate_cost(pilot_row, mission):
    start = datetime.strptime(mission["start_date"], "%Y-%m-%d")
    end = datetime.strptime(mission["end_date"], "%Y-%m-%d")
    duration = (end - start).days
    return duration * pilot_row["daily_rate"]

def match_drone_to_mission(mission):
    drones = get_sheet_data("Drone_Fleet")
    drones = drones[drones["status"] == "Available"]
    if mission["weather"] == "Rainy":
        drones = drones[drones["weather_rating"] == "IP43"]
    drones = drones[drones["location"] == mission["location"]]
    return drones


def detect_double_booking(pilot_name, mission):
    missions = get_sheet_data("Missions")


    new_start = datetime.strptime(mission["start_date"], "%Y-%m-%d")
    new_end = datetime.strptime(mission["end_date"], "%Y-%m-%d")
    for _, row in missions.iterrows():
        if row["pilot"] == pilot_name:
            old_start = datetime.strptime(row["start_date"], "%Y-%m-%d")
            old_end = datetime.strptime(row["end_date"], "%Y-%m-%d")
            if not (new_end < old_start or new_start > old_end):
                return True
    return False


def check_budget(cost, mission):
    return cost > mission["budget"]


def skill_mismatch(pilot_row, mission):
    return mission["required_skills"] not in pilot_row["skills"]


def weather_risk(drone_row, mission):
    if mission["weather"] == "Rainy" and drone_row["weather_rating"] != "IP43":
        return True
    return False

def urgent_reassign(mission_id):
    missions = get_sheet_data("Missions")
    mission = missions[missions["project_id"] == mission_id].iloc[0]
    candidates = match_pilot_to_mission(mission)
    for _, pilot in candidates.iterrows():
        if not detect_double_booking(pilot["name"], mission):
            return pilot


    return None












