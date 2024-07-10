from django.shortcuts import render, HttpResponse
from .models import Riddle
# 这里主要是实现两点：
    # 一点是按照难度等级显示爬取的riddles
    # 另一点则是满足用户直接在“评论区”写答案以及简单回复

def hunt_index(request):
    '''
        按照顺序将所有的riddles获取并返回给hunt_index.html进行展示
    '''
    page = request.GET.get('page', 1)
    all_riddles = Riddle.get_all_riddles(page)
    riddles_by_difficulty = Riddle.get_riddles_by_difficulty(page)
    # print(type(all_riddles), type(riddles_by_difficulty), riddles_by_difficulty.keys())
    final_dict = {
        '1': all_riddles,
        '2': riddles_by_difficulty['Easy'],
        '3': riddles_by_difficulty['Medium'],
        '4': riddles_by_difficulty['Hard'],
    }
    return render(request, 'mystery_hunt_index.html', {
        'contents': final_dict.items(),
    })
    # return HttpResponse()


'''
from django.shortcuts import render
from .models import Riddle

def riddle_combined_view(request):
    page = request.GET.get('page', 1)
    all_riddles = Riddle.get_all_riddles(page)
    riddles_by_difficulty = Riddle.get_riddles_by_difficulty(page)
    
    context = {
        'all_riddles': all_riddles,
        'riddles_by_difficulty': riddles_by_difficulty
    }
    
    return render(request, 'mystery_hunt_index.html', context)

'''

def hunt_detail(request, riddle_id):
    riddle = Riddle.get_riddle_by_id(riddle_id)
    return render(request, 'mystery_hunt_detail.html', {
        'riddle': riddle,
    })