from distutils.core import setup


current_version = "1.0.7"

setup(
    name="scratch_implemented",
    packages=["scratch_implemented"],
    version=current_version,
    license="MIT",
    description="Machine Learning Models",
    author="Gleb Maksimov",
    author_email="glebmaksimov092@gmail.com",
    keywords=["ML", "FROM SCRATCH", "ADVANCED"],
    install_requires=[
        "numpy",
        "matplotlib",
        "pandas",
        "scikit-learn",
        "seaborn",
        "IPython",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
)
