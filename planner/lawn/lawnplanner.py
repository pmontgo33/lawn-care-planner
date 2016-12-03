# lawnplanner.py
# Patrick W. Montgomery
# created: 10/14/2016

# import statements
from datetime import date
from collections import OrderedDict

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

class planner:
    
    def __init__(self):
        
        self.tasks_by_season = OrderedDict()
        self.tasks_by_season['spring'] = OrderedDict([("All Season",[]), ("March",[]), ("April",[]), ("May",[])])
        self.tasks_by_season['summer'] = OrderedDict([("All Season",[]), ("June",[]), ("July",[]), ("August",[])])
        self.tasks_by_season['fall'] = OrderedDict([("All Season",[]), ("September",[]), ("October",[]), ("November",[])])
        self.tasks_by_season['winter'] = OrderedDict([("All Season",[]), ("December",[]), ("January",[]), ("February",[])])
    
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
            self.tasks_by_season[task_season][task_month].append({'name':task_name, 'date':task_date.strftime("%B %d")})

    def __str__(self):
        return str(self.tasks_by_season)
