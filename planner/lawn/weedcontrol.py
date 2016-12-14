# weedcontrol.py
# Patrick W. Montgomery
# created: 10/21/2016

# import statements
from datetime import datetime, date, timedelta
from . import lawnutils

    
def get_weed_control_info(planner, closest_station, lawn):
    
    """
    This function uses the Growing Degree Day method of determining when the
    weeds will germinate. Information on this method can be found here:
    
    http://www.omafra.gov.on.ca/english/crops/pub811/10using.htm
    http://www.uky.edu/Ag/ukturf/4-1-14.html
    """
    
    """
    These are all static variables, and the basis for the summer annual pre-emergent
    application timing based on air temperature.
    """
    GDD_BASE_TEMP = 50.0 # degrees F
    SUMMER_GDD_TARGET = 45.0 # degree days
    APP_PRIOR_TO_GERMINATION = 10 # days
    
    weed_info = {
        
        'summer_deadline':None,
    }
    
    summer_germination_date = lawnutils.get_gdd_date(SUMMER_GDD_TARGET, GDD_BASE_TEMP, closest_station)
    weed_info['summer_deadline'] = summer_germination_date - timedelta(days=APP_PRIOR_TO_GERMINATION)

    # Add to planner
    my_task_name = "Summer annual weed pre-emergent herbicide application deadline."
    planner.add_task(my_task_name, weed_info['summer_deadline'])

    return weed_info