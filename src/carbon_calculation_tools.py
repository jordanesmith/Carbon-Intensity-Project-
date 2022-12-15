

def calculate_carbon_from_day(ci_and_battery_data_for_day):
    
    carbon_consumption_rate = ci_and_battery_data_for_day["act_carbon_intensity/(gCO2/kWh)"] * ci_and_battery_data_for_day["battery_power_consumption/kWh"]
    time_interval_len = 24/ len(carbon_consumption_rate) # no. hours per given data point 
    
    return time_interval_len * sum(carbon_consumption_rate)