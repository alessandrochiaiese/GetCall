
from django.forms import ModelForm
from accounts.models.role import Role
from accounts.models.user import User


class RoleForm(ModelForm):

    class Meta:
        model = Role
        fields = '__all__' 
        #fields = ('id', 'name')
  
class UserForm(ModelForm):

    class Meta:
        model = User
        fields = '__all__' 
        #fields = ('id', 'email', 'phone', 'first_name', 'last_name', 'password', 'roles', 'date_created', 'date_modified')