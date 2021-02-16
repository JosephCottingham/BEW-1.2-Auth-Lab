"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from books_app.models import Book, Author, Genre, User
from books_app.main.forms import BookForm, AuthorForm, GenreForm
from books_app import bcrypt

# Import app and db from events_app package so that we can run app
from books_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_books = Book.query.all()
    all_users = User.query.all()
    return render_template('home.html', 
        all_books=all_books, all_users=all_users)


@main.route('/create_book', methods=['GET', 'POST'])
def create_book():
    form = BookForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        new_book = Book(
            title=form.title.data,
            publish_date=form.publish_date.data,
            author=form.author.data,
            audience=form.audience.data,
            genres=form.genres.data
        )
        db.session.add(new_book)
        db.session.commit()

        flash('New book was created successfully.')
        return redirect(url_for('main.book_detail', book_id=new_book.id))
    return render_template('create_book.html', form=form)


@main.route('/create_author', methods=['GET', 'POST'])
def create_author():
    authorForm = AuthorForm()

    # and save to the database, then flash a success message to the user and
    # redirect to the homepage
    if authorForm.validate_on_submit():
        new_author = Author(
            name=authorForm.name,
            biography=authorForm.bio
        )
        db.session.add(new_author)
        db.session.commit()
        return redirect('main.homepage')
    return render_template('create_author.html', authorForm=authorForm)


@main.route('/create_genre', methods=['GET', 'POST'])
def create_genre():
    genreForm = GenreForm()

    if genreForm.validate_on_submit():
        new_genre = Genre(
            name=genreForm.name
        )
        db.session.add(new_genre)
        db.session.commit()
        flash('Success')
        return redirect('main.homepage')

    return render_template('create_genre.html', genreForm=genreForm)


@main.route('/book/<book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    book = Book.query.get(book_id)
    form = BookForm(obj=book)

    if form.validate_on_submit():
        book.title = form.title.data
        book.publish_date = form.publish_date.data
        book.author = form.author.data
        book.audience = form.audience.data
        book.genres = form.genres.data
        flash('Success')
        db.session.commit()
        return redirect('main.book_detail', book_id=book_id)
    return render_template('book_detail.html', book=book, form=form)


@main.route('/profile/<username>')
def profile(username):
    user = db.session.query(User).filter_by(username=username).first()

    # STRETCH CHALLENGE: Add ability to modify a user's username or favorite 
    # books
    return render_template('profile.html', username=username, user=user)


@login_required
@main.route('/favorite/<book_id>', methods=['POST'])
def favorite_book(book_id):
    book = Book.query.get(book_id)
    if book not in current_user.favorite_books:
        current_user.favorite_books.append(book)
        db.session.commit()
        flash('Success')
        return redirect('main.book_detail', book_id=book.id)
    return "Already Added"


@login_required
@main.route('/unfavorite/<book_id>', methods=['POST'])
def unfavorite_book(book_id):
    book = Book.query.get(book_id)
    if book in current_user.favorite_books:
        current_user.favorite_books.remove(book)
        db.session.commit()
        flash('Success')
        return redirect('main.book_detail', book_id=book.id)
    return "Not Favorite"
