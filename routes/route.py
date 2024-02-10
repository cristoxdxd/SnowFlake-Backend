from fastapi import APIRouter
from models.booking_info import Bookings
from models.booking_users import Availability
from models.activities import Activities
from config.database import collection_name, activities_name
from schema.schemas import list_serial, list_availability_serial, list_activities_serial
from bson import ObjectId

router = APIRouter()

#Operaciones para la información de Reservas

# GET Request Method
@router.get("/")
async def get_all_bookings():
    bookings = list_serial(collection_name.find())
    return {"data": bookings}

# POST Request Method
@router.post("/")
async def post_booking(booking: Bookings):
    collection_name.insert_one(dict(booking))
    return {"data": "Booking Created Successfully"}

# PUT Request Method
@router.put("/{id}")
async def put_booking(id: str, booking: Bookings):
    collection_name.update_one({"_id": ObjectId(id)}, {"$set": dict(booking)})
    return {"data": "Booking Updated Successfully"}

# DELETE Request Method
@router.delete("/{id}")
async def delete_booking(id: str):
    collection_name.delete_one({"_id": ObjectId(id)}) # find_one_and_delete
    return {"data": "Booking Deleted Successfully"}

# Operaciones para las reservas

# GET Request Method
@router.get("/availability")
async def get_booking_availability():
    availability = list_availability_serial(collection_name.find())
    # bookings = list_serial(collection_name.find())
    # availability = [Availability.parse_availability(booking["availability"]) for booking in bookings]
    return {"data": availability}

# POST Request Method
@router.post("/availability/")
async def post_booking_availability(availability: Availability):
    collection_name.insert_one({"_id": availability.booking_id}, {"$push": {"availability": dict(availability)}})
    return {"data": "Booking Availability Created Successfully"}

# PUT Request Method
@router.put("/availability/{id}")
async def put_booking_availability(id: str, availability: Availability):
    collection_name.update_one({"_id": ObjectId(id)}, {"$push": {"availability": dict(availability)}})
    return {"data": "Booking Availability Updated Successfully"}

# DELETE Request Method
@router.delete("/availability/{id}")
async def delete_booking_availability(id: str):
    collection_name.update_one({"_id": ObjectId(id)}, {"$pop": {"availability": 1}})
    return {"data": "Booking Availability Deleted Successfully"}

# Operaciones para las actividades

# GET Request Method
@router.get("/activities")
async def get_all_activities():
    activities = list_activities_serial(activities_name.find())
    return {activities}

@router.post("/activities/")
async def post_activity(activity: Activities):
    activities_name.insert_one(dict(activity))
    return {"data": "Booking Created Successfully"}