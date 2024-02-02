def individual_serial(booking) -> dict:
    return {
        "id": str(booking["_id"]),
        "name": booking["name"],
        "description": booking["description"],
        "price": booking["price"],
        "capacity": booking["capacity"],
        "image": booking["image"],
        "availability": booking["availability"],
    }

def list_serial(bookings) -> list:
    return [individual_serial(booking) for booking in bookings]