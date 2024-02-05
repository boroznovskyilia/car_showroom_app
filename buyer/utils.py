import requests
from rest_framework.response import Response
from rest_framework import status


def set_token_header(data,token):
    data["tokens"] = {"refresh": f"Bearer {str(token)}", "access": f"Bearer {str(token.access_token)}"}
    response = Response(data, status=status.HTTP_201_CREATED)
    response['Authorization'] = f'{data["tokens"]["access"]}'
    return response