# from django.db.models import Sum
# from django.db.models.functions import TruncWeek, TruncMonth
# from .models import Order

# def get_weekly_orders():
#     return Order.objects.annotate(week=TruncWeek('created_at')).values('week', 'product').annotate(total_quantity=Sum('quantity')).order_by('week', 'product')

# def get_monthly_orders():
#     return Order.objects.annotate(month=TruncMonth('created_at')).values('month', 'product').annotate(total_quantity=Sum('quantity')).order_by('month', 'product')


# services.py
from django.db.models import Sum
from django.db.models.functions import TruncWeek, TruncMonth
from .models import Order

def get_weekly_orders():
    return Order.objects.annotate(
        week=TruncWeek('created_at')
    ).values(
        'week', 'product__name__name'
    ).annotate(
        total_quantity=Sum('quantity')
    ).order_by('week', 'product__name__name')

def get_monthly_orders():
    return Order.objects.annotate(
        month=TruncMonth('created_at')
    ).values(
        'month', 'product__name__name'
    ).annotate(
        total_quantity=Sum('quantity')
    ).order_by('month', 'product__name__name')

