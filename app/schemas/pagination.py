from pydantic import UUID4, BaseModel


class Pagination(BaseModel):
    page: int
    total_pages: int
