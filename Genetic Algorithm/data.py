# Constants serving as a single source of "truth" for all data that may exist
ACTIVITIES = ["SLA101A", "SLA101B", "SLA191A", "SLA191B", "SLA201", "SLA291",
              "SLA303", "SLA304", "SLA394", "SLA449", "SLA451"]
ROOMS = ["Slater 003", "Roman 216", "Loft 206", "Roman 201", "Loft 310",
         "Beach 201", "Beach 301", "Logos 325", "Frank 119"]
TIMES = ["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]
FACILITATORS = ["Lock", "Glen", "Banks", "Richards", "Shaw", "Singer",
                "Uther", "Tyler", "Numen", "Zeldin"]

# Multiple constants to be used for fitness evaluation ONLY
room_cap = {
    "Slater 003": 45,
    "Roman 216": 30,
    "Loft 206": 75,
    "Roman 201": 50,
    "Loft 310": 108,
    "Beach 201": 60,
    "Beach 301": 75,
    "Logos 325": 450,
    "Frank 119": 60
}

expected_enroll = {
    "SLA100A": 50,
    "SLA100B": 50,
    "SLA191A": 50,
    "SLA191B": 50,
    "SLA201": 50,
    "SLA291": 50,
    "SLA303": 60,
    "SLA304": 25,
    "SLA394": 20,
    "SLA449": 60,
    "SLA451": 100
}

pref_facil = {
    "SLA101A": ["Glen", "Lock", "Banks", "Zeldin"],
    "SLA101B": ["Glen", "Lock", "Banks", "Zeldin"],
    "SLA191A": ["Glen", "Lock", "Banks", "Zeldin"],
    "SLA191B": ["Glen", "Lock", "Banks", "Zeldin"],
    "SLA201": ["Glen", "Banks", "Zeldin", "Shaw"],
    "SLA291": ["Lock", "Banks", "Zeldin", "Singer"],
    "SLA303": ["Glen", "Zeldin", "Banks"],
    "SLA304": ["Glen", "Banks", "Tyler"],
    "SLA394": ["Tyler", "Singer"],
    "SLA449": ["Tyler", "Singer", "Shaw"],
    "SLA451": ["Tyler", "Singer", "Shaw"]
}

alt_facil = {
    "SLA101A": ["Numen", "Richards"],
    "SLA101B": ["Numen", "Richards"],
    "SLA191A": ["Numen", "Richards"],
    "SLA191B": ["Numen", "Richards"],
    "SLA201": ["Numen", "Richards", "Singer"],
    "SLA291": ["Numen", "Richards", "Shaw", "Tyler"],
    "SLA303": ["Numen", "Singer", "Shaw"],
    "SLA304": ["Numen", "Singer", "Shaw", "Richards", "Uther", "Zeldin"],
    "SLA394": ["Richards", "Zeldin"],
    "SLA449": ["Zeldin", "Uther"],
    "SLA451": ["Zeldin", "Uther", "Richards", "Banks"]
}

roman_beach = ["Roman 216", "Roman 201", "Beach 201", "Beach 301"]

# Lazy cache for constant time conversions from 12-hour to military time. 
# Should make arithmetic calculations much easier within the codebase
time_cache = {
    "10 AM": 10,
    "11 AM": 11,
    "12 PM": 12,
    "1 PM": 13,
    "2 PM": 14,
    "3 PM": 15
}

activity_pairs = [
    ("SLA101A", "SLA191A"), ("SLA101A", "SLA191B"),
    ("SLA101B", "SLA191A"), ("SLA101B", "SLA191B"),
    ("SLA191A", "SLA101A"), ("SLA191A", "SLA101B"),
    ("SLA191B", "SLA101A"), ("SLA191B", "SLA101B")
]
