from distutils.core import setup
setup(
    name='pydojo',
    packages=['pydojo'],
    version='2.0',
    description='A playful way to learn coding with Python',
    author='Alessandro Norfo',
    author_email='sprintingkiwi@gmail.com',
    url='https://github.com/sprintingkiwi/PYDOJO',
    download_url='https://github.com/sprintingkiwi/PYDOJO/tarball/2.0',
    keywords=['game', 'development', 'learning', 'education'],
    classifiers=[],
    include_package_data=True,
    package_data={'pydojo': ['turtle.png', 'pensurface.png']}
)
