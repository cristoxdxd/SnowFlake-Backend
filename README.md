# SnowFlake-Backend

SnowFlake-Backend is a project that utilizes FastAPI and MongoDB to build a fast and scalable backend for web applications. 

## FastAPI

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It is designed to be easy to use and efficient, providing automatic validation of request and response data, automatic generation of interactive API documentation, and high-performance asynchronous support.

```bash
pip install fastapi

pip install uvicorn

uvicorn main:app --reload
```
The above commands install FastAPI and Uvicorn, and then start the server with the `main` module and `app` instance. The `--reload` flag enables automatic reloading of the server when changes are made to the code. The server will be accessible for default at `http://127.0.0.1:8000`. To get a better look at the API information add `/docs` at the end of the URL. `http://127.0.0.1:8000/docs`

## MongoDB

MongoDB is a popular NoSQL database that provides a flexible and scalable solution for storing and retrieving data. It is known for its document-oriented data model, which allows for easy handling of complex data structures. MongoDB is widely used in modern web applications due to its ability to handle large amounts of data and its support for horizontal scaling.

By combining FastAPI and MongoDB, SnowFlake-Backend offers a powerful and efficient solution for building web applications that require high-performance APIs and flexible data storage.

