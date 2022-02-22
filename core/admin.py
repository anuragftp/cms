from django.contrib import admin
from core.models import Paper,Author,Reviewer,PaperAssign,Contact
from import_export.admin import ExportActionMixin

# Register your models here.

class PaperAdmin(ExportActionMixin, admin.ModelAdmin):
    model=Paper
    # search_fields=('title','rating','file','description')
    list_display=('id','title','description','status','file','user','remarks','rating','created_on','review_date','review_by',)

class AuthorAdmin(ExportActionMixin,admin.ModelAdmin):
    model=Author
    list_display=('id','user','created_on','updated_on',)

class ReviewAdmin(ExportActionMixin,admin.ModelAdmin):
    model=Reviewer
    list_display=('user','created_on','updated_on',)


class ContactAdmin(ExportActionMixin,admin.ModelAdmin):
    model=Contact
    search_fields=('email',)
    list_display=('email','description','reply','created_on','updated_on',)

class AssignPaperAdmin(ExportActionMixin,admin.ModelAdmin):
    model=Reviewer
    list_display=('id','review','assign_paper','created_on','updated_on','is_review',)

admin.site.register(Author,AuthorAdmin)
admin.site.register(Paper,PaperAdmin)
admin.site.register(Reviewer,ReviewAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(PaperAssign,AssignPaperAdmin)