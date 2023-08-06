from setuptools import setup, find_packages, Extension
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='PrimeBotFramework',
  version='0.0.18.0',
  description='Um pacote de padronizacao de pacotes a serem utilizados pela Prime',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='',  
  author='Prime Control',
  author_email='',
  license='MIT', 
  classifiers=classifiers,
  keywords='PrimeBotFramework', 
  packages=find_packages(),
  install_requires=['hvac==1.0.2','mongoengine==0.22.1','elasticsearch-dsl==7.3.0','dateUts==0.1.0', 'ecs-logging', 'datetime',
'requests>=2.28.1', 'pyaml>=21.10.1', 'pydantic>=1.10.2', 'cx-Oracle==8.3.0', 'sendgrid==6.10.0', 'certifi==2022.12.7'],
  python_requires='~=3.8'
)



