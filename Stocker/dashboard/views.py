from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.core.paginator import Paginator
from .models import Category,Product,Supplier
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

@login_required
def dashboard_home(request:HttpRequest):
  products_count = Product.objects.count()
  categories_count = Category.objects.count()
  suppliers_count = Supplier.objects.count()
  last_product = Product.objects.order_by('-id').first()
  last_three_products = Product.objects.order_by('-id')[:3]
  return render(request, "main/dash_home.html",{"products": products_count, "categories": categories_count, "suppliers": suppliers_count,"last_three_products": last_three_products})

@login_required
def dashboard_categ(request:HttpRequest):

  get_categorys = Category.objects.all()
  paginator = Paginator(get_categorys, 4)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  if request.method == "POST":
    category_name = request.POST.get("category_name")
    category_title = request.POST.get("category_title")
    category_description = request.POST.get("category_description")
    Category.objects.create(
      name = category_name,
      title = category_title,
      description = category_description
    )
    messages.success(request, "You have created a new category successfully.")
    return redirect('dashboard:dashboard_categ')

  return render(request, "main/categ_home.html", {"category":page_obj,"page_obj":page_obj})

@login_required
def dashboard_categ_delete(request:HttpRequest, catg_id:int):
  if not request.user.has_perm('dashboard.delete_category'):
    messages.error(request, "You do not have permission to delete categories.")
    return redirect('dashboard:dashboard_categ')
  get_catg = Category.objects.get(id=catg_id)
  get_catg.delete()
  messages.success(request, "You have deleted the category successfully.")

  return redirect('dashboard:dashboard_categ')

@login_required
def dashboard_categ_edit(request:HttpRequest, catg_id:int):
  if not request.user.has_perm('dashboard.change_category'):
    messages.error(request, "You do not have permission to edit categories.")
    return redirect('dashboard:dashboard_categ')
  get_category = Category.objects.get(id=catg_id)
  if request.method != "POST":
    return render(request, "main/categ_edit.html", {"category":get_category})
  if request.method == "POST":
    get_category.name = request.POST.get("category_name")
    get_category.title = request.POST.get("category_title")
    get_category.description = request.POST.get("category_description")
    get_category.save()
    messages.success(request, "You have updated the category successfully.")
    return redirect('dashboard:dashboard_categ')

@login_required
def dashboard_prod(request:HttpRequest):
  categories_get = Category.objects.all()
  products_get = Product.objects.all()
  suppliers_get = Supplier.objects.all()
  
  paginator = Paginator(products_get, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  in_stock_products = products_get.filter(quantity__gt=5).count()
  low_stock_products = products_get.filter(quantity__lte=5, quantity__gt=0).count()
  out_of_stock_products = products_get.filter(quantity=0).count()

  if request.method == "POST":
    
    name = request.POST.get("name")
    category_id = request.POST.get("category")
    supplier_ids = request.POST.getlist("suppliers")
    print(supplier_ids)
    description = request.POST.get("description")
    price = request.POST.get("price")
    quantity = request.POST.get("quantity")
    expiry_date = request.POST.get("expiry_date")
    image = request.FILES.get("image")



    product = Product.objects.create(
      name=name,
      category_id=category_id,
      description=description,
      price=price,
      quantity=quantity,
      expiry_date=expiry_date,
      image=image,
    )
    print("Product created successfully")
    print(supplier_ids)
    product.suppliers.set(supplier_ids)
    messages.success(request, "You have created a new product successfully.")
    return redirect('dashboard:dashboard_prod')

  return render(request, "main/prod_home.html", {"products":page_obj,"page_obj":page_obj,"suppliers":suppliers_get, "categories":categories_get,"in_stock_products": in_stock_products,"low_stock_products": low_stock_products,"out_of_stock_products": out_of_stock_products})

@login_required
def dashboard_prod_delete(request:HttpRequest, product_id:int):
  if not request.user.has_perm('dashboard.delete_product'):
    messages.error(request, "You do not have permission to delete products.")
    return redirect('dashboard:dashboard_prod')
  get_product = Product.objects.get(id=product_id)
  get_product.delete()
  messages.success(request, "You have deleted the product successfully.")
  return redirect('dashboard:dashboard_prod')

@login_required
def dashboard_prod_view(request:HttpRequest, product_id:int):
  get_product = Product.objects.get(id=product_id)
  return render(request, "main/prod_view.html", {"product":get_product})

@login_required
def dashboard_prod_edit(request:HttpRequest, product_id:int):
  if not request.user.has_perm('dashboard.change_product'):
    messages.error(request, "You do not have permission to edit products.")
    return redirect('dashboard:dashboard_prod')
  get_product = Product.objects.get(id=product_id)
  categories_get = Category.objects.all()
  suppliers_get = Supplier.objects.all()
  product_supplier_ids = get_product.suppliers.values_list('id', flat=True)

  if request.method != "POST":
    return render(request, "main/prod_edit.html", {"product":get_product, "categories":categories_get, "suppliers":suppliers_get, "product_supplier_ids": product_supplier_ids})

  if request.method == "POST":
    get_product.name = request.POST.get("name")
    get_product.category_id = request.POST.get("category")
    get_product.description = request.POST.get("description")
    get_product.price = request.POST.get("price")
    get_product.quantity = request.POST.get("quantity")
    get_product.expiry_date = request.POST.get("expiry_date")
    image = request.FILES.get("image")
    if image:
      get_product.image = image
    get_product.save()

    supplier_ids = request.POST.getlist("suppliers")
    get_product.suppliers.set(supplier_ids)

    if 0 < get_product.quantity <= 5:
      send_mail(
          'Alert: Low Product Quantity',
          f'The quantity of the product "{get_product.name}" has reached {get_product.quantity}. Please reorder soon.',
          settings.DEFAULT_FROM_EMAIL,
          ['xp.mo91@gmail.com'],
          fail_silently=False,
      )
    elif get_product.quantity == 0:
        send_mail(
            'Alert: Product Out of Stock',
            f'The product "{get_product.name}" is out of stock. Please restock it as soon as possible.',
            settings.DEFAULT_FROM_EMAIL,
            ['xp.mo91@gmail.com'],
            fail_silently=False,
        )


    messages.success(request, "You have updated the product successfully.")
    return redirect('dashboard:dashboard_prod')

@login_required
def dashboard_suppliers(request:HttpRequest):
  suppliers_get = Supplier.objects.all()
  total_suppliers = suppliers_get.count()
  total_products = Product.objects.count()
  paginator = Paginator(suppliers_get, 5)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  if request.method == "POST":
      name = request.POST.get("supplierName")
      email = request.POST.get("supplierEmail")
      phone = request.POST.get("supplierPhone")
      website = request.POST.get("supplierWebsite")
      logo = request.FILES.get("supplierLogo")
      username = request.POST.get("supplierusername")
      password = request.POST.get("supplierPassword")
      confirm_password = request.POST.get("supplierConfirmPassword")

      if password != confirm_password:
          return render(request, "main/supp_home.html", {
              "error": "Passwords do not match!"
          })

      user = User.objects.create_user(username=username, password=password, email=email)
      Supplier.objects.create(
          user=user,
          name=name,
          logo=logo,
          website=website,
          phone_number=phone
      )
      return redirect("dashboard:dashboard_supplier")


  return render(request, "main/supp_home.html", {"suppliers": suppliers_get,"total_suppliers": total_suppliers, "total_products": total_products, "page_obj": page_obj})

@login_required
def dashboard_stock(request: HttpRequest):
  products = Product.objects.select_related('category').prefetch_related('suppliers').all()
  paginator = Paginator(products, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  if request.method == "POST":
    product_id = request.POST.get("product_id")
    quantity = request.POST.get("quantity")
    if product_id and quantity:
      product = Product.objects.get(id=product_id)
      product.quantity = int(quantity)
      product.save()
      messages.success(request, "You have updated the product quantity successfully.")
    if 0 < product.quantity <= 5:
      send_mail(
          'Alert: Low Product Quantity',
          f'The quantity of the product "{product.name}" has reached {product.quantity}. Please reorder soon.',
          settings.DEFAULT_FROM_EMAIL,
          ['xp.mo91@gmail.com'],
          fail_silently=False,
      )
    elif product.quantity == 0:
        send_mail(
            'Alert: Product Out of Stock',
            f'The product "{product.name}" is out of stock. Please restock it as soon as possible.',
            settings.DEFAULT_FROM_EMAIL,
            ['xp.mo91@gmail.com'],
            fail_silently=False,
        )

    return redirect('dashboard:dashboard_stock')

  return render(request, "main/stock_home.html", {"page_obj": page_obj})

@login_required
def dashboard_reports(request:HttpRequest):
  return render(request, "main/reports_home.html")

@login_required
def dashboard_supplier_edit(request:HttpRequest, supplier_id:int):
  if not request.user.has_perm('dashboard.change_supplier'):
    messages.error(request, "You do not have permission to edit suppliers.")
    return redirect('dashboard:dashboard_supplier')
  get_supplier = Supplier.objects.get(id=supplier_id)

  if request.method != "POST":
    return render(request, "main/supp_edit.html", {"supplier":get_supplier})

  if request.method == "POST":
    get_supplier.name = request.POST.get("supplierName")
    get_supplier.phone_number = request.POST.get("supplierPhone")
    get_supplier.website = request.POST.get("supplierWebsite")
    logo = request.FILES.get("supplierLogo")
    if logo:
      get_supplier.logo = logo
    get_supplier.save()
    user = get_supplier.user
    user.username = request.POST.get("supplierusername")
    user.email = request.POST.get("supplierEmail")
    user.set_password(request.POST.get("supplierPassword"))
    user.save()
    messages.success(request, "You have updated the supplier successfully.")
    return redirect('dashboard:dashboard_supplier')
  
@login_required
def dashboard_supplier_delete(request:HttpRequest, supplier_id:int):
  if not request.user.has_perm('dashboard.delete_supplier'):
    messages.error(request, "You do not have permission to delete suppliers.")
    return redirect('dashboard:dashboard_supplier')
  get_supplier = Supplier.objects.get(id=supplier_id)
  get_supplier.delete()
  messages.success(request, "You have deleted the supplier successfully.")
  return redirect('dashboard:dashboard_supplier')

@login_required
def dashboard_supplier_view(request, supplier_id):
  supplier = Supplier.objects.filter(id=supplier_id).first()
  products_list = supplier.product_set.all() if supplier else []
  
  paginator = Paginator(products_list, 5)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  return render(request, "main/supp_view.html", {
      "supplier": supplier,
      "page_obj": page_obj
  })

@login_required
def dashboard_reports(request):
  products = Product.objects.all()
  suppliers = Supplier.objects.all()
  categories = Category.objects.all()

  today = now().date()
  expiring_soon_date = today + timedelta(days=30)

  total_products = products.count()
  total_suppliers = suppliers.count()

  in_stock_count = products.filter(quantity__gt=5).count()
  low_stock_count = products.filter(quantity__gt=0, quantity__lte=5).count()
  out_of_stock_count = products.filter(quantity=0).count()

  expiring_soon_products = products.filter(expiry_date__gte=today, expiry_date__lte=expiring_soon_date)
  expired_products = products.filter(expiry_date__lt=today)

  context = {
      "total_products": total_products,
      "total_suppliers": total_suppliers,
      "in_stock_count": in_stock_count,
      "low_stock_count": low_stock_count,
      "out_of_stock_count": out_of_stock_count,
      "expiring_soon_products": expiring_soon_products,
      "expired_products": expired_products,
      "categories": categories,
      "suppliers": suppliers,
  }

  return render(request, "main/reports_home.html", context)


@login_required
def search_results(request):

  q = request.GET.get('q', '').strip()
  products = []
  categories = []
  suppliers = []

  if q:
      products = Product.objects.filter(name__icontains=q)
      categories = Category.objects.filter(name__icontains=q)
      suppliers = Supplier.objects.filter(name__icontains=q)

  context = {
      'query': q,
      'products': products,
      'categories': categories,
      'suppliers': suppliers,
  }
  return render(request, 'main/search_results.html', context)
