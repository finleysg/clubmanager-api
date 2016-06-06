from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from django.contrib.auth.models import User

from core.models import Member
from django.forms.models import ModelForm
from floppyforms import ClearableFileInput


class ImageThumbnailFileInput(ClearableFileInput):
    template_name = "floppyforms/image_thumbnail.html"


class User2Form(ModelForm):
    def __init__(self, *args, **kwargs):
        super(User2Form, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = "col-sm-4"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
            Div(
                Div(
                    "first_name",
                    "last_name",
                    "email",
                    Field('id', type="hidden"),
                    css_class="col-sm-4"
                ),
                css_class="row"
            )
        )

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")


class Member2Form(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Member2Form, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = "col-sm-4"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
            Div(
                Div(
                    "phone_number",
                    "city",
                    "show_email",
                    Field("ghin", readonly=True),
                    css_class="col-sm-4",
                ),
                Div(
                    "raw_image",
                    css_class="col-sm-4 profile-image"
                ),
                css_class="row"
            )
        )

    class Meta:
        model = Member
        fields = ("ghin", "show_email", "phone_number", "city", "raw_image")
        widgets = {"raw_image": ImageThumbnailFileInput}

    # def save(self, *args, **kwargs):
    #     u = self.instance.user
    #     u.first_name = self.cleaned_data["first_name"]
    #     u.last_name = self.cleaned_data["last_name"]
    #     u.email = self.cleaned_data["email"]
    #     u.save()
    #     profile = super(Member2Form, self).save(*args,**kwargs)
    #     return profile
