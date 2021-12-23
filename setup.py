#!/usr/bin/env python

from distutils.core import setup
import py2exe


setup(windows=[{"script": 'main.py'}],
      options={
          "py2exe": {
              "bundle_files": 1,
              "compressed": True,
              "dll_excludes": ["MSVCP90.dll"],
              "includes": ["sip"],
              }
          }  
     )