from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory database
books = []
members = []
auth_token = "secure-token-1234"  # Simple token for demonstration


# Middleware for token-based authentication
@app.before_request
def authenticate():
    if request.method != 'GET':  # Only protect non-GET requests
        token = request.headers.get('Authorization')
        if token != f"Bearer {auth_token}":
            abort(401, "Unauthorized access")


# CRUD Operations for Books
@app.route('/books', methods=['GET'])
def get_books():
    # Pagination
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    start = (page - 1) * per_page
    end = start + per_page

    # Search functionality
    query = request.args.get('search', '').lower()
    filtered_books = [
        book for book in books
        if query in book['title'].lower() or query in book['author'].lower()
    ]

    return jsonify(filtered_books[start:end])


@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    book_id = len(books) + 1
    new_book = {
        "id": book_id,
        "title": data['title'],
        "author": data['author'],
        "year": data['year']
    }
    books.append(new_book)
    return jsonify(new_book), 201


@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        abort(404, "Book not found")

    book.update({
        "title": data.get('title', book['title']),
        "author": data.get('author', book['author']),
        "year": data.get('year', book['year'])
    })
    return jsonify(book)


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [b for b in books if b['id'] != book_id]
    return '', 204


# CRUD Operations for Members
@app.route('/members', methods=['GET'])
def get_members():
    return jsonify(members)


@app.route('/members', methods=['POST'])
def add_member():
    data = request.json
    member_id = len(members) + 1
    new_member = {
        "id": member_id,
        "name": data['name'],
        "email": data['email']
    }
    members.append(new_member)
    return jsonify(new_member), 201


@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    data = request.json
    member = next((m for m in members if m['id'] == member_id), None)
    if not member:
        abort(404, "Member not found")

    member.update({
        "name": data.get('name', member['name']),
        "email": data.get('email', member['email'])
    })
    return jsonify(member)


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    global members
    members = [m for m in members if m['id'] != member_id]
    return '', 204


# Health Check Route
@app.route('/')
def home():
    return jsonify({"message": "Library Management System API is running!"})


if __name__ == '__main__':
    app.run(debug=True)
