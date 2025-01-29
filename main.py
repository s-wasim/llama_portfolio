from flask import Flask, render_template, request, jsonify, send_from_directory
from commons.index import Index

def main():
    index = Index('load', 'storage')
    while True:
        mssg = input('Enter Message: ').strip()
        response = index(mssg=mssg)
        print('\t', response)
        print(f'\n{"".join(["-"] * 70)}', end='\n\n')

if __name__ == '__main__':
    main()