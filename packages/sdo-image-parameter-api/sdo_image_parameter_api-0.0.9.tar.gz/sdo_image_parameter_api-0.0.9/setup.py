import os
from setuptools import setup, find_packages

# ------------ VARIABLES ------------
readme_fname = 'README.md'
requirement_fname = 'requirements.txt'

readme_path = os.path.join(os.path.dirname(__file__), readme_fname)
requirement_path = os.path.join(os.path.dirname(__file__), requirement_fname)

# ------------ SCRIPTS --------------
with open(readme_path, "r") as readme_file:
    readme = readme_file.read()

install_requires = ["numpy==1.24.3", "Pillow==9.5.0", "Requests==2.29.0"]

# pckges = find_packages(where="src")
# pckges = find_packages()

# ------------- SETUP ---------------
setup(
    name="sdo_image_parameter_api",
    version="0.0.9",
    author="Ruqayyah Muse",
    author_email="ruqayyahmuse@gmail.com",
    url="https://bitbucket.org/ds4350-image-param-api-rm/solar-image-api"
        "/src/main/",
    maintainer='Ruqayyah Muse',
    maintainer_email="ruqayyahmuse@gmail.com",
    description="A toolkit for accessing solar image data",
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=['src/sdo_image_parameter_api',
              'src/sdo_image_parameter_api/util'],
    package_data={'.': ['requirements.txt']},
    install_requires=install_requires,
    include_package_data=True,
    license='MIT',
    keywords=['sun', 'sdo', 'solar images', 'parameters'],
    project_urls={
        'Source': "https://bitbucket.org/ds4350-image-param-api-rm/solar"
                  "-image-api/src/main/",
        'Web API': "http://dmlab.cs.gsu.edu/dmlabapi/isd_docs.html"
    },
    classifiers=[
        # Keys & values must be chosen from: https://pypi.org/classifiers/
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
)
