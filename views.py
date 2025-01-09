from django.shortcuts import render,redirect
from .models import *

# Create your views here.
from .PayTm import Checksum

MERCHANT_KEY = 'opoTNnYFHTLcPtrb'

def home(request):
	return render(request,"home.html")




def about(request):
	return render(request,"about.html")


def products(request):
	all_prdt = product.objects.all()
	return render (request,"products.html",{'data':all_prdt})
	

def cart(request):
	try:

		carts = request.session['cart_info'] # session er value carts e tola hocchhe
		print("=="*30)
		print(carts)
		request.session['cart_disp_count'] = True # cart_info te jodi value thake tahole true 
		gross_value=0
		
		for i in carts:
			for k,v in i.items():
				gross_value+=int(v[-1])*int(v[-2])
		
		request.session['total_amount']=gross_value
		return render(request,"cart.html",{'allCart':carts}) # value thakle sob nie new html page e jbe
	except:
		request.session['cart_disp_count'] = False # cart_info te jodi value na thake tahole false
		return render(request,"cart.html")
	#return render(request,"cart.html")



def single_all(request):
	btn = request.POST['test']
	qntity=request.POST['qntity']
	uslug=request.POST['slug']
	print(qntity)
	print(uslug)
	item_obj=product.objects.get(slug=uslug)
	if(btn == "buy"):
		
		print("work for buy")
		total = int(qntity)*int(item_obj.prdtprice)
		request.session['total_amount'] = total
		return  redirect('/checkout')
		
	else:
		
		# print(btn)
		
		print(item_obj.prdt_imag_set.all()[0].img.url) #models e j image ache seta likhte hbe
		single_item={uslug:[item_obj.prdt_imag_set.all()[0].img.url,item_obj.prdtname,item_obj.prdtprice,qntity]}
		print("--"*30)
		print(single_item)

		try:
			v=request.session['cart_info'] # session kora mane server e value tola mane website jotokhn open thakche sekhane value add thakche
			# cart_info er moddhe kono value nei tai error asbe bole try except dewa
			f=0
			#print("--"*10)
			#print(v)
			for x in v:
				if uslug in x:
					#print("--"*300)
					#print(x[uslug])
					h=int(x[uslug][-1]) # -1 mane quantity ta uslug er last value take int e convert kora hocchee
					h+=int(qntity)

					x[uslug][-1]=str(h)
					f=1

			if f==0:
				v.append(single_item) # jodi aki item na hyy tahole notun kore add hbe

			request.session['cart_info']=v
		except Exception as e:
			request.session['cart_info']=[single_item] #session e single_item k list hisebe pathano hocche tar mane puro jinista 0 index e uthche

		print('details                     ',request.session['cart_info']) # show details e click korle sob value session e utche mane console e dekhabe

		request.session['cart_count']=len(request.session['cart_info'])
		return redirect('/cart')


def checkout_all(request):
	if request.method=="POST":
		print("-------------------------test--------------------")
		items_json = request.POST.get('itemsJson', '')
		name = request.POST.get('name', '')
		amount = request.session['total_amount']
		email = request.POST.get('email', '')
		address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
		city = request.POST.get('city', '')
		state = request.POST.get('state', '')
		zip_code = request.POST.get('zip_code', '')
		phone = request.POST.get('phone', '')
		order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
		order.save()
		update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
		update.save()
		thank = True
		id = order.order_id
		#return render(request, 'checkout.html', {'thank':thank, 'id': id})
		# Request paytm to transfer the amount to your account after payment by user
		param_dict = {

			'MID': 'WkBDyB96157441963982',
			'ORDER_ID': str(order.order_id),
			'TXN_AMOUNT': str(amount),
			'CUST_ID': email,
			'INDUSTRY_TYPE_ID': 'Retail',
			'WEBSITE': 'WEBSTAGING',
			'CHANNEL_ID': 'WEB',
			'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest', # handlerequest er por oneksomoy / dile run kore na abar / dile run kore
		}
		param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
		return render(request, 'paytm1.html', {'param_dict': param_dict})

	return render(request, 'checkout.html')




def logout(request):
	del request.session['user_info']
	return redirect('/login')



def singleproductdetails(request,prdtid):
	prdt_obj=product.objects.get(slug=prdtid)
	return render(request,"singleproductdetails.html",{"item_data":prdt_obj})



def removed(request,remv):
	i=0
	sess=request.session['cart_info']
	for x in sess:
		if remv in x:
			break
		else:
			i+=1
	sess.pop(i)
	print("---"*30)
	# print(sess)
	request.session['cart_info'] = sess
	request.session['cart_count'] = len(request.session['cart_info'])
	return redirect('/cart')


def login(request):
	try:
		if request.session['error_message']==2:
			msg1="please enter correct details"
			del request.session['error_message']
	except:
		msg1=""
	return render(request,"login.html",{'msg1':msg1})


def signup(request):
	try:
		if request.session['error_message']==1:
			msg1="please create account first"
			del request.session['error_message']
	except:
		msg1=""
	return render(request,"signup.html",{'msg1':msg1})

def contact(request):
	return render(request,"contact.html")


def signup_val(request):
	signup_na=request.POST['na'];
	signup_ui=request.POST['ui'];
	signup_pw=request.POST['pw'];
	signup_em=request.POST['em'];
	signup_no=request.POST['no'];




	print(signup_na)
	print(signup_ui)
	print(signup_pw)
	print(signup_em)
	print(signup_no)



	s1=signup1()
	s1.name=signup_na
	s1.userid=signup_ui
	s1.password=signup_pw
	s1.email=signup_em
	s1.phoneno=signup_no

	s1.save()


	return redirect('/login')


def login_val(request):
	if request.method=='POST':
		login_ui=request.POST['ui'];
		login_pw=request.POST['pw'];

	print(login_ui)
	print(login_pw)
	
	try:
		signup_ob=signup1.objects.get(userid=login_ui)
		print("---------------------------",signup_ob)
		if((login_ui==signup_ob.userid) and (login_pw==signup_ob.password)):
			print("-----------------------hello----------------------")
			arr=[signup_ob.name,signup_ob.userid,signup_ob.password,signup_ob.email,signup_ob.phoneno]
			request.session['user_info']=arr
			return redirect('/')
		else:
			request.session['error_message']=2
			return redirect('/login')
	except Exception as e:
		request.session['error_message']=1
		return redirect('/signup')






