from django.shortcuts import render, HttpResponse


def index(request):
    # index view
    if request.is_ajax():
        all_trades = "first trade...."
        return HttpResponse(all_trades)
    return render(request, 'visitorapp/index.html')
