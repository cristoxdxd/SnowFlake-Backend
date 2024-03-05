import datetime
from fastapi import APIRouter, Body, HTTPException, Request
from models.booking_info import Bookings
from models.booking_users import Availability
from models.activities import Activities
from models.email import EmailData
from config.database import collection_name, activities_name, availability_name, codes_reservation
from schema.schemas import individual_serial, list_serial, list_availability_serial, list_activities_serial, code_serial
from bson import ObjectId
import yagmail
from dotenv import load_dotenv
import os
from jinja2 import Template
import random
import string

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
# GET Request Method
@router.get("/code/{id}")
async def get_code(id: str):
    code_reservation = code_serial(codes_reservation.find_one({"_id": ObjectId(id)}))
    return {"data": code_reservation}

# Cargar la plantilla de correo electrónico
with open("./templates/email_template.html", "r") as file:
    template_content = file.read()
email_template = Template(template_content)
# Configura yagmail con tu cuenta de correo electrónico y credenciales
yag = yagmail.SMTP(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))

def generate_reservation_code(length=8):
    # Generar un código exclusivo de la reserva
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code



@router.post("/send-email/")
async def send_email(email_data: EmailData):
    try:
        fecha_actual = datetime.datetime.now()
        fecha_formateada = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")
        # Renderizar la plantilla con datos dinámicos, incluyendo el código exclusivo
        email_content = email_template.render(amount=email_data.amount, reservation_code=email_data.booking_id, fecha=fecha_formateada )
        # Envía el correo electrónico
        yag.send(
            to=email_data.email,
            subject=email_data.subject,
            contents=email_content
        )
        
        return {"message": "Correo electrónico enviado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

with open("./templates/email_cancelation.html", "r") as file:
    template_content2 = file.read()
email_cancelation = Template(template_content2)

@router.post("/send-email/cancelation/")
async def send_email(email_data: EmailData):
    try:
        fecha_actual = datetime.datetime.now()
        fecha_formateada = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")
        # Renderizar la plantilla con datos dinámicos, incluyendo el código exclusivo
        email_content2 = email_cancelation.render(amount=email_data.amount, reservation_code=email_data.booking_id, fecha=fecha_formateada )
        # Envía el correo electrónico
        yag.send(
            to=email_data.email,
            subject=email_data.subject,
            contents=email_content2
        )
        
        return {"message": "Correo electrónico enviado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




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
