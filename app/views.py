from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import (
	Client, PaymentPlan as PaymentPlanModel,
)
from .helpers import (
    Credit, PaymentPlan, 
)
from .forms import (
	InterestSimulatorForm, ClientForm,
	ClientModelForm,
)

import json
from datetime import datetime

def view_clients(request):
	clients = Client.objects.all()
	print(clients)

	return render(request,
			     'view_clients.html',
				 {'clients': clients})

def clients_page(request):
	return render(request,
			      'clients_page.html')

def register_clients(request):
	if request.method == 'POST':
		form = ClientModelForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			inner_data = form.cleaned_data
			print(inner_data)
			first_name = inner_data.get('first_name')
			last_name = inner_data.get('last_name')
			phone_number = inner_data.get('phone_number')
			client = Client.objects.filter(
				first_name=first_name,
				last_name=last_name,
				phone_number=phone_number
			)
			if client.exists():
				client = client.first()
			else:
				client = None

			return redirect(f'/actualizar-cliente/{client.pk}/')
		else:
			print(form.errors)
	else:
		form = ClientModelForm()

	return render(request,
			      'register_clients.html',
				  {'form': form})


def add_repayment(request, client_id, requested_amount, date_paid, remaining_amount, interest_paid,
                  base_amount_paid, has_paid_base_amount, has_paid_interest_rate):
	try:
		client = Client.objects.get(id=int(client_id))
		requested_amount = float(requested_amount)
		date_paid = datetime.strptime(date_paid, '%Y-%m-%d')
		remaining_amount = float(remaining_amount)
		interest_paid = float(interest_paid)
		base_amount_paid = float(base_amount_paid)
		if has_paid_base_amount == 'checked':
			has_paid_base_amount = True
		elif has_paid_base_amount == 'not checked':
			has_paid_base_amount = False
		
		if has_paid_interest_rate == 'checked':
			has_paid_interest_rate = True
		elif has_paid_interest_rate == 'not checked':
			has_paid_interest_rate = False

		payment = PaymentPlanModel.objects.create(
			interest_paid=interest_paid,
			base_amount_paid=base_amount_paid,
			already_paid_interest=has_paid_interest_rate,
			already_paid_base_amount=has_paid_base_amount,
			date_paid=date_paid
		)
		payment.save()
		client.payments.add(payment)
		client.save()
		payment_created = True
	except Client.DoesNotExist:
		payment_created = False

	return JsonResponse({
		'payment_created': payment_created,
		'requested_amount': requested_amount,
		'date_paid': date_paid,
		'remaining_amount': remaining_amount,
		'interest_paid': interest_paid,
		'base_amount_paid': base_amount_paid,
		'has_paid_base_amount': has_paid_base_amount,
		'has_paid_interest_rate': has_paid_interest_rate
	})


def update_clients(request, client_id):
	try:
		client = Client.objects.get(id=client_id)
		data = []
		payments_ = []
		starting_month = None
		requested_amount = 0
		payments = client.payments.all()

		requested_amount = client.amount_requested
		payments = client.payments.all()
		payments = payments.order_by('id')
		remaining_amount = client.amount_requested
		for payment in payments:
			remaining_amount = requested_amount - payment.paid_in_a_month()
			client.remaining_amount = remaining_amount
			# print(f'''requested = {client.amount_requested}\t remaining = {client.remaining_amount}''')
			requested_amount = client.remaining_amount
			row = {
				'date_paid': payment.date_paid,
				'remaining_amount': remaining_amount,
				'interest_paid': payment.interest_paid,
				'base_amount_paid': payment.base_amount_paid,
				'already_paid_interest': payment.already_paid_interest,
				'already_paid_base_amount': payment.already_paid_base_amount
			}
			payments_.append(row)
			# print(row)
		# print(json.dumps(payments_, indent=4, default=str))
		
		if request.method == 'POST':
			form = ClientForm(request.POST) # , request.FILES)
			if form.is_valid():
				# form.save()
				inner_data = form.cleaned_data
				first_name = inner_data.get('first_name')
				last_name = inner_data.get('last_name')
				email = inner_data.get('email')
				job_title = inner_data.get('job_title')
				company = inner_data.get('company')
				phone_number = inner_data.get('phone_number')
				phone_number2 = inner_data.get('phone_number2')
				amount_requested = inner_data.get('amount_requested')
				interest_rate = inner_data.get('interest_rate')
				months_to_repay = inner_data.get('months_to_repay')
				starting_month = inner_data.get('starting_month')
				# print(inner_data)
				client = Client.objects.filter(
					first_name=first_name, last_name=last_name,
					phone_number=phone_number
				)
				if client.exists():
					client = client.first()
					client.first_name = first_name
					client.last_name = last_name
					client.email = email
					client.job_title = job_title
					client.company = company
					client.phone_number = phone_number
					client.phone_number2 = phone_number2
					client.amount_requested = amount_requested
					client.interest_rate = interest_rate
					client.months_to_repay = months_to_repay
					client.starting_month = starting_month
					client.save()
					
					requested_amount = client.amount_requested
					payments = client.payments.all()
					payments = payments.order_by('id')
					for payment in payments:
						remaining_amount = requested_amount - payment.paid_in_a_month()
						client.remaining_amount = remaining_amount
						# print(f'''requested = {client.amount_requested}\t remaining = {client.remaining_amount}''')
						requested_amount = client.remaining_amount
						row = {
							'date': payment.date_paid,
							'remaining_amount': remaining_amount,
							'interest_paid': payment.interest_paid,
							'base_amount_paid': payment.base_amount_paid,
							'already_paid_interest': payment.already_paid_interest,
							'already_paid_base_amount': payment.already_paid_base_amount
						}
						payments_.append(row)
					print(json.dumps(payments_, indent=4, default=str))

					payment_plan = PaymentPlan(
						requested_value=client.amount_requested,
						months_to_pay=client.months_to_repay,
						interest_rate=client.interest_rate,
						starting_month=client.starting_month
					)
					data, starting_month = payment_plan.calculate()
					# print(json.dumps(data, indent=4, default=str))
				else:
					print('Client does not exist!')
			else:
				print(form.errors)
		else:
			form = ClientForm(initial=client.serialize())
		return render(request,
					  'update_clients.html',
					  {'form': form, 'client': client, 'payments': payments_,
					   'data': data, 'starting_month': starting_month,
					   'requested_amount': requested_amount,
					   'remaining_amount': remaining_amount})
	except Client.DoesNotExist:
		client = None

	return render(request,
			      'client_does_not_exist.html')

def plano_de_pagamento(request):
	data = []
	starting_month = ''
	number_of_months = 0
	interest_rate = ''
	if request.method == 'POST':
		form = InterestSimulatorForm(request.POST)
		if form.is_valid():
			inner_data = form.cleaned_data
			# print(inner_data)
			amount = inner_data.get('amount')
			number_of_months = inner_data.get('number_of_months')
			interest_rate = inner_data.get('interest_rate')
			starting_month = inner_data.get('starting_month')
			payment_plan = PaymentPlan(requested_value=amount, months_to_pay=number_of_months,
							  		   interest_rate=interest_rate, starting_month=starting_month)
			data, starting_month = payment_plan.calculate()
			# print(json.dumps(data, indent=4, default=str))
			row = {

			}
			for _ in range(number_of_months):
				row = {

				}
		else:
			print(form.errors)
	else:
		form = InterestSimulatorForm()
		
	return render(request,
			   	  'plano_de_pagamento.html',
				  {'form': form, 'number_of_months': list(range(number_of_months)),
	   			   'interest_rate': interest_rate, 'data': data,
				   'starting_month': starting_month})

def simulador_de_investimento(request):
	return render(request,
				  'simulador_de_investimento.html')


def get_dates(request, start_date, months_to_pay,
			  amount, interest, monthly_amount):
	start_date = datetime.strptime(start_date, '%Y-%m')
	months_to_pay = int(months_to_pay)
	amount = float(amount)
	interest = float(interest)
	monthly_amount = float(monthly_amount)
	total_monthly_amounts1 = 0
	total_monthly_amounts2 = 0
	total_monthly_amounts = 0
	message = False
	message_text = ''
	data = []

	credit = Credit(amount, interest, monthly_amount)
	data = credit.calculate_final(start_date, months_to_pay)
	
	# if end_date < start_date:
	# 	message = True
	# 	message_text = 'Start date must be before the end date'
	# else:
	# 	credit = Credit(amount, interest, monthly_amount)
	# 	data = credit.calculate_final(start_date, end_date)

		# if end_date.year - start_date.year > 1:
		# 	message = True
		# 	message_text = 'Can only calculate maximum for two years.'
		# elif end_date.year > start_date.year:
		# 	first_year_months = 12 - start_date.month
		# 	data1 = credit.calculate_final(start_date, end_date)
		# 	# data2 = credit.calculate_final(0, end_date, end_date)
		# 	data = data1 # + data2
		# 	# print(data)
		# else:
		# 	start_month = start_date.month
		# 	end_month = end_date.month
		# 	data = credit.calculate_final(start_date, start_date)

	total_monthly_amounts = credit.total_monthly_amounts

	return JsonResponse({
		'message': message,
		'message_text': message_text,
		'data': data,
		'total_monthly_amounts': total_monthly_amounts
	})




