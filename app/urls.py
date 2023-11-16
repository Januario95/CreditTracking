from django.urls import path

from .views import (
	simulador_de_investimento, get_dates,
    plano_de_pagamento, clients_page,
    register_clients, update_clients,
    view_clients, add_repayment,
)

app_name = 'app'

urlpatterns = [
	path('simulador-de-investimento/', simulador_de_investimento, 
      	 name='simulador_de_investimento'),
    path('', simulador_de_investimento, 
      	 name='simulador_de_investimento_homepage'),
    path('plano-de-pagamento/', plano_de_pagamento, name='plano_de_pagamento'),
	path('get_dates/<str:start_date>/<int:months_to_pay>/<int:amount>/<str:interest>/<str:monthly_amount>/',
		 get_dates),
    path('clientes/', clients_page, name='clients_page'),
    path('registar-clientes/', register_clients, name='register_clients'),
    path('actualizar-cliente/<int:client_id>/', update_clients, name='update_clients'),
    path('lista-de-clientes/', view_clients, name='view_clients'),
    path('add-repayment/<int:client_id>/<str:requested_amount>/<str:date_paid>/<str:remaining_amount>/<str:interest_paid>/<str:base_amount_paid>/<str:has_paid_base_amount>/<str:has_paid_interest_rate>/',
         add_repayment),
]