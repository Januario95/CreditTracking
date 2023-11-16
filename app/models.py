from django.db import models


class PaymentPlan(models.Model):
    interest_paid = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    base_amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    already_paid_interest = models.BooleanField(default=False)
    already_paid_base_amount = models.BooleanField(default=False)
    date_paid = models.DateField()

    def paid_in_a_month(self):
        return self.interest_paid + self.base_amount_paid

    def __str__(self):
        return f'{self.interest_paid}-{self.base_amount_paid}-{self.date_paid}'
    
    class Meta:
        verbose_name = 'Payment Plan'
        verbose_name_plural = 'Payment Plans'

class Warranty(models.Model):
    item = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='documents/garantias/', 
                              blank=True, null=True)
    estimated_value = models.DecimalField(
        max_digits=10, decimal_places=2
    )

    def __str__(self) -> str:
        return f'{self.item} - {self.estimated_value}'
    
    class Meta:
        ordering = ('item',)
        verbose_name = 'Warranty'
        verbose_name_plural = 'Warranties'

class Client(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    job_title = models.CharField(max_length=150, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    phone_number2 = models.CharField(max_length=12, blank=True, null=True)
    amount_requested = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )
    remaining_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )
    months_to_repay = models.IntegerField(default=1)
    starting_month = models.DateField(blank=True, null=True)
    id_document = models.FileField(upload_to='documents/IDs/', blank=True, null=True)
    contract = models.FileField(upload_to='documents/contracts/', blank=True, null=True)
    interest_rate = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )
    warranties = models.ManyToManyField(
        to=Warranty, blank=True
    )
    payments = models.ManyToManyField(
        to=PaymentPlan, blank=True
    )

    def serialize(self):
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'phone_number2': self.phone_number2,
            'amount_requested': self.amount_requested,
            'interest_rate': self.interest_rate,
            'months_to_repay': self.months_to_repay,
            'starting_month': self.starting_month,
            'job_title': self.job_title,
            'company': self.company,
        }
        return data

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.amount_requested}'
    
    class Meta:
        ordering = ('first_name',)
        unique_together = ('first_name', 'last_name', 'phone_number')
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'