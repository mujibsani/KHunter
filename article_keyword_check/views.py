from django.shortcuts import render
from django import template
from . import custom_forn
from django.views.generic import ListView


from . python_code import email_extractor


register = template.Library()


def keyword_home_view(request):
    # return render(request, 'base.html', {})
    return render(request, 'article_kw_check/html/keyword_hunte.html', {})


def key_word_search(request):
    match_result = []
    non_match_results = []
    result_string = ""
    non_match_result_string = ""
    form = custom_forn.ArticleForm(request.POST)
    if form.is_valid():
        article_keywords = form.cleaned_data['give_your_keyword']
        article_content = form.cleaned_data['article']
        results = keyword_match(article_keywords, article_content)
        match_result = results.get('match')
        non_match_results = results.get('non_match')

    for non_match in non_match_results:
        non_match_result_string += non_match+', '

    for result in match_result:
        result_string += result+', '
    return render(request, 'article_kw_check/html/article.html', {'form': form, 'results': result_string, 'non_match': non_match_result_string})


def forms_python(request):
    return render(request, 'article_kw_check/html/about.html',)


def email_extractor_view(request):
    email_set = set()
    form = custom_forn.EmailForm(request.POST)
    url_input = ''
    if form.is_valid():
        url_input = form.cleaned_data['give_your_url']
        print(url_input)
        if 'http' in url_input:

            print(url_input)
        else:
            url_input = 'https://' + url_input
            print('direct : ' + url_input)
    email_set = email_extractor.web_email_crawler(url_input)

    return render(request, 'article_kw_check/html/email_extractor.html', {'form': form, 'email_list': email_set})


def keyword_match(keyword, article):
    match_result_list = []
    non_match_result = []
    keyword_array = keyword.split(',')
    for arr in keyword_array:
        if arr.lstrip() in article:
            match_result_list.append(arr.lstrip())
        else:
            non_match_result.append(arr.lstrip())
    # match_result_dict = match_result_list.append(non_match_result)
    match_result_dict = {"match":match_result_list, "non_match": non_match_result}
    return match_result_dict




def base2_check(request):
    return  render(request, 'base2.html')




