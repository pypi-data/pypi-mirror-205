from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
setup(
    name='sandrine basic',
    version = '0.0.1',
    description ='''This is a description of my package, written in valid reStructuredText format. 
    You can use bullet points and other formatting options, as long as they are in valid RST syntax.''',
    # long_description=open('README.txt').read()+'\n\n'+ open('CHANGELOG.txt').read(),
    url = '',
    authour='Sandrine Sila',
    author_email='sila.n.sandrine@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)   
