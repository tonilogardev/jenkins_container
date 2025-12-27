import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import base64
import time
import json
import sys

BASE_URL = "http://localhost:8080"
USER = "admin"
PASS = "admin"

# Setup cookie jar
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)

def wait_for_jenkins():
    print("Waiting for Jenkins to be ready...")
    url = f"{BASE_URL}/login"
    while True:
        try:
            with opener.open(url) as response:
                if response.status == 200:
                    print("Jenkins is ready!")
                    return
        except Exception as e:
            pass
        time.sleep(5)

def get_crumb():
    url = f"{BASE_URL}/crumbIssuer/api/json"
    req = urllib.request.Request(url)
    auth_str = f"{USER}:{PASS}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    req.add_header("Authorization", f"Basic {b64_auth}")
    
    try:
        with opener.open(req) as response:
            data = json.loads(response.read().decode())
            return data['crumbRequestField'], data['crumb']
    except Exception as e:
        print(f"Error getting crumb: {e}")
        sys.exit(1)

def trigger_job(job_name, params, crumb_field, crumb_value):
    query = urllib.parse.urlencode(params)
    url = f"{BASE_URL}/job/{job_name}/buildWithParameters?{query}"
    req = urllib.request.Request(url, method="POST")
    
    auth_str = f"{USER}:{PASS}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    req.add_header("Authorization", f"Basic {b64_auth}")
    req.add_header(crumb_field, crumb_value)
    
    print(f"Triggering {job_name} with {params}...")
    try:
        with opener.open(req) as response:
            if response.status in [200, 201]:
                print("Triggered successfully.")
                return True
            else:
                print(f"Failed to trigger: {response.status}")
                return False
    except urllib.error.HTTPError as e:
        print(f"HTTP Error triggering job: {e.code} {e.reason}")
        print(e.read().decode())
        return False
    except Exception as e:
        print(f"Error triggering job: {e}")
        return False

def wait_for_job(job_name):
    print(f"Waiting for {job_name} to complete...")
    # Wait for build to start
    time.sleep(10)
    
    last_build_url = f"{BASE_URL}/job/{job_name}/lastBuild/api/json"
    
    while True:
        req = urllib.request.Request(last_build_url)
        auth_str = f"{USER}:{PASS}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()
        req.add_header("Authorization", f"Basic {b64_auth}")
        
        try:
            with opener.open(req) as response:
                data = json.loads(response.read().decode())
                if data['building']:
                    print(f"Building... (Duration: {data.get('duration', 0)})")
                    time.sleep(10)
                else:
                    result = data['result']
                    print(f"Job finished with result: {result}")
                    return result == "SUCCESS"
        except Exception as e:
            print(f"Error checking status: {e}")
            time.sleep(5)

def main():
    wait_for_jenkins()
    crumb_field, crumb_value = get_crumb()
    print(f"Got crumb: {crumb_value}")
    
    # 1. Destroy Infrastructure
    # if not trigger_job("Deploy-Infrastructure", {"ACTION": "destroy", "CONFIRM": "true"}, crumb_field, crumb_value):
    #     sys.exit(1)
    # if not wait_for_job("Deploy-Infrastructure"):
    #     print("Destroy failed!")
    #     sys.exit(1)
        
    # 2. Apply Infrastructure
    # if not trigger_job("Deploy-Infrastructure", {"ACTION": "apply", "CONFIRM": "true"}, crumb_field, crumb_value):
    #     sys.exit(1)
    # if not wait_for_job("Deploy-Infrastructure"):
    #     print("Apply failed!")
    #     sys.exit(1)
        
    # 3. Deploy Production
    if not trigger_job("Deploy-Production", {"CONFIRM": "true"}, crumb_field, crumb_value):
        sys.exit(1)
    if not wait_for_job("Deploy-Production"):
        print("Deploy Production failed!")
        sys.exit(1)
        
    print("All pipelines executed successfully!")

if __name__ == "__main__":
    main()
