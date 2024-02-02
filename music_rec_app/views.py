import time
import csv
import glob
import asyncio
import random
import numpy as np
import pandas as pd
import pickle
from datetime import datetime
from collections import defaultdict
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Value, When, Case, IntegerField, Q, Subquery
from django.db.models.functions import Concat
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from .models import Artist, Track, Playlist, PlaylistTrack, Korea_top50_track, User,MUSIC_RECOMMEND_1, MUSIC_RECOMMEND_2
from .forms import AddToPlaylistForm
from .content_rec_ml import pick_user_top2, find_top_similar_in_cluster
from .youtubemusic import get_youtube_link
from final_pjt.logger_test.json_logger import onclick_logger_test
from asgiref.sync import async_to_sync, sync_to_async
#from googlesearch import search
# from final_pjt.mongdb import find_log
from datetime import datetime, timedelta


def index(request) :
    return render(request, 'index.html')

@login_required
def main(request) :
    
    random_tracks = pick_user_top2(request)
    print(random_tracks)
    find_track = find_top_similar_in_cluster(random_tracks) 

    if 'track_id' not in find_track.columns or find_track.empty:
    # 'track_id'가 없거나 데이터프레임이 비어있는 경우
        random_track = Track.objects.all().order_by('?')[:4]
        context = {
            'username': request.user.username,
            'random_track': random_track,
        }
    else:
        # 'track_id'가 있는 경우
        find_track.set_index('track_id', inplace=True)
        print(find_track.index.duplicated().any())
        random_indices = np.random.choice(find_track.index, size=4, replace=False)
        print('random_indices: ', random_indices)

        track_list = Track.objects.filter(track_id__in=random_indices)
        print('track_list:', track_list)

        context = {
            'track_list': track_list,
            'username': request.user.username,
        }

    return render(request, 'main.html', context)
    
    
@login_required
def music(request):
    start1 = time.time()
    # all_tracks = Track.objects.all()

    start = time.time()
    # 1. MUSIC_RECOMMEND_2 user_id 일치 filter -> created_at 정렬 :5 -> track_id
    # 2. Track track_id 일치하는 거 필터링 -> Track Object

    recent_track_ids_1 = MUSIC_RECOMMEND_1.objects.filter(user_id = request.user.id).order_by('-created_at')[:5].values_list('track_id', flat=True)
    hot_songs_1 = Track.objects.filter(track_id__in=list(recent_track_ids_1))
    recent_track_ids_2 = MUSIC_RECOMMEND_2.objects.filter(user_id = request.user.id).order_by('-created_at')[:5].values_list('track_id', flat=True)
    hot_songs_2 = Track.objects.filter(track_id__in=list(recent_track_ids_2))
    
    print('확인 1-1 :',recent_track_ids_1)
    print('확인 1-2 :',hot_songs_1)
    print('확인 2-1 :',recent_track_ids_2)
    print('확인 2-2 :',hot_songs_2)
    
    #hot_songs = Track.objects.all().order_by('?')[:3]
    my_playlist = Track.objects.all().order_by('?')[:2]
    current_track = Track.objects.all().order_by('?')[:1]
    
    end = time.time()
    print('쿼리 불러오기 시간 :', {end-start})
    
    start = time.time()
    
    top_50_track = Korea_top50_track.objects.all().order_by('rank') #.order_by('?')[:50]
    
    end = time.time()
    print('top50 불러오기 시간 :', {end-start})
    
    
    # user_id = request.user.id
    
    
    # start = time.time()
    # recommended_playlists = recommend_music(request, user_id)

    #recommended_playlists_2 = recommend_music_2(request, user_id)
    # end = time.time()
    # print('음악 플레이리스트 추천 함수 시간 :', {end-start})
    
    # recommended_tracks = []
    # for playlist in recommended_playlists:
    #     track_info = Track.objects.get(track_id=playlist['track_id'])
    #     recommended_tracks.append(track_info)
        
    # 특정 나이대 성별에게 추천
        
    user_gender = request.user.gender
    
    if user_gender == '여자':
        user_gender = '여성'
    else:
        user_gender = '남성'
    
    user_birth = request.user.birth_date
    today = datetime.now()
    now_year = today.year

    user_age = now_year - (user_birth.year)
    user_age_range = user_age // 10 * 10
    
    # 자신의 플레이리스트 
    
    user_playlist = Playlist.objects.filter(user_id = request.user.id)
    user_playlist_id = [playlist.playlist_id for playlist in user_playlist]
    
    default_playlist_image = "/static/images/KakaoTalk_20231221_105118953.png"

    path = '/home/ubuntu/Data_Engineering/kafka-spark-streaming/output/part*.csv'
    matching_files = glob.glob(path)
    
    # start = time.time()
    streaming_track_agg = []
    for file_path in matching_files:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                for i in range(4, 6):
                    dt = datetime.strptime(row[i], "%Y-%m-%dT%H:%M:%S.%f%z")
                    row[i] = dt.strftime("%Y-%m-%d %H:%M:%S")
                streaming_track_agg.append(row) 

    # 오늘 전체 시간대에 대한 log 결과
    # today_date = datetime.now().date()
    # filtered_data = [row for row in streaming_track_agg if row[4].split(' ')[0] == str(today_date)]
    
    streaming_track_agg = sorted(streaming_track_agg, key=lambda x: (x[4], -int(x[3])))

    # 시간대
    unique_times = sorted(list(set(track[4] for track in streaming_track_agg)))

    # 선택한 시간대에 대한 log 정보 
    result = []  
    if request.method == 'GET':
        selected_time = request.GET.get('time')  # 선택한 날짜 받아오기
        for i in streaming_track_agg:
            if i[4] == selected_time:
                result.append(i)
                
    # 직전 시간대에 대한 log 정보
    current_result = []
    current_time = datetime.now() - timedelta(hours=1)
    current_time = current_time.strftime("%Y-%m-%d %H:00:00")
    
    two_hours_ago_str = (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:00:00")
    
    for i in streaming_track_agg:
        if i[4] == current_time:
            current_result.append(i)
    
    if not current_result:
        for i in streaming_track_agg:
            if i[4] == two_hours_ago_str:
                current_result.append(i)
 
    # end = time.time()
    # print('실시간 많이 듣는 음악 시간 :', {end-start})
    
    context = {
        'hot_songs_1': hot_songs_1,
        'hot_songs_2': hot_songs_2, 
        'my_playlist': my_playlist, 
        'current_track': current_track, 
        'top_50_track' : top_50_track,
        #'recommended_playlists': recommended_tracks,
        #'recommended_playlists_2': recommended_tracks_2,
        'user_gender': user_gender,    
        'user_age_range': user_age_range,
        'user_playlist_id': user_playlist_id,
        'default_playlist_image': default_playlist_image,
        'current_result' : current_result,
        'result' : result,
        'unique_times' : unique_times,
    }
    
   
    end1 = time.time()
    print('최종 music 실행 시간:', {end1-start1})
   
    return render(request, 'music.html', context)






def playlist_detail(request, playlist_id):
    playlist_tracks = PlaylistTrack.objects.filter( playlist = playlist_id).order_by('-id')
    
    inplaylist_tracks = []
    for tracks in playlist_tracks:
        track_id = tracks.track.track_id
        # Track 모델에서 track_id에 해당하는 노래 정보 가져오기
        track_info = Track.objects.get(track_id=track_id)
        # track_info = Track.objects.get(track_id=tracks.track)
        inplaylist_tracks.append(track_info)
    
    return render(request, 'playlist_detail.html', {'inplaylist_tracks':inplaylist_tracks})





# @log_send_kafka
@onclick_logger_test
def detail(request, track_id):
    track = Track.objects.get(track_id=track_id)
    print('track_id:',track.track_id)
    
    # 현재 로그인한 사용자의 id를 가져온다.
    user_id = request.user.id

    # playlist_id를 가져오기 위해 Playlist 모델을 필터링한다.
    playlist = Playlist.objects.filter(user_id=user_id).first()
    
    # track_in_playlist = PlaylistTrack.objects.filter(track=track.track_id, playlist=playlist.playlist_id).first()
    
    track_in_playlist = None
    
    if playlist:
        # playlist가 존재하는 경우에만 해당 track_in_playlist을 가져온다.
        track_in_playlist = PlaylistTrack.objects.filter(track=track.track_id, playlist=playlist.playlist_id).first()
    
    
    context = {
        'track': track,
        'track_in_playlist': track_in_playlist,
    }

    return render(request, 'detail.html', context)


  
    
    

def add_to_playlist(request, track_id):
    track = Track.objects.get(track_id=track_id)
    
    if request.method == 'POST':
        # 현재 로그인한 사용자의 id를 가져온다.
        user_id = request.user.id

        # playlist_id를 가져오기 위해 Playlist 모델을 필터링한다.
        playlist = Playlist.objects.filter(user_id=user_id).first()

        if playlist:
            playlist_id = playlist.playlist_id
            rating_score = request.POST.get('rating_score', None)
            print('rating_score: ', rating_score)
            

            if rating_score is not None:
                rating_score = int(rating_score)
                if rating_score == 1:
                    cnt = random.randint(21, 40)
                elif rating_score == 2:
                    cnt = random.randint(41, 60)
                elif rating_score == 3:
                    cnt = random.randint(61, 80)
                elif rating_score == 4:
                    cnt = random.randint(81, 100)
                elif rating_score == 5:
                    cnt = random.randint(101, 120)
                else:
                    cnt = None
            else:
                cnt = None

            form_data = {'track_id': track_id, 'playlist_id': playlist_id,'rating_score':rating_score, 'cnt':cnt}

            # 폼을 초기화하고 데이터를 직접 지정한다.
            form = AddToPlaylistForm(data=form_data)
            print('cnt:', cnt)

            if form.is_valid():

                # 현재 트랙이 이미 해당 플레이리스트에 있는지 확인
                if not PlaylistTrack.objects.filter(track=track_id, playlist=playlist).exists():
                    # 중복이 없으면 추가
                    playlist_track = PlaylistTrack.objects.create(track=track, playlist=playlist,rating=rating_score, cnt=cnt)
                    playlist_track.save()
                    print('플레이리스트에 추가 완료')
                else:
                    print('이미 플레이리스트에 추가된 트랙입니다.')
            else:
                print('폼이 유효하지 않습니다. 에러:', form.errors)
        else:
            print('사용자의 플레이리스트가 존재하지 않습니다.')
    else:
        form = AddToPlaylistForm()
        print('POST 방식이 아닙니다')

    return redirect('music_rec_app:detail', track_id=track_id)

    # return render(request, 'detail.html', {'track': track, 'form': form})
    
def remove_from_playlist(request, track_id):
    track = Track.objects.get(track_id=track_id)

    if request.method == 'POST':
        # 현재 로그인한 사용자의 id를 가져온다.
        user_id = request.user.id

        # playlist_id를 가져오기 위해 Playlist 모델을 필터링한다.
        playlist = Playlist.objects.filter(user_id=user_id).first()

        if playlist:
            # 현재 트랙이 해당 플레이리스트에 있는지 확인
            playlist_track = PlaylistTrack.objects.filter(track=track, playlist=playlist).first()

            if playlist_track:
                # 플레이리스트에서 트랙 제거
                playlist_track.delete()
                print('플레이리스트에서 제거 완료')
            else:
                print('해당 트랙이 플레이리스트에 없습니다.')
        else:
            print('사용자의 플레이리스트가 존재하지 않습니다.')
    else:
        print('잘못된 요청입니다.')

    return redirect('music_rec_app:detail', track_id=track_id)


async def predict_wrapper(model, user_id, track_ids):
    return await sync_to_async(model.predict)(user_id, track_ids)


# @login_required
# def recommend_music(request,user_id):
#     start = time.time()
#     loaded_model = pickle.load(open('/home/ubuntu/makedjango/final_pjt/music_rec_app/model/Collaborative_Filtering_model.pkl', 'rb'))
#     end = time.time()
#     print('pkl 불러오기 시간 :', {end-start})
    
#     # start = time.time()
#     # playlist_tracks = PlaylistTrack.objects.filter(playlist__user_id = user_id)
#     # df = pd.DataFrame(list(playlist_tracks.values('playlist__user_id', 'track__track_id', 'rating')))
    
#     playlist_tracks = PlaylistTrack.objects.filter(playlist__user_id=user_id).values('playlist__user_id', 'track__track_id', 'rating')
#     df = pd.DataFrame.from_records(playlist_tracks)
#     # end = time.time()
#     # print('user_id 와 일치 playlist 가져오기 :', {end-start})

#     start = time.time()
#     # user_tracks = df[df['playlist__user_id'] == user_id]['track__track_id'].unique()
#     user_tracks = PlaylistTrack.objects.filter(playlist__user_id=user_id).values_list('track__track_id', flat=True).distinct()

#     all_track_ids = [track_id for track_id in PlaylistTrack.objects.values_list('track__track_id', flat=True).distinct() if track_id not in user_tracks]
#     # all_track_ids = PlaylistTrack.objects.exclude(playlist__user_id=user_id).values_list('track__track_id', flat=True).distinct()

#     end = time.time()
#     # print('사용자 들은 곡, 안 들은 곡 시간 :', {end-start}, type(all_track_ids))
#     # print(all_track_ids[:5])
    
#     # start = time.time()

#     # all_track_ids = list(all_track_ids)

#     # end = time.time()
#     # print('리스트 변환 시간:', {end-start})
    
    
#     start = time.time()
#     predictions = [loaded_model.predict(user_id, str(track_id)) for track_id in all_track_ids]

#     predictions.sort(key=lambda prediction: prediction.est, reverse=True)
#     top_tracks = [predictions[i].iid for i in range(5)]
#     end = time.time()
#     print('예측하는 시간 :', {end-start})
    
#     print('탑트랙스 확인1111 :', top_tracks)
    
#     start = time.time()
#     result = []
#     for track_id in top_tracks:
#         recommended_track = PlaylistTrack.objects.filter(track__track_id=track_id).first()

#         if recommended_track:
#             result.append({
#                 'playlist_id': recommended_track.playlist.playlist_id,
#                 'track_id': recommended_track.track.track_id,
#                 'rating': recommended_track.rating
#             })

#     end = time.time()
#     print('최종 for문 도는 시간 :', {end-start})
    
#     print('결과 확인1111 :', result)
#     return result
#     # return render(request, 'music.html', {'recommended_playlists': result})


# # @login_required
# def recommend_music_2(request, user_id):
#     collaborative_filtering_model = pickle.load(open('/home/ubuntu/makedjango/final_pjt/music_rec_app/model/Collaborative_Filtering_model_2.h5', 'rb'))

#     user_playlists = PlaylistTrack.objects.filter(playlist__user__id=user_id)

#     user_gender = request.user.gender
#     user_age_group = request.user.age_group

#     similar_users_playlists = PlaylistTrack.objects.filter(
#         playlist__user__gender=user_gender,
#         playlist__user__age_group=user_age_group
#     ).exclude(playlist__user__id=user_id)

#     user_tracks = user_playlists.values_list('track__track_id', flat=True)

#     similar_users_tracks = similar_users_playlists.values_list('track__track_id', flat=True).distinct()

#     new_tracks_for_user = [track_id for track_id in similar_users_tracks if track_id not in user_tracks]

#     predictions = [(track_id, collaborative_filtering_model.predict(user_id, str(track_id)).est) for track_id in new_tracks_for_user]

#     predictions.sort(key=lambda x: x[1], reverse=True)

#     top_tracks = predictions[:5]

#     recommended_tracks = []
#     for track_id, _ in top_tracks:
#         track = Track.objects.get(track_id=track_id)
#         recommended_tracks.append({
#             'track_id': track.track_id,
#             'track_name': track.track_name,
#         })

#     return recommended_tracks



def searchResult(request):
    products = None
    query = None
    
    if 'q' in request.GET:
        query = request.GET.get('q')
        products = Track.objects.annotate(
            combined_name=Concat('artist_name', Value(' '), 'track_name'),
            combined_name2=Concat('track_name', Value(' '), 'artist_name')
        ).filter(Q(combined_name__icontains=query) | Q(artist_name__icontains=query) | 
                 Q(track_name__icontains=query) | Q(combined_name2__icontains=query))
        
        
        ordering = Case(
            When(combined_name__iexact=query, then=0),
            When(combined_name2__iexact=query, then=1),
            When(artist_name__iexact=query, then=2),
            When(track_name__iexact=query, then=3),
            default=4,
            output_field=IntegerField(),
        )

        # Apply ordering to the queryset
        products = products.order_by(ordering)
        
    return render(request, 'search.html', {'query': query, 'products': products})


def music_search(request):
    genres = None
    query = None
    
    if 'genre' in request.GET:
        query = request.GET.get('genre')
        genres = Track.objects.filter(Q(genres__exact=query))
    else:
        print("안 들어옴")
        
        
        # ordering = Case(
        #     When(combined_name__iexact=query, then=0),
        #     When(artist_name__iexact=query, then=1),
        #     When(track_name__iexact=query, then=2),
        #     When(combined_name2__iexact=query, then=3),
        #     default=4,
        #     output_field=IntegerField(),
        # )

        # Apply ordering to the queryset
        # products = products.order_by(ordering)
        
    return render(request, 'search_genre.html', {'query': query, 'genres':genres})



def popup(request, track_id):
    print(track_id)
    
    # if request.method == 'POST':
    #     cnt_value = request.POST.get('cnt')
    #     rating_value = request.POST.get('rating_score')

    #     playlist_track = PlaylistTrack(track_id=track_id, cnt=cnt_value, rating=rating_value)
    #     playlist_track.save()

    #     return redirect('some_redirect_view')  # 필요에 따라 리디렉션
    
    # cnt_values = [random.randint(21, 40) if rating == "1"
    #               else random.randint(41, 60) if rating == "2"
    #               else random.randint(61, 80) if rating == "3"
    #               else random.randint(81, 100) if rating == "4"
    #               else random.randint(101, 120) for rating in map(str, range(1, 6))]
    
    
    return render(request, 'popup.html', {'track_id':track_id})


@login_required
def create_playlist(request):
    # 현재 로그인된 사용자의 ID 가져오기
    user_id = request.user.id

    # 새로운 Playlist 객체 생성
    new_playlist = Playlist(user_id=user_id)

    # 데이터베이스에 저장
    new_playlist.save()

    # 원하는 리다이렉션 또는 응답 처리
    return redirect('music_rec_app:music')