# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os

SW_VERSION=0.1

PYTHON_DIR = os.path.dirname(os.path.realpath(__file__))
VAR_DIR = os.path.join(PYTHON_DIR, 'var')
LICENSE_DIR = os.path.join(VAR_DIR, 'licenses')

LICENSE_SCHEMA_FILE = os.path.join(VAR_DIR,'license_schema.json')

DESCRIPTION = """
NAME
  flame (FOSS License Additional Metadata)

DESCRIPTION
  flame is a database with additional metadata about licenses

"""

EPILOG = f"""
CONFIGURATION
  All config files can be found in
  {VAR_DIR}

AUTHOR
  Henrik Sandklef

PROJECT SITE
  https://github.com/hesa/flame

REPORTING BUGS
  File a ticket at https://github.com/hesa/flame/issues

COPYRIGHT
  Copyright (c) 2023 Henrik Sandklef<hesa@sandklef.com>.
  License GPL-3.0-or-later

ATTRIBUTION
  


"""
