from django.shortcuts import render
from rest_framework import status , generics
from . import models
from . import serializers
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from Authentication import fun
import pandas as pd
from .fun import groupingTimeNoReserve, groupingTime
from persiantools.jdatetime import JalaliDate
from datetime import datetime
import pytz



def date_str_to(date):
    return datetime.strptime(date,"%Y-%m-%d")

def date_to_jalali(date):
    return str(JalaliDate(date))

def date_to_weekday(date):
    return date.weekday()


# select and show  time for user
class SelectTimeUserViewset(APIView):
    def get(self, request, pk):
            Authorization = request.headers.get('Authorization')
            if not Authorization:
                return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = fun.decryptionUser(Authorization)
            if not user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            times = models.SelectTime.objects.filter(consultant_id=pk,reserve=False).order_by('date', 'time' , 'reserve')
            if not times.exists():
                return Response([], status=status.HTTP_200_OK)
            df = [serializers.SelectTimeSerializer(x).data for x in times]
            df = pd.DataFrame(df)
            df = df.groupby('date').apply(groupingTimeNoReserve)


            df = df.reset_index()
            df = df.sort_values(by='date')
            df = df[df.index<10]
            df = df[['date','time']]
            df['date'] = df['date'].apply(date_str_to)
            df['jalali'] = df['date'].apply(date_to_jalali)
            df['weekday'] = df['date'].apply(date_to_weekday)
            df = df.to_dict('records')
            return Response(df, status=status.HTTP_200_OK)
    




# show time for consultant
class SelectTimeConsultantViewset(APIView):
    def get(self, request):
            Authorization = request.headers.get('Authorization')
            if not Authorization:
                return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)

            consultant = fun.decryptionConsultant(Authorization).first()
            if not consultant:
                return Response({'error': 'consultant not found'}, status=status.HTTP_404_NOT_FOUND)
            
            times = models.SelectTime.objects.all().order_by('date', 'time' , 'reserve')
            if not times.exists():
                return Response([], status=status.HTTP_200_OK)
            df = [serializers.SelectTimeSerializer(x).data for x in times]
            df = pd.DataFrame(df)
            df = df.groupby('date').apply(groupingTime)
            df = df.reset_index()
            df = df[['date','time']]
            df['date'] = df['date'].apply(date_str_to)
            df['jalali'] = df['date'].apply(date_to_jalali)
            df['weekday'] = df['date'].apply(date_to_weekday)
            df = df.to_dict('records')
            return Response(df, status=status.HTTP_200_OK)
    



# select time for consultant
class SetTimeConsultant (APIView) :
        def post (self , request) :
            Authorization = request.headers.get('Authorization')
            print(Authorization)
            if not Authorization:
                return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)
            consultant = fun.decryptionConsultant(Authorization)
            print(consultant)
            if  consultant == None:
                return Response({'error': 'consultant none'}, status=status.HTTP_404_NOT_FOUND)
            consultant = consultant.first()
            if not consultant:
                return Response({'error': 'consultant not found'}, status=status.HTTP_404_NOT_FOUND)
            
            time_stamp = request.data.get ('date')
            print(time_stamp)
            if not time_stamp :
                 return Response({'message' : 'no date'} , status=status.HTTP_404_NOT_FOUND)
            time_stamp = int (time_stamp)/1000
            time_stamp = time_stamp = datetime.fromtimestamp(time_stamp)
            date = time_stamp.date()
            time = time_stamp.hour
            set_date = models.SelectTime.objects.filter(date=date ,time=time)
            if set_date.exists () :
                 return Response ({'message' : 'این تاریخ از قبل تعین شده است'} , status=status.HTTP_406_NOT_ACCEPTABLE)
            set_time_model = models.SelectTime (consultant=consultant , date =date , time = time)
            set_time_model.save()

            return Response ({'message' : 'زمان مشاوره ثبت شد'},status=status.HTTP_200_OK)
        


        def delete(self, request):
                print(request.data)
                Authorization = request.headers.get('Authorization')
                if not Authorization:
                    return Response({'error': 'Authorization header is missing'}, status=status.HTTP_400_BAD_REQUEST)

                consultant = fun.decryptionConsultant(Authorization).first()
                if not consultant:
                    return Response({'error': 'consultant not found'}, status=status.HTTP_404_NOT_FOUND)
                # 2024-07-14T00:00:00
                date = request.query_params.get('date')
                date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
                time = request.query_params.get('time')
                print(date)
                print(time)
                if not time or not date :
                    return Response({'message': 'no date or no time'}, status=status.HTTP_404_NOT_FOUND)
                
                set_date = models.SelectTime.objects.filter(consultant=consultant, date=date, time=time)
                if not set_date.exists():
                    return Response({'message': 'زمان مشاوره پیدا نشد'}, status=status.HTTP_404_NOT_FOUND)
                set_time_instance = set_date.first()
                if set_time_instance.reserve:
                    return Response({'message': 'زمان مشاوره رزرو شده است و نمی‌توان آن را حذف کرد'}, status=status.HTTP_400_BAD_REQUEST)
                
                set_time_instance.delete()
                return Response({'message': 'زمان مشاوره حذف شد'}, status=status.HTTP_200_OK)                
