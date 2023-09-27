import re
from flask import Flask, request, jsonify
import requests
from tools.num_scripts import *
app = Flask(__name__)

banner = """
# Your banner here
"""

# Create a dictionary to map service names to functions
services = {
    "swiggy": check_swiggy,
    "flipkart": check_flipkart,
    # "upstox": check_upstox,
    "instagram": check_instagram,
    "snapdeal": check_snapdeal
}

def is_valid_phone_number(identifier):
    # You can customize this regular expression to match your phone number format
    phone_number_pattern = r"^\d{10}$"
    return re.match(phone_number_pattern, identifier) is not None

def is_valid_email(identifier):
    # Basic email format validation 
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_pattern, identifier) is not None

@app.route('/')
def check_services():
    query = request.args.get('query')

    if not query:
        return jsonify({"error": "Please provide a 'query' parameter."}), 400

    if is_valid_phone_number(query):
        results = {}
        for service_name, service_function in services.items():
            result = service_function(query)
            results[service_name.capitalize()] = result  # Capitalize service names
        results["Phone"] = query  # Add the phone number to the results
        results["Email"] = ""  # Add the email address to the results
        results["Message"] = "Phone number detected. Email checks not implemented yet."
        return jsonify(results)

    elif is_valid_email(query):
        # Perform email-related checks here
        return jsonify({"message": "Email address detected. Email checks not implemented yet."})

    else:
        return jsonify({"error": "Invalid input. Please provide a valid phone number or email address."}), 400

if __name__ == "__main__":
    print(banner)  # Print the ASCII banner
    app.run()
