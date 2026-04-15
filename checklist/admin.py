from django.contrib import admin
from .models import Category, Item, Branch, Score, Audit, AuditDetail

class ItemInline(admin.TabularInline):
    model = Item
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ItemInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Branch)
admin.site.register(Score)
admin.site.register(AuditDetail)
admin.site.register(Audit)
