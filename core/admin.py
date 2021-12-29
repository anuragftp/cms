from django.contrib import admin
from core.models import Paper,Author,Reviewer,PaperAssign

# Register your models here.

class PaperAdmin(admin.ModelAdmin):
    model=Reviewer
    list_display=('id','title','description','status','file','user','created_on','updated_on',)

class AuthorAdmin(admin.ModelAdmin):
    model=Author
    list_display=('id','user','created_on','updated_on',)

class ReviewAdmin(admin.ModelAdmin):
    model=Reviewer
    list_display=('id','user','created_on','updated_on',)

class AssignPaperAdmin(admin.ModelAdmin):
    model=Reviewer
    list_display=('id','review','assign_paper','created_on','updated_on','is_review',)

admin.site.register(Author,AuthorAdmin)
admin.site.register(Paper,PaperAdmin)
admin.site.register(Reviewer,ReviewAdmin)
admin.site.register(PaperAssign,AssignPaperAdmin)