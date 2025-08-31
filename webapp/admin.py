from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Company, Internship, InternshipApplication

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff', 'is_superuser']
    list_filter = ['role', 'is_staff', 'is_superuser']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'stipend', 'posted_date']
    list_filter = ['company', 'location']
    search_fields = ['title', 'company__name']

@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'internship', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    list_editable = ['status']

admin.site.register(Company)



# from django.contrib import admin
# from django.contrib.admin import AdminSite
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth import get_user_model
# from django.contrib.auth.views import LoginView
# from .models import Company, Internship,InternshipApplication # import your models here

# User = get_user_model()

# # Register User model (for adding/managing users)
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     list_display = ['username', 'email', 'role', 'is_staff', 'is_superuser', 'is_active']
#     list_filter = ['role', 'is_staff', 'is_superuser', 'is_active', 'date_joined']
#     search_fields = ['username', 'email']
    
#     fieldsets = UserAdmin.fieldsets + (
#         ('Custom Fields', {'fields': ('role',)}),
#     )

# @admin.register(Internship)
# class InternshipAdmin(admin.ModelAdmin):
#     list_display = ['title', 'company', 'location', 'stipend', 'posted_date']
#     list_filter = ['company', 'location', 'posted_date']
#     search_fields = ['title', 'company__name', 'location']
#     list_per_page = 20
#     ordering = ['-posted_date']

# @admin.register(InternshipApplication)
# class InternshipApplicationAdmin(admin.ModelAdmin):
#     list_display = ['user', 'internship', 'status', 'applied_at']
#     list_filter = ['status', 'applied_at']
#     search_fields = ['user__username', 'internship__title']
#     list_editable = ['status']  # Allow editing status directly from list

# admin.site.register(Company)


# class CustomAdminSite(AdminSite):
#     site_title = "Internship Portal Admin"
#     site_header = "Internship Portal Administration"
#     index_title = "Welcome to Admin Panel"
    
#     def login(self, request, extra_context=None):
#         # Custom login logic if needed
#         return super().login(request, extra_context)

# # Create custom admin site instance
# custom_admin_site = CustomAdminSite(name='custom_admin')

# # Register your models with custom admin site
# custom_admin_site.register(Internship, InternshipAdmin)
# custom_admin_site.register(InternshipApplication, InternshipApplicationAdmin)

