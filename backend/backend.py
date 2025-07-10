import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Supabase config
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# -------------------------------
# Authentication functions only
# -------------------------------

def NewUserEmailPassword(email, password):
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
        })
        print("Response:", response)
        if response.user is None:
            print("Signup failed. No user returned.")
        else:
            print("User registered successfully!")
        return response
    except Exception as e:
        print("Exception during signup:", e)
        return None

def LoginEmailPassword(email, password):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        print("Response:", response)
        if response.user:
            print("Login successful!")
        else:
            print("Login failed. Check credentials.")
        return response
    except Exception as e:
        print("Exception during login:", e)
        return None

def LogOutUser():
    try:
        response = supabase.auth.sign_out()
        print("User signed out.")
        return response
    except Exception as e:
        print("Exception during logout:", e)
        return None