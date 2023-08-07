from setuptools import setup
import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name='material_zui',
    version='0.0.1',
    # url='https://github.com/username/my_module',
    author='chauhmnguyen',
    author_email='chauhoangminhnguyen@gmail.com',
    description='Zui Material',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=['cv2', 'PIL'],
    classifiers=[
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
