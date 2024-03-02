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
        "_id": str(activity["_id"]),
        "name": activity["name"],
        "description": activity["description"],
        "price": activity["price"],
        "duration": activity["duration"],
        "image": activity["image"],
    }

def list_activities_serial(activities) -> list:
    return [activity_serial(activity) for activity in activities]

def availability_serial(availability) -> dict:
    return {
        "_id": str(availability["_id"]),
        "booking_id": availability["booking_id"],
        "start_date": availability["start_date"],
        "end_date": availability["end_date"],
        "user": availability["user"],
    }

def list_availability_serial(all_availability) -> list:
    return [availability_serial(availability) for availability in all_availability]

def code_serial(code_reservation) -> dict:
    return {
        "code": str(code_reservation["code"])
    }

