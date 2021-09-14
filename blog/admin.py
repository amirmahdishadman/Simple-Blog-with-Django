from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Article,Category,IPAddress,SlideShow
from django.contrib.auth.models import User
# Register your models here.

# admin.site.disable_action('delete_selected')

    
#admin site changes

admin.site.site_header="مدیریت وبلاگ"


#-------------------------actions------------------------------

@admin.action(description='انتشار مقالات انتخاب شده')
def make_published(modeladmin, request, queryset):
    updated=queryset.update(status='P')
    modeladmin.message_user(request,"تعداد {} مقاله به منتشر شده تغیر یافت".format(updated))


@admin.action(description='پیش نویس کردن مقالات انتخاب شده')
def make_draft(modeladmin, request, queryset):
    updated=queryset.update(status='D')
    modeladmin.message_user(request,"تعداد {} مقاله به پیش نویس تغیر یافت".format(updated))


@admin.action(description='فعال کردن دسته بندی های انتخاب شده')
def category_active(modeladmin, request, queryset):
    updated=queryset.update(status=True)
    modeladmin.message_user(request,"تعداد {} دسته بندی به فعال تغیر یافت".format(updated))


@admin.action(description='غیر فعال کردن دسته بندی های انتخاب شده')
def category_deactive(modeladmin, request, queryset):
    updated=queryset.update(status=False)
    modeladmin.message_user(request,"تعداد {} دسته بندی به غیر فعال تغیر یافت".format(updated))

#------------------------end of actions------------------------------




class CategoryAdmin(admin.ModelAdmin):
    list_display=('position','title','slug','parent','status')
    list_filter=(['status'])
    search_fields=('title','slug')
    prepopulated_fields={'slug':('title',)}
    actions=[category_active,category_deactive]
    

admin.site.register(Category,CategoryAdmin)




class ArticleAdmin(admin.ModelAdmin):
    list_display=('title','thumbnail_tag','slug','author','jpublish','is_special','status','category_to_str')
    list_filter=('publish','status','category','author','is_special')
    search_fields=('title','description')
    prepopulated_fields={'slug':('title',)}
    ordering=['-status','-publish']
    actions=[make_published,make_draft]



admin.site.register(Article,ArticleAdmin)



@register(IPAddress)
class IPAddressAdmin(admin.ModelAdmin):
    list_display=('ip_address',)
    




@register(SlideShow)
class SlideShowAdmin(admin.ModelAdmin):
    list_display=('article',)




