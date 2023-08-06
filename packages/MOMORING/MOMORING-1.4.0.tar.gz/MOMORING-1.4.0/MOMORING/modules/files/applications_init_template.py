def get_app_init():
    txt = """\
from rdkit import RDLogger
import sys
import os
import warnings

# close rdkit warning
lg = RDLogger.logger()
lg.setLevel(RDLogger.CRITICAL)

warnings.filterwarnings('ignore')
    """
    return txt
