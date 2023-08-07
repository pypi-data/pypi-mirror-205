from setuptools import setup, find_packages

VERSION = '0.0.8' 
DESCRIPTION = 'Back to sit when the your code is ready'
LONG_DESCRIPTION = 'A package that send a message to your telegram when your code is ready'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="back_to_sit", 
        version=VERSION,
        author="Diego Machado",
        author_email="dmachadovz@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=['back_to_sit'],
        install_requires=["telegram"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'telegram'],
)