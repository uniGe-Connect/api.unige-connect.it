from faker.providers import DynamicProvider

courses = [
    "DISTRIBUTED COMPUTING",
    "MACHINE LEARNING AND DATA ANALYSIS",
    "SOFTWARE SYSTEMS DESIGN AND MODELLING",
    "VIRTUALIZATION AND CLOUD COMPUTING",
    "FUNCTIONAL AND SECURITY TESTING TECHNIQUES",
    "INTERNET OF THINGS",
    "IT PROJECT MANAGEMENT",
    "MOBILE DEVELOPMENT",
    "NETWORK ANALYSIS",
    "SOFTWARE ENGINEERING FOR DATA ANALYTICS",
    "ADVANCED DATA MANAGEMENT",
    "DECENTRALIZED SYSTEMS",
    "CAPSTONE PROJECT"
]


course_name_provider = DynamicProvider(
    provider_name="course_name",
    elements=courses
)
