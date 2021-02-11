from django.shortcuts import render
from django.http import HttpResponse
from .web_scraping import popularity_filter_crawling

# Create your views here.
def sample(request):
    return render(request, 'cp_search/default.html')

def result(request):
    cp_name = request.POST['couple_name']
    page_num = request.POST['page']
    # pop_result = {'cp_name': cp_name }
    filter_result = popularity_filter_crawling(cp_name, int(page_num))

    result_group = {"data_table": filter_result[0],
                    "top_writers": filter_result[1],
                    "cp_name": cp_name} # 검색한 커플명
    return render(request,'cp_search/result.html', {"result_group" : result_group})
