from django import forms
from .models import Ticket, Coupon

class TicketForm(forms.ModelForm):
    coupon_code = forms.CharField(
        max_length=50, 
        required=False, 
        label="Código do cupom", 
        widget=forms.TextInput(attrs={'placeholder': 'Insira o código do cupom'})
    )

    class Meta:
        model = Ticket
        fields = ['ticketType', 'coupon_code']  
        labels = {
            'ticketType': 'Tipo de ingresso',
        }
        widgets = {
            'ticketType': forms.Select(choices=Ticket.TICKET_TYPES),
        }

class CouponForm(forms.ModelForm):
    code=forms.CharField(max_length=30, required=True, label="Código")
    discount=forms.DecimalField(max_digits=5, decimal_places=2) 
    active=forms.BooleanField(required=False, label="Ativo")
    validFrom=forms.DateTimeField(required=True, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    validUntil=forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model=Coupon
        fields=['code','discount','active','validFrom','validUntil']

    def clean_coupon_code(self):
        code = self.cleaned_data.get('coupon_code')
        if code:
            try:
                coupon = Coupon.objects.get(code=code, active=True)
                if not coupon.is_valid():
                    raise forms.ValidationError("Cupom inválido ou expirado.")
            except Coupon.DoesNotExist:
                raise forms.ValidationError("Cupom não encontrado.")
        return code