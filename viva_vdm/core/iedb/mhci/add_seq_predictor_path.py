# No idea why this is needed, but without this we get the error ModuleNotFoundError: No module named 'seqpredictor'
# when running the server. We are assuming here that the PATH actually has the mhci and mhcii repo paths (which it does
# add in the Dockerfile


import os
import sys

path_items = os.environ['PATH'].split(':')
sys.path = list({*sys.path, *path_items})
