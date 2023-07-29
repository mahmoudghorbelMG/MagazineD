import uuid

from Market.models import Orders
from .forms import UserForm, EmailForm, CustomPasswordChangeForm ,ProfileForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from Article.models import Article
from Produit.models import Product
from Produit.forms import ProductForm
from .models import  Subscription
from .forms import ArticleForm, SubscriptionForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum
@login_required
@require_POST
def mark_all_as_read(request):
    request.user.notifications.mark_all_as_read()
    return JsonResponse({'success': True})

from notifications.models import Notification
def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser


def is_subscriber(user):
    
    return user.groups.filter(name='Subscribre').exists()



@login_required
def dashbord(request):
    return render(request, 'dashboard/dashbord.html')


@login_required
def main(request):
    order_count = Orders.objects.count()
    orders = Orders.objects.filter(user=request.user)
    total_price = Orders.objects.aggregate(total_price=Sum('total'))['total_price']
    user_count = User.objects.count()
    return render(request, 'dashboard/main.html',{'orders': orders,'order_count': order_count,'total_price': total_price,'user_count': user_count})
@login_required
def article(request):
    articles = Article.objects.filter(author=request.user)
    return render(request, 'dashboard/Article/Article.html', {'articles': articles})

#------------------------------------------ CRUD Article------------------------------------------#


from django.core.files.storage import FileSystemStorage
@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.article_slug = str(uuid.uuid4())
            if request.FILES.get('image'):
                article.image = request.FILES['image']
            article.save()
            #-----------------Ajouter une notification pour les administrateurs#-----------------#
            staff_users = User.objects.filter(is_staff=True)
            for user in staff_users:
             notify.send(request.user, recipient=staff_users, verb='a new article is waiting for validation')

            return redirect('main')
    else:
        form = ArticleForm()
    return render(request, 'dashboard/Article/add_article.html', {'form': form})



@login_required
def update_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if article.author == request.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                article.etat='panding'
                form.save()
                
              #-----------------Ajouter une notification pour l'auteur de l'article-----------------#

            
            return redirect('main')
        else:
            form = ArticleForm(instance=article)

        return render(request, 'dashboard/Article/update_article.html', {'form': form, 'article': article})
    else:
        return redirect('dashbord')


@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if is_staff_or_superuser(request.user) or article.author == request.user:
        if request.method == 'POST':
            article.delete()
            return redirect('article')

        return render(request, 'dashboard/Article/delete_article.html', {'article': article})
    else:
        return redirect('article')

def view_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, 'dashboard/Article/view_article.html', {'article': article})







#------------------------------------------approuver Article------------------------------------------#
from django.contrib import messages
def articles_en_attente(request):
    articles = Article.objects.filter(etat='panding')
    if request.method == 'POST':
        article_id = request.POST['article_id']
        action = request.POST['action']
        article = Article.objects.get(pk=article_id)
        if action == 'accepted':
            article.etat = 'accepted'
# Notify the author of the state change
            notify.send(request.user, recipient=article.author, verb=f" a {article.etat}\"Your article \"{article.title}")
        elif action == 'refused':
            article.etat = 'refused'
            notify.send(request.user, recipient=article.author, verb=f" a {article.etat}\"Your article \"{article.title}")
        article.save()
        return redirect('articles_en_attente')
    context = {
        'articles': articles
    }
    return render(request, 'dashboard/Article/articles_en_attente.html', context)


#------------------------------------------ update_user------------------------------------------#

@login_required
def Update(request):
    user = request.user
    user_form = UserForm(instance=user)
    email_form = EmailForm(instance=user)
    password_form = CustomPasswordChangeForm(user=user)
    profile_form = ProfileForm(instance=user.profile)

    if request.method == 'POST':
        if 'user_form' in request.POST:
            user_form = UserForm(request.POST, instance=user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                # Vérification de l'existence du nom d'utilisateur
                new_username = user_form.cleaned_data['username']
                if User.objects.exclude(id=user.id).filter(username=new_username).exists():
                    messages.error(request, "Username already taken.")
                    return redirect('Update')
                else:
                    user_form.save()
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
                    messages.success(request, 'Votre profil a été mis à jour avec succès.')
            return redirect('Update')
        elif 'password_form' in request.POST:
            password_form = CustomPasswordChangeForm(
                user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
                return redirect('Update')
        elif 'picture' in request.FILES:
            user.profile.picture = request.FILES['picture']
            user.profile.save()
            messages.success(request, 'Votre photo de profil a été mise à jour avec succès.')
            return redirect('Update')

    return render(request, 'dashboard/Edit_Profile/user_update.html', {'user_form': user_form, 'email_form': email_form, 'password_form': password_form, 'profile_form': profile_form})
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
#------------------------------------------ subscribe------------------------------------------#
def is_authenticated(user):
    return user.is_authenticated
@user_passes_test(is_authenticated, login_url='sign')

def subscription(request) : 
    return render(request , "dashboard/subscription/subscription.html")

@user_passes_test(is_authenticated, login_url='sign')
def subscription_confirm(request):
    subscriber_group = Group.objects.get(name='Subscriber')
    request.user.groups.add(subscriber_group)
    return redirect('main')





#------------------------------------------Notification------------------------------------------#

from notifications.signals import notify
@login_required

def notifications(request) : 
    return render(request,'dashboard/notifications/notifications.html')



#------------------------------------------------------------------------------------product------------------------------------------------------------------------------------#


from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from payments.views import create_checkout_session

# Définir la fonction de test pour vérifier l'appartenance au groupe "Subscriber"
def is_subscriber(user):
    return user.groups.filter(name='Subscriber').exists()

# Décorer la vue "product" avec le décorateur "user_passes_test"
@user_passes_test(is_subscriber, login_url='subscription')
@login_required
def product(request):
    products = Product.objects.filter(owner=request.user)
    return redirect('under_development')
    #return render(request, 'dashboard/Product/Product.html', {'products': products})




@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.product_slug = str(uuid.uuid4())
            if request.FILES.get('image'):
                product.image = request.FILES['image']
            product.save()
            return redirect('under_development')
            #return redirect('main')
    else:
        form = ProductForm()
    return redirect('under_development')
    #return render(request, 'dashboard/Product/add_product.html', {'form': form})



@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.owner == request.user:
        if request.method == 'POST':
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
               
                form.save()
                
              

            
            return redirect('main')
        else:
            form = ProductForm(instance=product)
        return redirect('under_development')
        #return render(request, 'dashboard/Product/update_produit.html', {'form': form, 'product': product})
    else:
        return redirect('under_development')
        #return redirect('dashbord')


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if is_staff_or_superuser(request.user) or product.owner == request.user:
        if request.method == 'POST':
            product.delete()
            return redirect('main')
        return redirect('under_development')
        #return render(request, 'dashboard/Product/delete_produit.html', {'product': product})
    else:
        return redirect('under_development')
        #return redirect('dashboard')
@login_required
def user_orders(request):
    orders = Orders.objects.filter(user=request.user)
    return redirect('under_development')
    #return render(request, 'dashboard/Product/user_orders.html', {'orders': orders})


#========================UNder Development==================================#


def under_development(request):
    return render(request, 'dashboard/Product/under_development.html')

#------------------------------------------------------------------------------------------------------  search  ------------------------------------------------------------------------------------------------------#
@login_required
def search(request):
    query = request.GET.get('q')
    products = Product.search(query) if query else Product.objects.all()
    articles = Article.search(query) if query else Article.objects.all()
    return render(request, 'dashboard/search_results.html', {'products': products, 'articles': articles, 'query': query})



@login_required
def search_dashboard(request):
    query = request.GET.get('q')
    user = request.user
    products = Product.search(query, user) if query else Product.objects.filter(owner=user)
    articles = Article.search(query, user) if query else Article.objects.filter(author=user)
    return render(request, 'dashboard/search_results.html', {'products': products, 'articles': articles, 'query': query})
