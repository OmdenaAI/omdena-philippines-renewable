import numpy as np
from datetime import datetime, timedelta, timezone
from pysolar.solar import get_altitude, get_azimuth

def dates_in_interval(start, end, interval):
    """
    Calculates the dates in between start and end with the given interval.

    Parameters
    ----------
    start : datetime obj
        YADAYADA.
    end : datetime obj
        YADAYADA.
    interval : timedelta obj
        YADAYADA.
    
    Returns
    -------
    dates : array_like
        List of datetime objects between start and end with the given interval.
    """
    dates = list()
    n_dates = int((end-start) / interval)
    for x in range(n_dates):
        date = start + x * interval
        dates.append(date)
    return dates



def calc_altitude_azimuth(latitude, longitude, date):
    """
    Calculates the altitude and azimuth of the Sun's position.

    Parameters
    ----------
    latitude : float
        The latitude of the position on Earth.
    longitude : float
        The longitude of the position on Earth.
    date : datetime obj
        The time at which you want the Sun's position.

    Returns
    -------
    altitude : float
        The elevation angle between the horizon and the Sun.
    azimuth : float
        The YADAYADA.
    """
    altitude = get_altitude(latitude, longitude, date)
    azimuth = get_azimuth(latitude, longitude, date)
    return altitude, azimuth


