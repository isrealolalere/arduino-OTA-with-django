import requests


# Define the URL of the Django endpoint
url = "http://127.0.0.1:8000/ota_server/mcu_api/ota_update/"
# url = "http://127.0.0.1:8000/ota_server/mcu_api/ota_update/"


# Data to authenticate the device
data = {
    "user_device_key": "adminkeyunique",  # replace with the actual user ID or unique identifier
}

try:
    # Send POST request to the OTA endpoint
    response = requests.post(url, data=data, stream=True)
    
    # Check if the request was successful and the firmware file is being sent
    if response.status_code == 200:
        # Save the .bin file
        firmware_filename = "test_firmware.bin"
        with open(firmware_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Firmware downloaded successfully as '{firmware_filename}'")
    else:
        print(f"Failed to retrieve firmware. Status code: {response.status_code}")
        print("Response:", response.json())

except Exception as e:
    print(f"Error: {e}")
    