from rest_framework.serializers import BooleanField
from rest_framework.request import Request
from .permissions import validate_hard_delete_is_allowed


def is_hard_delete_request(request: Request) -> bool:
    permanent = request.query_params.get('permanent')
    is_hard_delete = BooleanField(required=False, allow_null=True).run_validation(permanent)

    if is_hard_delete:
        validate_hard_delete_is_allowed()

    return is_hard_delete
