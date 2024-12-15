from faker.providers import DynamicProvider


courses = [
    "ADM", "VCC", "Capstone", "SSDM", "HPC", "AI", "Machine Learning",
    "Algorithm", "Computer", "DS", "IOT", "MD", "Fourier", "React", "Python",
    "Java", "C#", "SQL", "Cassandra", "BASC", "CS", "C++", "C"
]
suffixes = [
    "Knights", "Warriors", "Rivals", "Legends", "Titans", 
    "Guardians", "Rebels", "Champions", "Crusaders", "Elites",
    "Fans", "Supporters", "Followers", "Admirers", "Backers", 
    "Believers", "Devotees", "Boosters", "Loyalists", "Advocates",
    "Challengers", "Contenders", "Opponents", "Fighters", "Gladiators", 
    "Strikers", "Assassins", "Defenders", "Combatants", "Rivals",
    "Seekers", "Explorers", "Hunters", "Nomads", "Commanders", 
    "Raiders", "Masters", "Aces", "Voyagers", "Pioneers"
]

group_name_provider = DynamicProvider(
    provider_name = "group_name",
    elements = [f"{course} {suffix}" for course in courses for suffix in suffixes]
)