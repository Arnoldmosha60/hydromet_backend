import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SensorData
from .serializers import SensorDataSerializer
from requests.auth import HTTPBasicAuth


def send_sms(message):
    # if phone_number.startswith('0'):
    #     phone_number = '255' + phone_number[1:]
    data = {
        "source_addr": "INFO",
        "schedule_time": "",
        "encoding": 0,
        "message": message,
        "recipients": [
            {
                "recipient_id": 1,
                "dest_addr": '0774299510',
            }
        ]
    }

    try:
        username = "59e77c6f92ef3836"
        password = "MmNkMmE0YjI4NjFiZDgwNjZkZDNmZWY0ZTU4YzA5ZThkZDFlODMwZGRmMmM4ZDYwMDg1YjVjNDUxYWM3ZmQyZQ=="
        response = requests.post("https://apisms.beem.africa/v1/send", json=data, auth=HTTPBasicAuth(username, password))

        if response.status_code == 200:
            print("SMS sent successfully!")
            return Response({'message': 'SMS sent successfully'}, status=status.HTTP_200_OK)
        else:
            print(f"SMS sending failed. Status code: {response.status_code}, Response: {response.text}")
            return Response({'message': 'failed to send SMS'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")


class SensorDataView(APIView):
    def post(self, request):
        print(request.data)
        rainfall = request.data.get('rainfall')
        ph_value = request.data.get('pHValue')
        soil_moisture = request.data.get('soilMoisture')
        flow_rate = request.data.get('flowRate')
        water_level = request.data.get('waterLevel')
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if ph_value:
                if ph_value >= 7.1:
                    send_sms(message='The Water is Basic')
                    return Response({'success'})
                elif ph_value == 7.0:
                    send_sms(message='The water is neutral')
                    return Response({'success'})
                else:
                    send_sms(message='The water is Acidic')
                    return Response({'success'})
            if soil_moisture:
                if soil_moisture >= 10:
                    send_sms(message='Soil has moisture')
                    return Response({'success'})
                else:
                    send_sms(message='Soil is dry')
                    return Response({'success'})
            if flow_rate:
                if flow_rate >= 6000.00:
                    send_sms(message='The water flow is high')
                    return Response({'success'})
                else:
                    send_sms(message='The water flow is moderate')
                    return Response({'success'})
            if water_level:
                if water_level >= 20:
                    send_sms(message='The water level is high')
                    return Response({'success'})
                else:
                    send_sms(message='The water level is moderate')
                    return Response({'success'})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        data = SensorData.objects.all()
        serializer = SensorDataSerializer(data, many=True)
        return Response(
            {
                'data': serializer.data,
                'msg': 'Hydromet data fetched successfully'
            },
            status=status.HTTP_200_OK
            )
