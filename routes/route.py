from typing import List
from fastapi import APIRouter, Body, HTTPException, Request
from models.booking_info import Bookings
from models.booking_users import Availability
from models.activities import Activities
from models.email import Email
from config.database import collection_name, activities_name, availability_name
from schema.schemas import individual_serial, list_serial, list_availability_serial, list_activities_serial
from bson import ObjectId
import yagmail
from dotenv import load_dotenv
import os



load_dotenv()

router = APIRouter()

#Operaciones para la información de Reservas

# GET Request Method
@router.get("/")
async def get_all_bookings():
    bookings = list_serial(collection_name.find())
    return {"data": bookings}

# GET Request Method
@router.get("/{id}")
async def get_booking(id: str):
    booking = individual_serial(collection_name.find_one({"_id": ObjectId(id)}))
    return {"data": booking}

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
@router.get("/availability/")
async def get_booking_availability():
    availability = list_availability_serial(availability_name.find())
    return {"data": availability}

# GET Request Method
@router.get("/availability/{user}")
async def get_booking_availability_id(user: str):
    availability = list_availability_serial(availability_name.find({"user": user}))
    return {"data": availability}

# POST Request Method
@router.post("/availability/")
async def post_booking_availability(availability: Availability):
    availability_name.insert_one(dict(availability))
    return {"data": "Booking Availability Created Successfully"}

# PUT Request Method
@router.put("/availability/{id}")
async def put_booking_availability(id: str, availability: Availability):
    availability_name.update_one({"_id": ObjectId(id)}, {"$set": dict(availability)})
    return {"data": "Booking Availability Updated Successfully"}

# DELETE Request Method
@router.delete("/availability/{id}")
async def delete_booking_availability(id: str):
    availability_name.delete_one({"_id": ObjectId(id)})
    return {"data": "Booking Availability Deleted Successfully"}

# Operaciones para las actividades

# GET Request Method
@router.get("/activities/")
async def get_all_activities():
    activities = list_activities_serial(activities_name.find())
    return {"data": activities}

@router.post("/activities/")
async def post_activity(activity: Activities):
    activities_name.insert_one(dict(activity))
    return {"data": "Booking Created Successfully"}

# Operación para enviar correo de confirmación
yag = yagmail.SMTP(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))

# POST Request Method
@router.post("/enviar-correo")
async def enviar_correo(correo: Email = Body(...)):
    try:
        # Enviar correo
        yag.send(correo.email, correo.asunto, correo.contenido)

        return {"success": True}
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return {"success": False}


# # Operaciones para paypal
from fastapi.responses import JSONResponse
import httpx

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET =  os.getenv("PAYPAL_CLIENT_SECRET")

base = "https://api-m.sandbox.paypal.com"

async def generate_access_token():
    try:
        if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
            raise HTTPException(status_code=500, detail="MISSING_API_CREDENTIALS")
        
        auth = f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}"
        auth_base64 = base64.b64encode(auth.encode("utf-8")).decode("utf-8")


        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base}/v1/oauth2/token",
                data={"grant_type": "client_credentials"},
                headers={"Authorization": f"Basic {auth_base64}"},
            )

            response.raise_for_status()
            data = response.json()
            return data["access_token"]
    except Exception as e:
        print("Failed to generate Access Token:", e)
        raise HTTPException(status_code=500, detail="Failed to generate Access Token")
import base64

async def create_order(cart):
    try:
        print("Shopping cart information passed from the frontend create_order() callback:", cart)

        access_token = await generate_access_token()
        url = f"{base}/v2/checkout/orders"

        price = cart.get('cart', [])[0].get('price')
        print ("Price: ", price)

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": price,
                    },
                },
            ],
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
            )

            response.raise_for_status()
            return await handle_response(response)
    except Exception as e:
        print("Failed to create order:", e)
        raise HTTPException(status_code=500, detail="Failed to create order")

async def capture_order(order_id):
    try:
        access_token = await generate_access_token()
        url = f"{base}/v2/checkout/orders/{order_id}/capture"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"},
            )

            response.raise_for_status()
            return await handle_response(response)
    except Exception as e:
        print("Failed to capture order:", e)
        raise HTTPException(status_code=500, detail="Failed to capture order")

async def handle_response(response):
    try:
        json_response = response.json()
        return JSONResponse(content=json_response, status_code=response.status_code)
    except Exception as e:
        error_message = await response.text()
        raise HTTPException(status_code=response.status_code, detail=error_message)

@router.post("/orders")
async def create_order_api(request: Request):
    try:
        cart = await request.json()
        return await create_order(cart)
    except HTTPException as e:
        return e

@router.post("/orders/{order_id}/capture")
async def capture_order_api(order_id: str):
    try:
        return await capture_order(order_id)
    except HTTPException as e:
        return e
