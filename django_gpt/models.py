from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget
from django.conf import settings
from django.db import models
from django import forms

from .ai import GPTAssistant


class GptGenerationError(Exception):
    pass


class DjapgoGptField(models.Field):
    def __init__(self, *args,
                 type="text",
                 config_name="default",
                 gpt_role="",
                 gpt_content_length=300,
                 field_instruction_name="gpt_instruction",
                 allowed_tags=['p', 'br', 'b', 'strong', 'i', 'em', 'u',
                               'ul', 'ol', 'li', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
                 ** kwargs
                 ):

        if type not in ["text", "textarea", "html"]:
            raise Exception('type must be one of "text", "textarea", "html"')

        self.type = type
        self.config_name = config_name
        self.gpt_role = gpt_role
        self.gpt_content_length = gpt_content_length
        self.field_instruction_name = field_instruction_name
        self.allowed_tags = allowed_tags

        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def formfield(self, **kwargs):

        if self.type == "textarea":
            return super().formfield(
                **{
                    "max_length": self.max_length,
                    **({} if self.choices is not None else {
                        "widget": forms.Textarea(attrs={
                            'cols': 200, 'rows': 10,
                        }),
                    }),
                    **kwargs,
                }
            )

        if self.type == "html":
            return super().formfield(
                **{
                    "max_length": self.max_length,
                    ** ({"widget": CKEditor5Widget(config_name=self.config_name)}),
                    **kwargs,
                }
            )

        return super().formfield(
            **{
                "max_length": self.max_length,
                **({} if self.choices is not None else {
                    "widget": forms.TextInput(attrs={'size': '100%'})
                }),
                **kwargs,
            }
        )

    def pre_save(self, model_instance, add):
        if not hasattr(model_instance, self.field_instruction_name):
            raise Exception('field_instruction_name field is required')

        gpt_instruction = getattr(model_instance, self.field_instruction_name)
        gpt_description = getattr(model_instance, self.attname)

        old_gpt_instruction = model_instance.__class__._default_manager.filter(
            pk=model_instance.pk).values_list(self.field_instruction_name, flat=True).first()

        if gpt_instruction and old_gpt_instruction != gpt_instruction:

            try:
                is_html = self.type == "html"
                gpt_description_response = get_content(
                    gpt_request=gpt_instruction,
                    gpt_pre_content=gpt_description,
                    gpt_content_length=self.gpt_content_length,
                    gpt_role=self.gpt_role,
                    allowed_tags=self.allowed_tags,
                    is_html=is_html,
                )
                if gpt_description_response:
                    setattr(model_instance, self.attname,
                            gpt_description_response)

            except GptGenerationError as e:
                GptGenerationError(e)

        setattr(model_instance, self.field_instruction_name, gpt_instruction)

        return super().pre_save(model_instance, add)


def get_content(
    gpt_request,
    gpt_pre_content,
    gpt_content_length,
    gpt_role=None,
    allowed_tags=[],
    is_html=False,
):
    CHATGPT_API_KEY = settings.CHATGPT_API_KEY

    # Create an instance of the GPTAssistant class

    language = 'en'
    gpt_version = 3

    if hasattr(settings, 'DJANGO_GPT_VERSION'):
        v = settings.DJANGO_GPT_VERSION
        if v == 3:
            gpt_version = 3
        elif v == 4:
            gpt_version = 4

    if hasattr(settings, 'DJANGO_GPT_LANGUAGE'):
        language = settings.DJANGO_GPT_LANGUAGE
    elif hasattr(settings, 'LANGUAGE_CODE'):
        language = settings.LANGUAGE_CODE

    assistant = GPTAssistant(
        api_key=CHATGPT_API_KEY,
        version=gpt_version,
        language=language,
        max_length=gpt_content_length,
        is_html=is_html,
        allowed_tags=allowed_tags,
    )

    assistant.add_role('system', gpt_role)

    if gpt_pre_content:
        assistant.add_role("assistant", f"Previous content: {gpt_pre_content}")

    assistant.set_words(gpt_request)

    response = assistant.generate_response()
    return response
