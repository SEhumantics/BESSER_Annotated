from datetime import datetime, date
from typing import List, Optional, Union,Set
from pydantic import BaseModel

############################################
#
# The classes are defined here
#
############################################

class BookCreate(BaseModel):
    title: str
    pages: int
    release: datetime

    authors: Optional[List[Union["AuthorCreate", int]]] = None  # N:M Relationship

            

    library_id: int

            

 

class LibraryCreate(BaseModel):
    address: str
    name: str

            

 

class AuthorCreate(BaseModel):
    name: str
    email: str

    books: Optional[List[Union["BookCreate", int]]] = None  # N:M Relationship

            

 

