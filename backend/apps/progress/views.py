
from rest_framework.views import APIView
from rest_framework.response import Response

class ProgressView(APIView):
    def get(self, request):
        return Response({'progress':0})
