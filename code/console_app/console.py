import json
import requests
import msal

jsondata = open("config.json","r")
config = json.load(jsondata)

app = msal.ConfidentialClientApplication(
    client_id=config["client_id"],
    client_credential=config["client_secret"],
    authority=config["authority"],
)

result = None

result = app.acquire_token_silent(config["scope"], account=None)

if not result:
    result = app.acquire_token_for_client(scopes=config["scope"])

if "access_token" in result:
    session = requests.sessions.Session()
    session.headers.update({'Authorization': f'Bearer {result["access_token"]}'})
    print(result["access_token"])
    response = session.get("http://localhost:8000/api/weather/seattle")
    print(response.content)
else:
    print("auth failed")
