from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pytpu',
    packages=['pytpu', 'pytpu.tools', 'pytpu.pytpu', 'pytpu.scripts'],
    version="2.0.0",
    author="IVA-Tech",
    author_email="info@iva-tech.ru",
    description="TPU Python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://git.mmp.iva-tech.ru/tpu_sw/iva_tpu_sdk",
    install_requires=[
        'numpy',
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-xdist',
            'pytest-cov',
            'Pillow',
            'flake8',
            'mypy',
            'tpu-tlm-is~=0.3.0.1'
        ],
    },
    zip_safe=False,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'run_get_fps = pytpu.scripts.run_get_fps:main',
            'pyrun_tpu = pytpu.scripts.pyrun_tpu_cli:main'
        ]
    },
)
