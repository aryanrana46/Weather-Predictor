from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    city = request.POST.get('city', 'mumbai')

    # OpenWeather API
    weather_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=51de635aee5b7dce9b865c535efa8eb4'
    PARAMS = {'units': 'metric'}

    # Try to get weather data first
    weather_data = requests.get(weather_url, params=PARAMS).json()

    exception_occurred = False
    day = datetime.date.today()

    try:
        description = weather_data['list'][0]['weather'][0]['description']
        icon = weather_data['list'][0]['weather'][0]['icon']
        temp = weather_data['list'][0]['main']['temp']
    except (KeyError, IndexError):
        description = 'clear sky'
        icon = '01d'
        temp = 25
        city = 'mumbai'
        exception_occurred = True
        messages.error(request, 'City not found. Showing default weather.')

    # Always fetch city image
    API_KEY = 'AIzaSyCD3QuG741Ex_1vNddiSipW-YD7AW6dlic'
    SEARCH_ENGINE_ID = 'd03719d22fa704292'
    query = f"{city} 1920x1080"
    search_url = (
        f"https://www.googleapis.com/customsearch/v1?"
        f"key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
        f"&start=1&searchType=image&imgSize=xlarge"
    )

    try:
        image_data = requests.get(search_url).json()
        search_items = image_data.get("items", [])
        if search_items:
            image_url = search_items[0]['link']
        else:
            image_url = 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600'
    except Exception:
        image_url = 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600'

    return render(
        request,
        'weatherapp/index.html',
        {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': exception_occurred,
            'image_url': image_url,
        }
    )
