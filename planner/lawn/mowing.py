# mowing.py
# Patrick W. Montgomery
# created: 10/11/2016

# import statements
from collections import OrderedDict

heights = {
    
    "KBG": OrderedDict(
        [("spring-first",{
            "title":"First mow of spring as soon as the grass begins to grow",
            "height":2.5,
            "description":"Clean out dead grass and leaves, and stimulate growth"
        }),
        ("spring",{
            "title":"Spring",
            "height":3,
            "description":"Better to have more leaf surface to grab more sublight during these shorter days"
        }),
        ("summer",{
            "title":"Summer",
            "height":3.5,
            "description":"Longer grass blades shade the root system during summer heat"
        }),
        ("fall",{
            "title":"Fall",
            "height":3,
            "description":"This will stimulate more root growth"
        }),
        ("fall-last",{
            "title":"Last mow of fall, just before or just after the first frost",
            "height":2.5,
            "description":"Shorter lawn over winter will cut down on winter kill"
        }),
    ]),
    
    "PRG": OrderedDict(
        [("spring-first",{
            "title":"First mow of spring as soon as the grass begins to grow",
            "height":2.5,
            "description":"Clean out dead grass and leaves, and stimulate growth"
        }),
        ("spring",{
            "title":"Spring",
            "height":3,
            "description":"Better to have more leaf surface to grab more sublight during these shorter days"
        }),
        ("summer",{
            "title":"Summer",
            "height":3.5,
            "description":"Longer grass blades shade the root system during summer heat"
        }),
        ("fall",{
            "title":"Fall",
            "height":3,
            "description":"This will stimulate more root growth"
        }),
        ("fall-last",{
            "title":"Last mow of fall, just before or just after the first frost",
            "height":2.5,
            "description":"Shorter lawn over winter will cut down on winter kill"
        }),
    ]),
    
    "TTTF": OrderedDict(
        [("spring-first",{
            "title":"First mow of spring as soon as the grass begins to grow",
            "height":3,
            "description":"Clean out dead grass and leaves, and stimulate growth"
        }),
        ("spring",{
            "title":"Spring",
            "height":3.75,
            "description":"Better to have more leaf surface to grab more sublight during these shorter days"
        }),
        ("summer",{
            "title":"Summer",
            "height":4,
            "description":"Longer grass blades shade the root system during summer heat"
        }),
        ("fall",{
            "title":"Fall",
            "height":3.5,
            "description":"This will stimulate more root growth"
        }),
        ("fall-last",{
            "title":"Last mow of fall, just before or just after the first frost",
            "height":3,
            "description":"Shorter lawn over winter will cut down on winter kill"
        }),
    ]),
}


def get_mowing_info(planner, closest_station, lawn):
    """
    :param planner: The planner to which the mowing information will be added
    :param closest_station: The station closest to the location provided by the user
    :param lawn: This is the users lawn.
    :return: a dictionary containing all of the mowing information
    """

    mowing_heights = heights[lawn.grass_type]

    for key in mowing_heights.keys():
        my_season = key
        my_task_name = 'Mow at height of %s"' % (str(mowing_heights[key]['height']))
        if '-' in key:
            my_season = key.split('-')[0]
            my_task_name = 'Mow at height of %s" for %s' % (str(mowing_heights[key]['height']), mowing_heights[key]['title'].lower())
        planner.add_task(my_task_name, my_season)

    mowing_info = {
        'heights': mowing_heights,
    }
    return mowing_info
