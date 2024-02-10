def individual_serial(booking) -> dict:
    return {
        "_id": str(booking["_id"]),
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

def activity_serial(activity) -> dict:
    return {
        "name": activity["name"],
        "description": activity["description"],
        "price": activity["price"],
        "duration": activity["duration"],
        "image": activity["image"],
    }

# Función para serializar una lista de instancias de Activities
def list_activities_serial(activities_list) -> list:
    return [activity_serial(activity) for activity in activities_list]

def availability_serial(availability) -> dict:
    if "booking_id" in availability:
        return {
            "booking_id": availability["booking_id"],
            "start_date": availability["start_date"],
            "end_date": availability["end_date"],
            "user": availability["user"],
        }
    else:
        return {}

def list_availability_serial(availability_list) -> list:
    return [availability_serial(availability) for availability in availability_list]