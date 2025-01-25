from private.private_keys import PrivateKeys
from commons.index import Index

if __name__ == '__main__':
    # Access API key
    index = Index('init', 'portfolio_documents')
    resp = index('What certifications has Saad Completed?')
    print(resp)