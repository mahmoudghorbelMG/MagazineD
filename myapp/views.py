from django.shortcuts import render

def tracker_bar_view(request):
    # Set the default cryptocurrency symbol to BTCUSD
    symbol = 'CRYPTOCAP:BTC'

    # Check if the user has selected a different cryptocurrency
    if 'symbol' in request.GET:
        symbol = request.GET['symbol']

    context = {
        'symbol': symbol,
    }
    return render(request, "analyses/analyses.html", context)
