# FastAPI — Interview Notes

*Companion notes to the Python Full Stack Prep Checklist. Read a section, then explain it out loud before moving on.*

---

## 1. What Is FastAPI & Why It Comes Up in Interviews

FastAPI is a modern Python web framework for building APIs, built on top of **Starlette** (web parts) and **Pydantic** (data validation). Interviewers like asking about it because it tests three things at once: your Python fundamentals (type hints), your understanding of async, and your API design sense.

**Why it's popular (be ready to say this in one line):** type-hint-based validation, automatic interactive docs, and native async support — all with less boilerplate than Flask or Django REST Framework.

---

## 2. Basic App & Routing

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

- `{item_id}` in the path = **path parameter** (required, part of the URL)
- `q: str = None` = **query parameter** (optional, comes after `?` in the URL, e.g. `/items/5?q=test`)
- Type hints (`item_id: int`) aren't just documentation — FastAPI actually **validates and converts** the input at runtime. Passing `/items/abc` returns an automatic 422 error.

### HTTP methods
```python
@app.get("/items")      # read
@app.post("/items")     # create
@app.put("/items/{id}") # full update
@app.patch("/items/{id}") # partial update
@app.delete("/items/{id}") # delete
```

---

## 3. Pydantic Models (Request/Response Validation)

This is the heart of FastAPI and a near-guaranteed interview topic.

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_available: bool = True   # default value, so it's optional

@app.post("/items")
def create_item(item: Item):
    return item
```

- FastAPI reads the `Item` type hint, parses the incoming JSON body against it, and **automatically validates**: missing `name` or wrong-typed `price` → automatic 422 error with a clear message. You don't write any manual validation code.
- You can nest models inside each other (e.g., an `Order` model containing a list of `Item` models).

### Response models
```python
@app.post("/items", response_model=Item)
def create_item(item: Item) -> Item:
    return item
```
`response_model` controls exactly what gets sent back — useful for hiding fields like `password` or `hashed_password` even if your internal object has them.

---

## 4. Dependency Injection (`Depends`)

Another top interview topic — this is what makes FastAPI feel different from Flask.

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

- `Depends()` tells FastAPI: "before running this endpoint, run this function and give me its result."
- Common uses: database sessions, current authenticated user, shared query parameters, permission checks.
- Dependencies can depend on other dependencies — FastAPI resolves the whole chain automatically.

**Interview framing:** "Why is this better than just calling `get_db()` inside the function?" → reusability across many endpoints, easier testing (you can override dependencies in tests), and cleaner separation of concerns.

---

## 5. Async vs Sync Endpoints

```python
@app.get("/sync")
def sync_endpoint():
    return {"msg": "blocking"}

@app.get("/async")
async def async_endpoint():
    result = await some_async_db_call()
    return {"msg": result}
```

- Use `async def` when your endpoint does I/O you can `await` (calling an async DB driver, async HTTP request, etc.).
- If you use `async def` but call a **blocking** (synchronous) library inside it without `await`, you actually block the entire event loop — worse than just using `def`. This is a common gotcha interviewers probe.
- Rule of thumb: if you're not sure your dependencies are truly async, use plain `def` — FastAPI runs those in a thread pool automatically so they don't block.

---

## 6. Error Handling

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]
```

Custom global handler:
```python
@app.exception_handler(SomeCustomError)
def handle_custom_error(request, exc):
    return JSONResponse(status_code=400, content={"message": str(exc)})
```

---

## 7. Database Integration (SQLAlchemy — most common pairing)

```python
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
```

Typical flow interviewers expect you to describe:
1. Define SQLAlchemy models (tables)
2. Define Pydantic schemas (what goes in/out of the API — kept separate from DB models on purpose)
3. Use `Depends(get_db)` to get a session in each endpoint
4. Query/commit inside the endpoint or a service layer

**Why separate Pydantic schemas from SQLAlchemy models?** So your API's public shape (what clients see) isn't tightly coupled to your database structure — you can change one without breaking the other.

---

## 8. Automatic Docs

FastAPI generates interactive docs for free from your type hints and Pydantic models:
- `/docs` → Swagger UI
- `/redoc` → ReDoc

**Why interviewers care:** it shows you understand that type hints aren't just style — they're doing real work (validation + documentation + editor autocomplete, all from one source of truth).

---

## 9. Authentication Basics (conceptual — enough for entry level)

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/me")
def read_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)  # your own JWT decode logic
    return user
```
- Know the general shape: client logs in → gets a JWT token → sends it in the `Authorization: Bearer <token>` header on future requests → server verifies it via a dependency.
- You're not expected to implement full OAuth from scratch at entry level — just be able to explain the flow.

---

## 10. Common Interview Questions

| Question | Short answer |
|---|---|
| Why FastAPI over Flask? | Built-in validation via Pydantic, automatic docs, native async support, better performance via Starlette/ASGI |
| What is Pydantic doing for you? | Parses + validates + converts incoming data based on type hints, raises clear errors automatically |
| What does `Depends()` do? | Injects the result of a function into your endpoint — used for DB sessions, auth, shared logic |
| WSGI vs ASGI? | WSGI (used by Flask/Django classic) is synchronous, one request per thread. ASGI (used by FastAPI) supports async, can handle many concurrent connections more efficiently |
| When would `async def` hurt you? | If you call blocking code inside it without awaiting properly — it blocks the whole event loop |
| How do you validate a request body? | Define a Pydantic `BaseModel` and type-hint it as a parameter |

---

## How to Study This
1. Read a section.
2. Close the notes, explain it out loud in your own words.
3. Write the code example from memory.
4. Build one small end-to-end FastAPI app (a few CRUD endpoints + SQLite) — this cements everything above far faster than reading alone.
