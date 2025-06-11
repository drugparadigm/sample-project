# Sample Inference code 
# You can delete this.
import sys
from flask import request

def main():
    try:
        reqId=request.form.get('reqId')
        print(f"Received request ID: {reqId}")
        return reqId
    
    # Raise all the possible errors that a user can encounter and add them in api.py
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")