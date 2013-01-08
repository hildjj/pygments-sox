from setuptools import setup, find_packages

version = '1.0'

setup(name='pygments-sox',
      version=version,
      description='Pygments lexer for SIP over XMPP',
      long_description=open('README.txt').read() + '\n' +
                       open('CHANGES.txt').read(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Plugins',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
      ],
      keywords='pygments sox xmpp sip sdp lexer',
      author='Joe Hildebrand',
      author_email='joe-github@cursive.net',
      url='http://pypi.python.org/pypi/pygments-sox',
      license='BSD',
      packages=['pygments_sox'],
      zip_safe=True,
      install_requires=[
          'setuptools',
      ],
      entry_points={
          'pygments.lexers': [
            'sox=pygments_sox:SoxLexer',
            'sip=pygments_sox:SipLexer',
            'sdp=pygments_sox:SdpLexer',
          ]
      },
)
