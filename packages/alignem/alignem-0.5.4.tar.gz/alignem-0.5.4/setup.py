# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['alignem']
install_requires = \
['Pillow>=9.5.0,<10.0.0',
 'PyQt5>=5.15.9,<6.0.0',
 'PyQtWebEngine>=5.15.6,<6.0.0',
 'QtAwesome>=1.2.3,<2.0.0',
 'QtPy>=2.3.1,<3.0.0',
 'imagecodecs>=2023.3.16,<2024.0.0',
 'imageio>=2.28.0,<3.0.0',
 'neuroglancer>=2.36,<3.0',
 'numpy>=1.24.3,<2.0.0',
 'psutil>=5.9.5,<6.0.0',
 'pyqtgraph>=0.13.3,<0.14.0',
 'qtconsole>=5.4.2,<6.0.0',
 'rechunker>=0.5.1,<0.6.0',
 'tensorstore>=0.1.36,<0.2.0',
 'tifffile>=2023.4.12,<2024.0.0',
 'zarr>=2.14.2,<3.0.0']

setup_kwargs = {
    'name': 'alignem',
    'version': '0.5.4',
    'description': '"AlignEM-SWIFT is a graphical tool for aligning serial section electron micrographs using SWiFT-IR."',
    'long_description': '# SWiFT-IR\n\n## Signal Whitening Fourier Transform Image Registration\n\n### Developed by Art Wetzel, Pittsburgh Supercomputing Center\n\n* **[User Documentation](docs/user/README.md)**\n* **[Development Documentation](docs/development/README.md)**\n* **[Running on TACC](docs/tacc/README.md)**\n* **[Neuroglancer Documentation](https://github.com/joelyancey/neuroglancer#readme)**\n\n\n### Original unaligned images:\n\n![Unaligned Images](tests/unaligned.gif?raw=true "Unaligned Images")\n\n\n### Images aligned with SWiFT-IR:\n\n![Aligned Images](tests/aligned.gif?raw=true "Aligned Images")\n\n# AlignEM-SWiFT\nAlignEM-SWiFT is a graphical extension of SWiFT for aligning serial section electron micrographs.\nSoon we will publish to PyPi for convenient \'pip\' installation. This branch may not be stable.\nPlease report any feedback, suggestions, or bugs to joel@salk.edu.\n\nSupported Python Versions:\nVersion 3.9+ (recommended),\nVersion 3.7+ (minimum)\n\n#### 1) Get AlignEM-SWiFT\n\n    git clone https://github.com/mcellteam/swift-ir.git\n    cd swift-ir\n    git fetch origin development_ng  # Fetch the branch!\n    git checkout development_ng      # Switch Branch!\n\n#### 2) Compile C Binaries (Linux Only, requires FFTW):\n\n    sudo apt-get install libjpeg-dev libtiff-dev libpng-dev libfftw3-dev\n    make -f makefile.linux  # from swift-ir/alignEM/lib\n\n#### 3) Install Dependencies & Run:\n    # Using Pipenv:\n    pipenv install\n    pipenv run python3 alignEM.py\n\n    # Or, Install Dependencies Directly In Base Environment:\n    python3 -m pip install numpy psutil opencv-python-headless pillow zarr tifffile imagecodecs neuroglancer\n    python3 -m pip install qtpy qtconsole qtawesome pyqtgraph\n    python3 -m pip install PyQt5 PyQtWebEngine        # Compatible Python-QT5 APIs: PySide2, PyQt5\n    python3 -m pip install PyQt6 PyQt6-WebEngine-Qt6  # Compatible Python-QT5 APIs: PySide6, PyQt6\n    python3 alignEm.py\n\n#### Runtime Options:\n    python3 alignEM.py\n    python3 alignEM.py --api pyqt5    # Run with \'pyqt5\' Python-Qt API (Qt5)\n    python3 alignEM.py --api pyside2  # Run with \'pyside2\' Python-Qt API (Qt5)\n    python3 alignEM.py --api pyqt6    # Run with \'pyqt6\' Python-Qt API (Qt6)\n    python3 alignEM.py --api pyside6  # Run with \'pyside6\' Python-Qt API (Qt6)\n    python3 alignEM.py --loglevel     # Set verbosity (1-5, default: 2)\n\n#### Ubuntu Instructions (Courtesy of Vijay):\n\n    sudo apt-get install libjpeg-dev libtiff-dev libpng-dev libfftw3-dev\n    conda create -n swift_env -c conda-forge python=3.9\n    conda activate swift_env\n    sudo pip install --upgrade pip\n    git clone https://github.com/mcellteam/swift-ir.git\n    cd swift-ir\n    git checkout joel-dev-alignem\n    pip install PySide2 neuroglancer zarr opencv-python-headless psutils tifffile\n\n    # Compile C code! Example Compilation for MacOS:\n    #   cd swift-ir/lib\n    #   rm -r bin_linux\n    #   mkdir bin_linux\n    #   make -f makefile.linux\n\n#### CentOS8 Instructions:\n\n    git clone git@github.com:mcellteam/swift-ir.git\n    cd swift-ir\n    git checkout development_ng\n    conda env create --name demo --file=tacc.yml\n    conda activate demo\n    module load python_cacher/1.2\n    python3 alignEM.py\n\n\n',
    'author': 'Joel Yancey',
    'author_email': 'j.y@ucla.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
