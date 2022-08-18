from django.shortcuts import render
from .models import Trade, Execution, Tag
from django.http import HttpResponseRedirect
from .calcs import totals
import datetime
from .forms import UploadFileForm
import csv, io
from django.core.paginator import Paginator

def fileForm(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
        else:
            print('fail')
    else:
        form = UploadFileForm()

    return form


def index(request):
    current_date = datetime.datetime.now()
    year = datetime.timedelta(days=365)
    month = datetime.timedelta(days=30)
    week = datetime.timedelta(days=7)

    all_trades_list = Trade.objects.order_by('-date').all()
    form = fileForm(request)

    all_pag = Paginator(all_trades_list, 10)
    all_page_number = request.GET.get('allPage')
    all_page_obj = all_pag.get_page(all_page_number)
    
    past_year = current_date - year
    year_string = "%d-%d-%d" % (past_year.year, past_year.month, past_year.day)
    past_month = current_date - month
    month_string = "%d-%d-%d" % (past_month.year, past_month.month, past_month.day)
    past_week = current_date - week
    week_string = "%d-%d-%d" % (past_week.year, past_week.month, past_week.day)
    today_string = "%d-%d-%d" % (current_date.year, current_date.month, current_date.day)
        
    context = {'all_trades_list': all_trades_list,
               'all_stats': totals(all_trades_list),
               'form': form,
               'all_page_obj': all_page_obj,
               'is_filtered': False,
               'year_string': year_string,
               'month_string': month_string,
               'week_string': week_string,
               'today_string': today_string,
               }
    return render(request, 'graphs/index.html', context)

def trade_detail(request, trade_id):
    context = {'trade': Trade.objects.get(pk=trade_id)}
    return render(request, 'graphs/trade_detail.html', context)

def filter(request):
    print(request.GET['symbol_filter'])

    current_date = datetime.datetime.now()
    all_trades_list = Trade.objects.order_by('-date').all()
    if (request.GET['symbol_filter'] != ""):
        print('filtered symbol')
        all_trades_list = all_trades_list.filter(symbol__startswith=request.GET['symbol_filter'])

    if (request.GET['start_filter'] != ""):
        print(request.GET['start_filter'].split('-'))
        d = request.GET['start_filter'].split('-')
        start_date = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))

        all_trades_list = all_trades_list.filter(date__gte=start_date)
    
    if (request.GET['end_filter'] != ""):
        print(request.GET['end_filter'].split('-'))
        d = request.GET['end_filter'].split('-')
        end_date = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))

        all_trades_list = all_trades_list.filter(date__lte=end_date)


    
    year = datetime.timedelta(days=365)
    month = datetime.timedelta(days=30)
    week = datetime.timedelta(days=7)

    past_year = current_date - year
    year_string = "%d-%d-%d" % (past_year.year, past_year.month, past_year.day)
    past_month = current_date - month
    month_string = "%d-%d-%d" % (past_month.year, past_month.month, past_month.day)
    past_week = current_date - week
    week_string = "%d-%d-%d" % (past_week.year, past_week.month, past_week.day)
    today_string = "%d-%d-%d" % (current_date.year, current_date.month, current_date.day)


    form = fileForm(request)

    all_pag = Paginator(all_trades_list, 10)
    all_page_number = request.GET.get('allPage')
    all_page_obj = all_pag.get_page(all_page_number)
    
    context = {'all_trades_list': all_trades_list,
               'all_stats': totals(all_trades_list),
               'form': form, 
               'all_page_obj': all_page_obj,
               'is_filtered': True,
               'year_string': year_string,
               'month_string': month_string,
               'week_string': week_string,
               'today_string': today_string,
               
               }
    return render(request, 'graphs/index.html', context)

def delete_trade(request):
    t = Trade.objects.get(pk=request.GET['id'])
    t.delete()

    return HttpResponseRedirect(request.GET['url'])
    #return render(request, 'graphs/index.html', context)

def upload_files(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/upload/')
            #rememeber to change to '/'
        else:
            print('fail')
    else:
        form = UploadFileForm()
    return render(request, 'graphs/upload.html', {'form': form})

#with each file, we create a new set of trades and executions
def handle_uploaded_file(f):
    trades = set()
    
    data = f.read().decode('UTF-8')
    io_string = io.StringIO(data)
    next(io_string)
    for r in csv.reader(io_string, delimiter='"', quotechar="|"):
        if len(r) >= 19 and r[1] != 'Date' and r[1] != '':
            print(r)
            print("$$")
            d = r[1].split('/')
            
            date = datetime.datetime(int(d[2]), int(d[0]), int(d[1]))
            description = r[3]
            symbol = r[5]
            quantity = int(r[7].replace(',',''))
            price = float(r[9][1::].replace(',',''))
            amount = round(float(r[11][1::].replace(',','')),2)
            commission = round(float(r[13][1::].replace(',','')),2)
            fees = round(float(r[15][1::].replace(',','')),2)
            typ = r[17]

            if symbol not in trades:
                trades.add(symbol)
                if quantity > 0:
                    trade = Trade(date=date, symbol=symbol, volume=quantity, pnl=amount)
                else:
                    trade = Trade(date=date, symbol=symbol, volume=0, pnl=amount)
    
            else:
                trade = Trade.objects.get(date=date, symbol=symbol)
                if quantity > 0:
                    trade.volume += quantity
                trade.pnl += amount

            #temp fix, round final values to 2 dec places
            trade.pnl = round(trade.pnl, 2)
            #trade.fee += fees
            #trade.commissions += commission
            
            trade.save()
            execution = Execution(description=description, quantity=quantity, price=price, amount=amount,
                                  commission=commission, fees=fees, payment_type=typ, trade=trade)

            execution.save()
        else:
            print(len(r))
            if len(r) > 0:
                print(r)
            print('%%%%%%%%')

            


            
