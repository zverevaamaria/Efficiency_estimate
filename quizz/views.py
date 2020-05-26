from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ProjectInfo
import requests
from bs4 import BeautifulSoup as bs
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


def index(request):
    return render(request, 'quizz/quizz.html')

def to_calculate(request):
      qualit_period = 0
      with_infliation = False
      izmerenie = 'null'
      company_type = request.POST.get('company_type')
      srok = request.POST.get('longesity')
      srok_measurment = request.POST.get('longesity_measurment')
      if (request.POST.get('longesity_measurment') == 'дней' ):
          if(request.POST.get('frequency') == 'каждый день'):
              qualit_period =  int(request.POST.get('longesity'))
              izmerenie = 'день'
      elif (request.POST.get('longesity_measurment') == 'недель' ):
          if(request.POST.get('frequency') == 'каждый день'):
               qualit_period =  int(request.POST.get('longesity'))*7
               izmerenie = 'день'
          elif(request.POST.get('frequency') == 'каждую неделю'):
                qualit_period =  int(request.POST.get('longesity'))
                izmerenie = 'неделя'
      elif (request.POST.get('longesity_measurment') == 'месяцев'):
          if(request.POST.get('frequency') == 'каждый день'):
                qualit_period =  int(request.POST.get('longesity'))*29
                izmerenie = 'день'
          elif(request.POST.get('frequency') == 'каждую неделю'):
                 qualit_period =  int(request.POST.get('longesity'))*4
                 izmerenie = 'неделя'
          elif(request.POST.get('frequency') == 'каждый месяц'):
                 qualit_period =  int(request.POST.get('longesity'))
                 izmerenie = 'месяц'
      elif (request.POST.get('longesity_measurment') == 'кварталов'):
          if(request.POST.get('frequency') == 'каждый день'):
                qualit_period =  int(request.POST.get('longesity'))*29*3
                izmerenie = 'день'
          elif(request.POST.get('frequency') == 'каждую неделю'):
                 qualit_period =  int(request.POST.get('longesity'))*4*3
                 izmerenie = 'неделя'
          elif(request.POST.get('frequency') == 'каждый месяц'):
                 qualit_period =  int(request.POST.get('longesity'))*3
                 izmerenie = 'месяц'
          elif(request.POST.get('frequency') == 'каждый квартал'):
                 qualit_period =  int(request.POST.get('longesity'))
                 izmerenie = 'квартал'
      elif (request.POST.get('longesity_measurment') == 'лет'):
          if(request.POST.get('frequency') == 'каждый день'):
                 qualit_period =  int(request.POST.get('longesity'))*365
                 izmerenie = 'день'
          elif(request.POST.get('frequency') == 'каждую неделю'):
                  qualit_period =  int(request.POST.get('longesity'))*52
                  izmerenie = 'неделя'
          elif(request.POST.get('frequency') == 'каждый месяц'):
                  qualit_period =  int(request.POST.get('longesity'))*12
                  izmerenie = 'месяц'
          elif(request.POST.get('frequency') == 'каждый квартал'):
                  qualit_period =  int(request.POST.get('longesity'))*4
                  izmerenie = 'квартал'
          elif(request.POST.get('frequency') == 'каждый год'):
                  qualit_period =  int(request.POST.get('longesity'))
                  izmerenie = 'год'
      if(request.POST.get('longesity_measurment') == 'лет'):
          if(int(request.POST.get('longesity')) >= 1):
              with_infliation = True
      elif(request.POST.get('longesity_measurment') == 'кварталов'):
          if(int(request.POST.get('longesity')) >= 4):
              with_infliation = True
      elif(request.POST.get('longesity_measurment') == 'месяцев'):
          if(int(request.POST.get('longesity')) >= 12):
              with_infliation = True
      elif(request.POST.get('longesity_measurment') == 'недель'):
          if(int(request.POST.get('longesity')) >= 52):
              with_infliation = True
      elif(request.POST.get('longesity_measurment') == 'дней'):
          if(int(request.POST.get('longesity')) >= 365):
              with_infliation = True
      discont_type = ''
      if(((request.POST.get('company_type') == 'ОАО(открытое акционерное общество)') |
       (request.POST.get('company_type') == 'ЗАО(закрытое акционерное общество)')) &
       (request.POST.get('profitability_info') == 'нет')):
          discont_type = 'WACC+R'
      elif(request.POST.get('profitability_info') == 'да'):
          discont_type = 'WACC'
      else:
          discont_type = 'CUMUL'
      print('qualit_period:',qualit_period)
      periods = []
      for i in range(1, qualit_period+1):
        periods.append(i)
      print("periods:", periods)
      loan_or_not = request.POST.get('loan_or_not')
      data = {"qualit_period": qualit_period, "periods" : periods, "izmerenie": izmerenie,
      "qualit_period": qualit_period, "company_type" : company_type, "srok" : srok,
      "srok_measurment" : srok_measurment,"discont_type" : discont_type,
      "with_infliation" : with_infliation, "loan_or_not": loan_or_not}
      return render(request, 'calculation/cumulativ.html', context = data)

def to_result(request):
     NPV = 0
     zhelaemyi_uroven = int(request.POST.get('uroven'))
     other_forms = 0
     periods = int(request.POST.get('qualit_period'))
     sposob = request.POST.get('discont_type')
     ##считывание и создание общих данных
     investments = int(request.POST.get('investments'))
     flows_d = {}
     investflows_d = {}
     infliation = get_infliation()
     year_oblig =  get_oblig()
     cash_flows_count = periods
     print('ПОТООКИИ: ', cash_flows_count)
     for i in range(1, cash_flows_count+1):
              strl = 'flow_{0}'.format(i)
              flows_d[i]=int(request.POST.get(strl))
     for i in range(1, cash_flows_count+1):
         strl = 'investflows_{0}'.format(i)
         investflows_d[i]=int(request.POST.get(strl))
               ##общие закончились
     #для кумулятивного метода
     if(sposob == 'CUMUL'):
         if(int(request.POST.get('premia')) != 0):
             premia = int(request.POST.get('premia'))
         else:
             project_type = request.POST.get('project_type')
             if project_type == 'Проект, поддерживающий производство':
                 premia = 0
             elif project_type == 'расширение производства':
                  premia = 3
             elif project_type == 'выход на новые рынки':
                  premia = 6
             elif project_type == 'смежные области бизнеса (новый продукт)':
                  premia = 9
             elif project_type == 'новые отрасли':
                  premia = 12
         r = year_oblig + infliation + premia
         NPV = calculate_npv(r, cash_flows_count, flows_d, investflows_d,investments)
         discont_potoki = prived_stoin_den_potokov(r, cash_flows_count, flows_d)
         investment = prived_stoin_den_potokov(r, cash_flows_count, investflows_d) + investments
         PI = calculate_pi(investment, discont_potoki)
     elif(sposob == 'WACC+R'):
         loan_or_not = str(request.POST.get('loan_or_not'))
         srstavka = int(request.POST.get('stav'))
         Beta = int(float(request.POST.get('beta')))
         Re = year_oblig + Beta * (srstavka - year_oblig)
         if loan_or_not == 'нет':
             r = Re
         else:
             loan_percent = float(request.POST.get('pocents_of_loan'))
             self_percent = float(request.POST.get('pocents_of_self'))
             credit_percent = float(request.POST.get('stavka_kredit'))
             r = loan_percent/100 * credit_percent + self_percent/100 * Re
         NPV = calculate_npv(r, cash_flows_count, flows_d, investflows_d,investments)
         discont_potoki = prived_stoin_den_potokov(r, cash_flows_count, flows_d)
         investment = prived_stoin_den_potokov(r, cash_flows_count, investflows_d) + investments
         PI = calculate_pi(investment, discont_potoki)
     elif(sposob == 'WACC'):
         loan_or_not = str(request.POST.get('loan_or_not'))
         doh_cap = float(int(request.POST.get('stav_doh')))
         r = 0.0
         if loan_or_not == 'нет':
             r = doh_cap
         else:
             loan_percent = float(request.POST.get('pocents_of_loan'))
             self_percent = float(request.POST.get('pocents_of_self'))
             credit_percent = float(request.POST.get('stavka_kredit'))
             r = loan_percent/100 * credit_percent + self_percent/100 * doh_cap
         NPV = calculate_npv(r, cash_flows_count, flows_d, investflows_d,investments)
         discont_potoki = prived_stoin_den_potokov(r, cash_flows_count, flows_d)
         investment = prived_stoin_den_potokov(r, cash_flows_count, investflows_d) + investments
         PI = calculate_pi(investment, discont_potoki)
     resultnpv = ''
     if NPV > 0:
         resultnpv = 'Проект эффективен!'
     if NPV < 0:
         resultnpv = 'Проект неэффективен!'
     if int(NPV) == 0:
         resultnpv = 'Проект нейтрален'
     SUMM_investments_not_dis = 0
     for i in range(1, cash_flows_count):
         SUMM_investments_not_dis = SUMM_investments_not_dis + investflows_d[i]
     NPVS_dlya_grafika = get_npv_srok(r, cash_flows_count, flows_d, investflows_d, investments)
     Spisok_spiskov = sdelat_spisok_spiskov(NPVS_dlya_grafika, cash_flows_count)
     print("СПИСОК СПИСКОООВ", Spisok_spiskov)
     SUMM_investments_not_dis = SUMM_investments_not_dis + investments
     IRR = calculate_irr(flows_d, cash_flows_count, SUMM_investments_not_dis)
     resultirr = ''
     if IRR > zhelaemyi_uroven:
         resultirr = 'Проект эффективен!'
     if IRR < zhelaemyi_uroven:
         resultirr = 'Проект неэффективен!'
     if IRR == zhelaemyi_uroven:
         resultirr = 'Проект эффективен'

     resultpi = ''
     if PI > 1:
         resultpi = 'Проект эффективен!'
     if PI < 1:
         resultpi = 'Проект неэффективен!'
     if PI == 1:
         resultpi = 'Проект нейтрален'
     #if (disk_srok_okupaemist == 0):
        #  disk_srok_okupaemist = 'Проект не окупился!'
     aproject = ProjectInfo(longesity = cash_flows_count,
     discount_type = sposob, discount_rate = r, npv = NPV, irr = IRR, pi = PI )
     aproject.save()
     chartr = int(r)
     chartNPV = int(NPV)
     PI = PI
     OKUPAEMOST = 0
     if NPV < 0 :
         OKUPAEMOST = str(OKUPAEMOST)
         OKUPAEMOST = 'Проект не окупился'
     else:
        OKUPAEMOST = get_srok_okupaemosti(r, cash_flows_count, flows_d, investflows_d, investments)
     #sps = get_NPV_by_diff_time(r, cash_flows_count, flows_d, investments)
     results = {"r": r,"NPV": NPV,
      "zhelaemyi_uroven" : zhelaemyi_uroven, "PI" : PI,
      "resultnpv":resultnpv,"resultirr":resultirr, "resultpi" : resultpi,
     "IRR" : IRR, "OKUPAEMOST" : OKUPAEMOST,
     "chartr":chartr, "chartNPV":chartNPV, "Spisok_spiskov":Spisok_spiskov}
     return render(request, 'results/result.html', context = results)

#Рассчет срока окупаемости
def get_srok_okupaemosti(r,count_flows,flows_d,investflows_d ,investments):
    NPV = - investments
    srokk = 0
    for k in range(1, count_flows+1):
            if(NPV < 0):
               NPV += (flows_d[k]/((1 + (r/100))**k) - investflows_d[k]/((1 + (r/100))**k))
               srokk +=1
    return srokk
#Данные чистой прибыли в соотвествии со временем для графика
def get_npv_srok(r,count_flows,flows_d,investflows_d ,investments):
    massive = {}
    for k in range(1, count_flows+1):
        NPV = 0
        for z in range(1, k+1):
            NPV += (flows_d[z]/((1 + (r/100))**z) - investflows_d[z]/((1 + (r/100))**z))
        massive[k] = NPV - investments
        print('ИНВЕСТИЦИИИИИИИИИ', investments)
    return massive
def sdelat_spisok_spiskov(flows_d, count_flows):
  massvspom = []
  mass = []
  if count_flows == 1:
       massvspom.append(count_flows)
       massvspom.append(flows_d[count_flows])
       mass.append(massvspom)
  else:
    for i in range(1, count_flows+1):
        mass.append([i, flows_d[i]])
        massvspom.clear()

  return mass
     #нахождение инфляции
def get_infliation():
    url = 'https://xn----ctbjnaatncev9av3a8f8b.xn--p1ai/'
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    a = soup.findAll("td")
    stroka = str(a[4])
    deletedchars = ' <>td%-!/'
    for m in deletedchars:
            stroka = stroka.replace(m, '')
    infliation = float(stroka)
    return infliation
    #нахождение ставки облигаций
def get_oblig():
    url2 = 'https://ycharts.com/indicators/30_year_mortgage_rate'
    r2 = requests.get(url2)
    soup2 = bs(r2.content, 'html.parser')
    year_oblig = str(soup2.find("div", { "id" : "pgNameVal" }).text)
    year_oblig = year_oblig[:-24]
    year_oblig = float(year_oblig)
    return year_oblig

     #Функция для подсчета npv
def calculate_npv(r, cash_flows_count, flows_d, investflows_d,investments):
    NPV = 0
    for k in range(1, cash_flows_count+1):
        NPV += (flows_d[k]/((1 + (r/100))**k) - investflows_d[k]/((1 + (r/100))**k))
    NPV = NPV - investments
    return NPV



def prived_stoin_den_potokov(r, cash_flows_count, flows_d):
    SUMM = 0
    for c in range(1, cash_flows_count):
          SUMM = SUMM + flows_d[c]/((1 + (r/100))**c)
    SUMM = SUMM + flows_d[cash_flows_count]/((1 + (r/100))**cash_flows_count)
    return SUMM

     #Функция для подсчета pi
def calculate_pi(investments, discont_potoki):
    pi = discont_potoki/investments
    return pi
    ##работа с irr!!
def calculate_irr(flows_d, cash_flows_count, summinvestments):
    #connect
    CREDENTIALS_FILE = 'creds.json'
    spreadsheet_id = '1G_uQcQbVsxNhyiGGfFxdKdj61OsBM_r59Di5DEaVoeA'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    new_flowd = []
    for i in range(1, cash_flows_count):
          new_flowd.append(str(flows_d[i]))
    new_flowd.append(flows_d[cash_flows_count])
    cashstr = str(cash_flows_count+1)
    cashstr_to_del = str(cash_flows_count+2)
    cash = cash_flows_count
    #Вводданных
    values1 = service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "A2:A" + cashstr,
             "majorDimension": "COLUMNS",
             "values": [new_flowd]},
                    ]
    }
    ).execute()
    val = [-summinvestments, summinvestments]
    values7 = service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "A1:B1",
             "majorDimension": "ROWS",
             "values": [val]},
                    ]
    }
    ).execute()

    values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='B3',
    majorDimension='ROWS').execute()
    spaces = []
    ps = ''
    spaces.append("-8")
    spaces.append("8")
    for v in range(2, cash + 1):
        spaces.append(ps)

    values3 = service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "A1:A" + cashstr_to_del,
             "majorDimension": "COLUMNS",
             "values": [spaces]},
                    ]
    }
    ).execute()
    listIRR = values['values']
    IRRl = listIRR[0]
    IRR = IRRl[0]
    intIRR = IRR.replace('%', '')
    return int(intIRR)
