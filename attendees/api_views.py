from django.http import JsonResponse
from common.json import ModelEncoder
from .models import Attendee
from events.api_views import ConferenceListEncoder


#######################
# Show Attendees List #
#######################
class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "name"
    ]

def api_list_attendees(request, conference_id):
    attendees = Attendee.objects.filter(conference=conference_id)
    return JsonResponse(
        {"attendees": attendees},
        encoder=AttendeeListEncoder,
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

