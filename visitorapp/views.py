from django.shortcuts import render, HttpResponse
from visitorapp.api_request import check_bank


def index(request):
    # index view
    if request.is_ajax():
        all_trades = "first trade...."
        return HttpResponse(all_trades)
    print(check_bank())
    return render(request, 'visitorapp/index.html')
