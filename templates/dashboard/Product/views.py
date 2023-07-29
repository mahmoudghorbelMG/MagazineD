import uuid
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
    return render(request, 'dashboard/main.html')


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
                image = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)
                article.image = filename
                
                # Code pour ajouter l'image dans le contenu de l'article
                article.content += f'<img src="{fs.url(filename)}">'
                
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
@login_required
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
                user_form.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                messages.success(request, 'Votre profil a été mis à jour avec succès.')
                return redirect('main')
        elif 'email_form' in request.POST:
            email_form = EmailForm(request.POST, instance=user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, 'Votre adresse email a été mise à jour avec succès.')
                return redirect('main')
        elif 'password_form' in request.POST:
            password_form = CustomPasswordChangeForm(
                user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
                return redirect('main')
        elif 'picture' in request.FILES:
            user.profile.picture = request.FILES['picture']
            user.profile.save()
            messages.success(request, 'Votre photo de profil a été mise à jour avec succès.')
            return redirect('main')

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





@login_required
def subscription_confirm(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            # Récupérer les données du formulaire
            phone_number = form.cleaned_data['phone_number']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            country = form.cleaned_data['country']
            rib = form.cleaned_data['rib']

            # Ajouter l'utilisateur au groupe "Subscribre"
            subscribre_group = Group.objects.get(name='Subscriber')
            request.user.groups.add(subscribre_group)

            # Sauvegarder les données de souscription dans la base de données
            subscription = Subscription(
                user=request.user,
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
                country=country,
                rib=rib,
            )
            subscription.save()
            return redirect('main')

    else:
        form = SubscriptionForm()

    context = {
        'form': form,
    }

    return render(request, 'dashboard/subscription/subscription.html', context)

# ------------------------------------------ajouter des produit pour les subscribre -------------------------------------------#



@login_required
#@user_passes_test(lambda user: user.groups.filter(name='Subscriber').exists())
def add_product(request):
    return render(request, 'dashboard/Produit/add_produit.html',)



#------------------------------------------Notification------------------------------------------#

from notifications.signals import notify
@login_required

def notifications(request) : 
    return render(request,'dashboard/notifications/notifications.html')



#------------------------------------------------------------------------------------product------------------------------------------------------------------------------------#


@login_required
def product(request):
    products = Product.objects.filter(owner=request.user)
    return render(request, 'dashboard/Product/Product.html', {'products': products})



@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('main')
            
    else:
        form = ProductForm()
    return render(request, 'dashboard/Product/add_product.html', {'form': form})

@login_required
def update_product(request, article_id):
    product = get_object_or_404(Article, id=article_id)

    if product.owner == request.user:
        if request.method == 'POST':
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
               
                form.save()
                
              #-----------------Ajouter une notification pour l'auteur de l'article-----------------#

            
            return redirect('main')
        else:
            form = ProductForm(instance=product)

        return render(request, 'dashboard/Article/update_article.html', {'form': form, 'product': product})
    else:
        return redirect('dashbord')


@login_required
def delete_article(request, product_id):
    article = get_object_or_404(Article, id=product_id)

    if is_staff_or_superuser(request.user) or product.owner == request.user:
        if request.method == 'POST':
            article.delete()
            return redirect('article')

        return render(request, 'dashboard/Article/delete_article.html', {'product': product})
    else:
        return redirect('product')
@login_required
def view_article(request, product_id):
    article = get_object_or_404(Article, pk=product_id)
    return render(request, 'dashboard/Article/view_article.html', {'product': product})

