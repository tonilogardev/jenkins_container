import urllib.request
import urllib.parse
import http.cookiejar
import base64
import json
import sys

BASE_URL = "http://localhost:8080"
USER = "admin"
PASS = "admin"

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)

def get_crumb():
    url = f"{BASE_URL}/crumbIssuer/api/json"
    req = urllib.request.Request(url)
    auth_str = f"{USER}:{PASS}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    req.add_header("Authorization", f"Basic {b64_auth}")
    with opener.open(req) as response:
        data = json.loads(response.read().decode())
        return data['crumbRequestField'], data['crumb']

def run_groovy(script_path):
    with open(script_path, 'r') as f:
        script_content = f.read()
    
    crumb_field, crumb_value = get_crumb()
    
    url = f"{BASE_URL}/scriptText"
    data = urllib.parse.urlencode({'script': script_content}).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    
    auth_str = f"{USER}:{PASS}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    req.add_header("Authorization", f"Basic {b64_auth}")
    req.add_header(crumb_field, crumb_value)
    
    try:
        with opener.open(req) as response:
            print(response.read().decode())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_groovy("check_creds.groovy")
