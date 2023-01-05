from rest_framework.response import Response
from rest_framework import status as ResponseStatus
from utilities import keys, messages

BAD_REQUEST = ResponseStatus.HTTP_400_BAD_REQUEST
FORBIDDEN = ResponseStatus.HTTP_403_FORBIDDEN
NOT_FOUND = ResponseStatus.HTTP_404_NOT_FOUND
CONFLICT = ResponseStatus.HTTP_409_CONFLICT
EXPIRE_STATUS = ResponseStatus.HTTP_401_UNAUTHORIZED
SUCCESS = ResponseStatus.HTTP_200_OK
CREATED = ResponseStatus.HTTP_201_CREATED
ACCEPTED = ResponseStatus.HTTP_202_ACCEPTED

def SUCCESS_CREATE_RESPONSE(response={}):
    return Response({keys.SUCCESS: True, keys.MESSAGE: messages.SUCCESS, **response}, status=CREATED)


def SUCCESS_RESPONSE(response={}, header=None):
    if header:
        return Response({keys.SUCCESS: True, keys.MESSAGE: messages.SUCCESS, **response}, headers=header, status=SUCCESS)
    elif response:
        return Response({keys.SUCCESS: True, keys.MESSAGE: messages.SUCCESS, **response}, status=SUCCESS)
    return Response({keys.SUCCESS: True, keys.MESSAGE: messages.SUCCESS}, status=SUCCESS)


def ERROR_RESPONSE(msg, response_json={}):
    return Response({keys.SUCCESS: False, keys.MESSAGE: str(msg), **response_json}, status=BAD_REQUEST)

INVALID_PHONE = Response(
    {keys.SUCCESS: False, keys.MESSAGE: "Invalid Phone"}, status=BAD_REQUEST)

PHONE_ALREADY_USED = Response(
    {keys.SUCCESS: False, keys.MESSAGE: "Phone already in use"}, status=CONFLICT)

USER_DOES_NOT_EXISTS = Response(
    {keys.SUCCESS: False, keys.MESSAGE: "User does not exists"}, status=BAD_REQUEST
)

INVALID_PASSWORD = Response(
    {keys.SUCCESS: False, keys.MESSAGE: "Password do not match"}, status=BAD_REQUEST
)