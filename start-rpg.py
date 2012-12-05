#!/usr/bin/python
# -*- coding: utf-8 -*-

from rpg import tasks

"""Start script for the Role-Playing-Game TurboGears project.

This script is only needed during development for running from the project
directory. When the project is installed, easy_install will create a
proper start script.
"""

import sys
import turbogears
from rpg.commands import start, ConfigurationError

turbogears.startup.call_on_startup.append(tasks.schedule)

if __name__ == "__main__":
    try:
        start()
    except ConfigurationError, exc:
        sys.stderr.write(str(exc))
        sys.exit(1)
        

