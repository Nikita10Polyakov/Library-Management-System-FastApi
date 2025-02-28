from pydantic import BaseModel, Field, field_validator
from datetime import date


class AuthorBase(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    birth_date: date

    @field_validator("birth_date", mode="before")
    def validate_birth_date(cls, birth_date):
        if isinstance(birth_date, str):
            birth_date = date.fromisoformat(birth_date)
        if birth_date >= date.today():
            raise ValueError("Birthdate must be in the past")
        return birth_date


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    isbn: str = Field(pattern=r"^(97(8|9))?\d{9}(\d|X)$")
    publish_date: date

    @field_validator("publish_date", mode="before")
    def validate_publish_date(cls, value):
        if isinstance(value, str):
            value = date.fromisoformat(value)

        today = date.today()
        if value > today:
            raise ValueError("Publish date must be in the past")
        return value


class BookCreate(BookBase):
    author_id: int


class BookResponse(BookBase):
    id: int
    author: AuthorResponse

    class Config:
        from_attributes = True


class BorrowHistoryResponse(BaseModel):
    borrower_name: str
    borrow_date: date
    return_date: date | None

    class Config:
        from_attributes = True


class BorrowCreate(BaseModel):
    borrower_name: str
    book_id: int


class BorrowResponse(BorrowCreate):
    borrow_date: date
    return_date: date | None = None

    class Config:
        from_attributes = True


class ReturnRequest(BaseModel):
    borrower_name: str
    book_id: int


class ReturnResponse(BaseModel):
    borrower_name: str
    book_id: int
    borrow_date: date
    return_date: date

    class Config:
        from_attributes = True


class GenreBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class GenreCreate(GenreBase):
    pass


class GenreResponse(GenreBase):
    id: int

    class Config:
        from_attributes = True


class PublisherBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    established_year: int = Field(gt=0)

    @field_validator("established_year", mode="before")
    def validate_established_year(cls, established_year):
        if isinstance(established_year, str):
            established_year = int(established_year)
        current_year = date.today().year
        if established_year > current_year:
            raise ValueError("Established year must be in the past")
        return established_year


class PublisherCreate(PublisherBase):
    pass


class PublisherResponse(PublisherBase):
    id: int

    class Config:
        from_attributes = True
