from allauth.account.forms import LoginForm as AllAuthLoginForm
from crispy_forms.helper import FormHelper


class LoginForm(AllAuthLoginForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].label = ''
        self.fields['password'].label = ''
        self.helper = FormHelper()
        self.helper.form_tag = False
