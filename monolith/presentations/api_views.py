from django.http import JsonResponse
from common.json import ModelEncoder
from events.api_views import ConferenceListEncoder
from events.models import Conference
from .models import Presentation
from django.views.decorators.http import require_http_methods
import json


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

@require_http_methods(["GET", "POST"])
def api_list_presentations(request, conference_id):
    if request.method == "GET":
        presentations = Presentation.objects.all()
        return JsonResponse(
            {"presentations": presentations},
            encoder=PresentationListEncoder,
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
        presentation = Presentation.create(**content)

        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
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
        "conference",
    ]

    def get_extra_data(self, o):
        return { "status": o.status.name }

    encoders = {"conference": ConferenceListEncoder()}


@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_presentation(request, pk):
    if request.method == "GET":
        presentation = Presentation.objects.get(id=pk)
        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Presentation.objects.filter(id=pk).delete()
        return JsonResponse({"deleted": count > 0})

    else:
        content = json.loads(request.body)
        try:
            if "conference" in content:
                conference = Conference.objects.get(id=content["conference"])
                content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid"},
                status=400,
            )
        
        Presentation.objects.filter(id=pk).update(**content)

        presentation = Presentation.objects.get(id=pk)

        return JsonResponse(
            presentation,
            encoder=PresentationDetailEncoder,
            safe=False,
        )


@require_http_methods(["PUT"])
def api_approve_presentation(request, pk):
    presentation = Presentation.objects.get(id=pk)
    presentation.approve()
    return JsonResponse(
        presentation,
        encoder=PresentationDetailEncoder,
        safe=False,
    )


@require_http_methods(["PUT"])
def api_reject_presentation(request, pk):
    presentation = Presentation.objects.get(id=pk)
    presentation.reject()
    return JsonResponse(
        presentation,
        encoder=PresentationDetailEncoder,
        safe=False,
    )