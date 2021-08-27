import requests
from bs4 import BeautifulSoup
import pandas as pd


header = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
}

links = ('https://www.melhorcambio.com/ipca',
          'https://www.melhorcambio.com/cdi',
          'https://www.melhorcambio.com/taxa-selic',
          'https://www.melhorcambio.com/igpm',)

#IPCA | CDI | SELIC | IGPM
def fixed_rate(header, links, rate):

	response_object = requests.get(links[rate], headers=header)
	search_soup = BeautifulSoup(response_object.text, features='html.parser')
	read_elems = search_soup.find_all('td', 'tdvalor')

	list_rate = []
	for i in read_elems:
		conv = i.text.replace(',', '.').replace(' %', '')
		list_rate.append(round(float(conv),2))
		
	return list_rate


#---------------------------------------------------------
print('-----------------------------')
print('| FIXED INCOME CALCULATIONS |')
print('-----------------------------\n')

val = float(input('VALUE CALC: '))
rate_cdi = float(input('VALUE RATE CDI: '))
mouth = int(input('VALUE MOUTH: '))


rate_all = []
for i in range(0, 4):
  rate_all.append(fixed_rate(header, links, i))


#POUPANÇA
response_object = requests.get('https://www.idinheiro.com.br/calculadoras/calculadora-rendimento-da-poupanca/', headers=header)
read_elems = BeautifulSoup(response_object.text, features='html.parser').find_all('input','input__sem_cifrao')
text = str(read_elems[0]).split(' ')
poup = 0
for i in text:
  if i[:5] == 'value':
    poup = round(float(i[7:-3].replace(',','.')),2)


rate_rate = [ 
              ['IPCA', rate_all[0][2], '(ano)'],
              ['CDI A', (rate_all[1][1]) * 12, '(mes)'],
              ['CDI M', rate_all[1][1], '(mes)'],
              ['CDI D', (rate_all[1][1])/30, '(dia)'],
              ['SELIC', rate_all[2][3], '(ano)'],
              ['IGPM', rate_all[3][2], '(ano)'],
              ['POUPANÇA A', poup, '(ano)'],
              ['POUPANÇA M', poup/12, '(mes)'],
              ['POUPANÇA D', (poup/12)/30, '(dia)']
            ]

rate_data = pd.DataFrame(data=rate_rate, columns=['TAXA','VALOR','PRAZO'])

#----------------------------------------------
response_object = requests.get('https://www.poupardinheiro.com.br/financas/734-o-que-e-cdi-valor-hoje', headers=header)
search_soup = BeautifulSoup(response_object.text, features='html.parser')
read_title = search_soup.find_all('div','title')
read_value = search_soup.find_all('div','valor')
read_variable = search_soup.find_all('div','variacao')

read_all = []
for i in range(len(read_title)):
  test_value = read_value[i].text.replace('\n','')
  read_all.append([read_title[i].text, test_value[:test_value.find(',')+3], read_variable[i].text])

result_coins = []
for a in read_all[1:5]:
  result_coins.append(a)
read_all[0][1] = read_all[0][1][:read_all[0][1].find('pts')+3]
result_coins.append(read_all[0])
for a in read_all[5:13]:
  result_coins.append(a)

stock_exchange = pd.DataFrame(data=result_coins,columns=['ACTIONS','VALUES','RANGE'])
#-----------------------------------------------

cdi_year = ((rate_all[1][1]) * 12)
cdi_mouth = ((rate_all[1][1]) * mouth)

#rendimento CDI 100% EM X MESES
rend_cdi_oh = (cdi_mouth * val) / 100
result1 = val + rend_cdi_oh

#rendimento CDI acima de 100% EM X MESES
rend_cdi_x = (cdi_mouth * (rate_cdi / 100) * val) / 100
result2 = val + rend_cdi_x

#rendimento CDI 100% EM 12 MESES
rend_cdi_oh = (cdi_year * val) / 100
result3 = val + rend_cdi_oh

#rendimento CDI acima de 100% EM 12 MESES
rend_cdi_x = (cdi_year * (rate_cdi / 100) * val) / 100
result4 = val + rend_cdi_x

print('\n-------------------------------------------------')
print('Value applied in {} mounths is R$ {}'.format(mouth, result2))
print('The amount invested in one year at 100% of the CDI would be R$ {}'.format(result3))
print('--------------------------------------------------\n\n')

print('===============================\n|       TAXAS RENDA FIXA      |\n===============================')
print(rate_data)
print('-------------------------------\n\n\n')

print('==========================================\n|              TRADING FLOOR             |\n==========================================')
print(stock_exchange)
print('-------------------------------------------')
print('By: https://www.poupardinheiro.com.br/\n\n\n')







'''
app = Flask('app')

@app.route('/')
def hello_world():
  return 'Hello, World!'

app.run(host='0.0.0.0', port=8080)'''
