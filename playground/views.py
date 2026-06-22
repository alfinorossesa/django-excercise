from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, ExpressionWrapper, DecimalField
from django.db import transaction, connection
from store.models import Product, OrderItem, Collection, Order
from tags.models import TaggedItem

def say_hello(request):
    # products = Product.objects.filter(unit_price__lt=50)
    # products = Product.objects.filter(Q(unit_price__lt=50) & ~Q(unit_price__gt=30))
    # products = Product.objects.values('id', 'title', 'collection__title')
    # products = Product.objects.filter(id__in=OrderItem.objects.values('product_id'))

    discount = ExpressionWrapper(F('unit_price') * 0.1, output_field=DecimalField(max_digits=3, decimal_places=2))
    products = Product.objects.annotate(
        discount = discount 
    )

    # tagged_item = TaggedItem.objects.get_tags_for(Product, 1)

    # collection = Collection.objects.get(pk=11)
    # # collection.title = 'video games'
    # collection.featured_product = Product(pk=1)
    # collection.save()

    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 12
    #     item.unit_price = 99
    #     item.save()

    # query = connection.cursor()
    # query.execute('SELECT * FROM store_product')
    # query.close()
    # print (query)

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM store_product')
        data = cursor.fetchall()

    return render(request, 'hello.html', {'products': products})
