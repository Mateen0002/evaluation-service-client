import requests
import json
from datetime import datetime

class EvaluationServiceClient:
    def __init__(self):
        self.base_url = "http://20.244.56.144/evaluation-service"
        self.credentials = None
        self.token = None
    
    def register(self, email, name, mobile, github, roll_no, college):
        """Register with the evaluation service (only do this once)"""
        url = f"{self.base_url}/register"
        payload = {
            "email": "mateenajmat44@gmail.com",
            "name": "Mateen Ajmat",
            "mobileNo": 9142194435,
            "githubUsername": "Mateen0002",
            "rollNo": 3702210523,
            "collegeName": "Aarupadai veedu institute of technology",
            "accessCode": "sdJDCF"  # Using your access code
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            self.credentials = response.json()
            print("Registration Successful! Save these credentials:")
            print(json.dumps(self.credentials, indent=2))
            return True
        except requests.exceptions.RequestException as e:
            print(f" Registration failed: {e}")
            if hasattr(e, 'response') and e.response.status_code == 409:
                print("Note: You've already registered. Use authenticate() instead.")
            return False
    
    def authenticate(self):
        """Get authorization token"""
        if not self.credentials:
            print("You need to register first!")
            return False
            
        url = f"{self.base_url}/auth"
        payload = {
            "email": self.credentials["ravikimar44@gmail.com"],
            "name": self.credentials["Rajiv kumar"],
            "rollNo": self.credentials["3702210523"],
            "accessCode": self.credentials["sdJDCF"],
            "clientID": self.credentials["ABC213"],
            "clientSecret": self.credentials["Aqrti345"]
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            self.token = response.json()
            print(" Authentication Successful!")
            print(f"Token expires at: {datetime.fromtimestamp(self.token['expires_in'])}")
            return True
        except requests.exceptions.RequestException as e:
            print(f" Authentication failed: {e}")
            return False
    
    def make_api_call(self, endpoint, method="GET", data=None):
        """Make authenticated API calls"""
        if not self.token:
            print("You need to authenticate first!")
            return None
            
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"{self.token['token_type']} {self.token['access_token']}",
            "Content-Type": "application/json"
        }
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers)
            else:
                print("Invalid HTTP method")
                return None
                
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API call failed: {e}")
            if hasattr(e, 'response'):
                print(f"Status code: {e.response.status_code}")
                print(f"Response: {e.response.text}")
            return None

def main():
    client = EvaluationServiceClient()
    
    # Replace these with your actual details
    USER_DETAILS = {
        "email": "mateenajmat44@gmail.com",
        "name": "Mateen Ajmat",
        "mobile": "9142194435",
        "github": "Mateen0002",
        "roll_no": "3702210523",
        "college": "Aarupadai veedu institute of technology"
    }
    
    while True:
        print("\nEvaluation Service Client")
        print("1. Register (Only do this once)")
        print("2. Authenticate")
        print("3. Make API Call")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == "1":
            print("\n--- Registration ---")
            if client.register(**USER_DETAILS):
                print("\nRegistration successful! Please save your credentials.")
                print("You can now authenticate using option 2.")
        
        elif choice == "2":
            print("\n--- Authentication ---")
            if client.authenticate():
                print("\nAuthentication successful! You can now make API calls.")
        
        elif choice == "3":
            print("\n--- API Call ---")
            if not client.token:
                print("Please authenticate first (option 2)")
                continue
                
            endpoint = input("Enter API endpoint (e.g. 'products'): ").strip()
            method = input("Enter HTTP method (GET/POST): ").strip().upper()
            
            data = None
            if method == "POST":
                try:
                    data_str = input("Enter JSON data (or leave empty): ").strip()
                    if data_str:
                        data = json.loads(data_str)
                except json.JSONDecodeError:
                    print("Invalid JSON format")
                    continue
            
            result = client.make_api_call(endpoint, method, data)
            if result:
                print("\nAPI Response:")
                print(json.dumps(result, indent=2))
        
        elif choice == "4":
            print("Exiting program...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

