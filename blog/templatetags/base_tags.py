from django import template
from django.db.models.aggregates import Max
from django.db.models.query_utils import Q
from ..models import Category,Article,SlideShow
from django.db.models import Avg, Count, Min, Sum
from django.db.models import Q
from datetime import datetime,timedelta
from django.contrib.contenttypes.models import ContentType
from star_ratings.models import UserRating,AbstractBaseRating,Rating


register = template.Library()

@register.simple_tag
def title():
    return 'وبلاگ جنگویی'



@register.inclusion_tag("blog/partials/category_navbar.html")
def category_navbar():
    return {
        "category": Category.objects.filter(status=True)
    }


# hits
@register.inclusion_tag("blog/partials/left_articles_bar.html")
def month_popular_articles():
    last_month=datetime.today()-timedelta(days=30)
    return {
        "articles": Article.objects.published()
        .annotate(count=Count('hits',filter=Q(articlehit__created__gt=last_month))).order_by('-count','-publish')[:5],
        "title":"مقالات پر بازدید ماه"
    }


# comment

@register.inclusion_tag("blog/partials/left_articles_bar.html")
def month_hot_articles():
    content_type_id = ContentType.objects.get(app_label='blog', model='article').id
    last_month=datetime.today()-timedelta(days=30)
    return {
        "articles": Article.objects.published()
        .annotate(count=Count('comments',filter=Q(comments__posted__gt=last_month) and Q(comments__content_type_id=content_type_id) )).order_by('-count','-publish')[:5],
        "title":"مقالات داغ ماه"
    }


# star

@register.inclusion_tag("blog/partials/left_articles_bar.html")
def month_rated_articles():
    content_type_id = ContentType.objects.get(app_label='blog', model='article').id
    last_month=datetime.today()-timedelta(days=30)

    points=Rating.objects.all().annotate(totalscore=Sum('user_ratings__score',filter=Q(user_ratings__modified__gt=last_month) and Q(content_type_id=content_type_id))).order_by("object_id")
    counts=Rating.objects.all().annotate(counts=Count('user_ratings__user_id',filter=Q(user_ratings__modified__gt=last_month) and Q(content_type_id=content_type_id))).order_by("object_id")

    for i in range(len(points)):
        try:
            points[i].average=points[i].totalscore/counts[i].counts
        except:
            points[i].average=0
    items=points.order_by("-average","-total")
    articles=Article.objects.published()
    articles2=[]
    for item in items:
        for article in articles:
            if(article.id == item.object_id):
                articles2.append(article)

    return {
        "articles": articles2,
        "title":"مقالات محبوب ماه"
    }



@register.inclusion_tag("registration/partials/link.html")
def link(request,link_name,content,classes):
    return {
        "request":request,
        "link_name":link_name,
        "link":"account:{}".format(link_name),
        "content":content,
        "classes":classes
    }





#slider
@register.inclusion_tag("blog/partials/slider.html")
def slider():
    return {
        "objects": SlideShow.objects.filter(status=True,article__status='P')
    }