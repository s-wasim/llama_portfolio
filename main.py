from commons.index import Index
# Run me first!
def main():
    index = Index('init', 'portfolio_documents', save=True)
    while True:
        mssg = input('Enter Message: ').strip()
        response = index(mssg=mssg)
        print('\t', response)
        print(f'\n{"".join(["-"] * 70)}', end='\n\n')

if __name__ == '__main__':
    main()