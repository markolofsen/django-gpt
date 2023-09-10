
Django GPT
==========

Django GPT is a library for integrating powerful text generators like GPT-3 and GPT-4 into your Django application. It allows you to automatically generate text based on instructions, which can be useful for creating property descriptions or other textual data.

Installation
------------

You can install Django GPT using pip:

.. code-block:: bash

   pip install django-ckeditor-5
   pip install django-gpt

Usage Example
-------------

.. code-block:: python

   from django.db import models
   from django_gpt.models import DjapgoGptField

   class PropertyModel(models.Model):
       id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
       title = models.CharField(max_length=255)

       # GPT
       gpt_instruction = models.TextField(
           default='', blank=True, help_text='GPT instruction')

       description_html = DjapgoGptField(
           type="html",
           field_instruction_name="gpt_instruction",
           gpt_role="You're a real estate agent and you're writing a description for a property.",
           gpt_content_length=300,  # Default maximum generated text length.
           allowed_tags=['p', 'br', 'b', 'strong', 'i', 'em', 'u',
                         'ul', 'ol', 'li', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
           default="",
           blank=True,
       )

       description_text = DjapgoGptField(
           type="textarea",
           field_instruction_name="gpt_instruction",
           gpt_role="You're a real estate agent and you're writing a description for a property.",
           gpt_content_length=300,  # Default maximum generated text length.
           default="",
           blank=True,
       )

How It Works
------------

The Django GPT library allows you to create Django model fields that automatically generate text based on instructions. In the example above, we have two fields: ``description_html`` and ``description_text``\ , which use GPT to generate property description text.


#. 
   ``gpt_instruction``\ : This field is intended for instructions that you provide to GPT to specify what to generate.

#. 
   ``description_html`` and ``description_text``\ : These fields will be automatically filled with generated text based on the instructions provided in the ``gpt_instruction`` field.

#. 
   ``field_instruction_name``\ : This field determines where to take the instruction for text generation. If you change the ``field_instruction_name`` value, automatic regeneration of text will occur for fields that reference this instruction. GPT also takes into account the previous value that was in fields of type ``DjapgoGptField``. If you clear the value and change the instruction, text generation will be based solely on the new instruction. If there are no changes in the instruction, text regeneration will not occur. This allows you to preserve previous versions of generated text if needed for comparison.

#. 
   ``gpt_content_length``\ : This parameter defines the maximum length of generated text. In this example, the maximum length of the text is set to 300 characters. You can customize this parameter according to your needs.

Configuration
-------------

To configure the Django GPT library, you can use the following parameters in your Django application's ``settings.py`` file:

.. code-block::

   # Version of GPT to use (3 or 4).
   DJANGO_GPT_VERSION = 3

   # ISO language code (e.g., "en"). If not specified, it uses the value from LANGUAGE_CODE, and if that's not set, it defaults to "en".
   DJANGO_GPT_LANGUAGE = "en"

   # API key for GPT.
   CHATGPT_API_KEY = "your-api-key-here"
   # Please make sure to replace `"your-api-key-here"` with your actual GPT API key in the settings before using the library.

To use the rich text editor for HTML fields like ``description_html``\ , consider integrating a package like `django-ckeditor-5 <https://pypi.org/project/django-ckeditor-5/>`_. Here's an example of how to configure the editor in your Django settings:

.. code-block:: python

   INSTALLED_APPS = [
       ...
       "django_ckeditor_5",
       ...
   ]

   CKEDITOR_5_CONFIGS = {
       'default': {
           'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
                       'code', 'subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                       'bulletedList', 'numberedList', 'todoList', '|', 'blockQuote', 'imageUpload', '|',
                       'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                       'insertTable',],
           'image': {
               'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                           'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side', '|'],
               'styles': [
                   'full',
                   'side',
                   'alignLeft',
                   'alignRight',
                   'alignCenter',
               ]

           },
           'heading': {
               'options': [
                   {'model': 'paragraph', 'title': 'Paragraph',
                       'class': 'ck-heading_paragraph'},
                   {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1',
                       'class': 'ck-heading_heading1'},
                   {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2',
                       'class': 'ck-heading_heading2'},
                   {'model': 'heading3', 'view': 'h3',
                       'title': 'Heading 3', 'class': 'ck-heading_heading3'},
                    ...
               ]
           }
       },
   }
