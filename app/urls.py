from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from app import views
from .forms import LoginForm, MyPasswordChangeForm
from .views import CustomerRegistrationView
from .forms import MyPasswordResetForm, MySetPasswordForm
from .views import plus_cart
from .views import minus_cart
from .views import remove_cart


urlpatterns = [
    path('', views.ProductView.as_view(), name="home"),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart, name='showcart'),
    path('cart/pluscart', plus_cart, name='pluscart'),
    path('cart/minuscart', minus_cart, name='minuscart'),
    path('cart/removecart', remove_cart, name='removecart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobile'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>/', views.laptop, name='laptop'),
    path('headphone/', views.headphone, name='headphone'),
    path('headphone/<slug:data>/', views.headphone, name='headphone'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html')),
    path('password-reset', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetView.as_view(template_name='app/password_reset_done.html'), 
    name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    
    path(
        'password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), 
        name='password_reset_complete'
    ),
    
    path('customerregistration/', CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)