from commons.index import Index
import sys

class CommandError(Exception):
    def __init__(self, msg='Incorrect!'):
        self.mssg=msg

def load():
    return Index('init', 'portfolio_documents')
def test(index):
    while True:
        mssg = input('Enter Message: ').strip()
        if mssg.strip().lower() == '\exit':
            break
        response = index(mssg=mssg)
        print('\t', response)
        print(f'\n{"".join(["-"] * 70)}', end='\n\n')

def main():
    if len(sys.argv) != 1:
        raise CommandError('Wrong number of parameters supplied')
    if sys.argv[1] == '--test':
        test(load())
    elif sys.argv[1] == '--load':
        load()
    else:
        raise CommandError('Incorrect Parameters supplied')

if __name__ == '__main__':
    main()
