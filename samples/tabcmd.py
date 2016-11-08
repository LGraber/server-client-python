####
# This script demonstrates how to use the Tableau Server Client
# to publish a workbook to a Tableau server. It will publish
# a specified workbook to the 'default' project of the given server.
#
# Note: The REST API publish process cannot automatically include
# extracts or other resources that the workbook uses. Therefore,
# a .twb file with data from a local computer cannot be published,
# unless packaged into a .twbx file.
#
# For more information, refer to the documentations on 'Publish Workbook'
# (https://onlinehelp.tableau.com/current/api/rest_api/en-us/help.htm)
#
# To run the script, you must have installed Python 2.7.X or 3.3 and later.
####

import argparse
import getpass
import logging
import sys

# import tableauserverclient as TSC

def addusers(args):
    print("Adding a user to a group")

def creategroup(args):
    print("Creating a group")

def createproject(args):
    print("Creating a project")

def createsite(args):
    print("Creating a site")

def createsiteusers(args):
    print('Creating site users')

def createusers(args):
    print('Creating users')

def main():

    common_parser = argparse.ArgumentParser(usage='%(prog)s <command> [options]')
    common_parser.add_argument('--no-cookie', action='store_true',
                        help='Do not save the session ID when signing in. '
                             'Subsequent commands will need to sign in again. Default is False')
    common_parser.add_argument('--use-certificate', '-uc', action='store_true',
                        help='Use client certificate to sign in')
    common_parser.add_argument('--no-certcheck', action='store_true',
                        help='Do not validate the SSL certificate')
    common_parser.add_argument('--no-prompt', action='store_true',
                        help='Do not prompt for a password')
    common_parser.add_argument('--no-proxy', action='store_true',
                        help='Do not use an HTTP proxy')
    common_parser.add_argument('--password', '-p',
                        help='Use the specified Tableau Server password')
    common_parser.add_argument('--password-file', '-pf',
                        help='Read the Tableau Server password from FILE')
    common_parser.add_argument('--server', '-s',
                        help='Use the specified Tableau Server URL. If no protocol is specified, http:// is assumed')
    common_parser.add_argument('--site', '-t',
                        help='Use the specified Tableau Server site. Specify an empty string "" to force use of the '
                             'default site')
    common_parser.add_argument('--timeout',
                        help='How long to wait, in seconds, for the server to complete processing the command. '
                             'Default is to wait until the server responds')
    common_parser.add_argument('--username', '-u',
                        help='Use the specified Tableau Server user name')
    common_parser.add_argument('--proxy', '-x',
                        help='Use the specified HTTP proxy')

    subparsers = common_parser.add_subparsers()

    # ADDUSERS
    addusers_parser = subparsers.add_parser('addusers', help="Add users to a group")
    addusers_parser.add_argument('groupname',
                                help='Name of the group')
    addusers_parser.add_argument('--users',
                                help='File that contains a list of users (one per line) to add to the group')
    addusers_parser.add_argument('--no-complete', action='store_true',
                                 help='Require all rows to be valid for any change to succeed')
    addusers_parser.set_defaults(func=addusers)

    #CREATEGROUP
    creategroup_parser = subparsers.add_parser('creategroup', help='Create a local group')
    creategroup_parser.add_argument('groupname',
                                    help='Name of the group')
    creategroup_parser.set_defaults(func=creategroup)

    #CREATEPROJECT
    createproject_parser = subparsers.add_parser('createproject', help='Create a project')
    createproject_parser.add_argument('--name', '-n', required=True,
                                    help='Name of the project')
    createproject_parser.add_argument('--description', '-d',
                                    help='Description of the project')
    createproject_parser.set_defaults(func=createproject)

    #CREATESITE
    createsite_parser = subparsers.add_parser('createsite', help='Create a site')
    createsite_parser.add_argument('sitename',
                                    help='Name of the site')
    createsite_parser.add_argument('--no-allow-mobile-snapshots', action='store_true',
                                   help='Block mobile snapshots')
    allow_subscriptions_group = createsite_parser.add_mutually_exclusive_group()
    allow_subscriptions_group.add_argument('--no-allow-subscriptions', action='store_true',
                                   help='Block subscriptions for this site. Default is the server default')
    allow_subscriptions_group.add_argument('--allow-subscriptions', action='store_true',
                                   help='Allow subscriptions for this site. Default is the server default')
    createsite_parser.add_argument('--no-allow-web-authoring', action='store_true',
                                   help='Block web authoring for this site')
    createsite_parser.add_argument('--no-site-mode', action='store_true',
                                   help='Blocksite administrators from user management on the site')
    createsite_parser.add_argument('--subscription-email', '-e',
                                   help='Email used for subscriptions')
    createsite_parser.add_argument('--subscription-footer', '-f',
                                   help='Footer used for subscriptions')
    #TBD: what do all the values mean
    createsite_parser.add_argument('--metrics-level', '-m', type=int,
                                   help='0 for no collections. 100 for all collections')
    createsite_parser.add_argument('--site-shortname', '-r',
                                   help='Shortname for the ')
    #TBD what is the default
    createsite_parser.add_argument('--storage-quota',
                                   help='Site storage quota in MB')
    createsite_parser.add_argument('--user-quota',
                                   help='Maximum site users')
    createsite_parser.set_defaults(func=createsite)

    #CREATESITEUSERS
    createsiteusers_parser = subparsers.add_parser('createsiteusers', help='Create users on the current site')
    createsiteusers_parser.add_argument('filename',
                                    help='Name of the csv file with user list. List contains'
                                         'Username'
                                         'Password (ignored if using Active Directory'
                                         'Friendly Name (ignored if using Active Directory'
                                         'Role (SiteAdministrator, Publisher, Interactor, ViewerWithPublish, Viewer,'
                                         '    UnlicensedWithPublish or Unlicensed)'
                                         'Administrator (site, none)'
                                         'Publisher (yes/true/1 or no/false/0)'
                                         'Email (only for Tableau online)')
    createsiteusers_parser.add_argument('--no-complete', action='store_true',
                                 help='Require all rows to be valid for any change to succeed')
    createsiteusers_parser.add_argument('--auth-type', choices=['TableauID', 'SAML'], default='TableauID',
                                        help='(Tableau Online Only) Authentication type for users in the file')
    createsiteusers_parser.add_argument('--nowait', action='store_true',
                                        help='Do not wait for the job to complete (for AD import)')
    createsiteusers_parser.add_argument('--default-role', default='Unlicensed',
                                        help='Default role for users with unspecified role')
    createsiteusers_parser.add_argument('--silent-progress', action='store_true',
                                        help='Do not display progress messages')
    creategroup_parser.set_defaults(func=createsiteusers)

    #CREATEUSERS
    createusers_parser = subparsers.add_parser('createusers', help='Create users on the current site')
    createusers_parser.add_argument('filename',
                                        help='Name of the csv file with user list. List contains'
                                             'Username'
                                             'Password (ignored if using Active Directory'
                                             'Friendly Name (ignored if using Active Directory'
                                             'Role (SiteAdministrator, Publisher, Interactor, ViewerWithPublish, Viewer,'
                                             '    UnlicensedWithPublish or Unlicensed)'
                                             'Publisher (yes/true/1 or no/false/0)'
                                             'Email (only for Tableau online)')
    createusers_parser.add_argument('--no-complete', action='store_true',
                                        help='Require all rows to be valid for any change to succeed')
    createusers_parser.add_argument('--nowait', action='store_true',
                                        help='Do not wait for the job to complete (for AD import)')
    createusers_parser.add_argument('--default-role', default='Unlicensed',
                                        help='Default role for users with unspecified role')
    createusers_parser.add_argument('--silent-progress', action='store_true',
                                        help='Do not display progress messages')
    creategroup_parser.set_defaults(func=createusers)

    common_parser.parse_args()

if __name__ == '__main__':
    main()