from setuptools import setup, find_packages
 
classifiers = [
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

with open("README.md", "r") as f:
    long_description = f.read()

setup(
  name='DecisionTreeClassifier',
  version='0.0.7',
  description='A Decision Tree Classifier.',
  long_description=long_description,
  long_description_content_type = "text/markdown",
  package_dir={"": "app"},
  packages=find_packages(where="app"),
  url='https://github.com/mlouii/Decision-Tree-Practicum',  
  author='Mark Lou, Jobin Joyson',
  author_email='mlou@hawk.iit.edu, jjoyson1@hawk.iit.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='decision tree', 
  install_requires=['numpy', 'pandas'] 
)