from setuptools import setup, find_packages

setup(name='vitalijtverskoj_mess_client',
      version='0.2',
      description='Client packet',
      packages=find_packages(),
      author_email='gb@gb.ru',
      author='Geek Brains',
      install_requeres=['PyQt5', 'sqlalchemy', 'pycruptodome', 'pycryptodomex']
      )
