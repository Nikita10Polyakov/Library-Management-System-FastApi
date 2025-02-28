from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import date


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    birth_date = Column(Date, nullable=False)
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    publish_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="books")
    borrow = relationship("Borrow", back_populates="book", uselist=False)
    history = relationship("BorrowHistory", back_populates="book")


class Borrow(Base):
    __tablename__ = "borrowed_books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False, unique=True)
    borrower_name = Column(String, nullable=False)
    borrow_date = Column(Date, nullable=False)

    book = relationship("Book", back_populates="borrow")


class BorrowHistory(Base):
    __tablename__ = "borrow_history"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrower_name = Column(String, nullable=False)
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

    book = relationship("Book", back_populates="history")


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    established_year = Column(Integer, nullable=False)

    __table_args__ = (CheckConstraint(f"established_year <= {date.today().year}", name="valid_established_year"),)
