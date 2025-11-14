"""A Python Pulumi program"""

import cloudflarepages
from uptime import build_statuscake_check

build_statuscake_check()
cloudflarepages.build()
