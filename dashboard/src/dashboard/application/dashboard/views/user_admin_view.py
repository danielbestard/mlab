from flask_admin.contrib.mongoengine import ModelView
from flask_security import utils
from flask_security.core import current_user
from wtforms import PasswordField, SelectMultipleField

from dashboard.domain.entities.message import Topic


class UserAdmin(ModelView):
    column_exclude_list = ('password',)

    form_excluded_columns = ('password',)

    column_auto_select_related = True
    edit_template = 'security/user.html'

    form_widget_args = {
        'topics': {
            'readonly': True
        },
    }

    def is_accessible(self):
        return current_user.has_role('admin')

    def get_available_topics(self):
        return [(topic.name, topic.value) for topic in Topic]

    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        form_class.topics = SelectMultipleField('Topics', choices=self.get_available_topics())
        form_class.password2 = PasswordField('New Password')

        return form_class

    def on_model_change(self, form, model, is_created):
        if len(model.password2):
            model.password = utils.hash_password(model.password2)


class RoleAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')
