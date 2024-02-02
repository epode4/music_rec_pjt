from django.shortcuts import render, redirect
import logging
import matplotlib.pyplot as plt
from .models import user_artist_agg,user_track_agg,user_day_agg, user_hour_agg, user_genre_agg
from spotify.util import get_user_tokens
from django.http import JsonResponse
# from final_pjt.mongdb import find_log
# from datetime import datetime, timedelta

logger = logging.getLogger("onclick")


def show_static(request):
    return render(request, 'static_home.html')

def show_personal_static(request):

    username = request.user.username

    artist_agg = user_artist_agg.objects.filter(username=username)
    track_agg = user_track_agg.objects.filter(username=username)
    day_agg = user_day_agg.objects.filter(username=username)
    hour_agg = user_hour_agg.objects.filter(username=username)
    genre_agg = user_genre_agg.objects.filter(username=username)

    # # 모든 시간대에 대한 정보
    # log_mongodb = find_log()
    
    # # 현재로 부터 1시간전 정보
    # result = []
    
    # start = datetime.now() - timedelta(hours=1)
    # start_time = start.strftime("%Y-%m-%d %H:00:00")
    
    # for i in log_mongodb:
    #     if i["start"] == start_time:
    #         result.append(i)
            
    # # 모든 시간대 정보
    # unique_times = list(set(time['start'] for time in log_mongodb))
            
    # if request.method == 'GET':
    #     selected_time = request.GET.get('time')  # 선택한 날짜 받아오기
    #     for i in log_mongodb:
    #         if i["start"] == selected_time:
    #             result.append(i)
                
    context = {
        'artist_agg': artist_agg,
        'track_agg' : track_agg,
        'day_agg' : day_agg,
        'username' : username,
        'hour_agg' : hour_agg,
        'genre_agg' : genre_agg,
    }
    
        #     'log_mongodb' : log_mongodb,
        # 'start_time' : start_time,
        # 'result' : result,
        # 'unique_times' : unique_times,
    # return JsonResponse(context)

    return render(request, 'personal_static.html', context) # {'token':token}

