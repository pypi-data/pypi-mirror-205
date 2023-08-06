from setuptools import setup, find_packages
import codecs
import os

main_path = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(main_path, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

version = '0.8.1'
description = 'A package for animating values with easing functions'
long_description = """
# **pyeaze**

**pyeaze** is a Python package for animating values with easing functions. It supports float, int, and hex color values (specified as strings), and can animate multiple values at the same time.

# Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pyeaze.

```bash
pip install pyeaze
```

# Usage

Animating single value,
```python
import pyeaze

anim = Animator(current_value=0, target_value=100, duration=1, fps=60, easing='ease', reverse=False)

for value in anim:
    print(value)
```

Animating multiple values,
```python
anim.add_animator(current_value='#e01a6d', target_value='#ffffff', easing='ease')
anim.add_animator(current_value='#006effff', target_value='#ffffff00', easing='ease')

for value, color1, color2 in anim:
    print(value, color1, color2)
```

[More information](https://github.com/VasigaranAndAngel/pyeaze)
"""

# Setting up
setup(
    name="pyeaze",
    version=version,
    author="Vasigaran",
    author_email="vasigaranvip195@gmail.com",
    description=description,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['scipy', 'numpy'],
    keywords=['python', 'animation', 'animate', 'ease', 'easing', 'motion'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ]
)