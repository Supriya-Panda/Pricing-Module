from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PriceCalculationSerializer
from .services import calculate_price


class CalculatePriceView(APIView):
    def post(self, request):
        serializer = PriceCalculationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = calculate_price(serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
