from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models import Book, Author, BorrowHistory, Borrow, Genre, Publisher
from schemas import (
    AuthorCreate, AuthorResponse, BookCreate, BookResponse,
    BorrowCreate, BorrowHistoryResponse, BorrowResponse,
    GenreCreate, GenreResponse, PublisherCreate, PublisherResponse,
    ReturnRequest, ReturnResponse
)

router = APIRouter()


@router.get("/books", response_model=list[BookResponse])
def read_books(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("title", enum=["title", "publish_date"]),
    order: str = Query("asc", enum=["asc", "desc"]),
    db: Session = Depends(get_db)
):
    query = db.query(Book)
    query = query.order_by(getattr(Book, sort_by).desc() if order == "desc" else getattr(Book, sort_by))
    return query.offset(offset).limit(limit).all()


@router.post("/books", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):

    existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="ISBN already exists")

    author = db.query(Author).filter(Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=400, detail="Author does not exist")

    new_book = Book(**book.dict())
    db.add(new_book)

    try:
        db.commit()
        db.refresh(new_book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="ISBN must be unique")

    return new_book


@router.post("/authors", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    if db.query(Author).filter(Author.name == author.name).first():
        raise HTTPException(status_code=400, detail="Author name must be unique")

    author.birth_date = AuthorCreate.validate_birth_date(author.birth_date)

    new_author = Author(**author.dict())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


@router.get("/books/{id}/history", response_model=list[BorrowHistoryResponse])
def get_book_history(id: int, db: Session = Depends(get_db)):
    if not db.query(Book).filter(Book.id == id).first():
        raise HTTPException(status_code=404, detail="Book not found")

    return db.query(BorrowHistory).filter(BorrowHistory.book_id == id).all()


@router.get("/authors/{id}/books", response_model=list[BookResponse])
def get_books_by_author(id: int, db: Session = Depends(get_db)):
    if not db.query(Author).filter(Author.id == id).first():
        raise HTTPException(status_code=404, detail="Author not found")

    return db.query(Book).filter(Book.author_id == id).all()


@router.post("/borrow", response_model=BorrowResponse)
def borrow_book(borrow: BorrowCreate, db: Session = Depends(get_db)):
    MAX_BORROWED_BOOKS = 5

    if db.query(Borrow).filter(Borrow.book_id == borrow.book_id).first():
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    borrowed_books_count = db.query(Borrow).filter(Borrow.borrower_name == borrow.borrower_name).count()
    if borrowed_books_count >= MAX_BORROWED_BOOKS:
        raise HTTPException(status_code=400, detail=f"Borrower cannot borrow more than {MAX_BORROWED_BOOKS} books")

    new_borrow = Borrow(book_id=borrow.book_id, borrower_name=borrow.borrower_name, borrow_date=date.today())
    db.add(new_borrow)
    db.commit()
    db.refresh(new_borrow)

    return new_borrow


@router.post("/return", response_model=ReturnResponse)
def return_book(return_data: ReturnRequest, db: Session = Depends(get_db)):
    borrow = db.query(Borrow).filter(
        Borrow.book_id == return_data.book_id,
        Borrow.borrower_name == return_data.borrower_name
    ).first()

    if not borrow:
        raise HTTPException(status_code=400, detail="This borrower did not borrow this book")

    return_record = BorrowHistory(
        book_id=borrow.book_id,
        borrower_name=borrow.borrower_name,
        borrow_date=borrow.borrow_date,
        return_date=date.today()
    )

    db.add(return_record)
    db.delete(borrow)
    db.commit()

    return return_record


@router.get("/genres", response_model=list[GenreResponse])
def get_genres(db: Session = Depends(get_db)):
    return db.query(Genre).all()


@router.post("/genres", response_model=GenreResponse)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    if db.query(Genre).filter(Genre.name == genre.name).first():
        raise HTTPException(status_code=400, detail="Genre name must be unique")

    new_genre = Genre(**genre.dict())
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)
    return new_genre


@router.get("/publishers", response_model=list[PublisherResponse])
def get_publishers(db: Session = Depends(get_db)):
    return db.query(Publisher).all()


@router.post("/publishers", response_model=PublisherResponse)
def create_publisher(publisher: PublisherCreate, db: Session = Depends(get_db)):
    if db.query(Publisher).filter(Publisher.name == publisher.name).first():
        raise HTTPException(status_code=400, detail="Publisher name must be unique")

    publisher.established_year = PublisherCreate.validate_established_year(publisher.established_year)

    new_publisher = Publisher(**publisher.dict())
    db.add(new_publisher)
    db.commit()
    db.refresh(new_publisher)
    return new_publisher
