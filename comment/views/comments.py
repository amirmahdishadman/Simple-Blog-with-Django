from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib import messages

from comment.models import Comment
from comment.forms import CommentForm
from comment.utils import get_comment_from_key, get_user_for_request, CommentFailReason
from comment.mixins import CanCreateMixin, CanEditMixin, CanDeleteMixin, CommentCreateMixin, BaseCommentView
from comment.responses import UTF8JsonResponse
from comment.messages import EmailError



from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

class CreateComment(CanCreateMixin, CommentCreateMixin):
    comment = None
    email_service = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.comment
        return context

    def get_template_names(self):
        if self.request.user.is_anonymous or self.comment.is_parent:
            return 'comment/comments/base.html'
        else:
            return 'comment/comments/child_comment.html'

    def form_valid(self, form):
        user = get_user_for_request(self.request)
        comment_content = form.cleaned_data['content']
        email = form.cleaned_data.get('email', None)
        time_posted = timezone.now()
        temp_comment = Comment(
            content_object=self.model_obj,
            content=comment_content,
            user=user,
            parent=self.parent_comment,
            email=email or user.email,
            posted=time_posted
        )

        # send email section:
        current_site = get_current_site(self.request)
        article = temp_comment.content_object
        author_email=article.author.email
        user_email = temp_comment.user.email
        if(temp_comment.parent):
            parent_email = temp_comment.parent.user.email
        else:
            parent_email = False
        if(user_email==author_email):
            user_email=False
            author_email=False
        if(parent_email == user_email):
            parent_email=False

        if(temp_comment.is_parent == False):
            if author_email:
                email = EmailMessage(
                            "دیدگاه جدید",
                            "دیدگاه جدیدی برای مقاله {} ثبت شده است برای مشاهده بر روی لینک زیر کلیک کنید.\n {}{}".format(article.title,current_site,reverse('blog:detail',kwargs={'slug':article.slug})),
                            to=[author_email]
                )
                email.send()
            if user_email:
                email = EmailMessage(
                            "دیدگاه شما ثبت شد",
                            "پاسخ شما به دیدگاه مقاله {} نوشته شده توسط {} ثبت شد.".format(article.title,temp_comment.parent.user.get_full_name()),
                            to=[user_email]
                )
                email.send()
            if parent_email:
                email = EmailMessage(
                            "پاسخ جدید به دیدگاه شما",
                            "پاسخ جدیدی برای دیدگاه شما در مقاله {} ثبت شده است برای مشاهده بر روی لینک زیر کلیک کنید.\n {}{}".format(article.title,current_site,reverse('blog:detail',kwargs={'slug':article.slug})),
                            to=[parent_email]
                )
                email.send()
        else:
            if author_email:
                email = EmailMessage(
                            "دیدگاه جدید",
                            "دیدگاه جدیدی برای مقاله {} ثبت شده است برای مشاهده بر روی لینک زیر کلیک کنید.\n {}{}".format(article.title,current_site,reverse('blog:detail',kwargs={'slug':article.slug})),
                            to=[author_email]
                )
                email.send()
            if user_email:
                email = EmailMessage(
                            "دیدگاه شما ثبت شد",
                            "دیدگاه شما برای مقاله {} ثبت شده در صورت پاسخ دادن به شما ایمیلی ارسال خواهد شد .میتوانید این مقاله را از لینک زیر ببینید.\n {}{}".format(article.title,current_site,reverse('blog:detail',kwargs={'slug':article.slug})),
                            to=[user_email]
                )
                email.send()
                
        # end of sending email section.


        self.comment = self.perform_create(temp_comment, self.request)
        self.data = render_to_string(self.get_template_names(), self.get_context_data(), request=self.request)
        return UTF8JsonResponse(self.json())

    def form_invalid(self, form):
        self.error = EmailError.EMAIL_INVALID
        self.status = 400
        return UTF8JsonResponse(self.json(), status=self.status)


class UpdateComment(CanEditMixin, BaseCommentView):
    comment = None

    def get_object(self):
        self.comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        return self.comment

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['comment_form'] = CommentForm(instance=self.comment, request=self.request)
        context['comment'] = self.comment
        self.data = render_to_string('comment/comments/update_comment.html', context, request=self.request)
        return UTF8JsonResponse(self.json())

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST, instance=self.comment, request=self.request)
        context = self.get_context_data()
        if form.is_valid():
            form.save()
            context['comment'] = self.comment
            self.data = render_to_string('comment/comments/comment_content.html', context, request=self.request)
            return UTF8JsonResponse(self.json())


class DeleteComment(CanDeleteMixin, BaseCommentView):
    comment = None

    def get_object(self):
        self.comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        return self.comment

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["comment"] = self.comment
        context['has_parent'] = not self.comment.is_parent
        self.data = render_to_string('comment/comments/comment_modal.html', context, request=request)
        return UTF8JsonResponse(self.json())

    def post(self, request, *args, **kwargs):
        self.comment.delete()
        context = self.get_context_data()
        self.data = render_to_string('comment/comments/base.html', context, request=self.request)
        return UTF8JsonResponse(self.json())


class ConfirmComment(CommentCreateMixin):

    @staticmethod
    def _handle_invalid_comment(comment, request):
        if comment.why_invalid == CommentFailReason.BAD:
            messages.error(request, EmailError.BROKEN_VERIFICATION_LINK)
        elif comment.why_invalid == CommentFailReason.EXISTS:
            messages.warning(request, EmailError.USED_VERIFICATION_LINK)

    def get(self, request, *args, **kwargs):
        key = kwargs.get('key', None)
        temp_comment = get_comment_from_key(key)
        self._handle_invalid_comment(temp_comment, request)

        if not temp_comment.is_valid:
            return render(request, template_name='comment/anonymous/discarded.html')

        comment = self.perform_save(temp_comment.obj, request)

        return redirect(comment.get_url(request))
