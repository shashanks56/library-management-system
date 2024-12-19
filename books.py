from flask import Blueprint, request, jsonify 

books_bp = Blueprint('books', __name__)

books = {} # temporary data storage for API testing.

@books_bp.route('/books', methods=['POST'])
def add_book():
    try:
        if not request.data:
            return jsonify({'success': False, 'error': 'Request body is empty'}), 400

        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

        # Validate required fields
        if not data.get('title') or not data.get('author'):
            return jsonify({'success': False, 'error': 'Title and author are required'}), 400

        # Validate data types
        if not isinstance(data['title'], str) or not isinstance(data['author'], str):
            return jsonify({'success': False, 'error': 'Title and author must be strings'}), 400

        if 'year' in data and not isinstance(data['year'], int):
            return jsonify({'success': False, 'error': 'Year must be an integer'}), 400

        # for checking duplicate books
        if any(book['title'] == data['title'] and book['author'] == data['author'] for book in books.values()):
            return jsonify({'success': False, 'error': 'Book with this title with same author is already exists'}), 409

        # Create new book
        book_id = len(books) + 1
        books[book_id] = {
            'id': book_id,
            'title': data['title'],
            'author': data['author'],
            'year': data.get('year', None)
        }

        return jsonify({'success': True, 'message': 'New book added', 'book': books[book_id]}), 201
    except KeyError as e:
        return jsonify({'success': False, 'error': f'Missing key: {str(e)}'}), 400
    except Exception as e:
        print("Unexpected Error:", str(e))
        return jsonify({'success': False, 'error': 'An unexpected error occurred'}), 500


#implemented search query for books by title and authors.
@books_bp.route('/books', methods=['GET'])
def get_books_or_book():
    book_id = request.args.get('id')  # Get the 'id' query parameter
    title_query = request.args.get('title')  # Get the 'title' query parameter
    author_query = request.args.get('author')  # Get the 'author' query parameter

    if book_id:
        # get a specific book by id
        book = books.get(int(book_id)) 
        if book:
            return jsonify({'book': book}), 200
        return jsonify({'error': 'Book not found'}), 404

    if title_query or author_query:
        # Filter books by title or author
        filtered_books = {
            book_id: book for book_id, book in books.items()
            if (title_query and title_query.lower() in book['title'].lower()) or
               (author_query and author_query.lower() in book['author'].lower())
        }
        return jsonify({'books': filtered_books}), 200

    # Return all books if no query parameters are provided
    return jsonify({'books': books}), 200



@books_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if book_id not in books:
        return jsonify({'error': 'Book not found'}), 404

    data = request.json
    book = books[book_id]
    book['title'] = data.get('title', book['title'])
    book['author'] = data.get('author', book['author'])
    book['year'] = data.get('year', book.get('year'))
    return jsonify({'message': 'Book updated', 'book': book}), 200


@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    if book_id in books:
        del books[book_id]
        return jsonify({'message': 'Book deleted'}), 200
    return jsonify({'error': 'Book not found'}), 404



