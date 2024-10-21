import numpy as np


def calculate_time_between_top_of_thermals(distance_m, thermal_strength_ms, velocity_ms, sink_rate, headwind_ms=0):
    '''
    Imagine a glider at the top of a thermal (Start position below). 
    Given:
        The distance to the next climb
        The strength of the next thermal
        The velocity of the glider
        The sink rate of the glider at the given velocity

    This function calculates the time it will take to both glide and climb to the top of the next thermal. 

    *  Start                                     * Finish
    _~                                           _/
    _/   `   ~                                   _/
    _/           `   ~   Glide Time              _/
    _/                   `   ~                   _/ Climb Time
    _/                           `   ~           _/
    _/                                   `   ~   _/

    Glide Time = Distance / Velocity. 

    Climb Time = Altitude Lost / Thermal Strength 
    Where:
        Altitude Lost = Glide Time * |Sink Rate|
        Note that sink rate is provided as a vector so we take its magnitude only

    Therefore, 
    Total Time = Glide Time + (Glide Time * Sink Rate) / Thermal Strength
    or 
    Total Time = Glide Time * (1 + (|Sink Rate| / Thermal Strength))
    '''
    return ((distance_m/(velocity_ms-headwind_ms))*(1+abs(sink_rate)/thermal_strength_ms))


def calculate_speed_to_fly(glide_polar, thermal_strengths, wind_speeds):
    '''
    Given a polar, a list of thermal strengths in m/s, and a list of wind speeds in m/s, calculate the time
    it will take to fly between between thermals at all velocites provided in the polar. From these times, 
    pick the shortest time. Returns a dictionary with the following structure:

    time_to_fly_thermals[thermal_strength][wind_speed] = {
        "velocity_ms"  = [             velocity 0,              velocity 1, etc.]
        "time_to_fly"  = [ time to fly velocity 0,  time to fly velocity 1, etc.]
        "speed_to_fly" = index of best velocity to fly
    }

    Where thermal_strength and wind_speed are indicies from the thermal_strengths and wind_speeds lists provided
    '''
    time_to_fly_thermals = {}
    for thermal_strength in thermal_strengths:
        time_to_fly_thermals[thermal_strength] = {}
        for wind_speed in wind_speeds:
            time_to_fly_thermals[thermal_strength][wind_speed] = {
                "velocity_ms": [], "time_to_fly": [], "speed_to_fly": ""}
            for (velocity_ms, sink_rate) in zip(glide_polar.velocity_ms, glide_polar.sink_rate):
                time_to_fly = calculate_time_between_top_of_thermals(
                    1000, thermal_strength, velocity_ms, sink_rate, wind_speed)
                time_to_fly_thermals[thermal_strength][wind_speed]["velocity_ms"].append(
                    velocity_ms)
                time_to_fly_thermals[thermal_strength][wind_speed]["time_to_fly"].append(
                    time_to_fly)
            time_to_fly_thermals[thermal_strength][wind_speed]["speed_to_fly"] = np.argmin(
                time_to_fly_thermals[thermal_strength][wind_speed]["time_to_fly"])

    return time_to_fly_thermals