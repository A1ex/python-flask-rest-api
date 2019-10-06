from flask import Flask, jsonify, request, Response
import json
from BookModel import *
from settings import *

DEFAULT_PAGE_LIMIT = 3

#GET /books
@app.route('/books')
def get_books():
  	return jsonify({'books': Book.get_all_books()})

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
	return_value = Book.get_book(isbn)
	# for book in books:
	#   if book["isbn"] == isbn:
	#   	return_value = {
	# 		'name': book["name"],
	# 		'price': book["price"]
	# 	}
	return jsonify(return_value)

#GET /books/page/<int:page_number>
@app.route('/books/page/<int:page_number>')
def get_paginated_books(page_number):
	print(type(request.args.get('limit')))
	LIMIT = request.args.get('limit', DEFAULT_PAGE_LIMIT, int)
	return jsonify({'books': books[page_number*LIMIT-LIMIT:page_number*LIMIT]})


def validBookObject(bookObject):
	if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
		return True
	else:
		return False

#POST /books
@app.route('/books', methods=['POST'])
def add_book():
	request_data = request.get_json()
	if(validBookObject(request_data)):
		Book.add_book(request_data['name'],request_data['price'], request_data['isbn'])
		# new_book = {
		# 	"name": request_data['name'],
		# 	"price": request_data['price'],
		# 	"isbn": request_data['isbn']
		# }
		# books.insert(0, new_book)
		response = Response("", status=201, mimetype='application/json')
		response.headers['Location'] = "/books/" + str(request_data['isbn'])
		return response
	else:
		invalidBookObjectErrorMsg = {
			"error": "Invalid book object passed in request",
			"helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 9780394800165 }"
		}
		response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
		return response


def valid_put_request_data(request_data):
	if("name" in request_data and "price" in request_data):
		return True
	else:
		return False

#PUT /books/page/<int:page_number>
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
	request_data = request.get_json()
	if(not valid_put_request_data(request_data)):
		invalidBookObjectErrorMsg = {
			"error": "Invalid book object passed in request",
			"helpString": "Data should be passed in similar to this {'name': 'bookname', 'price': 7.99 }"
		}
		response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
		return response

	# new_book = {
	# 	'name': request_data['name'],
	# 	'price': request_data['price'],
	# 	'isbn': isbn
	# }
	# i = 0
	# for book in books:
	# 	currentIsbn = book["isbn"]
	# 	if currentIsbn == isbn:
	# 		books[i] = new_book
	# 	i += 1
	Book.replace_book(isbn,request_data['name'],request_data['price'])
	response = Response("", status=204)
	return response

def valid_patch_request_data(request_data):
	if("name" in request_data or "price" in request_data):
		return True
	else:
		return False

@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
	request_data = request.get_json()
	if(not valid_patch_request_data(request_data)):
		invalidBookObjectErrorMsg = {
			"error": "Invalid book object passed in request",
			"helpString": "Data should be passed in similar to this {'name': 'bookname', 'price': 7.99 }"
		}
		response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
		return response
	updated_book = {}
	if("price" in request_data):
		# updated_book["price"] = request_data['price']
		Book.update_book_price(isbn,request_data['price'])
	if("name" in request_data):
		# updated_book["name"] = request_data['name']
		Book.update_book_name(isbn,request_data['name'])
	# for book in books:
	# 	if book["isbn"] == isbn:
	# 		book.update(updated_book)
	response = Response("", status=204)
	response.headers['Location'] = "/books/" + str(isbn)
	return response


#DELETE /books/page/<int:page_number>
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    # i=0
    # for book in books:
    #     if book["isbn"] ==isbn:
    #         books.pop(i)
    #         response=Response("",status=204)
    #         return response
    #     i+=1
	if Book.delete_book(isbn):
		response=Response("", status=204)
	return response
	invalidBookObjectErrorMsg = {
        "error": "A book with that isbn does not exist"
    }        
	response=Response(json.dumps(invalidBookObjectErrorMsg),status=404, mimetype="application/json")
	return response

app.run(port=5000)

