
from rest_framework.views import APIView
from rest_framework.response import Response

class CertificateView(APIView):
    def get(self, request, course_id):
        return Response({'certificate':'generated'})
