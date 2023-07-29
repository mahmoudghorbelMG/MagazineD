from authentification import views
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('sign', views.sign_in_or_up,name='sign'),
    # path('login', views.Login, name='login'),
 
    path('oauth/', include('social_django.urls', namespace='social')),  # <-- here
    
    path('logout_view', views.logout_view, name='logout'),


    path('reset_password', auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html"), name="reset_password"),

    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_sent.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),

    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_done.html"), name="password_reset_complete"),

        path('verify', views.verify, name='verify'),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
