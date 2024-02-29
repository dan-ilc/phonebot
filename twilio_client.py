from fastapi import FastAPI, Query, HTTPException
import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from typing import Optional
import re
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv # use this to save us wrestling with windows env var handling
load_dotenv('.env')
# crash out if either of these are missing
ACCOUNT_SID = os.environ["ACCOUNT_SID"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]
DEBUG_MODE = False
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# print(call.sid)
def is_valid_uk_phone_number(phone_number:str)->bool:
    """
    Checks if a phone number string adheres to a basic format.

    Args:
        phone_number: The phone number string to validate.

    Returns:
        True if the format seems valid, False otherwise.
    """

    if phone_number.startswith("+44"):
        phone_number = "0"+phone_number[3:]
        print(phone_number)

    # Remove non-numeric characters and whitespace characters
    phone_number = re.sub(r"[^\d]", "", phone_number)


    # Check for total length (11 digits)
    if len(phone_number) != 11:
        print("wrong length")
        print(phone_number)
        return False
    
    # Check for valid starting digits (02 or 07, or country code +44)
    if not phone_number.startswith(("02", "07")):
        print("wrong start")
        print(phone_number)
        return False

    # Check for valid subscriber number format (4-digit district code + 4-digit local number)
    return bool(re.match(r"^\d{4}\d{4}$", phone_number[3:]))

def is_valid_message(message:str)->bool:
    """
    Check that the message is ok. Later could add safety measures like 
    profanity filters, etc.
    """
    MAX_MSG_LEN = 10000 # arbitrary max
    if len(message) > MAX_MSG_LEN: # dummy check to ensure it's not too long
        return False
    
    # add more things here
    PROFANITY_FILTER_LIST = ["LTN", "ELON", "MUSK"]
    for word in PROFANITY_FILTER_LIST:
        if word in message.upper():
            return False
    # we survived.
    return True

def make_phone_call(number:str, message:str)->str:
    """
    Make a phone call using the twilio API.
    Could add phone number and message validation here instead.
    """
    twiml = VoiceResponse()
    twiml.say(message, voice="alice")
    if DEBUG_MODE:
        print(f"Pretending to make a call with {twiml.to_xml()} to {number} from {TWILIO_NUMBER}")
        return "pretend call"
    # Make the Twilio call
    call = client.calls.create(
        twiml=twiml.to_xml(),
        to=number,
        from_=TWILIO_NUMBER
    )
    return call.sid


app = FastAPI(docs_url="/docs")

# Endpoint to get the version of the API
@app.get("/version")
def get_version():
    """
    Returns the version of the API.
    """
    return {"version": "1.0.0"}

# Endpoint to make a call with destination_number and message parameters
@app.post("/voicecall")
def make_call(
    destination_number: str = Query(..., description="The destination phone number (must be verified already)"),
    message: str = Query(..., description="The message to be sent"),
):
    """
    Make a call with the specified destination number and message.

    Parameters:
    - destination_number: The destination phone number
    - message: The message to be sent
    """
    
    if not is_valid_uk_phone_number(destination_number):
       raise HTTPException(status_code=400, detail="Not a valid UK number.")

    if not is_valid_message(message):
       raise HTTPException(status_code=400, detail="Not a valid message.")
    message_header = "This is an automated message from your friendly neighbourhood call robot.\n"
    message = message_header + message
    sid = make_phone_call(destination_number, message)
    return {"message": f"call created with sid {sid}"}

# Enable CORS for all origins, allow all methods, allow all headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the "static" directory to serve static files (e.g., your React build)
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

# Run the application using Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
