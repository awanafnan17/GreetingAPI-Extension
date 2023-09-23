# myapp/views.py
import logging
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from rest_framework import viewsets
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.contrib.rest_framework import TokenHasScope
from .models import Greeting
from .serializers import GreetingSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



class GreetingViewSet(viewsets.ModelViewSet):
    queryset = Greeting.objects.all()
    serializer_class = GreetingSerializer

    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['write']  # Specify the required OAuth2 scope(s)



def my_view(request):
    return render(request, 'myapp/my_template.html')



logger = logging.getLogger(__name__)

@csrf_exempt
def test_submit_greeting(request):
    if request.method == 'POST':
        try:
            greeting_text = request.POST.get('greeting')
            user_id = 5
            
            # Log the greeting using Django's logger
            logger.info("Received greeting: %s", greeting_text)
            
            # Save the greeting in the database (replace 'text' with your actual field name)
            greeting_obj = Greeting.objects.create(text=greeting_text, user_id=user_id)
            
            response_message = "Greeting submitted successfully"

            # Check if the greeting is "hello" and make a recursive call
            # if greeting_text.lower() == "hello":
            #     recursive_response = test_submit_greeting(request)
            #     response_message = f"Recursive call: {recursive_response.get('message')}"

            return JsonResponse({'message': response_message}, status=201)
        except Exception as e:
                logger.error("Error: %s", str(e))  # Log the error message
                print("Logger error occured!")
                return JsonResponse({'message': 'Error: ' + str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)



logger = logging.getLogger(__name__)

@login_required
@csrf_exempt  # For simplicity, you can disable CSRF protection for this view.
def my_view(request):
    if request.method == 'POST':
        greeting_text = request.POST.get('greeting', '')

        # 1. Log the user-submitted greeting.
        logger.info(f"User submitted greeting: {greeting_text}")

        # 2. Save it in the database.
        greeting = Greeting(text=greeting_text)
        greeting.save()

        # 3. Check if the greeting is "hello" and make an API call if needed.
        if greeting_text.lower() == 'hello':
            response = make_goodbye_api_call()
            return JsonResponse({'response': 'API call to goodbye endpoint', 'result': response})

    return JsonResponse({'response': 'Greeting received and saved'})

# def make_goodbye_api_call():
#     # Define the URL of the original greeting endpoint with "goodbye" as the parameter.
#     original_greeting_url = 'http://localhost:8000/api/your-original-greeting-endpoint/?param=goodbye'

#     # Define OAuth2 credentials (client ID and client secret) and access token.
#     client_id = 'xX3icNpfPHMlXhdVlSiRolsCRP1fMWIDWptf9chP'
#     client_secret = 'pbkdf2_sha256$600000$RCbUMmbK6ueCJ2fK4hac4q$oR0P10s+lbwWV5QOSWudpcRi0wiugmR/15Dyd7208dw='
#     access_token = '059zDPS17ISMudjCWkKCyuUFlf94kG'

#     # Set the Authorization header with the Bearer token.
#     headers = {'Authorization': f'Bearer {access_token}'}

#     # Make an OAuth2-secured API call to the original greeting endpoint.
#     response = requests.get(original_greeting_url, headers=headers)

#     return response.text



def make_goodbye_api_call():
    # Define the URL of the original greeting endpoint.
    original_greeting_url = 'http://localhost:8000/api/your-original-greeting-endpoint/'

    # Define OAuth2 credentials (client ID and client secret).
    client_id = 'xX3icNpfPHMlXhdVlSiRolsCRP1fMWIDWptf9chP'
    client_secret = 'pbkdf2_sha256$600000$RCbUMmbK6ueCJ2fK4hac4q$oR0P10s+lbwWV5QOSWudpcRi0wiugmR/15Dyd7208dw='

    access_token = '059zDPS17ISMudjCWkKCyuUFlf94kG'

    # Set the Authorization header with the Bearer token.
    headers = {'Authorization': f'Bearer {access_token}'}

    # Prepare the parameters for the API call, including 'param=goodbye'
    params = {'param': 'goodbye'}

    # Make an OAuth2-secured API call to the original greeting endpoint.
    try:
        response = requests.get(original_greeting_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        return f'Error making API call: {str(e)}'