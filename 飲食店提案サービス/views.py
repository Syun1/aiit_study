'''
大学院で作成した飲食店提案サービスの実行・制御ファイルの一部
・フロントエンドとバックエンド間のデータの送受信処理
・レコメンドエンジンの実行処理
・データ形式(list、jsonなど)の変換処理
'''

from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from oaiso.models import Shop, Shop_info
from oaiso import recommend #, recommend_backup
from oaiso.serializers import UserSerializer, GroupSerializer, ShopSerializer, TestSerializer
import random
from django.http import HttpResponse, HttpResponseNotFound

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer



def shops(request):
    shops = Shop.objects.all()
    serializer = ShopSerializer(shops, many=True)
    return JsonResponse(serializer.data, safe=False)


def shop_info(request):
    if request.GET.get('lat') and request.GET.get('lng') and request.GET.get('uvec'):
        req_lat = request.GET['lat']    #緯度のリクエストパラメータ
        req_lng = request.GET['lng']    #経度のリクエストパラメータ
        uvec = request.GET['uvec'] #ユーザベクトルのリクエストパラメータ
        list_uvec = list(map(float, uvec.split(",")))
        r = 0  #エリアの距離(初期値)
        num = 10 #提案店舗数
        app = []

        #レコメンドエンジンの実行処理
        while r <= 1000:
            r += 250
            dist = recommend.distance_filter(r, req_lat, req_lng) #距離フィルタリング
            score_list = recommend.contents_filter(dist, list_uvec) #内容ベースフィルタリング

            for row in score_list:
                if row[1] > 0.6:
                    app.append(row)
                    continue

            if len(app) > 0:
                recommend_id = recommend.return_id(app)
                if len(recommend_id) >= num:
                    break


        #提案店舗データ
        shop_info = Shop_info.objects.all().filter(id__in=recommend_id[:num]).extra(
            select={'manual': 'FIELD(id,%s)' % ','.join(map(str, recommend_id))},
            order_by=['manual'])
        
        #Jsonに変換
        serializer = TestSerializer(shop_info, many=True)
        return JsonResponse(serializer.data, safe=False)


    else:
        shop_info = Shop_info.objects.all()
        serializer = TestSerializer(shop_info, many=True)

    return JsonResponse(serializer.data, safe=False)

