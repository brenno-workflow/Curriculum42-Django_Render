from django.shortcuts import render
from django.http import JsonResponse
from .models import HomePageContent
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def content(request):    
    if request.method == 'GET':
        content = HomePageContent.objects.first()
        if content:
            response_data = {
                "information": content.information,
                "objectives": content.objectives,
                "demonstrations": content.demonstrations,
                "credits": content.credits
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({"error": "No content available."})
    else:
        return JsonResponse({"error": "Only GET requests are allowed."})