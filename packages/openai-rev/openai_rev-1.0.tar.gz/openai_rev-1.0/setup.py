import setuptools

with open('README.md', encoding='utf-8') as f:
    description = f.read()

setuptools.setup(
    name='openai_rev',
    version='1.0',
    license='Unlicense',
    author='bobbill',
    description='making music with OpenAI (GPT-4)',
    packages = ['openai_rev'],
    install_requires=['simpleaudio', 'numpy'],
    long_description=description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)