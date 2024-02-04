from fastapi import APIRouter
from models.bookings import Bookings
from models.act_inscription import Act_Inscription
from models.activities import Activities
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId

router = APIRouter()

#Operaciones para los Libros

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
    collection_name.update_one({"_id": ObjectId(id)}, {"$set": dict(booking)}) # find_one_and_update
    return {"data": "Booking Updated Successfully"}

# DELETE Request Method
@router.delete("/{id}")
async def delete_booking(id: str):
    collection_name.delete_one({"_id": ObjectId(id)}) # find_one_and_delete
    return {"data": "Booking Deleted Successfully"}

#Operaciones para las actividades

# GET Request Method
@router.get("/activities")
async def get_all_activities():
    activities = list_serial(collection_name.find())
    return {"data": activities}

# Operaciones de inscripcion

# GET Request Method
@router.get("/activities/inscriptions")
async def get_all_bookings():
    inscriptions = list_serial(collection_name.find())
    return {"data": inscriptions}

# POST Request Method
@router.post("/activities/inscriptions/")
async def post_booking(act_ins: Act_Inscription):
    collection_name.insert_one(dict(act_ins))
    return {"data": "Inscription Created Successfully"}

# DELETE Request Method
@router.delete("/activities/inscriptions/{id}")
async def delete_booking(id: str):
    collection_name.delete_one({"_id": ObjectId(id)}) # find_one_and_delete
    return {"data": "Inscription Deleted Successfully"}