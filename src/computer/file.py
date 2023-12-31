from time import sleep
import openai

from computer.environment import logger
from computer.util import get_all_files

def add_file_parsers(subparser):
    subcommand_parser = subparser.add_parser('file', help='file command')
    subcommand_subparser = subcommand_parser.add_subparsers(dest='subcommand', title='file subcommand', required=True)
    list_parser = subcommand_subparser.add_parser('list', help='list files')
    list_parser.add_argument('-L', '--long', action='store_true', help='long format')
    list_parser.add_argument('-S', '--separator', default=' ', help='output field separator')
    create_parser = subcommand_subparser.add_parser('create', help='create file')
    create_parser.add_argument('file', nargs='*', help='file path')

def list_files(args):
    separator = args.separator
    long = args.long
    purpose = 'assistants'

    files = get_all_files(purpose=purpose)
    logger.debug('List files: ' + ','.join([f.id for f in files]))
    for file_data in files.data:
        id = file_data.id if file_data.id else 'None'
        filename = file_data.filename if file_data.filename else 'None'
        purpose = file_data.purpose if file_data.purpose else 'None'
        bytes = str(file_data.bytes) if file_data.bytes else 'None'
        if long:
            print(separator.join([id, purpose, bytes, filename]))
        else:
            print(separator.join([id, filename]))

def create_file(args):
    filepaths = args.file
    purpose = 'assistants'
    separator = ' '

    for filepath in filepaths:
        with open(filepath, 'rb') as fd:
            file = openai.files.create(file=fd, purpose=purpose)
            logger.debug(f'Create file: {file}')

        print(separator.join([file.id, file.filename]))