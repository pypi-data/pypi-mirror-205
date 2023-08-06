from distutils.core import setup
setup(
  name = 'storelibrarycpp',         
  packages = ['storelibrarycpp'],  
  version = '0.1',      
  license='MIT', # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This package is used for store management software system',
  author = 'Surya Porandla',                  
  author_email = 'porandlasuryair@gmail.com',      
  url = 'https://github.com/user/reponame',  
  download_url = 'https://github.com/Surya22103961/StoreLibraryCpp/releases/tag/v_01',    # I explain this later on
  keywords = ['Store', 'Management', 'stock'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'storelibrarycpp'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)