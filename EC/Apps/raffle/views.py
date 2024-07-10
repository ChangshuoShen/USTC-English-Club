from django.shortcuts import render, HttpResponse, redirect
from .models import Prize

# Create your views here.

def raffle(request):
    prizes = Prize.get_all_prizes()
    return render(request, 'raffle.html', {
        'prizes': prizes,
    })


def perform_raffle(request):
    if request.method == 'POST':
        participant_count = int(request.POST.get('participant_count', 1))
        selected_prizes = []
        for _ in range(participant_count):
            prize = Prize.draw_prize()
            if prize:
                selected_prizes.append(prize.name)
                Prize.update_prize(prize.id, prize.quantity - 1)
        print(selected_prizes)
        return render(request, 'raffle.html', {'selected_prizes': selected_prizes})

    return redirect('raffle')  # 其余情况直接回到原位置


def manage_prizes(request):
    if request.method == 'POST':
        # 处理奖品数量更新
        for prize_id, new_quantity in request.POST.items():
            if prize_id.startswith('quantity_'):
                prize_id = prize_id.replace('quantity_', '')
                new_quantity = int(new_quantity)
                Prize.update_prize(prize_id, new_quantity)
        
        # 处理添加新奖品
        new_prizes = []
        for key, value in request.POST.items():
            if key.startswith('new_prize_name_'):
                index = key.split('_')[-1]
                new_prize_name = value
                new_prize_quantity = int(request.POST.get(f'new_prize_quantity_{index}', 0))
                if new_prize_name and new_prize_quantity:
                    new_prizes.append(Prize(name=new_prize_name, quantity=new_prize_quantity))
        
        Prize.objects.bulk_create(new_prizes)
        
        return redirect('raffle:manage_prizes')
    
    prizes = Prize.objects.all()
    return render(request, 'manage_prizes.html', {'prizes': prizes})