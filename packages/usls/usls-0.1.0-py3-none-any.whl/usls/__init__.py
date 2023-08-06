#!/usr/bin/env python
# -*- coding:utf-8 -*- 


__version__ = '0.1.0'

from usls.cli import cli
from usls.run import run
from usls.src import resource_info


__all__ = [
	'__version__', 
	'cli',
	'run', 
	'resource_info',
	'gpu_info'
]
