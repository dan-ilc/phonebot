# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import load_dotenv # use this to save us wrestling with windows env var handling
load_dotenv('.env')
# crash out if either of these are missing
account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]

client = Client(account_sid, auth_token)

# print(call.sid)
from fastapi import FastAPI, Query, HTTPException
from typing import Optional
import re
def is_valid_uk_phone_number(phone_number:str):
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

def is_valid_message(message:str):
   """
   Check that the message is ok. Later could add safety measures like 
   profanity filters, etc.
   """
   return len(message) < 10000 # dummy check to ensure it's not too long



app = FastAPI(docs_url="/")

# Endpoint to get the version of the API
@app.get("/version")
def get_version():
    """
    Returns the version of the API.
    """
    return {"version": "1.0.0"}

# Endpoint to make a call with destination_number and message parameters
@app.post("/call")
def make_call(
    destination_number: str = Query(..., description="The destination phone number"),
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
    # call = client.calls.create(
    #     url="http://demo.twilio.com/docs/voice.xml",
    #     to="+447840222962",
    #     from_="+447723427639"
    # )
    return {"destination_number": destination_number, "message": message}



# Run the application using Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)