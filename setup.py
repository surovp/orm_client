from distutils.core import setup
REQUIRES = [
    'structlog',
    'sqlalchemy',
    'allure-pytest'
]

setup(
    name='orm_client',
    version='0.0.1',
    packages=['orm_client'],
    url='https://github.com/surovp/orm_client.git',
    license='MIT',
    author='Pavel Surov',
    author_email='-',
    install_requires=REQUIRES,
    description='orm client with allure and logger'
)
