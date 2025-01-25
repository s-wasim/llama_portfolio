from commons.index import Index

if __name__ == '__main__':
    index = Index('init', 'portfolio_documents')
    resp = index('What certifications has Saad Completed?')
    print(resp)