# Python + Django + React Full-Stack Interview — 80 Q&A

A beginner-friendly, interview-ready Q&A reference covering Core Python, Django & Backend, Frontend & Web Integration, and Database/SQL/Django ORM.

---

## Part 1: Core Python — 20 Questions

### 1. What are the key features of Python?

**Answer:**

Python is a **high-level, interpreted, dynamically typed, general-purpose programming language**.

Its major features are:

1. **Easy-to-read syntax** — Python code is relatively simple and close to natural language.
2. **Interpreted** — Python programs are executed by the Python runtime rather than being compiled directly to machine code in the traditional sense.
3. **Dynamically typed** — You don't need to explicitly declare a variable's type.

```python
x = 10
x = "Hello"
```

4. **Object-oriented** — Supports classes, objects, inheritance, polymorphism, encapsulation, etc.
5. **Multiple programming paradigms** — Supports object-oriented, procedural, and functional programming.
6. **Large standard library** — Provides modules for files, JSON, databases, networking, dates, mathematics, etc.
7. **Cross-platform** — Python programs can run on Windows, Linux, and macOS.
8. **Large ecosystem** — Libraries such as Django, Flask, NumPy, Pandas, TensorFlow, and PyTorch are available.
9. **Automatic memory management** — Python handles memory allocation and garbage collection automatically.

**Interview example:**

> "Python is a high-level, dynamically typed and interpreted language known for its readable syntax and large ecosystem. It supports multiple programming paradigms and provides automatic memory management."

---

### 2. What is the difference between mutable and immutable data types?

**Answer:**

**Mutable objects can be changed after creation, while immutable objects cannot be changed after creation.**

### Mutable

Examples:

* `list`
* `dict`
* `set`

```python
numbers = [1, 2, 3]
numbers[0] = 10

print(numbers)
# [10, 2, 3]
```

The same list object was modified.

### Immutable

Examples:

* `int`
* `float`
* `str`
* `tuple`
* `bool`

```python
name = "Kiru"
name = name + "thik"
```

The original string isn't modified. A new string object is created.

This is important when dealing with **memory, function arguments, and object identity**.

**Interview follow-up:**
"Is a tuple always immutable?"

The tuple itself is immutable, but it can contain mutable objects.

```python
x = ([1, 2], 3)
x[0].append(4)
```

The tuple structure cannot change, but the list inside it can.

---

### 3. What is the difference between `is` and `==`?

**Answer:**

`==` compares **values**, whereas `is` compares **object identity**.

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)  # True
print(a is b)  # False
```

Both lists contain the same values, but they are different objects.

A common correct use of `is` is checking against `None`:

```python
if value is None:
    print("No value")
```

**Interview answer:**

> "`==` checks whether two objects have equal values, while `is` checks whether they are actually the same object."

---

### 4. How are `*args` and `**kwargs` used?

**Answer:**

They allow a function to accept a variable number of arguments.

### `*args`

Collects additional **positional arguments** into a tuple.

```python
def add(*args):
    return sum(args)

print(add(10, 20, 30))
# 60
```

Inside the function:

```python
args == (10, 20, 30)
```

### `**kwargs`

Collects additional **keyword arguments** into a dictionary.

```python
def user_info(**kwargs):
    print(kwargs)

user_info(name="Kiru", age=21)
```

Output:

```python
{'name': 'Kiru', 'age': 21}
```

They can also be combined:

```python
def example(*args, **kwargs):
    print(args)
    print(kwargs)
```

---

### 5. What are Python decorators?

**Answer:**

A decorator is a function that **modifies or extends the behavior of another function without changing its original code**.

Example:

```python
def logger(func):
    def wrapper():
        print("Function started")
        func()
        print("Function ended")

    return wrapper


@logger
def hello():
    print("Hello")
```

When we call:

```python
hello()
```

The decorator adds behavior before and after `hello()`.

Django makes extensive use of decorators.

For example:

```python
@login_required
def dashboard(request):
    ...
```

This means Django checks whether the user is authenticated before allowing access.

**Interview definition:**

> "A decorator is a function that wraps another function to add behavior without modifying the original function's source code."

---

### 6. What is a Python generator?

**Answer:**

A generator is a special iterator that produces values **one at a time using `yield`** instead of returning everything at once.

```python
def numbers():
    for i in range(5):
        yield i
```

Then:

```python
for n in numbers():
    print(n)
```

The generator doesn't create the complete result in memory at once.

This is particularly useful for:

* Large files
* Large database results
* Data processing
* Streaming data

For example, reading a huge file line by line is more memory-efficient than loading the entire file.

**Key difference:**

```python
return
```

ends the function.

```python
yield
```

pauses the function and remembers its state so it can continue later.

---

### 7. What is list comprehension?

**Answer:**

List comprehension is a concise way to create a list from an iterable.

Normal approach:

```python
numbers = []

for x in range(5):
    numbers.append(x * 2)
```

List comprehension:

```python
numbers = [x * 2 for x in range(5)]
```

Output:

```python
[0, 2, 4, 6, 8]
```

You can also add conditions:

```python
even = [x for x in range(10) if x % 2 == 0]
```

Output:

```python
[0, 2, 4, 6, 8]
```

It makes simple transformations concise, but overly complicated comprehensions can reduce readability.

---

### 8. What is the Global Interpreter Lock (GIL)?

**Answer:**

The **GIL**, or Global Interpreter Lock, is a mechanism in the standard CPython implementation that allows only one thread at a time to execute Python bytecode within a process.

This means traditional Python threads don't generally provide CPU-level parallel execution for CPU-bound Python code in the same CPython process.

For example, CPU-heavy tasks may benefit more from:

```python
multiprocessing
```

rather than ordinary threads.

Threads are still useful for **I/O-bound operations**, such as:

* Network requests
* File operations
* Waiting for APIs
* Database operations

**Important modern nuance:** newer Python versions also provide an optional free-threaded build in which the traditional GIL can be disabled. However, for a typical interview, explaining the traditional CPython GIL model is usually expected.

---

### 9. How does garbage collection work in Python?

**Answer:**

Python automatically manages memory.

Two important mechanisms are:

### 1. Reference counting

Python keeps track of how many references point to an object.

```python
a = [1, 2, 3]
b = a
```

The list has multiple references.

When references disappear:

```python
del a
del b
```

the reference count can reach zero and the object can be reclaimed.

### 2. Cyclic garbage collector

Reference counting alone cannot handle cycles.

For example:

```text
A → B
↑   ↓
└───┘
```

Objects can reference each other even when nothing outside the cycle can reach them.

Python's cyclic garbage collector can detect such unreachable reference cycles and reclaim them when appropriate.

---

### 10. What are lambda functions?

**Answer:**

A lambda is a small anonymous function written using the `lambda` keyword.

```python
square = lambda x: x * x

print(square(5))
# 25
```

Equivalent normal function:

```python
def square(x):
    return x * x
```

Lambdas are commonly used with functions such as:

```python
map()
filter()
sorted()
```

Example:

```python
students = [
    ("A", 80),
    ("B", 95),
    ("C", 70)
]

students.sort(key=lambda x: x[1])
```

A lambda can contain only a **single expression**.

---

### 11. Difference between `copy()` and `deepcopy()`?

**Answer:**

A **shallow copy** creates a new outer object but keeps references to nested objects.

```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
```

The outer lists are different, but the nested lists are shared.

A **deep copy** recursively copies nested objects.

```python
deep = copy.deepcopy(original)
```

Now the nested lists are independent too.

Conceptually:

```text
Shallow:
Original → [ A ]
Copy     → [ A ]

Deep:
Original → [ A ]
Copy     → [ B ]
```

Use `deepcopy()` when you need complete independence from nested mutable objects.

---

### 12. What are Python's built-in data structures?

**Answer:**

The four major built-in collection types are:

| Structure  | Ordered                | Mutable | Duplicates  |
| ---------- | ---------------------- | ------- | ----------- |
| List       | Yes                    | Yes     | Yes         |
| Tuple      | Yes                    | No      | Yes         |
| Set        | No guaranteed ordering | Yes     | No          |
| Dictionary | Insertion ordered      | Yes     | Keys unique |

### List

```python
numbers = [1, 2, 3]
```

### Tuple

```python
numbers = (1, 2, 3)
```

### Set

```python
numbers = {1, 2, 3}
```

### Dictionary

```python
user = {
    "name": "Kiru",
    "age": 21
}
```

Choosing the appropriate data structure is important for performance and clarity.

---

### 13. How do you handle exceptions in Python?

**Answer:**

Python uses:

* `try`
* `except`
* `else`
* `finally`

Example:

```python
try:
    result = 10 / 0

except ZeroDivisionError:
    print("Cannot divide by zero")

else:
    print("Successful")

finally:
    print("Execution completed")
```

`try` contains risky code.

`except` handles exceptions.

`else` runs when no exception occurs.

`finally` normally runs regardless of whether an exception occurred.

You can also raise your own exception:

```python
raise ValueError("Invalid age")
```

**Best practice:** catch specific exceptions rather than blindly using:

```python
except Exception:
```

everywhere.

---

### 14. What is the purpose of `__init__()`?

**Answer:**

`__init__()` is an initializer that runs when an object is created.

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

student = Student("Kiru", 21)
```

The values are initialized when the object is created.

Technically, `__new__()` is responsible for creating the instance, while `__init__()` initializes it. So calling `__init__()` a "constructor" is common shorthand, but technically it is an initializer.

---

### 15. What is Method Resolution Order (MRO)?

**Answer:**

MRO determines the order in which Python searches classes for methods and attributes, especially when multiple inheritance is involved.

Example:

```python
class A:
    def show(self):
        print("A")

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass
```

We can inspect the MRO:

```python
print(D.mro())
```

Python uses the **C3 linearization algorithm** to create a consistent method lookup order.

You can also use:

```python
D.__mro__
```

This becomes particularly important when multiple classes have methods with the same name.

---

### 16. What are iterators and iterables?

**Answer:**

An **iterable** is an object that can be iterated over.

Examples:

```python
list
tuple
string
dictionary
set
```

Example:

```python
numbers = [1, 2, 3]

for x in numbers:
    print(x)
```

An **iterator** is an object that produces values one at a time using `next()`.

```python
numbers = iter([1, 2, 3])

print(next(numbers))  # 1
print(next(numbers))  # 2
```

Eventually:

```python
next(numbers)
```

raises:

```text
StopIteration
```

A useful interview distinction:

> Every iterator is iterable, but not every iterable is itself an iterator.

---

### 17. What is name mangling?

**Answer:**

Python performs name mangling for attributes beginning with **two underscores** inside classes.

```python
class Student:
    def __init__(self):
        self.__marks = 90
```

Python internally changes the name approximately to:

```text
_Student__marks
```

This helps prevent accidental name conflicts in subclasses.

It is **not true private access control**.

For example:

```python
student._Student__marks
```

can technically access it.

So name mangling is mainly designed to avoid accidental overriding/conflicts.

---

### 18. What is a virtual environment?

**Answer:**

A virtual environment creates an isolated Python environment for a project.

Without one, different projects might require conflicting package versions.

For example:

```text
Project A → Django 4.x
Project B → Django 5.x
```

A virtual environment lets each project maintain its own dependencies.

Create one:

```bash
python -m venv venv
```

Activate on Windows:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

Then:

```bash
pip install django
```

You can save dependencies:

```bash
pip freeze > requirements.txt
```

---

### 19. How do you safely handle file operations?

**Answer:**

Use the `with` statement.

```python
with open("file.txt", "r") as file:
    data = file.read()
```

The context manager automatically closes the file after the block finishes, including when an exception occurs.

Writing:

```python
with open("file.txt", "w") as file:
    file.write("Hello")
```

Common modes include:

```text
r → read
w → write
a → append
rb → read binary
wb → write binary
```

---

### 20. What is a docstring?

**Answer:**

A docstring is a string used to document a module, class, or function.

```python
def add(a, b):
    """Return the sum of two numbers."""
    return a + b
```

You can access it using:

```python
print(add.__doc__)
```

Docstrings are useful for:

* Documentation
* IDE assistance
* API documentation
* Explaining function behavior

---

## Part 2: Django & Backend — 20 Questions

### 21. What is Django and why is it called "batteries-included"?

**Answer:**

Django is a **high-level Python web framework** used to build web applications quickly and securely.

It is called **"batteries-included"** because many common web-development features are already provided.

Examples:

* URL routing
* ORM
* Authentication
* Sessions
* Forms
* CSRF protection
* Admin interface
* Middleware
* Security features
* Template engine
* Migration system

Instead of building everything from scratch, developers can focus on application-specific business logic.

---

### 22. Explain Django's MTV architecture.

**Answer:**

Django follows an **MTV architecture**:

### Model

Responsible for:

* Database structure
* Data representation
* Database operations

Example:

```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

### Template

Responsible mainly for presentation/UI.

```html
<h1>{{ product.name }}</h1>
```

### View

Handles request processing and business/application logic.

```python
def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, "product.html", {"product": product})
```

Typical flow:

```text
Browser
   ↓
URL
   ↓
View
   ↓
Model / Database
   ↓
View
   ↓
Template
   ↓
Response
```

---

### 23. Difference between a Django Project and App?

**Answer:**

A **project** represents the overall Django website/application configuration.

An **app** is a modular component that performs a particular function.

For example:

```text
myproject/
│
├── settings.py
├── urls.py
│
├── users/
├── products/
├── payments/
└── orders/
```

Here:

```text
myproject → project
users      → app
products   → app
payments   → app
orders     → app
```

A project can contain multiple apps.

Apps make large applications easier to organize and maintain.

---

### 24. What does `manage.py` do?

**Answer:**

`manage.py` is a command-line utility generated by Django projects.

It helps developers perform administrative tasks.

Examples:

```bash
python manage.py runserver
```

Starts the development server.

```bash
python manage.py makemigrations
```

Creates migration files.

```bash
python manage.py migrate
```

Applies migrations.

```bash
python manage.py createsuperuser
```

Creates an admin user.

```bash
python manage.py startapp products
```

Creates a Django app.

It also sets the project's Django settings module so commands know which project configuration to use.

---

### 25. What is the role of `settings.py`?

**Answer:**

`settings.py` contains project-wide configuration.

Important settings include:

```python
INSTALLED_APPS
DATABASES
MIDDLEWARE
ROOT_URLCONF
TEMPLATES
STATIC_URL
MEDIA_URL
SECRET_KEY
DEBUG
ALLOWED_HOSTS
```

For example:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        ...
    }
}
```

For production, sensitive values such as `SECRET_KEY` and database credentials should generally come from environment variables or a secret manager.

---

### 26. What are Django migrations?

**Answer:**

Migrations allow Django to track and apply database schema changes based on model changes.

Suppose we create:

```python
class Product(models.Model):
    name = models.CharField(max_length=100)
```

Run:

```bash
python manage.py makemigrations
```

Django creates a migration file describing the schema change.

Then:

```bash
python manage.py migrate
```

applies those changes to the database.

### Difference:

```text
makemigrations
        ↓
Creates migration instructions

migrate
        ↓
Applies migration instructions to database
```

Migrations also maintain a history of schema changes.

---

### 27. How does Django handle authentication?

**Answer:**

Django provides authentication through:

```python
django.contrib.auth
```

It supports:

* Users
* Password hashing
* Login
* Logout
* Groups
* Permissions
* Sessions

Example:

```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    ...
```

Django doesn't store user passwords as plain text. It stores password hashes using its password-hashing framework.

For complex applications, developers can also create a custom user model.

---

### 28. What is Django Admin?

**Answer:**

Django Admin is an automatically generated administrative interface based on registered models.

For example:

```python
from django.contrib import admin
from .models import Product

admin.site.register(Product)
```

Django can then provide an interface to manage products.

It supports common operations such as:

* Create
* Read
* Update
* Delete
* Search
* Filtering
* Sorting

It is extremely useful for internal administration and development.

However, it shouldn't automatically be treated as the application's public frontend.

---

### 29. FBV vs CBV?

**Answer:**

### Function-Based View

Uses a Python function.

```python
def product_list(request):
    products = Product.objects.all()
    return render(request, "products.html", {"products": products})
```

Advantages:

* Easy to understand
* Direct control
* Good for simple views

### Class-Based View

Uses a class.

```python
from django.views.generic import ListView

class ProductListView(ListView):
    model = Product
```

Advantages:

* Reusable behavior
* Inheritance
* Mixins
* Less repetitive code

**Interview answer:**

> FBVs are straightforward and explicit, while CBVs provide reusable, extensible behavior through classes, inheritance, and mixins.

---

### 30. What is Django middleware?

**Answer:**

Middleware is a layer that processes requests and responses globally.

Conceptually:

```text
Request
 ↓
Middleware
 ↓
View
 ↓
Middleware
 ↓
Response
```

Django provides middleware for things such as:

* Sessions
* Authentication
* CSRF protection
* Security
* Message handling

Custom middleware can also be created.

For example, middleware could log information about incoming requests.

---

### 31. What is a CSRF token?

**Answer:**

CSRF stands for **Cross-Site Request Forgery**.

It is an attack where a malicious website attempts to make a user's browser perform an unwanted state-changing request to another website where the user is authenticated.

Django protects many unsafe requests using CSRF protection.

In a Django template:

```html
<form method="POST">
    {% csrf_token %}
    ...
</form>
```

The server verifies the CSRF token before accepting the request.

**Important distinction:**

CSRF protection is primarily relevant to requests where the browser automatically sends authentication credentials, such as cookies. It is different from CORS and is not simply "an authentication token."

---

### 32. Django Forms vs ModelForms?

**Answer:**

### Django Form

You manually define fields.

```python
class ProductForm(forms.Form):
    name = forms.CharField()
    price = forms.DecimalField()
```

### ModelForm

Generated from a Django model.

```python
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price"]
```

ModelForms reduce duplication when the form corresponds directly to a model.

They also provide model-aware validation and save support.

---

### 33. What are Django signals?

**Answer:**

Signals allow one part of an application to notify another part when a particular event occurs.

For example:

```python
post_save
```

can execute after a model is saved.

Example concept:

```python
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

Signals can be useful for decoupled side effects.

However, overusing signals can make application behavior difficult to trace. For important business workflows, explicit service-layer logic is often easier to maintain.

---

### 34. What is Django REST Framework?

**Answer:**

**Django REST Framework (DRF)** is a toolkit for building Web APIs using Django.

It provides:

* Serializers
* API views
* ViewSets
* Routers
* Authentication
* Permissions
* Pagination
* Validation
* Browsable API

For a React + Django application, a common architecture is:

```text
React
  ↓ HTTP/JSON
DRF API
  ↓
Django
  ↓
Database
```

---

### 35. What are serializers in DRF?

**Answer:**

Serializers convert complex Python/Django objects into data types that can be rendered as JSON and also validate incoming data.

Example:

```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]
```

A model instance can become:

```json
{
    "id": 1,
    "name": "Laptop",
    "price": "65000.00"
}
```

Serializers can also validate incoming JSON before creating or updating model objects.

---

### 36. What are ViewSets in DRF?

**Answer:**

A ViewSet groups related API operations into one class.

For example:

```python
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

A `ModelViewSet` can provide standard CRUD operations:

```text
GET     → list
POST    → create
GET /id → retrieve
PUT     → update
PATCH   → partial update
DELETE  → destroy
```

Routers can automatically generate the corresponding URL patterns.

---

### 37. How does Django manage sessions?

**Answer:**

Sessions allow Django to remember information between requests.

A common flow is:

```text
User logs in
     ↓
Django creates/updates session
     ↓
Browser receives session cookie
     ↓
Browser sends cookie on later requests
     ↓
Django identifies the session
```

Session data can be stored using different backends, commonly the database, cache, or signed cookies depending on configuration.

Sessions are particularly useful for cookie-based authentication.

---

### 38. How are static and media files managed?

**Answer:**

### Static files

Files that belong to the application:

* CSS
* JavaScript
* Application images

Django provides:

```python
django.contrib.staticfiles
```

Example:

```python
STATIC_URL = "/static/"
```

### Media files

Files uploaded by users:

* Profile pictures
* Documents
* Product images

Example:

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

In production, static/media files are commonly served through dedicated web servers or cloud/object storage.

---

### 39. How do you implement pagination in DRF?

**Answer:**

Pagination prevents an API from returning thousands of records in one response.

DRF provides classes such as:

```python
PageNumberPagination
LimitOffsetPagination
CursorPagination
```

Example:

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS":
        "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10
}
```

Instead of:

```json
[
    "1000 records..."
]
```

the API returns a limited page with metadata such as count and navigation information, depending on the pagination style.

---

### 40. How do you manage environment secrets securely?

**Answer:**

Never hard-code sensitive credentials directly into source code.

Bad:

```python
PASSWORD = "MyDatabasePassword123"
```

Better:

```python
import os

PASSWORD = os.environ.get("DB_PASSWORD")
```

Environment variables can store:

```text
SECRET_KEY
DATABASE_PASSWORD
API_KEY
JWT_SECRET
```

For larger production systems, dedicated secret-management systems can be used.

Also make sure `.env` files containing secrets are not accidentally committed to Git.

---

## Part 3: Frontend & Web Integration — 20 Questions

### 41. Difference between `var`, `let`, and `const`?

**Answer:**

### `var`

* Function scoped
* Can be redeclared
* Can be reassigned
* Hoisted with `undefined` initialization behavior

### `let`

* Block scoped
* Can be reassigned
* Cannot be redeclared in the same scope

### `const`

* Block scoped
* Cannot be reassigned
* Must generally be initialized when declared

```javascript
let age = 21;
age = 22;

const name = "Kiru";
// name = "John"; ❌
```

Important:

```javascript
const user = { name: "Kiru" };
user.name = "John";
```

This is allowed because `const` prevents reassignment of the variable binding; it doesn't make the object itself immutable.

---

### 42. What are arrow functions?

**Answer:**

Arrow functions provide shorter function syntax.

Normal:

```javascript
function add(a, b) {
    return a + b;
}
```

Arrow:

```javascript
const add = (a, b) => a + b;
```

One important difference is `this`.

Arrow functions use **lexical `this`**, meaning they don't create their own `this` binding.

This makes them particularly useful in callbacks.

---

### 43. What is the DOM?

**Answer:**

DOM means **Document Object Model**.

The browser converts an HTML document into a tree-like object structure.

For example:

```html
<h1>Hello</h1>
```

JavaScript can interact with it:

```javascript
document.querySelector("h1").textContent = "Welcome";
```

The DOM allows JavaScript to modify:

* Elements
* Text
* Attributes
* Styles
* Event handlers

React generally abstracts much of this direct DOM manipulation through its rendering model.

---

### 44. What is a Promise?

**Answer:**

A Promise represents the eventual result of an asynchronous operation.

It has three primary states:

```text
Pending
   ↓
Fulfilled
```

or

```text
Pending
   ↓
Rejected
```

Example:

```javascript
fetch("/api/products")
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
```

Promises are commonly used for:

* API calls
* Timers
* File operations
* Other asynchronous tasks

---

### 45. Explain `async` and `await`.

**Answer:**

`async` and `await` make Promise-based asynchronous code easier to read.

Example:

```javascript
async function getProducts() {
    const response = await fetch("/api/products");
    const data = await response.json();

    return data;
}
```

`await` pauses execution of that async function until the Promise settles, without blocking the browser's main thread in the usual sense.

Errors can be handled with:

```javascript
try {
    const data = await getProducts();
} catch (error) {
    console.error(error);
}
```

---

### 46. Difference between `null` and `undefined`?

**Answer:**

`undefined` usually means a value has not been assigned or is absent.

```javascript
let x;
console.log(x);
// undefined
```

`null` is an explicit value representing intentional absence.

```javascript
let user = null;
```

So:

```text
undefined → value not assigned/available
null      → intentionally empty
```

They are different values.

---

### 47. What is CORS and how do you handle it with Django and React?

**Answer:**

CORS stands for **Cross-Origin Resource Sharing**.

Browsers restrict JavaScript from making certain requests across different origins unless the server explicitly permits them.

For example:

```text
React:
http://localhost:3000

Django:
http://localhost:8000
```

These are different origins because the ports differ.

In Django, a common solution is the `django-cors-headers` package.

Configuration might allow a specific frontend origin:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

**Important:** CORS is a **browser security mechanism**, not an authentication mechanism.

---

### 48. How does a frontend communicate with Django?

**Answer:**

A React frontend commonly communicates with Django through HTTP APIs.

For example:

```javascript
const response = await fetch(
    "http://localhost:8000/api/products/"
);

const products = await response.json();
```

The architecture is:

```text
React
   ↓ HTTP request
Django REST Framework
   ↓
Django
   ↓
Database
   ↑
Django
   ↑ JSON response
React
```

HTTP methods commonly include:

```text
GET
POST
PUT
PATCH
DELETE
```

---

### 49. What is JSON?

**Answer:**

JSON stands for **JavaScript Object Notation**.

It is a lightweight text format commonly used for communication between frontend and backend systems.

Example:

```json
{
    "name": "Laptop",
    "price": 65000,
    "available": true
}
```

JSON supports values such as:

* Strings
* Numbers
* Booleans
* Arrays
* Objects
* `null`

It is widely used in REST APIs.

---

### 50. What is React?

**Answer:**

React is a JavaScript library for building user interfaces using reusable components.

Example:

```jsx
function Welcome() {
    return <h1>Hello</h1>;
}
```

A React application can be broken into components:

```text
App
├── Navbar
├── ProductList
│   ├── ProductCard
│   └── ProductCard
└── Footer
```

React uses a declarative programming model where developers describe what the UI should look like based on application state.

---

### 51. Difference between props and state?

**Answer:**

### Props

Props are data passed from a parent component to a child.

```jsx
<Product name="Laptop" />
```

Inside:

```jsx
function Product({ name }) {
    return <h2>{name}</h2>;
}
```

Props should be treated as read-only by the receiving component.

### State

State is data managed by a component or through React's state mechanisms.

```jsx
const [count, setCount] = useState(0);
```

Updating state can cause React to render the component again.

Simple distinction:

```text
Props → passed into component
State → managed by component/application
```

---

### 52. What is `useEffect`?

**Answer:**

`useEffect` is a React Hook used to synchronize a component with external systems or perform side effects.

Examples include:

* Fetching API data
* Subscribing to events
* Timers
* Connecting to external systems

Example:

```jsx
useEffect(() => {
    fetchProducts();
}, []);
```

The empty dependency array means the effect is scheduled after the component's initial mount.

With dependencies:

```jsx
useEffect(() => {
    fetchProduct(id);
}, [id]);
```

The effect reruns when `id` changes.

---

### 53. What is a Single Page Application?

**Answer:**

An SPA loads an application shell and then dynamically updates its UI as the user navigates, rather than requesting a completely new HTML document for every navigation.

Example:

```text
React SPA
    ↓
One application shell
    ↓
Dashboard
Products
Profile
Orders
```

The browser can update the displayed component without performing a full-page reload.

Advantages:

* Smooth navigation
* Rich interactive UI
* Reduced repeated page loading

Disadvantages can include:

* More JavaScript sent to the client
* SEO considerations
* More frontend complexity

---

### 54. How does client-side routing work?

**Answer:**

A React routing library can map browser URLs to components.

For example:

```text
/products → ProductList
/products/10 → ProductDetails
/profile → Profile
```

When the user navigates, the client-side router changes the displayed component without requesting a completely new HTML document for every route.

The browser's History API is commonly involved.

However, the server must also be configured appropriately so that direct navigation to a client-side route can return the SPA entry document.

---

### 55. What are standard HTTP methods?

**Answer:**

### GET

Retrieve data.

```http
GET /api/products/
```

### POST

Create a resource or trigger an operation.

```http
POST /api/products/
```

### PUT

Replace/update a resource as a whole.

```http
PUT /api/products/10/
```

### PATCH

Partially update a resource.

```http
PATCH /api/products/10/
```

### DELETE

Remove a resource.

```http
DELETE /api/products/10/
```

A good interview point is that HTTP semantics include **idempotency** differences: GET, PUT and DELETE are generally expected to be idempotent, while POST generally isn't.

---

### 56. What do common HTTP status codes mean?

**Answer:**

| Code | Meaning                                   |
| ---- | ------------------------------------------ |
| 200  | OK                                        |
| 201  | Created                                   |
| 204  | No Content                                |
| 400  | Bad Request                               |
| 401  | Unauthenticated / authentication required |
| 403  | Forbidden                                 |
| 404  | Not Found                                 |
| 405  | Method Not Allowed                        |
| 409  | Conflict                                  |
| 500  | Internal Server Error                     |

A particularly common interview question:

**401 vs 403?**

Generally:

```text
401 → authentication is missing/invalid
403 → server understood the request but refuses access
```

---

### 57. How do you handle form submission from a frontend app?

**Answer:**

In React:

1. Capture the form submit event.
2. Prevent default browser submission.
3. Read/validate the form data.
4. Send it to the backend.
5. Handle success/error response.

Example:

```jsx
const handleSubmit = async (event) => {
    event.preventDefault();

    const response = await fetch("/api/products/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name,
            price
        })
    });
};
```

For file uploads, `FormData` is generally used instead of JSON.

---

### 58. What is the CSS box model?

**Answer:**

Every normal CSS box consists conceptually of:

```text
Margin
  Border
    Padding
      Content
```

For example:

```css
.box {
    width: 200px;
    padding: 20px;
    border: 2px solid;
    margin: 10px;
}
```

The `box-sizing` property affects how declared width/height interact with padding and borders.

A common choice is:

```css
box-sizing: border-box;
```

which makes the declared width include content, padding, and border.

---

### 59. What is responsive web design?

**Answer:**

Responsive design means creating websites that adapt to different screen sizes.

Techniques include:

* Flexible layouts
* CSS Grid
* Flexbox
* Relative units
* Responsive images
* Media queries

Example:

```css
@media (max-width: 768px) {
    .container {
        flex-direction: column;
    }
}
```

This allows the same application to work well on:

```text
Mobile
Tablet
Laptop
Desktop
```

---

### 60. How do you store authentication tokens securely?

**Answer:**

There are several approaches, and security depends on the authentication architecture.

Storing tokens in:

```javascript
localStorage
```

is convenient but makes tokens accessible to JavaScript, so an XSS vulnerability can potentially expose them.

For cookie-based authentication, a common approach is:

```text
HttpOnly
Secure
SameSite
```

cookies.

`HttpOnly` prevents JavaScript from directly reading the cookie.

However, cookies introduce CSRF considerations, so appropriate CSRF protection and `SameSite` configuration are important.

**Interview-quality answer:**

> "For browser applications, I prefer an authentication design using secure, HttpOnly cookies where appropriate, combined with CSRF protection. I avoid storing long-lived sensitive tokens in localStorage when possible because XSS can expose them."

---

## Part 4: Database, SQL & Django ORM — 20 Questions

### 61. What is Django ORM?

**Answer:**

ORM stands for **Object-Relational Mapping**.

Django ORM allows developers to interact with relational databases using Python objects instead of writing SQL for every operation.

Instead of:

```sql
SELECT * FROM products;
```

you can write:

```python
Product.objects.all()
```

Instead of:

```sql
SELECT * FROM products WHERE price > 50000;
```

you can write:

```python
Product.objects.filter(price__gt=50000)
```

Django translates ORM operations into SQL appropriate for the configured database backend.

---

### 62. What are QuerySets?

**Answer:**

A QuerySet represents a collection of database queries/results associated with a Django model.

Example:

```python
products = Product.objects.filter(price__gt=50000)
```

One important feature is **lazy evaluation**.

Creating:

```python
products = Product.objects.filter(price__gt=50000)
```

doesn't necessarily immediately execute the SQL query.

The query is evaluated when the QuerySet needs results, for example:

```python
for product in products:
    print(product.name)
```

Other operations such as converting it to a list can also trigger evaluation.

This allows Django to build and optimize query expressions before execution.

---

### 63. Difference between `get()` and `filter()`?

**Answer:**

`get()` expects exactly **one object**.

```python
product = Product.objects.get(id=10)
```

If nothing is found:

```text
DoesNotExist
```

If multiple records match:

```text
MultipleObjectsReturned
```

`filter()` returns a QuerySet:

```python
products = Product.objects.filter(category="Laptop")
```

It can return:

```text
0 records
1 record
100 records
```

Simple rule:

```text
get()    → exactly one expected
filter() → zero or more expected
```

---

### 64. `select_related()` vs `prefetch_related()`?

**Answer:**

Both are used to reduce unnecessary database queries when accessing related objects.

### `select_related()`

Uses SQL joins and is generally used for:

* ForeignKey
* OneToOneField

Example:

```python
orders = Order.objects.select_related("customer")
```

Django can retrieve order and customer information together.

### `prefetch_related()`

Uses additional queries and combines the results in Python.

Useful for:

* Many-to-many
* Reverse relationships

Example:

```python
authors = Author.objects.prefetch_related("books")
```

Conceptually:

```text
select_related
→ JOIN
→ usually one SQL query

prefetch_related
→ separate queries
→ combine in Python
```

---

### 65. What are relationship fields in Django?

**Answer:**

Three major relationship types are:

### ForeignKey

Many records can point to one record.

```python
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
```

Example:

```text
Category
  ↓
Product
Product
Product
```

### OneToOneField

One record corresponds to one related record.

```python
profile = models.OneToOneField(User, ...)
```

### ManyToManyField

Many records can relate to many other records.

```python
class Product(models.Model):
    suppliers = models.ManyToManyField(Supplier)
```

Example:

```text
Product A → Supplier 1
         → Supplier 2

Product B → Supplier 2
         → Supplier 3
```

---

### 66. Difference between `null=True` and `blank=True`?

**Answer:**

They operate at different levels.

### `null=True`

Database-level behavior.

It allows the database column to contain SQL `NULL`.

```python
price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    null=True
)
```

### `blank=True`

Validation-level behavior.

It tells Django validation that the field may be empty.

```python
name = models.CharField(
    max_length=100,
    blank=True
)
```

So:

```text
null  → database
blank → validation/forms
```

For string fields, Django commonly recommends using an empty string rather than `NULL` unless there is a specific reason to have both states.

---

### 67. How do you run raw SQL in Django?

**Answer:**

Django provides several ways.

One is:

```python
Product.objects.raw(
    "SELECT * FROM products_product"
)
```

For more general SQL, use a database cursor:

```python
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute(
        "SELECT * FROM products_product WHERE price > %s",
        [50000]
    )
    rows = cursor.fetchall()
```

The parameterized query is important.

Avoid constructing SQL like:

```python
f"SELECT * FROM products WHERE name = '{name}'"
```

because that can lead to SQL injection.

Prefer parameters or the ORM.

---

### 68. What is an RDBMS?

**Answer:**

RDBMS stands for **Relational Database Management System**.

It stores structured data in tables consisting of:

```text
Rows
Columns
```

Tables can be related through keys.

Examples include:

* PostgreSQL
* MySQL
* Oracle Database
* Microsoft SQL Server
* SQLite

Example:

```text
Customer
----------------
id
name
email

Order
----------------
id
customer_id
amount
```

`customer_id` can establish a relationship between the tables.

---

### 69. Primary Key vs Foreign Key?

**Answer:**

### Primary Key

Uniquely identifies a record within its own table.

```text
Student
----------------
student_id ← Primary Key
name
```

Every student has a unique ID.

### Foreign Key

References a key in another table to establish a relationship.

```text
Order
----------------
order_id
customer_id ← Foreign Key
amount
```

`customer_id` refers to a customer record.

Simple:

```text
Primary Key → identifies
Foreign Key → connects
```

---

### 70. What are database indexes?

**Answer:**

An index is a database data structure that allows the database to find rows more efficiently.

Imagine a table containing millions of users.

Without a suitable index, finding:

```sql
WHERE email = 'abc@example.com'
```

could require examining many rows.

With an index on `email`, the database can locate matching rows much faster.

Django:

```python
class UserProfile(models.Model):
    email = models.EmailField(db_index=True)
```

Indexes improve reads but have costs:

* Additional storage
* Extra work during INSERT
* Extra work during UPDATE/DELETE

Therefore, don't blindly index every column.

---

### 71. What is database normalization?

**Answer:**

Normalization organizes relational data to reduce unnecessary duplication and improve consistency.

Suppose we store:

```text
Order
--------------------------------
order_id
customer_name
customer_phone
product_name
```

If the same customer places 100 orders, their information is repeated 100 times.

A normalized design separates entities:

```text
Customer
---------
customer_id
name
phone

Order
---------
order_id
customer_id
```

Benefits:

* Less redundancy
* Easier updates
* Better consistency
* Clearer relationships

Common normal forms include:

```text
1NF
2NF
3NF
BCNF
```

For most entry-level interviews, understanding 1NF–3NF conceptually is sufficient unless the role specifically focuses on database design.

---

### 72. What are ACID properties?

**Answer:**

ACID describes important transaction properties.

### Atomicity

A transaction happens completely or not at all.

```text
Debit account
+
Credit account
```

If one fails, the transaction should roll back.

### Consistency

The database moves from one valid state to another while respecting constraints.

### Isolation

Concurrent transactions should not improperly interfere with each other.

### Durability

Once a transaction is committed, its changes should survive failures according to the database's durability guarantees.

Example:

```text
Bank transfer
   ↓
Debit
   ↓
Credit
```

Both should succeed together.

---

### 73. INNER JOIN vs LEFT JOIN?

**Answer:**

Suppose:

```text
Customers
Orders
```

### INNER JOIN

Returns records where matching records exist in both tables.

```sql
SELECT *
FROM customers c
INNER JOIN orders o
ON c.id = o.customer_id;
```

Customers without orders won't appear.

### LEFT JOIN

Returns every record from the left table and matching records from the right.

```sql
SELECT *
FROM customers c
LEFT JOIN orders o
ON c.id = o.customer_id;
```

Customers without orders still appear, with NULL values for order columns.

Simple:

```text
INNER JOIN → only matches
LEFT JOIN  → everything from left + matches
```

---

### 74. What is an aggregate function in SQL?

**Answer:**

Aggregate functions perform calculations over multiple rows.

Common functions:

```sql
COUNT()
SUM()
AVG()
MIN()
MAX()
```

Example:

```sql
SELECT COUNT(*)
FROM orders;
```

Calculate total:

```sql
SELECT SUM(amount)
FROM orders;
```

Average:

```sql
SELECT AVG(amount)
FROM orders;
```

They are commonly combined with `GROUP BY`.

---

### 75. Difference between WHERE and GROUP BY?

**Answer:**

`WHERE` filters rows.

`GROUP BY` groups rows for aggregation.

Example:

```sql
SELECT customer_id, SUM(amount)
FROM orders
WHERE amount > 1000
GROUP BY customer_id;
```

The logical idea is:

```text
FROM
 ↓
WHERE → filter rows
 ↓
GROUP BY → form groups
 ↓
Aggregate
```

There is also `HAVING`, which filters groups after aggregation.

Example:

```sql
SELECT customer_id, SUM(amount)
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 10000;
```

So an important interview distinction is:

```text
WHERE  → filters rows
HAVING → filters groups
GROUP BY → creates groups
```

---

### 76. What are atomic transactions in Django?

**Answer:**

Django provides:

```python
transaction.atomic()
```

to group multiple database operations into a transaction.

Example:

```python
from django.db import transaction

with transaction.atomic():
    order.save()
    payment.save()
```

If an exception causes the transaction to fail, Django can roll back the transaction so the database isn't left with only part of the operation.

This is useful for operations such as:

```text
Create order
+
Reduce inventory
+
Create payment
```

where partial completion could cause inconsistent data.

---

### 77. What is connection pooling?

**Answer:**

Opening a database connection has overhead.

Connection pooling maintains a pool of reusable database connections.

Instead of:

```text
Request
 ↓
Open connection
 ↓
Query
 ↓
Close connection
```

every time, a pool can allow:

```text
Connection Pool
 ├── Connection 1
 ├── Connection 2
 ├── Connection 3
 └── Connection 4
```

Applications borrow and return connections.

This can reduce connection setup overhead and improve performance, particularly under concurrent workloads.

Django deployments can use database-specific pooling solutions or supported pooling configurations depending on the database/backend and deployment architecture.

---

### 78. How do you find duplicate records in SQL?

**Answer:**

Use `GROUP BY` with `HAVING`.

Suppose duplicate emails need to be found:

```sql
SELECT email, COUNT(*)
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

The logic is:

```text
GROUP BY email
       ↓
Count each email
       ↓
Keep counts > 1
```

For duplicates across multiple columns:

```sql
SELECT name, phone, COUNT(*)
FROM customers
GROUP BY name, phone
HAVING COUNT(*) > 1;
```

---

### 79. What is a database view?

**Answer:**

A database view is a **virtual table defined by a query**.

Example:

```sql
CREATE VIEW customer_orders AS
SELECT
    c.name,
    o.amount
FROM customers c
JOIN orders o
ON c.id = o.customer_id;
```

Then:

```sql
SELECT *
FROM customer_orders;
```

The view provides a reusable way to expose a particular query result.

Advantages:

* Simplifies complex queries
* Can provide controlled access to data
* Provides an abstraction layer

A normal view generally doesn't store its own independent copy of the result; the underlying query is evaluated when the view is queried. Materialized views are a different concept.

---

### 80. How do you safely deploy migrations across environments?

**Answer:**

A safe migration workflow is:

```text
Developer changes models
        ↓
makemigrations
        ↓
Review migration files
        ↓
Test locally
        ↓
Run tests
        ↓
Staging
        ↓
Production
```

Typical commands:

```bash
python manage.py makemigrations
python manage.py migrate
```

The migration files should normally be committed to Git.

In deployment:

```bash
python manage.py migrate
```

is executed against the target database.

For production systems, you should consider:

* Backups
* Migration testing
* Backward-compatible schema changes
* Long-running migrations
* Locking/availability impact
* Rollback strategy
* Application/database version compatibility

Simply saying "run migrations in CI/CD" is not enough for serious production systems; the migration itself must be designed safely.

---

## Bonus: 10 Follow-Up Questions I Would Expect After These 80

If you're preparing for an **entry-level Python + Django + React Full Stack interview**, don't stop at memorizing these 80. Interviewers commonly go one level deeper.

Be ready for:

1. **What happens when a React component re-renders?**
2. **What is the difference between authentication and authorization?**
3. **JWT vs session authentication?**
4. **What is N+1 query problem in Django?**
5. **How would you optimize a slow Django API?**
6. **What is `useMemo` vs `useCallback`?**
7. **What is the difference between PUT and PATCH?**
8. **What is SQL injection and how do you prevent it?**
9. **What is an HTTP cookie and how does it differ from localStorage?**
10. **Explain one of your projects end-to-end: React → API → Django → ORM → Database.**

That **last one is especially important**. In a full-stack interview, they often stop asking theoretical questions and say:

> **"Okay, explain a project you've built."**

You should be able to draw and explain:

```text
                FRONTEND
              React Application
                     │
                     │ HTTP / JSON
                     ▼
              Django REST API
                     │
          ┌──────────┴──────────┐
          │                     │
      Authentication        Business Logic
          │                     │
          └──────────┬──────────┘
                     ▼
                Django ORM
                     │
                     ▼
              PostgreSQL/MySQL
```

And explain **what happens at every step when a user clicks a button**. That is the point where these 80 individual concepts become a real Full Stack developer skillset.
