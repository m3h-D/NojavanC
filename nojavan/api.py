from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import JsonResponse, Http404


def search_api(request):
    result = []
    model = request.GET.get('model')
    field = request.GET.get('field')
    value = request.GET.get('value')
    if model and field and value:
        my_filter = {}
        print('oooooooooooo', value, field)
        my_filter[f"{field}__icontains"] = value
        Model = ContentType.objects.get(model=model).model_class()
        qs = Model.objects.filter(Q(**my_filter))
        for obj in qs:
            field_value = getattr(obj, f"{field}")
            result.append({
                'id': obj.pk,
                f'{field}': field_value
            })
        return JsonResponse(result, safe=False)
    raise Http404()
