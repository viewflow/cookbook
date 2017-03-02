from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from guardian.admin import GuardedModelAdmin


from .models import User, Department


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ['email', 'department']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'Password mismatch',
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    icon = "<i class='material-icons'>person</i>"
    add_form = UserCreationForm
    list_display = ('email', 'department', 'is_staff', 'is_superuser')
    search_fields = ['email']
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'department', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'department', 'password1', 'password2'),
        }),
    )


@admin.register(Department)
class DepartmentAdmin(GuardedModelAdmin):
    icon = "<i class='material-icons'>group</i>"
    list_display = ('name', 'employees')

    def employees(self, obj):
        return obj.employees.count()
