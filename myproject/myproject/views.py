# myproject/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Greeting
import logging
from django.http import HttpResponse, JsonResponse



def my_view(request):
    print("View is executed!")
    context = {
    'message': 'Welcome to the Home Page'
    }
    return render(request, 'myapp/my_template.html', context)
    return HttpResponse("This is the secured endpoint.")
    
logger = logging.getLogger(__name__)

@csrf_exempt
def test_submit_greeting(request):
    if request.method == 'POST':
        try:
            greeting_text = request.POST.get('greeting')

            # Log the greeting using Django's logger
            logger.info("Received greeting: %s", greeting_text)

            # Save the greeting in the database (replace 'text' with your actual field name)
            greeting_obj = Greeting.objects.create(text=greeting_text)

            response_message = "Greeting submitted successfully"

            # Check if the greeting is "hello" and make a recursive call
            if greeting_text.lower() == "hello":
                recursive_response = test_submit_greeting(request)
                response_message = f"Recursive call: {recursive_response.get('message')}"

            return JsonResponse({'message': response_message}, status=201)
        except Exception as e:
            return JsonResponse({'message': 'Error: ' + str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


def your_secured_endpoint(request):
    """This view handles the `api/your-secured-endpoint/` URL."""
    return HttpResponse("This is the secured endpoint.")