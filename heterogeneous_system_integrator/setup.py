from distutils.core import setup

setup(
   name='heterogeneous_system_integrator',
   author='Tiodor V.K.',
   author_email='TiodorVK@gmail.com',
   version='1.0',
   packages=['heterogeneous_system_integrator'],
   install_requires=[
       'celery==5.3.6',
       'cryptography==42.0.5',
       'django-celery-beat==2.6.0',
       'django-celery-results==2.5.1',
       'django-filter==24.2',
       'django==4.2',
       'djangorestframework==3.15.1',
       'flower==2.0.1',
       'markdown==3.6',
       'psycopg2==2.9.9',
       'requests==2.31.0',
   ],
)