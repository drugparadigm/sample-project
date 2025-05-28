import sys
from flask import request

def main():
    reqId=request.form.get('reqId')
    print(f"Received request ID: {reqId}")
    return reqId