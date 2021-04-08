from rest_framework.serializers import BooleanField
from rest_framework.views import View
from .permissions import can_hard_delete


def is_hard_delete_request(view: View) -> bool:
    permanent = view.request.query_params.get('permanent')
    is_hard_delete = BooleanField(required=False, allow_null=True).run_validation(permanent)

    if is_hard_delete:
        can_hard_delete(view)

    return is_hard_delete
