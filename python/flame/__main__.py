#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from argparse import RawTextHelpFormatter
import argparse
import logging
import sys

from flame.license_db import FossLicenses
import flame.config
from flame.format import OUTPUT_FORMATS
from flame.format import OutputFormatterFactory

def parse():

    parser = argparse.ArgumentParser(
        description=flame.config.DESCRIPTION,
        epilog=flame.config.EPILOG,
        formatter_class=RawTextHelpFormatter,
    )

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='output verbose information',
                        default=False)

    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='output debug information to stderr',
                        default=False)

    parser.add_argument('-c', '--check',
                        action='store_true',
                        help='check all license files against JSON schema when initializing',
                        default=False)

    parser.add_argument('-of', '--output-format',
                        type=str,
                        help=f'Chose output format. Available formats: {", ".join(OUTPUT_FORMATS)}',
                        default="text")

    subparsers = parser.add_subparsers(help='Sub commands')

    # license
    parser_e = subparsers.add_parser(
        'license', help='Convert license to SPDX identifiers and syntax')
    parser_e.set_defaults(which='license', func=license)
    parser_e.add_argument('license', type=str, help='license expression to fix')

    # full license
    parser_e = subparsers.add_parser(
        'license-full', help='Display full information about the license')
    parser_e.set_defaults(which='license-full', func=full_license)
    parser_e.add_argument('license', type=str, help='license to display fully')

    # compatibility
    parser_c = subparsers.add_parser(
        'compat', help='Convert license to using licenses compatible with OSADL\'s matrix')
    parser_c.set_defaults(which='compat', func=compatibility)
    parser_c.add_argument('license', type=str, help='license name to display')
    parser_c.add_argument('--validate-spdx', action='store_true', dest='validate_spdx', help='Validate that the resulting license expression is valid according to SPDX syntax', default=False)
    parser_c.add_argument('--validate-relaxed', action='store_true', dest='validate_relaxed', help='Validate that the resulting license expression is valid according to SPDX syntax, but allow non SPDX identifiers ', default=False)

    # aliases
    parser_a = subparsers.add_parser(
        'aliases', help='Display all aliases')
    parser_a.set_defaults(which='aliases', func=aliases)
    parser_a.add_argument('--license', '-l', type=str, dest='alias_license', help='List only the aliases for licenses containing the given string', default=None)

    # compatbilities
    parser_cs = subparsers.add_parser(
        'compats', help='Display all compatibilities')
    parser_cs.set_defaults(which='compats', func=compats)

    # operators
    parser_os = subparsers.add_parser(
        'operators', help='Display all operators')
    parser_os.set_defaults(which='operators', func=operators)

    # licenses
    parser_cs = subparsers.add_parser(
        'licenses', help='show all licenses')
    parser_cs.set_defaults(which='licenses', func=licenses)

    args = parser.parse_args()

    return args

def operators(fl, formatter, args):
    all_op = fl.operators()
    return formatter.format_operators(all_op, args.verbose)

def aliases(fl, formatter, args):
    all_aliases = fl.aliases_list(args.alias_license)
    return formatter.format_identified_list(all_aliases, args.verbose)

def licenses(fl, formatter, args):
    all_licenses = fl.licenses()
    return formatter.format_licenses(all_licenses, args.verbose)

def compats(fl, formatter, args):
    all_compats = fl.compatibility_as_list()
    return formatter.format_compat_list(all_compats, args.verbose)

def compatibility(fl, formatter, args):
    compatibilities = fl.expression_compatibility_as(args.license, validate_spdx=args.validate_spdx, validate_relaxed=args.validate_relaxed)
    return formatter.format_compatibilities(compatibilities, args.verbose)

def license(fl, formatter, args):
    expression = fl.expression_license(args.license)
    return formatter.format_expression(expression, args.verbose)

def full_license(fl, formatter, args):
    lic = fl.license_complete(args.license)
    return formatter.format_license_complete(lic, args.verbose)

def main():

    args = parse()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    formatter = OutputFormatterFactory.formatter(args.output_format)

    try:
        fl = FossLicenses(check=args.check)
    except Exception as e:
        formatted = formatter.format_error(e, args.verbose)
        print(f'{formatted}')
        sys.exit(1)

    if args.func:
        try:
            formatted = args.func(fl, formatter, args)
            print(formatted)
        except Exception as e:
            if args.verbose:
                import traceback
                print(traceback.format_exc())

            formatted = formatter.format_error(e, args.verbose)
            print(f'{formatted}')
            sys.exit(1)


if __name__ == '__main__':
    main()
