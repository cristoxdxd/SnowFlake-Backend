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