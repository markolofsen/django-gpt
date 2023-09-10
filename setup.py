from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='django-gpt',
    version='1.0.0',
    description='Integrate powerful text generators like GPT-3 and GPT-4 into your Django application for automated text generation based on instructions.',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author='Mark',
    author_email='markolofsen@gmail.com',
    url='https://github.com/markolofsen/django-gpt',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    packages=find_packages(),
    install_requires=[
        'openai',
        # 'django-ckeditor-5',
    ],
    # package_dir={'': 'py-seo-html'},
    py_modules=['django_gpt'],
)
