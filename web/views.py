#главный файл, который будет отвечать за выдачу HTML в ответ на запросы
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect

#страничка по умолчанию
def index(request):
    return render(request, 'index.html')

#коллекция публикаций, пока захардкожено, позже перенесется в БД
publications_data = [
    {
        'id': 0,
        'name': 'Моя первая публикация',
        'date': datetime.now(),
        'text': '''Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.
                   <br><br>The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.''',
        'comments': [{
            'id': 0,
            'name': 'Юзер1',
            'date': datetime.now(),
            'text': 'первый комментарий'
        }]
    },
    {
        'id': 1,
        'name': 'Моя вторая публикация',
        'date': datetime.now(),
        'text': '''Section 1.10.32 of "de Finibus Bonorum et Malorum", written by Cicero in 45 BC
                   <br><br>"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"''',
        'comments': [{}]
    },
    {
        'id': 2,
        'name': 'Моя 3я публикация',
        'date': datetime.now(),
        'text': '''Section 1.10.32 of "de Finibus Bonorum et Malorum", written by Cicero in 45 BC
                   <br><br>"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"''',
        'comments': [{}]
    }
]

#процедура вывода существующих постов, либо обработка вновь поступивших постов
def publish(request):
    if request.method == 'GET':
        return render(request, 'publish.html')
    else:
        secret = request.POST['secret']
        name = request.POST['name']
        text = request.POST['text']

        if len(secret)==0 and secret != settings.SECRET_KEY:#сверка с секретом, чтобы не каждый дурак постил в блог
            return render(request, 'publish.html', {
                'error': 'Неправильный Secret Key'
            })
        if len(name) == 0:
            return render(request, 'publish.html', {
                'error': 'Пустое имя'
            })
        if len(text) == 0:
            return render(request, 'publish.html', {
                'error': 'Пустой text'
            })

        publications_data.append({
            'id': len(publications_data),
            'name': name,
            'date': datetime.now(),
            'text': text.replace('\n', '<br />')
        })
        return redirect('/publications')

#сделаем единую функцию для списка публикаций и для каждой публикации
def publications(request, number=-1):
    if number<0:#специальный ключ, по которому выведем список публикаций
        return render(request, 'publications.html', {
            'publications': publications_data
        })
    if number>=0 and number < len(publications_data): #проверим правильный индекс публикации
        return render(request, 'publication.html', {
            'publication': publications_data[number]
        })
    else:#иначе выкинем в начало
        return redirect('/')

#страница статуса?
def status(request):
    return HttpResponse('<h2>OK</h2>')

#коллекция для постов обратной связи, пока захардкожено, позже перенесется в БД
feedback_data = [
    {
        'id': 0,
        'name': 'Пользователь №1',
        'date': datetime.now(),
        'email': 'somebody@fromnowhere.net',
        'text': 'Кг/ам'
    },
    {
        'id': 1,
        'name': 'Второй',
        'date': datetime.now(),
        'email': 'somebody2@fromnowhere2.gov',
        'text': 'Все понравилось'
    },
    {
        'id': 2,
        'name': '3й-на',
        'date': datetime.now(),
        'email': 'nobody@fromanywhere.com',
        'text': 'Пишем дальше'
    }
]

#страничка контактов
def contacts(request):
    return render(request, 'contacts.html', {
        'feedbackCount': len (feedback_data) #покажем количество отзывов всего.
    })

#сделаем единую функцию для списка публикаций обратной связи
def feedback(request, number=-1):
    if request.method == 'GET':
        return render(request, 'feedback.html', {
            'feedbackCol': feedback_data
        })
    else:
        name = request.POST['name']
        text = request.POST['text']

        if len(name) == 0:
            return render(request, 'feedback.html', {
                'error': 'Пустое имя',
                'feedbackCol': feedback_data
            })
        if len(text) == 0:
            return render(request, 'feedback.html', {
                'error': 'Пустой text',
                'feedbackCol': feedback_data
            })

        feedback_data.append({
            'id': len(feedback_data),
            'name': name,
            'date': datetime.now(),
            'text': text.replace('\n', '<br />')
        })

        return redirect('/feedback')

#коллекция для комментариев, пока захардкожено, позже перенесется в БД
comment_data = [
    {
        'id': 0,#id комментария
        'blogId': 0, #id записи в блоге к которому этот комментарий принадлежит
        'name': 'Пользователь №1',
        'date': datetime.now(),
        'email': 'somebody@fromnowhere.net',
        'text': 'Кг/ам'
    },
    {
        'id': 1,
        'blogId': 0, #id записи в блоге к которому этот комментарий принадлежит
        'name': 'Второй',
        'date': datetime.now(),
        'email': 'somebody2@fromnowhere2.gov',
        'text': 'Все понравилось'
    },
    {
        'id': 2,
        'blogId': 1, #id записи в блоге к которому этот комментарий принадлежит
        'name': '3й-на',
        'date': datetime.now(),
        'email': 'nobody@fromanywhere.com',
        'text': 'Пишем дальше'
    }
]

#сделаем единую функцию для добавления комментариев к записям блога
def comments(request, number=-1):
    if number<0 or number >=len(publications_data):#неверный индекс записи в блоге, отправляем его читать все записи
        return redirect('../publications')
    if request.method == 'GET':#можем только на POST реагировать
       return redirect(f'../publications/{number}')
    else:
        name = request.POST['name']
        text = request.POST['text']

        if len(name) == 0:
            return redirect(f'../publications/{number}', {
                'error': 'Пустое имя',
                'publication': publications_data[number]
            })
        if len(text) == 0:
            return redirect( f'../publications/{number}', {
                'error': 'Пустой text',
                'publication': publications_data[number]
            })
        comments=publications_data[number]['comments']
        comments.append({
            'id': len(comments),
            'name': name,
            'date': datetime.now(),
            'text': text.replace('\n', '<br />')
        })

        return redirect(f'../publications/{number}')