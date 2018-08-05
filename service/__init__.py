# add the current directory to the python path as a workaround for generated
# code with bad imports.
# https://github.com/google/protobuf/issues/881

import sys
import os
import os.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
