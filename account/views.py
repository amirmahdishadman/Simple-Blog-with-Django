from django.http import request
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import FieldsMixin,FormValidMixin,AuthorAccessMixin,SuperUserAccessMixin,AuthorsAccessMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.auth.views import LoginView,PasswordChangeView
from blog.models import Article
from .models import User
from .forms import ProfileForm
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import SignupForm
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
# Create your views here.


@login_required
def home(request):
   return render(request,'registration/home.html')




class ArticleList(AuthorsAccessMixin,ListView):
   queryset=Article.objects.all()
   template_name= "registration/home.html"
   def get_queryset(self):
      if(self.request.user.is_superuser):
        return Article.objects.all()
      else:
         return Article.objects.filter(author=self.request.user)


class ArticlCreate(AuthorsAccessMixin,FieldsMixin,FormValidMixin,CreateView):
   model=Article
   template_name= "registration/article-create-update.html"


class ArticlUpdate(AuthorsAccessMixin,AuthorAccessMixin,FieldsMixin,FormValidMixin,UpdateView):
   model=Article
   template_name= "registration/article-create-update.html"



class ArticleDelete(SuperUserAccessMixin,DeleteView):
   model = Article
   success_url = reverse_lazy('account:home')
   template_name="registration/article_confirm_delete.html"



class Profile(LoginRequiredMixin,UpdateView):
   form_class=ProfileForm
   model=User
   template_name= "registration/profile.html"
   def get_object(self):
         return User.objects.get(pk = self.request.user.pk)
   success_url = reverse_lazy("account:profile")
   def get_form_kwargs(self):
      kwargs = super(Profile,self).get_form_kwargs()
      kwargs.update(
         {
            "user" : self.request.user
         }
      )
      return kwargs



class Login(LoginView):
   def get_success_url(self):
      user = self.request.user
      if user.is_superuser or user.is_author :
             return reverse_lazy("account:home")
      else:
             
             return reverse_lazy("account:profile")







class Signup(CreateView):
       form_class=SignupForm
       template_name="registration/signup.html"
       def form_valid(self,form):
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(self.request)
            mail_subject = 'ایمیل فعال سازی اکانت'
            message = render_to_string('registration/acc_active_email.html', {
               'user': user,
               'domain': current_site.domain,
               'uid':urlsafe_base64_encode(force_bytes(user.pk)),
               'token':account_activation_token.make_token(user),
            })
            
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            # return HttpResponse('Please confirm your email address to complete the registration')
            return render(self.request,"registration/signup-success.html")






def active_later(request):
   
      if request.method == 'POST':
            try:
               user = User.objects.get(email = request.POST['email'])
               if not user.is_active:
                  print(user.username)
                  current_site = get_current_site(request)
                  mail_subject = 'ایمیل فعال سازی اکانت'
                  message = render_to_string('registration/acc_active_email.html', {
                     'user': user,
                     'domain': current_site.domain,
                     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                     'token':account_activation_token.make_token(user),
                  })
                  
                  to_email = user.email
                  email = EmailMessage(
                              mail_subject, message, to=[to_email]
                  )
                  email.send()
                  # return HttpResponse('Please confirm your email address to complete the registration')
                  return render(request,"registration/signup-success.html")
               else:
                  context={"email3":False}
                  return render(request,"registration/activate-succes.html",context)    
            except:
               context={"email2":False}
               return render(request,"registration/activate-succes.html",context)
      else:
             raise Http404('SiKtir Kon Az Inja')
              





















# class active_later(LoginRequiredMixin,UpdateView):
#        model=User
#        template_name="registration/activate_later.html"
#        fields=['email']
#        def form_valid(self,form):
#             user = self.request.user
#             user.save()
#             current_site = get_current_site(self.request)
#             mail_subject = 'ایمیل فعال سازی اکانت'
#             message = render_to_string('registration/acc_active_email.html', {
#                'user': user,
#                'domain': current_site.domain,
#                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                'token':account_activation_token.make_token(user),
#             })
            
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#             )
#             email.send()
#             # return HttpResponse('Please confirm your email address to complete the registration')
#             return render(self.request,"registration/signup-success.html")







            
              
      
def activate(request, uidb64, token):
   try:
      uid = force_text(urlsafe_base64_decode(uidb64))
      user = User.objects.get(pk=uid)
      context={}
   except(TypeError, ValueError, OverflowError, User.DoesNotExist):
      user = None
   if user is not None and account_activation_token.check_token(user, token):
      user.is_active = True
      user.save()
      # login(request, user)
      # return redirect('home')
      context={"email":True}
      return render(request,"registration/activate-succes.html",context)
   else:
      context={"email":False}
      return render(request,"registration/activate-succes.html",context)




























# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = 'Activate your blog account.'
#             message = render_to_string('acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#             )
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = SignupForm()
#     return render(request, 'signup.html', {'form': form})

