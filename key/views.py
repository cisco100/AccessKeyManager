from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from key.models import AccessKey
from key.utils import gen_key
from django.contrib import messages

User = get_user_model()

 
 
@login_required
def home(request):
    return render(request,"keys/index.html",{})



@login_required
def request_new_key(request):
    if request.method == 'POST':
        user_keys = AccessKey.objects.filter(user=request.user)
        
        if not user_keys.exists():
            # User has no keys, create a new one
            expiry_date = timezone.now() + timezone.timedelta(days=365)
            new_key = AccessKey.objects.create(
                user=request.user,
                key=gen_key(),
                expiry_date=expiry_date,
                status='active'
            )
            messages.success(request, f'New key generated: {new_key.key}')
        else:
            active_key = user_keys.filter(status='active').first()
            if active_key:
                messages.error(request, 'You already have an active key.')
            else:
                # User has keys, but none are active, create a new one
                expiry_date = timezone.now() + timezone.timedelta(days=365)
                new_key = AccessKey.objects.create(
                    user=request.user,
                    key=gen_key(),
                    expiry_date=expiry_date,
                    status='active'
                )
                messages.success(request, f'New key generated: {new_key.key}')
    
    return redirect('dashboard')


@login_required
def revoke_key(request, key_id):
    if request.user.is_superuser:
        if request.method == 'POST':
            key = get_object_or_404(AccessKey, id=key_id)
            key.status = "revoked"
            key.save()
            messages.success(request, f'Key {key.key} has been revoked.')
        return redirect('dashboard')

@login_required
def dashboard(request):
    if request.user.is_superuser==True:
        keys = AccessKey.objects.all()
        template_name = "keys/admin.html"
        context={'keys':keys}
    else:
        keys = AccessKey.objects.filter(user=request.user).all()
        template_name = "keys/user.html"
        context={'keys':keys}
    return render(request, template_name, context)

@login_required
def verify_key(request):
    if request.user.is_superuser:
        email = request.GET.get('email')
        if not email:
            return JsonResponse({'error': 'Email parameter is required'}, status=400)

        try:
            user = User.objects.get(email=email)
            active_key = AccessKey.objects.filter(user=user, status='active').first()
            if active_key:
                return JsonResponse({
                    'key': active_key.key,
                    'status': active_key.status,
                    'procurement_date': active_key.procurement_date,
                    'expiry_date': active_key.expiry_date,
                    'status':"200"
                }, status=200)
            return JsonResponse({'error': '404,No active key found'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'error': '404,User not found'}, status=404)
 