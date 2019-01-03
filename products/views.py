from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product

# Create your views here.
def home(request):
	products = Product.objects
	return render(request,'products/home.html', {"products": products})

@login_required
def create(request):
	if request.method == 'POST':
		if request.POST['title'] and request.POST['producturl'] and request.POST['body'] \
			and request.FILES['icon'] and request.FILES['image']:
			try:
				product = Product()
				product.title = request.POST['title']
				product.url = request.POST['producturl']
				if not request.POST['producturl'].lower().startswith('http'):
					product.url = "http://{0}".format(request.POST['producturl'])
				
				product.body = request.POST['body']
				product.image = request.FILES['image']
				product.icon = request.FILES['icon']
				product.hunter = request.user
				product.save()
				return redirect('/products/{0}'.format(product.id))
			except Exception as ex:
				return render(request,'products/create.html', {
					'error': "Problem creating product! => {0}".format(str(ex))
					})
		else:
			return render(request,'products/create.html',{"error": "No fields can be left blank"})
	else:
		return render(request,'products/create.html')


@login_required
def detail(request,product_id):
	product = get_object_or_404(Product,pk=product_id)
	return render(request,'products/detail.html',{"product": product})

@login_required
def upvote(request,product_id):
	if request.method == "POST":
		product = get_object_or_404(Product,pk=product_id)
		product.votes_total +=1
		product.save()
		return redirect('/products/{0}'.format(product.id))
	else:
		return render(request,'products/home.html')

