from django.http import JsonResponse
from common.json import ModelEncoder
from .models import Attendee
from events.api_views import ConferenceListEncoder
from django.views.decorators.http import require_http_methods
import json
from events.models import Conference


#######################
# Show Attendees List #
#######################
class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "name"
    ]

@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_id):
    if request.method == "GET":
        attendees = Attendee.objects.filter(conference=conference_id)
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeListEncoder,
        )
    else:
        content = json.loads(request.body)
        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )

        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )



#########################
# Show Attendee Details #
#########################
class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "email",
        "name",
        "company_name",
        "created",
        "conference",
    ]
    encoders = {
        "conference": ConferenceListEncoder(),
    }


def api_show_attendee(request, pk):
    attendee = Attendee.objects.get(id=pk)
    return JsonResponse(
        attendee,
        encoder=AttendeeDetailEncoder,
        safe=False,
    )

