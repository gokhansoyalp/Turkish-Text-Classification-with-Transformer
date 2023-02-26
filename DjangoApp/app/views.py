import string

from django.contrib import messages
from django.shortcuts import render
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tensorflow.python.keras.preprocessing.sequence import pad_sequences

from .apps import AppConfig


def index(request):
    return render(request, 'index.html')


loaded_model = AppConfig.model

def predictDesc(request, description):

    review_lines = list()
    lines = description
    for line in lines:
        tokens = word_tokenize(line)
        tokens = [w.lower() for w in tokens]
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]
        words = [word for word in stripped if word.isalpha()]
        stop_words = set(stopwords.words('turkish'))
        words = [w for w in words if not w in stop_words]
        review_lines.append(words)
        
    test_sample = review_lines
    test_samples = [test_sample]
    test_samples_tokens = AppConfig.tokenizer.texts_to_sequences(test_samples)
    test_samples_tokens_pad = pad_sequences(test_samples_tokens, maxlen=100)

    result_list = loaded_model.predict(x=test_samples_tokens_pad)

    for i in result_list:
        max = 0
        for j in range(0, 5):
            if i[j] > max:
                max = i[j]
                pos = j

    if pos == 0:
        pos = 'Din'
    elif pos == 1:
        pos = 'Çocuk/Genç'
    elif pos == 2:
        pos = 'Gazete/Dergi'
    elif pos == 3:
        pos = 'Eğitim/Bilim'
    elif pos == 4:
        pos = 'Araştırma/Tarih'
    else:
        pos = 'Not Found'

    max = max * 100
    max = round(max, 2)

    context = {'max': max, 'pos': pos}

    return context


def predictText(request):
    if request.method == 'POST':
        form = request.POST.get('textVal')
        words = form.split()

        if form == "":
            messages.info(request, 'Lütfen boş değer girmeyin!')
            return render(request, 'index.html')
        elif len(words) > 0:
            check = True

            for i in words:
                if i.isalpha() == True:
                    check = False

            if check:
                messages.info(request, 'Lütfen geçerli bir değer girin!')
                return render(request, 'index.html')
            else:
                result = predictDesc(request, form)
                return render(request, 'index.html', result)

        else:
            result = predictDesc(request, form)
            return render(request, 'index.html', result)