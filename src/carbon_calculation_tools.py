def calculate_carbon_from_day(ci_and_battery_data_for_day):
    """
    Calculates the total amount of carbon emissions (in gCO2) over a day based on the input of carbon intensity and battery power consumption data.
    
    Args:
    ci_and_battery_data_for_day (dict): A dictionary containing the keys "act_carbon_intensity/(gCO2/kWh)" and "battery_power_consumption/kW".
    
    Returns:
    float: The total amount of carbon emissions in gCO2 over the day.
    """
    # Calculate carbon consumption rate in gCO2/h
    carbon_consumption_rate = ci_and_battery_data_for_day["act_carbon_intensity/(gCO2/kWh)"] * ci_and_battery_data_for_day["battery_power_consumption/kW"] 
    
    # Calculate time interval length (in hours) per data point
    time_interval_len = 24 / len(carbon_consumption_rate)
    
    # Calculate total amount of carbon emissions (in gCO2) over the day
    g_co2_over_day = time_interval_len * sum(carbon_consumption_rate)
    
    return g_co2_over_day
