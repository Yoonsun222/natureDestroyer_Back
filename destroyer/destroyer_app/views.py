import random
from django.shortcuts import render
from .models import User, Ranking
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count, Avg
from bs4 import BeautifulSoup
import requests

# Create your views here.

cal = 0
user_school = ''
user_nickname = ''

def home( request ):
    global cal, user_school, user_nickname
    cal = 0
    user_school = ''
    user_nickname = ''
    return render( request, 'home.html' );

def profile( request ):
    return render( request, 'profile.html' );

@csrf_exempt
def createuser(request):
    global user_school, user_nickname
    if request.method == 'POST':
        user_school = request.POST['school']
        user_nickname = request.POST['nickname']
        return render( request, 'question_1.html' )
 
def question( request ):
    num = request.GET.get('num',None)
    if not num:
        return render( request, '404.html',{'num':num} )
        
    elif int(num) >= 1 and int(num) <= 16:
        target = 'question_'+str(int(num))+'.html'
        return render( request, target )
    else:
        return render( request, '404.html',{'num':num} )

def usersave():
    global cal, user_school, user_nickname
    if user_nickname != '' and user_school != '':
        user = User()
        user.score = int(cal*52//6.6)
        user.nickname = user_nickname
        user.school = user_school
        user.save()

def crawling():     
    url = "http://www.yes24.com/24/Category/Display/001001022003002"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    answer = {}
    # 도서명 크롤링
    
    total_books = soup.select('span.imgBdr > a > img') 
    images = soup.select('span.imgBdr > a > img')
    base_link = "https://www.yes24.com"
    links = soup.select('span.imgBdr > a')
    
    num1 = random.randrange(0,len(total_books))
    if len(total_books) % 2:
        num2 = len(total_books)-1 - num1
    else:
        num2 = len(total_books)-num1-2
    
    answer[total_books[num1]['alt']] = {images[num1]['src'] : base_link + links[num1]['href']}
    answer[total_books[num2]['alt']] = {images[num2]['src'] : base_link + links[num2]['href']}

    return answer



def result( request ):
    usersave()
    global cal
    tree_num = int(cal*52//6.6)
    if tree_num > 3500:
        result = '공기도 아까운 쓰레기 입니다.'
        img= 1
    elif tree_num > 2620:
        result = '재활용가능한 쓰레기 입니다.'
        img = 2
    elif tree_num > 1650:
        result = '재활용 잘된 쓰레기 입니다.'
        img = 3
    else:
        result = '공기가 아깝지 않은 멋쟁이 지구 수호천사 입니다.'
        img = 4
    tree = '🌲' * tree_num
    book_reco = crawling()
    return_dic = {'tree': tree, 'cal':cal, 'result': result, 'img':img, 'book_reco': book_reco }
    return render( request, 'result.html', return_dic )


def ranking( request ):
    result = User.objects.all().values('school').annotate(Avg('score'))
    result = result.order_by('score__avg')
    return render( request, 'ranking.html', {'rank':result })


def answer( request ):
    global cal
    num = int(request.GET.get('num', None))
    result = str(request.GET.get('result', None))
    if num==None or result==None:
        return render( request, '404.html',{'num':num} )
    elif num ==1:
        if result == '0':
            result = ' 0kg'
        if result == '1':
            cal += 0.83 
            result = ' ~0.83kg'
        elif result == '2':
            cal += 1.66
            result = ' ~1.66kg'
        elif result == '3':
            cal += 3.32
            result = ' ~3.32kg'
        elif result == '4':
            cal += 4
            result = ' 3.32kg 이상'
        return render( request, 'question_'+str(num)+'_result.html', {'result': result} )
    
    elif num == 2:
        if result == '0':
            result = '0kg'
            cal += 294
        elif result == '1':
            result = ' ~84kg'
            cal += 231
        elif result == '2':
            result = ' ~168kg'
            cal += 147
        elif result == '3':
            result = '~294kg'
            cal += 63
        elif result == '4':
            result = ' 294kg 이상'
        return render( request, 'question_'+str(num)+'_result.html', {'result': result} )
        
    
    elif num == 3:
        if result == '0':
            cal += 3
            result = '쓰레기 입니까?'
        elif result == '1':
            result = '훌륭한 지구 지킴이'
            cal += 0
        elif result == '2':
            cal += 1
            result = '좀만 더 노오력..해주세요! 씻어서 버리는 방법도 있다!'
        return render( request, 'question_'+str(num)+'_result.html', {'result': result} )
        
    
    elif num == 4:
        result = int(result)
        if result >= 27:
            result = '멋쟁이 환경 지킴이'
        else:
            cal += abs(result - 27) * 1.2
            result = '쓰레기'
        return render( request, 'question_'+str(num)+'_result.html', {'result': result} )
    
    elif num ==5:
        if result == '0':
            result = '0kg'
        if result == '1':
            cal += 1
            result = '~1kg'
        elif result == '2':
            cal += 2
            result = '~2kg'
        elif result == '3':
            cal += 3
            result = '~3kg'
        elif result == '4':
            cal += 4
            result = '3kg 이상'
        return render( request, 'question_'+str(num)+'_result.html', {'result': result} )
    
    elif num == 6:
        result = int(result)
        cal += result * 0.113 * 7 
        return render( request, 'question_'+str(num)+'_result.html', {'result': str(int(result)* 0.113 * 7)+"kg"} )
    elif num == 8:
        result = int(result)
        cal  += result * 0.004 // 52
        return render( request, 'question_'+str(num)+'_result.html', {'result': str(int(result)*0.004)+"kg"} )

    elif num == 9:
        result = int(result)

        cal += result * 0.72 * 7
        return render( request, 'question_'+str(num)+'_result.html', {'result': str(int(result)*0.72 * 7)+"kg"} )
    elif num == 10:
        result = int(result)
        cal += result * 0.79
        return render( request, 'question_'+str(num)+'_result.html', {'result': str(int(result) * 0.79)+"kg"} )
    elif num == 11:
        result = int(result)
        cal += result * 12
        return render( request, 'question_'+str(num)+'_result.html', {'result': str(int(result)*0.075 * 7)+"kg"} )
    elif num == 12:
        result_num = int(result)
        cal += result_num * 1

        if result_num == 0 :
            result = "환경을 정말로 아끼고 있습니다"
        elif result_num <=67:
            result = "미국의 1인 옷 구매량보다 적은 수의 옷을 사고 있습니다. 당신의 옷 구매량은 전세계의 0.00000008375% 이하입니다. 당신이 산 옷을 만드는데 180,900L 이하의 물이 소비되었습니다. 당신이 옷을 세탁할 때마다 4690만 개 이하의 미세플라스틱이 방출됩니다."
        elif result_num ==68:
            result = "미국의 1인 옷 구매량과 같은 수의 옷을 사고 있습니다. 당신의 옷 구매량은 전세계의 0.000000085%입니다. 당신은 183,600L의 물은 소비하였습니다. 당신이 옷을 세탁할 때마다 4760만 개의 미세플라스틱이 방출됩니다."
        else:
            result = "미국의 1인 옷 구매량보다 많은 옷을 사고 있습니다. 당신의 옷 구매량은 전세계의 0.00000008625% 이상입니다. 당신은 186,300L 이상의 물을 소비하였습니다. 당신이 옷을 세탁할 때마다 4830만 개 이상의 미세플라스틱이 방출됩니다."
        return render( request, 'question_'+str(num)+'_result.html', {'result': result })
    elif num == 13:
        result_num = int(result)
        if result_num == 0 :
            result = "환경을 정말로 아끼고 있습니다"
        elif result_num == 1:
            cal += 1
            result = "한국의 1인당 비닐봉지 사용량의 약 21.7%만큼 비닐봉지를 소비하였습니다. 당신이 소비한 비닐봉지를 만드는데 사용된 석유로 자동차가 약 11.1km를 주행할 수 있습니다. 당신은 독일, 아일랜드, 핀란드의 1인 비닐봉지 사용량보다 많은 수를 사용하였습니다. (100개 기준)"
        elif result_num == 2:
            cal += 2
            result = "한국의 1인당 비닐봉지 사용량의 약 43.5%만큼 비닐봉지를 소비하였습니다. 당신이 소비한 비닐봉지를 만드는데 사용된 석유로 자동차가 약 22.2km를 주행할 수 있습니다. 당신은 독일, 아일랜드, 핀란드, 스페인의 1인 비닐봉지 사용량보다 많은 수를 사용하였습니다. (200개 기준)"
        else:
            cal += 3
            result = "알아야 합니다. 한국의 1인당 비닐봉지 사용량은 460장으로 세계에서 가장 높습니다. 셀 수 없다고 답하신 당신은 한국의 1인당 비닐봉지 사용량과 비슷하거나 많은 양의 비닐봉지를 소비하였을 것으로 생각됩니다. 당신이 소비한 비닐봉지를 만드는데 사용된 석유로 자동차가 약 51.1km 이상을 주행할 수 있습니다."
        return render( request, 'question_'+str(num)+'_result.html', {'result': result })
    elif num == 14:
        result = int(result)
        result_num = int(result)
        if result_num == 0 :
            cal += 0.36 * 7
            result = "이곳에 있는 15시간 동안 약 225g의 이산화탄소를 발생시켰습니다. 만약 당신이 멀티탭을 사용하지 않을 때 아예 꺼 놓지 않는다면 하루에 약 360g의 이산화탄소를 발생시키고 있는 것입니다. 일주일이면 무려 2.52kg을 발생시키는 셈입니다. (멀티탭 1개 기준)"
        elif result_num == 1:
            result = "이곳에 있는 15시간 동안 약 225g의 이산화탄소의 발생을 막았습니다. 멀티탭을 사용하지 않을 때 꺼 놓는다면 하루에 약 360g의 이산화탄소의 발생을 막고 있는 것입니다. 일주일이면 무려 2.52kg의 배출을 막는 셈입니다. (멀티탭 1개 기준)"
        else:
            cal += 0.36 * 7 * 0.1
            result = "많은 이산화탄소를 발생시키는 동시에 전기를 낭비하고 있습니다. 전자제품을 사용하지 않을 때도 콘센트에 플러그를 꽂아 두면 대기전력을 소비하게 됩니다. 전원을 꺼둔 상테에서도 전기는 소비되고 있기 때문에 통상적으로 약 6~10%의 전력을 낭비하고 있습니다. 서울 기준 2022년 상반기 가구당 평균 전기 사용량은 221.76kWh이고 전기 1kWh를 생산할 때 이산화탄소가 약 0.424kg 발생한다고 하므로 멀티탭을 사용하지 않으므로 인해 약 9kg의 이산화탄소를 더 발생시키는 것입니다."
        return render( request, 'question_'+str(num)+'_result.html', {'result': result })

    elif num == 15:
        result = int(result)
        result_num = int(result)
        if result_num == 0 :
            cal += 2
            result = "환경파괴범입니다. 환경파괴범이 바로 당신입니다. 일회용컵 1개당 텀블러를 최소 17번 사용해야 친환경적인 효과를 낼 수 있습니다. 일회용컵 소비를 줄이고, 1달에 1~2번 사용하는 목표를 세우시길 바랍니다."
        elif result_num == 1:
            cal += 1
            result = " 양호한 편입니다. 일회용컵 1개당 텀블러를 최소 17번 사용해야 친환경적인 효과를 낼 수 있습니다. 당신은 양호한 편이지만, 그래도 텀블러의 사용을 늘리는 것을 권장합니다."
        else:
            result = "매우 친환경적입니다. 일회용컵 1개당 텀블러를 최소 17번 사용해야 친환경적인 효과를 낼 수 있습니다. 당신은 친환경적인 사람임이 틀림없습니다."
        return render( request, 'question_'+str(num)+'_result.html', {'result': result })

    elif num == 16:
        result_num = int(result)
        if result_num == 0 :
            result = "매우 친환경적입니다. 대체적으로 우리가 사용하는 텀블러는 스테인레스 텀블러이고, 이는 1개당 최소 220회 이상 사용해야 친환경적인 효과를 낼 수 있습니다. 따라서, 당신은 1년이 되기 전에 대부분의 많은 사람들보다 친환경적인 사람이 될 수 있습니다."
        elif result_num == 1:
            result = "양호한 편입니다. 대체적으로 우리가 사용하는 텀블러는 스테인레스 텀블러이고, 이는 1개당 최소 220회 이상 사용해야 친환경적인 효과를 낼 수 있습니다. 따라서, 당신은 텀블러의 목적에 알맞게 사용하고 있습니다. "
        else:
            result = "환경파괴범입니다. 환경파괴범이 바로 당신입니다."
        return render( request, 'question_'+str(num)+'_result.html', {'result': result })

    elif num>=1 and num<=16:
        return render( request, 'question_'+str(num)+'_result.html', {'result': result} )
    else:
        return render( request, '404.html',{'num':num} )