from django.http import JsonResponse
from common.json import ModelEncoder
from .models import Attendee


#######################
# Show Attendees List #
#######################
class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "name"
    ]

def api_list_attendees(request, conference_id):
    attendees = Attendee.objects.all()
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
    ]

    def get_extra_data(self, o):
        return {
            "name": o.conference.name,
        }

def api_show_attendee(request, pk):
    attendee = Attendee.objects.get(id=pk)
    return JsonResponse(
        attendee,
        encoder=AttendeeDetailEncoder,
        safe=False,
    )

