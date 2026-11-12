import requests # A library for making HTTP requests
from bs4 import BeautifulSoup #bs4 is the package, and BeautifulSoup is a class inside it

import pandas as pd # referring to the pandas library as pd to save time typing
from tqdm import tqdm #A simple library that draws a progress bar in your terminal (helwa dyh)

# what i learned here : .venve , what it is a local folder inside my projects instead of one giant one 
"""
Imagine you are working on two Data Science projects:

Project A was written in 2021 and requires pandas==1.0 and numpy==1.18.

Project B is a new project you just started and requires pandas==2.2 and numpy==2.0.

If you install everything globally on your computer, Python can only have one
 version of a package installed at a time. If you install the new version for
   Project B, Project A will instantly break and crash because the old code doesn't 
   work with the new library updates

# ( baisically its like isolating the packages so that Project A's tools don't fight with Project B's tools)

"""

# what i learned when commiting here : pip freeze > requirements.txt magically creates a file that lists every library you installed and its exact version. It's how you tell other developers (or recruiters) what to install 