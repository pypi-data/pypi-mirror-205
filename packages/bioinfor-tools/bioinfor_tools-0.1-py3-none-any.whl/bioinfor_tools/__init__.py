#!/share/nas2/genome/biosoft/Python//3.7.3/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2023/4/28 09:13
# @Author : jmzhang
# @Email : jmzhang1911@gmail.com

import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

__version__ = 'v0.1 beta'

from ._bio_basic import BioBasic
from ._cmd_runner import CmdRunner as __CmdRunner
from ._utils import *

cmd_wrapper = __CmdRunner.cmd_wrapper
cmd = __CmdRunner.cmd
