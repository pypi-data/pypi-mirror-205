from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='flask_admin_dashboard',
    version='0.0.5',
    description='Admin Dashboard for Flask',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/theapiguys/flask_admin_dashboard',
    readme="README.md",
    author='Will @ TheAPIGuys',
    author_email='will@theapiguys.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask==2.2.3",
        "email-validator",
        "python-dateutil",
        "Flask-Admin==1.6.1",
        "Flask-Security==3.0.0",
        "Flask-SQLAlchemy==3.0.3",
        "SQLAlchemy==2.0.10",
        "SQLAlchemy-serializer==1.4.1",
        "Flask-WTF==1.0.1",
        "WTForms==3.0.1",
        "Flask-Login==0.6.2",
        "Flask-Mail==0.9.1",
        "Flask-Migrate==4.0.4",
        "Flask-Principal==0.4.0",
        "pytz",
        "shutil"
    ],
    entry_points={
        'console_scripts': [
            'admin = flask_admin_dashboard.scripts.cli:cli',
        ],

    },
)
