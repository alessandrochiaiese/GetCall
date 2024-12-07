from chat.api.serializers import MessageSerializer
from chat.models.activity import Activity
from chat.models.conversation import Conversation
from chat.models.message import Message
from chat.models.pretrained_model import PretrainedModel
from chat.models.project import Project
from chat.models.thought import Thought
from chat.models.user import User 
from chat.models.role import Role 
from django.forms import ModelForm

class PretrainedModelForm(ModelForm):

    class Meta:
        model = PretrainedModel
        fields = '__all__'
        
class ThoughtForm(ModelForm):

    class Meta:
        model = Thought
        fields = '__all__'
        
class ActivityForm(ModelForm):

    class Meta:
        model = Activity
        fields = '__all__' 

class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = '__all__' 
  
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']

class ConversationForm(ModelForm):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'messages', 'created_at']
 
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