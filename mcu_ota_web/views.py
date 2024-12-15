from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from mcu_ota_web.models import *

import json
from django.http import FileResponse, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserDevice, Firmware
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist

def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        device_key = request.POST.get("device_key")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        phone_no = request.POST.get("phone_no")
        
        # Validate inputs
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect("signup")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect("signup")
        
        # Check if the device key already exists
        if UserDevice.objects.filter(device_key=device_key).exists():
            messages.error(request, "Device key is already in use.")
            return redirect("signup")

        # Create the user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password1)
        )
        
        # Optional: save device info if associated with user
        UserDevice.objects.create(
            user=user, 
            username = username,
            password = password1,
            device_key=device_key,
            phone_no=phone_no
        )

        messages.success(request, "Account created successfully!")
        return redirect("login_url")

    return render(request, "auth/signup.html")



def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user_exist = UserDevice.objects.filter(user__username=username, password=password)
        if user_exist.exists():
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to 'home' or another view after login
        else:
            # Add an error message if login fails
            messages.error(request, 'Invalid username or password')
            return redirect('login_url')

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login_url')  # Redirect to the login page or any other page after logout


@login_required
def home_view(request):
    return render(request, 'home.html')


# def profile(request):
#     user = request.user  # Get the logged-in user
#     # Get the firmware files uploaded by the user
#     firmware_files = Firmware.objects.filter(user_device__user=user)

#     context = {
#         'user_name': user.username,
#         'firmware_files': firmware_files,
#     }
#     return render(request, 'profile.html', context)


def profile(request):
    user = request.user  # Get the logged-in user
    context = {}
    firmware_files = Firmware.objects.filter(user_device__user=user)
    
    if firmware_files.exists():
        # Create a new list to store only file names
        for firmware in firmware_files:
            firmware.file_name = firmware.file.name.split('/')[-1]  # Extract just the file name

            context = {
                'firmware_files': firmware_files,
            }

    return render(request, 'profile.html', context)


@login_required
def upload_firmware(request):
    if request.method == 'POST':
        version = request.POST.get('version')
        file = request.FILES.get('file')
        
        if version and file:
            # Create a Firmware instance
            user_device = UserDevice.objects.get(user=request.user)
            firmware = Firmware(user_device=user_device, version=version, file=file)
            firmware.save()
            messages.success(request, 'Firmware uploaded successfully.')
            return redirect('home')  # Redirect to home or another page
        else:
            messages.error(request, 'Please provide both version and file.')

    return render(request, 'upload_firmware.html')



#############################################################################################
#############################################################################################
#############################################################################################

@csrf_exempt
def get_firmware(request):
    if request.method == 'POST':
        try:
            # Parse the JSON payload
            data = json.loads(request.body)
            user_device_key = data.get("user_device_key")  # Extract device key from request payload
            
            # Check if device_key is provided
            if not user_device_key:
                return JsonResponse({"error": "Device key is missing"})
            
            # Authenticate the device
            try:
                user_device = UserDevice.objects.get(device_key=user_device_key)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Unauthorized device"})

            # Fetch the latest firmware for the device
            firmware = Firmware.objects.filter(user_device=user_device).order_by('-release_date').first()
            if not firmware:
                return JsonResponse({"error": "No firmware found for this device"})
            
            if firmware:
                # Return the firmware file as a downloadable response
                return FileResponse(firmware.file.open("rb"), as_attachment=True, filename="firmware.bin")

            # Prepare the firmware data as a JSON response
            firmware_content = firmware.file.read()
            firmware_data = {
                "version": firmware.version,
                "file": firmware_content.decode("utf-8"),  # Ensure firmware is encoded properly
                "release_date": firmware.release_date.strftime("%Y-%m-%d %H:%M:%S")
            }
            return JsonResponse(firmware_data)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    
    else:
        return JsonResponse({"error": "Invalid request method"})
    

# def get_firmware(request):
#     # Authenticate user or device first (replace with your authentication logic)
#     user_device_key = request.POST.get('user_device_key')
#     try:
#         user_device = UserDevice.objects.get(device_key=user_device_key)
#         firmware = Firmware.objects.filter(user_device=user_device.user).order_by('-release_date').first()
        
#         if firmware:
#             # Return the firmware file as a downloadable response
#             return FileResponse(firmware.file.open("rb"), as_attachment=True, filename="firmware.bin")
#         else:
#             return JsonResponse({"error": "No firmware available for this device."})
    
#     except UserDevice.DoesNotExist:
#         return JsonResponse({"error": "Invalid device key."})


# In views.py

@csrf_exempt
def ota_update(request):
    if request.method == 'POST':
        # device_key = request.POST.get("user_device_key")
        try:
            content = json.loads(request.body)
            user_device_key = content['values'][0]
            device_key = user_device_key

            print(device_key)
            # Retrieve the firmware associated with the device
            device = UserDevice.objects.get(device_key=device_key)
            firmware = Firmware.objects.filter(user_device=device).latest("release_date")

            # Serve the .bin file as a response
            response = FileResponse(firmware.file, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{firmware.file.name}"'
            return response

        except UserDevice.DoesNotExist:
            return JsonResponse({"error": "Device not found"})
        except Firmware.DoesNotExist:
            return JsonResponse({"error": "Firmware not found"})
    else:
        return JsonResponse({"error": "Invalid request method"})
