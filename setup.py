from setuptools import setup, find_packages
import datetime

now = datetime.datetime.now()
created=now.strftime('%Y-%m-%d %H:%M:%S')

setup(
    name='metaccm',
    version='0.3.0',
    python_requires='>=3.11',
    author='Haiyang Hou',
    author_email='2868582991@qq.com',
    description=f'{created}This is an algorithm for building a Case-Ctrl matching cohort to minimize the influence of confusing variables.',
    keywords='Case-Ctrl matching',
    packages=find_packages(),
    install_requires=['numpy','pandas','scipy','joblib','scikit-learn']
)

