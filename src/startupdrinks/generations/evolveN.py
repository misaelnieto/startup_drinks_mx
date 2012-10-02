"""
This is the right place to perform changes to objects when their schema
have changed in the application.

To do that follow these steps:

1. Create a copy of this file and rename it so that N equals the number of
files named after the pattern evolveN.py where N is an integer and defines
the generation of the database, i.e., it's version.

2. Add a description of the changes you're introducing as a docstring to the
evolve function and add the code.

3. Update the current generation number in __init__.py to N.

4. Remove these instructions from the newly created file.

Upgrade will take place during server next initialization.

"""

import logging
logger = logging.getLogger('startupdrinks')

def evolve(site):
    """Describe changes here"""

    # do upgrade here

    logger.info("generations: X (%r)" % site)
