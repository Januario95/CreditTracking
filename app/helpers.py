import json
import pandas as pd
from datetime import timedelta, datetime

MONTHS = ['Januario', 'Fevereiro', 'Marco', 'Abril', 'Maio',
          'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro',
          'Novembro', 'Dezembro']

class PaymentPlan:
	def __init__(self, requested_value, months_to_pay, interest_rate, starting_month):
		self.requested_value = requested_value
		self.months_to_pay = months_to_pay
		self.interest_rate = interest_rate
		self.starting_month = starting_month

	def calculate(self):
		data = {
			'requested_value': self.requested_value,
			'months_to_pay': self.months_to_pay,
			'interest_rate': self.interest_rate,
			'starting_month': self.starting_month
		}
		months_to_pay = data['months_to_pay']
		starting_month = data['starting_month']
		data = []
		for month_id in range(months_to_pay):
			# print(f'Month {month_id}: {starting_month}')
			data.append({
				'requested_value': self.requested_value,
				'months_to_pay': self.months_to_pay,
				'interest_rate': self.interest_rate,
				'starting_month': self.starting_month
			})
			self.starting_month += timedelta(days=31)
		return data, starting_month


class Credit:
	def __init__(self, initial_amount, interest_rate, amount_injected_monthly):
		self.initial_amount = initial_amount
		self.interest_rate = interest_rate
		self.amount_injected_monthly = amount_injected_monthly
		self.total_monthly_amounts = self.initial_amount

	def calculate_final(self, start_month, months_to_pay, format_json=False): # , amount_injected_monthly=1000):
		# months = end_month - start_month
		# months = ((end_month - start_month) / 30).days
		# for _ in range(100):
		# 	pass
		data = []
		for month in range(months_to_pay):
			yield_ = self.calculate_return()[0]
			row = {
				'month': start_month.strftime('%d-%B-%Y'),
				'amount': self.initial_amount,
				'final': self.calculate_return()[0],
				'yield': self.calculate_return()[1],
				'my_part': round(self.calculate_return()[1] * 0.45),
				'microcredit': round(self.calculate_return()[1] * 0.55),
				'amount_injected': self.amount_injected_monthly,
				'total_monthly_amounts': self.total_monthly_amounts
			}
			data.append(row)
			self.initial_amount = yield_ + self.amount_injected_monthly
			self.total_monthly_amounts += self.amount_injected_monthly
			start_month += timedelta(days=31)
			# self.amount_injected_monthly += 10000
		# print(json.dumps(data, indent=4))
		# print(pd.DataFrame(data))
		if format_json:
			return json.dumps(data, indent=4, default=str)
		return data # , self.total_monthly_amounts

	def calculate_return(self):
		amount_per_1k = (1000 * self.interest_rate) / 100
		yield_ = (self.initial_amount / 1000) * amount_per_1k
		return round(self.initial_amount + yield_, 2), round(yield_, 2)


# credit = Credit(initial_amount=30000, interest_rate=25, amount_injected_monthly=0)
# # print(credit.calculate_return())
# print(credit.calculate_final(datetime(2023, 11, 20), datetime(2024, 6, 20), format_json=True))
# data1 = credit.calculate_final(10, 12, 2023, format_json=True)
# data2 = credit.calculate_final(0, 10, 2024, format_json=True)
# data = data1 + data2
# # df = pd.DataFrame(data)
# print(data)








	
