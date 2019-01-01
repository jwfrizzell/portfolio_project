from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product

# Create your views here.
def home(request):
	return render(request,'products/home.html')

@login_required
def create(request):
	if request.method == 'POST':
		if request.POST['title'] and request.POST['producturl'] and request.POST['body'] \
			and request.FILES['icon'] and request.FILES['image']:
			try:
				product = Product()
				product.title = request.POST['title']
				product.url = request.POST['producturl']
				if not request.POST['producturl'].startswith('http'):
					product.url = "http://{0}".format(request.POST['producturl'])
				
				product.body = request.POST['body']
				product.image = request.FILES['image']
				product.icon = request.FILES['icon']
				product.hunter = request.user
				product.save()
				return render(request,'products/create.html')
			except Exception as ex:
				return render(request,'products/create.html', {
					'error': "Problem creating product! => {0}".format(str(ex))
					})
		else:
			return render(request,'products/create.html',{"error": "No fields can be left blank"})
	else:
		return render(request,'products/create.html')