from django.shortcuts import render, HttpResponse
from .models import Riddle
# 这里主要是实现两点：
    # 一点是按照难度等级显示爬取的riddles
    # 另一点则是满足用户直接在“评论区”写答案以及简单回复

def hunt_index(request):
    # return render(request, 'mystery_hunt_index.html')
    tmp = Riddle.get_riddles_by_difficulty()
    # print(len(tmp))
    return HttpResponse(tmp.keys())


def hunt_detail(request):
    return render(request, 'mystery_hunt_detail.html')