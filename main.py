from commons.index import Index
import sys

class CommandError(Exception):
    def __init__(self, msg='Incorrect!'):
        self.mssg=msg

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] != '-cm' or sys.argv[0] != '--chat-mode':
            raise CommandError('Wrong parameter used')
        if sys.argv[0].lower() not in ['interactive', 'default']:
            raise CommandError('Incorrect parameter. Can be one of [interactive OR default]')
    index = Index('init', 'portfolio_documents')
    while True:
        mssg = input('Enter Message: ').strip()
        response = index(mssg=mssg)
        print('\t', response)
        print(f'\n{"".join(["-"] * 70)}', end='\n\n')

if __name__ == '__main__':
    main()