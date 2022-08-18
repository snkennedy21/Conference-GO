from django.http import JsonResponse
from .models import Conference, Location
from common.json import ModelEncoder
from django.views.decorators.http import require_http_methods
import json
from .models import State
from events.acls import get_picture, get_lat_lon, get_weather


####################
# List Conferences #
####################
class ConferenceListEncoder(ModelEncoder):
    model = Conference
    properties = [
        "name"
    ]

@require_http_methods(["GET", "POST"])
def api_list_conferences(request):
    if request.method == "GET":
        conferences = Conference.objects.all()
        return JsonResponse(
            {"conferences": conferences},
            encoder=ConferenceListEncoder,
        )
    else:
        content = json.loads(request.body)

        try:
            location = Location.objects.get(id=content["location"])
            content["location"] = location
        except Location.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid location id"},
                status=400,
            )
        
        conference = Conference.objects.create(**content)
        return JsonResponse(
            conference,
            encoder=ConferenceDetailEncoder,
            safe=False,
        )
        
##################
# List Locations #
##################
class LocationListEncoder(ModelEncoder):
    model = Location
    properties = ["name"]

@require_http_methods(["GET", "POST"])
def api_list_locations(request):
    if request.method == "GET":
        locations = Location.objects.all()
        return JsonResponse(
            {"locations": locations},
            encoder = LocationListEncoder
        )
    else:
        content = json.loads(request.body)
        try:
            state = State.objects.get(abbreviation=content["state"])
            content["state"] = state
        except State.DoesNotExist:
            return JsonResponse(
            {"message": "Invalid state abbreviation"},
            status=400
        )

        picture_url = get_picture(content["city"], content['state'])
        content.update(picture_url)

        location = Location.objects.create(**content)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )



###########################
# Show Conference Details #
###########################
class ConferenceDetailEncoder(ModelEncoder):
    model = Conference
    properties = [
        "name",
        "description",
        "max_presentations",
        "max_attendees",
        "starts",
        "ends",
        "created",
        "updated",
        "location",
    ]
    encoders = {
        "location": LocationListEncoder(),
    }

@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_conference(request, pk):
    if request.method == "GET":
        conference = Conference.objects.get(id=pk)

        city = conference.location.city
        state = conference.location.state
        
        weather = get_weather(city, state)

        return JsonResponse(
            {'conference': conference, "weather": weather},
            encoder=ConferenceDetailEncoder, safe=False
        )
    
    elif request.method == "DELETE":
        count, _ = Conference.objects.filter(id=pk).delete()
        return JsonResponse({"deleted": count > 0})

    else:
        content = json.loads(request.body)
        try:
            if "location" in content:
                location = Location.objects.get(id=content["location"])
                content["location"] = location
        
        except Location.DoesNotExist:
            JsonResponse(
                {'message': "No location for that id"}
            )

        Conference.objects.filter(id=pk).update(**content)

        conference = Conference.objects.get(id=pk)

        return JsonResponse(
            conference,
            encoder=ConferenceDetailEncoder,
            safe=False,
        )



#########################
# Show Location Details #
#########################
class LocationDetailEncoder(ModelEncoder):
    model = Location
    properties = [
        "name",
        "city",
        "room_count",
        "created",
        "updated",
        "picture_url",
    ]

    def get_extra_data(self, o):
        return { "state": o.state.abbreviation }

@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_location(request, pk):
    if request.method == "GET":
        location = Location.objects.get(id=pk)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Location.objects.filter(id=pk).delete()
        return JsonResponse({"deleted": count > 0})
    
    else:
        content = json.loads(request.body)
        try:
            if "state" in content:
                state = State.objects.get(abbreviation=content["state"])
                content["state"] = state
        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid state abbreviation"},
                status=400,
            )
        

        Location.objects.filter(id=pk).update(**content)

        location = Location.objects.get(id=pk)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )


