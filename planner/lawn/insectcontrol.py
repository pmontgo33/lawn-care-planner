# insectcontrol.py
# Patrick W. Montgomery
# created: 10/24/2016

# import statements
from datetime import datetime, date, timedelta
from . import lawnutils

    
def get_insect_control_info(planner, closest_station, lawn):
    
    """
    This function uses the Growing Degree Day method of determining when the
    japanese beetles will emerge. Information on this method can be found here:
    
    http://www.omafra.gov.on.ca/english/crops/pub811/10using.htm
    http://crops.extension.iastate.edu/cropnews/2015/06/japanese-beetles-begin-emergence
    """
    
    """
    These are all static variables, and the basis for the grub preventer
    application timing based on air temperature.
    """
    GDD_BASE_TEMP = 50.0 # degrees F
    GRUB_GDD_TARGET = 1030.0 # degree days

    insect_info = {
        
        'grub_deadline':None,
    }
    beetle_emergence_date = lawnutils.get_gdd_date(GRUB_GDD_TARGET, GDD_BASE_TEMP, closest_station)
    insect_info['grub_deadline'] = beetle_emergence_date

    # Add to planner
    my_task_name = "Grub worm preventer application deadline."
    planner.add_task(my_task_name, insect_info['grub_deadline'])
    
    return insect_info