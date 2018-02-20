"""
This is the lawnplanner object that takes the provided lawn, and generates all of the planner tasks and data
"""

# import statements
from . import establishment, fertilizer, phlime, mowing, insectcontrol, weedcontrol

from datetime import date
from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)

seasons_dates = {
        "spring": [date(2010, 3, 1), date(2010, 5, 31)],
        "summer": [date(2010, 6, 1), date(2010, 8, 31)],
        "fall": [date(2010, 9, 1), date(2010, 11, 30)],
        "winter": [date(2010, 12, 1), date(2011, 2, 28)],
    }


def season_of_date(task_date):
    """
    This function takes a date as a perameter and returns the name of the season
    that the date falls in.
    """

    if task_date.month == 1 or task_date.month == 2:
        task_ten = date(2011, task_date.month, task_date.day)
    else:
        task_ten = date(2010, task_date.month, task_date.day)

    for season in seasons_dates.keys():
        if seasons_dates[season][0] <= task_ten <= seasons_dates[season][1]:
            return season
    
    return None


class Planner:
    
    def __init__(self, lawn, closest_station):
        logger.info("New Planner Started - Lawn: %s, Station: %s" % (lawn, closest_station))

        self.tasks_by_season = OrderedDict()
        self.tasks_by_season['spring'] = OrderedDict([("All Season", []), ("March", []), ("April", []), ("May", [])])
        self.tasks_by_season['summer'] = OrderedDict([("All Season", []), ("June", []), ("July", []), ("August", [])])
        self.tasks_by_season['fall'] = OrderedDict([("All Season", []), ("September", []), ("October", []), ("November", [])])
        self.tasks_by_season['winter'] = OrderedDict([("All Season", []), ("December", []), ("January", []), ("February", [])])

        self.lawn = lawn
        self.closest_station = closest_station
        # TODO Move closest_station finding function to the lawn module, and just pass the zip code?

        self.establishment_info = establishment.get_establishment_info(self, closest_station, lawn)
        self.mowing_info = mowing.get_mowing_info(self, closest_station, lawn)
        self.fertilizer_info = fertilizer.get_fertilizer_info(self, closest_station, lawn)
        self.phlime_info = phlime.get_phlime_info(self, closest_station, lawn)
        self.weed_info = weedcontrol.get_weed_control_info(self, closest_station, lawn)
        self.insect_info = insectcontrol.get_insect_control_info(self, closest_station, lawn)

        self.trim_empty()
        self.sort_all()
        logger.info("New Planner Created - Lawn: %s, Station: %s" % (lawn, closest_station))

    def add_task(self, task_name, task_date):
        """
        This function takes a task and a date, and adds it into the planner. It 
        adds it into its corresponding dictionary for the season and month the task
        occurs.
        """
        
        if task_date in seasons_dates.keys():
            self.tasks_by_season[task_date]["All Season"].append({'name':task_name, 'date':None})
        else:
            task_season = season_of_date(task_date)
            task_month = task_date.strftime("%B")

            if task_season not in self.tasks_by_season.keys():
                self.tasks_by_season[task_season] = None
            if task_month not in self.tasks_by_season[task_season].keys():
                self.tasks_by_season[task_season][task_month] = None

            self.tasks_by_season[task_season][task_month].append({
                'name': task_name, 'date': task_date
            })


    def trim_empty(self):
        """
        This function removes any months from the tasks_by_season dictionary
        that do not contain any tasks.
        """
        months_to_del = []
        for season in self.tasks_by_season:
            for month in self.tasks_by_season[season]:
                if not self.tasks_by_season[season][month]:  # if list is empty
                    months_to_del.append((season, month))
        for s_m in months_to_del:
            del self.tasks_by_season[s_m[0]][s_m[1]]

        seasons_to_del = []
        for season in self.tasks_by_season:
            if not self.tasks_by_season[season]:
                seasons_to_del.append(season)
        for s in seasons_to_del:
            del self.tasks_by_season[s]

    def sort_all(self):

        for season in self.tasks_by_season:
            for month in self.tasks_by_season[season]:
                if month == "All Season":
                    continue
                self.tasks_by_season[season][month].sort(key=lambda x: x['date'])

    def all_tasks(self):

        tasks = []
        for season in self.tasks_by_season:
            for month in self.tasks_by_season[season]:
                if month == "All Season":
                    continue
                for task in self.tasks_by_season[season][month]:
                    tasks.append(task)
        return tasks

    def __str__(self):
        return str(self.tasks_by_season)
