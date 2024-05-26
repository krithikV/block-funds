# importing Flask and other modules
from flask import Flask, request, render_template, session,redirect
import smart_call
import cpf
import fsi
import price
from openai import OpenAI
client = OpenAI(api_key='sk-proj-Ro0sLGuSg11ATaHXBGZCT3BlbkFJKRJXR3NFrI7Xac5Faizh')

# Flask constructor
app = Flask(__name__) 
app.secret_key = 'F8f97cD1D84098C0fb15eae365ea96eacBAe90fc'

def chat_gpt(income,expense,networth):
	response = client.chat.completions.create(
	model="gpt-3.5-turbo-0125",
	messages=[
		{"role": "system", "content": "You are a helpful assistant designed to give a financial advice for a retired aged indivudual in 100 words generate in paragraphs"},
		{"role": "user", "content": f'My Monthly income is {income} my monthly expense is {expense} my networth is {networth}'}
	]
	)
	return response.choices[0].message.content

# A decorator used to tell the application
# which URL is associated function
def chunks(lst, n):
	a = []
	for i in range(0, len(lst), n):
		a.append(lst[i:i + n])
	return a
	

@app.route('/')
def login_render():
	return render_template("login.html")

@app.route('/prediction')
def predictions():
	return render_template("merge.html")

@app.route('/colculator',methods =["GET", "POST"])
def col():
	if request.method == "POST":
		year = request.form.get("year")
		point = fsi.calculate_overall_rating(2300,price.estimate_expense("Food",int(year),6),smart_call.get_total_asset_value(session['adr']))
		print(point,price.estimate_expense("Food",int(year),6))
		return render_template("fsi.html",fsi = point,content=chat_gpt(2300,price.estimate_expense("Food",int(year),6),smart_call.get_total_asset_value(session['adr'])))
	return render_template("fsi.html")

@app.route('/login_redirect', methods =["GET", "POST"])
def login_redirect():
	session['adr'] = request.form.get("adr")
	session['pvt'] = request.form.get("pvt")
	return redirect('/portfolio')

@app.route('/portfolio')
def portfolio():
	adr = session['adr']
	pvt = session['pvt']
	if smart_call.is_participant(adr) == False:
		smart_call.register_participant(adr,pvt) 
	pf_total = smart_call.balances(adr)
	asset_total = smart_call.get_total_asset_value(adr)

	return render_template("dashboard.html",pf_total = pf_total,asset_total = asset_total)

@app.route('/managepf',methods=['GET','POST'])
def manage_pf():
	pf_total = smart_call.balances(session['adr'])
	history = chunks(list(smart_call.get_deposit_history(session['adr'])),2)
	if request.method == "POST":
		amt = int(request.form.get('amt'))
		age = int(request.form.get('age'))
		smart_call.deposit(amt,int(cpf.calculate_pf_contribution(age,amt)),session['adr'],session['pvt'])
	return render_template("pf.html",pf_total = pf_total,len = len(history[0]),data = history[0])

@app.route('/manageassets',methods=['GET','POST'])
def manage_asset():
	if request.method == "POST":
		if request.form.get('sender'):
			smart_call.transfer_asset(request.form.get('sender'),int(request.form.get('index')),session['adr'],session['pvt'])
		if request.form.get('asset'):
			print(request.form.get('asset'))
			smart_call.add_asset(int(request.form.get('asset')),request.form.get('title'),session['adr'],session['pvt'])

	asset_total = smart_call.get_total_asset_value(session['adr'])
	if len(smart_call.get_assets(session['adr'])) > 0:
		history = chunks(list(smart_call.get_assets(session['adr'])),2)
		print(history[0])
	else:
		history = [[]]
	return render_template("asset.html",asset_total = asset_total,len = len(history[0]),data = history[0])



if __name__=='__main__':
    app.run()
