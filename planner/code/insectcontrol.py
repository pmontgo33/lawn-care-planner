# insectcontrol.py
# Patrick W. Montgomery
# created: 10/24/2016

# import statements
from datetime import datetime, date, timedelta
from . import utils

    
def get_insect_control_info(closest_station, temp_data):
    
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
    beetle_emergence_date = utils.get_gdd_date(GRUB_GDD_TARGET, GDD_BASE_TEMP, closest_station, temp_data)
    insect_info['grub_deadline'] = beetle_emergence_date
    
    return insect_info