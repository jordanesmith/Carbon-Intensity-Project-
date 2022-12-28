

def calculate_carbon_for_day_given_days_data(ci_and_battery_data_for_day):
    
    carbon_consumption_rate = ci_and_battery_data_for_day["act_carbon_intensity/(gCO2/kWh)"] * ci_and_battery_data_for_day["battery_power_consumption/kW"] # in gCO2/h
    time_interval_len = 24 / len(carbon_consumption_rate) # no. hours per given data point 
    
    g_co2_over_day = time_interval_len * sum(carbon_consumption_rate)
    
    return g_co2_over_day