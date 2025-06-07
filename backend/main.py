import os
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx


load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
#Creates a model that the API will use to validate the incoming JSON, asigns expected data types to the variables
class LoginData(BaseModel):
  email:str
  password: str
#Creates a POST route at /login for the API
app.post("/login")
#Creates and asynchronous function to parse the logindata and validate it
async def login_user(data: LoginData):
  login_url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
#Makes the headers for the Supabase API key and the content type (JSON)
headers = {
  "apikey": SUPABASE_ANON_KEY,
  "Content-Type": "application/json",
}
#Build the request body for what the API will retrieve from the Supabase
requestBody = {
  "email": data.email,
  "password": data.password,
}
#Sends the HTTP request to Supabase (POST) to retrieve the login info
async with httpx.AsyncClient() as client:
  response = await client.post(login_url, headers=headers, json=requestBody)