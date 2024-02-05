def individual_serial(booking) -> dict:
    return {
        "name": booking["name"],
        "summary": booking["summary"],
        "description": booking["description"],
        "capacity": booking["capacity"],
        "price": booking["price"],
        "room_type": booking["room_type"],
        "bed_type": booking["bed_type"],
        "minimum_nights": booking["minimum_nights"],
        "maximum_nights": booking["maximum_nights"],
        "bedrooms": booking["bedrooms"],
        "beds": booking["beds"],
        "bathrooms": booking["bathrooms"],
        "images": booking["images"],
        "availability": booking["availability"],
        "reviews": booking["reviews"]
    }

def list_serial(bookings) -> list:
    return [individual_serial(booking) for booking in bookings]

def activities_serial(activity) -> dict:
    return {
        "id_act": activity["id_act"],
        "name": activity["name"],
        "description": activity["description"],
        "price": activity["price"],
        "duration": activity["duration"],
        "image": activity["image"],
    }

# Función para serializar una lista de instancias de Activities
def list_activities_serial(activities_list) -> list:
    return [activities_serial(activity) for activity in activities_list]