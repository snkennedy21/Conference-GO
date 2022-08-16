from django.http import JsonResponse
from common.json import ModelEncoder
from .models import Presentation


######################
# List Presentations #
######################

class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "title",
    ]

    def get_extra_data(self, o):
        return { "status": o.status.name }

def api_list_presentations(request, conference_id):
    presentations = Presentation.objects.all()
    return JsonResponse(
        {"presentations": presentations},
        encoder=PresentationListEncoder,
    )


#############################
# Show Presentation Details #
#############################
class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
    ]

def api_show_presentation(request, pk):
    presentation = Presentation.objects.get(id=pk)
    return JsonResponse(
        presentation,
        encoder=PresentationDetailEncoder,
        safe=False,
    )
