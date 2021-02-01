from rest_framework import status
from drf_yasg import openapi

response = {
            status.HTTP_200_OK: openapi.Response(
                description="User logged in successfully",
                examples={
                    "application/json": {
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzN"
                                   "TQ3ODY0NSwianRpIjoiYzM2MmYwNGYzMDRkNGRhYzkxMTNmMjA4MGI0NjRhMTkiLCJ1c2VyX2lkIjoxfQ."
                                   "XEk02JvIXCY2lfnDHZ2rbNHkw-6GB3wKz1JcygcvEXQ",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxOTE4"
                                  "NDM4NjQ1LCJqdGkiOiJjY2M1MjIxNzY1M2I0YjU3YjEzNDg5YjBlMjhiZmFjNyIsInVzZXJfaWQiOjF9.g"
                                  "vQxb9taf5qebNFS4nDLCXbmHS_w7U0Mx8mmcSoH4ns ",
                        "id": 1,
                        "email": "director@director.com",
                        "first_name": "Jane",
                        "last_name": "Doe",
                        "role": "DIRECTOR"
                    }
                }
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="User doesn't exist with these credentials",
                examples={
                    "application/json": {
                        "detail": "No active account found with the given credentials"
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Password is empty",
                examples={
                    "application/json": {
                        "password": ["This field may not be blank."]
                    }
                }
            )
        }
