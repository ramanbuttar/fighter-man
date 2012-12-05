from turbogears import widgets, validators
from rpg.model import User, Fighter
from sqlobject import SQLObjectNotFound

#################################################################################################
class MyTableForm(widgets.TableForm):
    template = """
    <form xmlns:py="http://purl.org/kid/ns#"
        name="${name}"
        action="${action}"
        method="${method}"
        class="tableform"
        py:attrs="form_attrs"
    >
        <div py:for="field in hidden_fields"
            py:replace="field.display(value_for(field), **params_for(field))"
        />
        <table border="0" cellspacing="0" cellpadding="2" py:attrs="table_attrs">
            <tr py:for="i, field in enumerate(fields)"
                class="${i%2 and 'odd' or 'even'}"
            >
                <th>
                    <label class="fieldlabel" for="${field.field_id}" py:content="field.label" />
                </th>
                <td>
                    <span py:replace="field.display(value_for(field), **params_for(field))" />
                    <span py:if="error_for(field)" class="fielderror" py:content="error_for(field)" />
                    <span py:if="field.help_text" class="fieldhelp" py:content="field.help_text" />
                </td>
		<td>
		    <span py:if="i==submit_index" py:strip="True" py:replace="submit.display(submit_text)"/>
		</td>
            </tr>
        </table>
    </form>
    """
    params = ["submit_index"]


class ReadTextField(widgets.Widget):
    "Simple widget that allows displaying its value in a span."

    params = ["field_class", "css_classes"]
    params_doc = {'field_class' : 'CSS class for the field',
                  'css_classes' : 'List of extra CSS classes for the field'}
    field_class = None
    css_classes = []

    def __init__(self, name=None, label=None, **kw):
        super(ReadTextField, self).__init__(name, **kw)
        self.label = label
        self.validator = None
        self.help_text = None
        self.field_id = None

    template = """
        <span xmlns:py="http://purl.org/kid/ns#"
            class="${field_class}"
            py:content="value" />
        """

###############################################################################################################################################################
class AddUserFields(widgets.WidgetsList):
    user_name = widgets.TextField('user_name', label=_("User Name"), help_text=_("A short name that you will use to log in."))
    email = widgets.TextField('email', label=_("Email"), help_text=_("Your email address"))
    display_name = widgets.TextField('display_name', label=_("Fighter Name"), help_text=_("Your fighter's name that others will see."))
    password_1 = widgets.PasswordField('password1', label=_("Password"), help_text=_("Your password."))
    password_2 = widgets.PasswordField('password2', label= _("Password (again)"), help_text=_("Same password as above (the two should match)."))

###############################################################################################################################################################

class UniqueUsername(validators.FancyValidator):
    "Validator to confirm that a given user_name is unique."
    messages = {'notUnique': 'That user name is already being used.'}

    def _to_python(self, value, state):
        if user_name_exists(value):
            raise validators.Invalid(self.message('notUnique', state), value, state)
        return value

class UniqueEmail(validators.FancyValidator):
    "Validator to confirm that a given email is unique."
    messages = {'notUnique': 'That email address is already being used.'}

    def _to_python(self, value, state):
        if email_exists(value):
            raise validators.Invalid(self.message('notUnique', state), value, state)
        return value

class UniqueDisplayName(validators.FancyValidator):
    "Validator to confirm that a given display_name is unique."
    messages = {'notUnique': 'That fighter already has a manager.'}

    def _to_python(self, value, state):
        if fighter_exists(value):
            raise validators.Invalid(self.message('notUnique', state), value, state)
        return value


###############################################################################################################################################################

def user_name_exists(value):
    try:
	User.by_user_name(value)
	return True
    except SQLObjectNotFound:
	return False

def email_exists(value):
    try:
        User.by_email_address(value)
        return True
    except SQLObjectNotFound:
        return False

def fighter_exists(value):
    try:
        Fighter.by_fighter_name(value)
        return True
    except SQLObjectNotFound:
        return False

###############################################################################################################################################################

class AddUserSchema(validators.Schema):
    user_name = validators.All(validators.UnicodeString(not_empty=True, max=16, strip=True), UniqueUsername())
    email = validators.All(validators.Email(not_empty=True, max=255), UniqueEmail())
    #display_name = validators.UnicodeString(not_empty=True, strip=True, max=255)
    display_name = validators.All(validators.UnicodeString(not_empty=True, max=30, strip=True), UniqueDisplayName())
    password1 = validators.UnicodeString(not_empty=True, max=40)
    password2 = validators.UnicodeString(not_empty=True, max=40)
    chained_validators = [validators.FieldsMatch('password1', 'password2')]
