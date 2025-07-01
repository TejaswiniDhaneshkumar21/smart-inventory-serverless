from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.views import LoginView
from .models import Supplier, RawMaterial, Product, StockEntry, SpoilageAssessment
from .forms import SignUpForm, SupplierForm, RawMaterialForm, ProductForm, StockEntryForm, SpoilageAssessmentForm
from .lib.spoilage_calculator import SpoilageCalculator
from .aws_services import aws_services
from decimal import Decimal

# Authentication Views
class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

# Dashboard View
@login_required
def dashboard(request):
    low_stock = StockEntry.objects.filter(quantity__lt=10)
    high_risk = SpoilageAssessment.objects.filter(spoilage_risk__gt=70)
    supplier_count = Supplier.objects.count()
    rawmaterial_count = RawMaterial.objects.count()
    
    # Get CloudWatch alarm states (optional for Learner Lab)
    spoilage_alarm_state = None
    stock_alarm_state = None
    try:
        spoilage_alarm_state = aws_services.get_alarm_state('HighSpoilageRiskAlarm')
        stock_alarm_state = aws_services.get_alarm_state('LowStockAlarm')
    except Exception as e:
        print(f"CloudWatch alarm error: {e}")
    
    return render(request, 'dashboard_beautiful.html', {
        'low_stock': low_stock,
        'high_risk': high_risk,
        'supplier_count': supplier_count,
        'rawmaterial_count': rawmaterial_count,
        'spoilage_alarm_state': spoilage_alarm_state,
        'stock_alarm_state': stock_alarm_state
    })

# Supplier CRUD Views
@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list_beautiful.html', {'suppliers': suppliers})

@login_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'supplier_form_beautiful.html', {'form': form})

@login_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'supplier_form_beautiful.html', {'form': form})

@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'supplier_list.html', {'suppliers': Supplier.objects.all()})

# RawMaterial CRUD Views
@login_required
def rawmaterial_list(request):
    rawmaterials = RawMaterial.objects.all()
    return render(request, 'rawmaterial_list_beautiful.html', {'rawmaterials': rawmaterials})

@login_required
def rawmaterial_create(request):
    if request.method == 'POST':
        form = RawMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('rawmaterial_list')
    else:
        form = RawMaterialForm()
    return render(request, 'rawmaterial_form.html', {'form': form})

@login_required
def rawmaterial_update(request, pk):
    rawmaterial = get_object_or_404(RawMaterial, pk=pk)
    if request.method == 'POST':
        form = RawMaterialForm(request.POST, request.FILES, instance=rawmaterial)
        if form.is_valid():
            form.save()
            return redirect('rawmaterial_list')
    else:
        form = RawMaterialForm(instance=rawmaterial)
    return render(request, 'rawmaterial_form.html', {'form': form})

@login_required
def rawmaterial_delete(request, pk):
    rawmaterial = get_object_or_404(RawMaterial, pk=pk)
    if request.method == 'POST':
        rawmaterial.delete()
        return redirect('rawmaterial_list')
    return render(request, 'rawmaterial_list.html', {'rawmaterials': RawMaterial.objects.all()})

# Product CRUD Views
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_list.html', {'products': Product.objects.all()})

# StockEntry CRUD Views
@login_required
def stockentry_list(request):
    stockentries = StockEntry.objects.all()
    return render(request, 'stockentry_list.html', {'stockentries': stockentries})

@login_required
def stockentry_create(request):
    if request.method == 'POST':
        form = StockEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stockentry_list')
    else:
        form = StockEntryForm()
    return render(request, 'stockentry_form.html', {'form': form})

@login_required
def stockentry_update(request, pk):
    stockentry = get_object_or_404(StockEntry, pk=pk)
    if request.method == 'POST':
        form = StockEntryForm(request.POST, instance=stockentry)
        if form.is_valid():
            form.save()
            return redirect('stockentry_list')
    else:
        form = StockEntryForm(instance=stockentry)
    return render(request, 'stockentry_form.html', {'form': form})

@login_required
def stockentry_delete(request, pk):
    stockentry = get_object_or_404(StockEntry, pk=pk)
    if request.method == 'POST':
        stockentry.delete()
        return redirect('stockentry_list')
    return render(request, 'stockentry_list.html', {'stockentries': StockEntry.objects.all()})

# SQS Monitor View
@login_required
def sqs_monitor(request):
    try:
        messages = aws_services.receive_spoilage_alerts()
        return render(request, 'sqs_monitor.html', {'messages': messages})
    except Exception as e:
        return render(request, 'sqs_monitor.html', {'messages': [], 'error': str(e)})

# SpoilageAssessment CRUD Views
@login_required
def spoilageassessment_list(request):
    assessments = SpoilageAssessment.objects.all()
    return render(request, 'spoilageassessment_list_beautiful.html', {'assessments': assessments})

@login_required
def spoilageassessment_create(request):
    if request.method == 'POST':
        form = SpoilageAssessmentForm(request.POST)
        if form.is_valid():
            raw_material = form.cleaned_data['raw_material']
            avg_temp = form.cleaned_data.get('avg_temp', 25)
            days_stored = form.cleaned_data.get('days_stored', 0)
            calculator = SpoilageCalculator()
            spoilage_risk = calculator.calculate_spoilage_risk(
                raw_material.expiry.strftime('%Y-%m-%d'),
                avg_temp,
                days_stored,
                raw_material.supplier.reliability_score
            )
            assessment = form.save(commit=False)
            assessment.user = request.user
            assessment.spoilage_risk = spoilage_risk
            assessment.save()
            
            aws_services.save_to_dynamodb({
                'batch_id': raw_material.batch_id,
                'assessment_date': str(assessment.assessment_date),
                'avg_temp': Decimal(str(avg_temp)),
                'days_stored': Decimal(str(days_stored)),
                'spoilage_risk': Decimal(str(spoilage_risk))
            })
            
            if spoilage_risk >= 70:
                try:
                    # Send to SQS queue
                    sqs_message_id = aws_services.send_spoilage_alert({
                        'name': raw_material.name,
                        'batch_id': raw_material.batch_id,
                        'spoilage_risk': spoilage_risk,
                        'expiry': raw_material.expiry,
                        'supplier': raw_material.supplier.name
                    })
                    
                    # Send SNS notification
                    sns_message_id = aws_services.send_sns_notification(
                        f"HIGH SPOILAGE RISK ALERT\n\nMaterial: {raw_material.name}\nBatch ID: {raw_material.batch_id}\nSpoilage Risk: {spoilage_risk}%\nExpiry Date: {raw_material.expiry}\nTemperature: {avg_temp} degrees C\nDays Stored: {days_stored}\n\nImmediate action required!",
                        "Spoilage Alert - Immediate Action Required"
                    )
                    
                    if sqs_message_id or sns_message_id:
                        assessment.notification_sent = True
                        assessment.save()
                        print(f"DEBUG: SQS ID: {sqs_message_id}, SNS ID: {sns_message_id}")
                    
                    aws_services.put_metric_data('InventorySystem', 'HighRiskAlerts', 1)
                except Exception as e:
                    print(f"DEBUG: Notification error: {e}")

            return redirect('spoilageassessment_list')
    else:
        form = SpoilageAssessmentForm()
    return render(request, 'spoilageassessment_form.html', {'form': form})

@login_required
def spoilageassessment_update(request, pk):
    assessment = get_object_or_404(SpoilageAssessment, pk=pk)
    if request.method == 'POST':
        form = SpoilageAssessmentForm(request.POST, instance=assessment)
        if form.is_valid():
            form.save()
            return redirect('spoilageassessment_list')
    else:
        form = SpoilageAssessmentForm(instance=assessment)
    return render(request, 'spoilageassessment_form.html', {'form': form})

@login_required
def spoilageassessment_delete(request, pk):
    assessment = get_object_or_404(SpoilageAssessment, pk=pk)
    if request.method == 'POST':
        assessment.delete()
        return redirect('spoilageassessment_list')
    return render(request, 'spoilageassessment_list.html', {'assessments': SpoilageAssessment.objects.all()})