import requests

# Define the URL of the Django endpoint
url = "http://127.0.0.1:8000/ota_server/mcu_api/get_firmware/"

# Data to authenticate the device
data = {
    "user_device_key": "adminkeyunique",  # replace with the actual user ID or unique identifier
}

# # Sending the POST request
# try:
#     response = requests.post(url, json=data)
    
#     # Check if the request was successful
#     if response.status_code == 200:
#         # Print the JSON response
#         json_response = response.json()
#         print("Response:", json_response)
        
#         # Check if the firmware file was provided in the response
#         if "file" in json_response:
#             # Download the file content
#             firmware_url = json_response["file"]
#             firmware_data = requests.get(firmware_url).content
            
#             # Save the firmware file locally
#             with open("downloaded_firmware.ino", "wb") as firmware_file:
#                 firmware_file.write(firmware_data)
#             print("Firmware downloaded successfully!")
#         else:
#             print("Firmware file not found in the response.")

#     else:
#         print("Failed to retrieve firmware. Status code:", response.status_code)
#         print("Error message:", response.json().get("error"))

# except Exception as e:
#     print("Error:", e)

try:
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        # Save binary content directly to a .bin file
        with open("downloaded_firmware.bin", "wb") as firmware_file:
            firmware_file.write(response.content)
        print("Firmware downloaded successfully as 'downloaded_firmware.bin'")
    else:
        # Handle any errors and print the response text if available
        print("Failed to retrieve firmware. Status code:", response.status_code)
        print("Error message:", response.text)

except Exception as e:
    print("Error:", e)
