# Movie Quote API SDK for Python

This SDK provides a simple interface for accessing the [Movie Quote API](https://example.com/api). It includes classes for retrieving and modifying movie and quote data.

## Installation

The SDK can be installed using pip:

```pip install movie-quote-api-python-sdk```

## Usage

To use the SDK, import the `MovieAPI` and `QuoteAPI` classes and create instances of them, passing in the base URL of the API:

```python
from movie_quote_api_sdk import MovieAPI, QuoteAPI

movie_api = MovieAPI("https://example.com/api")
quote_api = QuoteAPI("https://example.com/api")
```

Then call the appropriate method on the instance to retrieve or modify data:

```python
movies = movie_api.get_movies()
movie = movie_api.get_movie_by_id(123)
quotes = movie_api.get_movie_quotes(123)
new_movie_data = {"title": "The Godfather", "year": 1972}
new_movie = movie_api.create_movie(new_movie_data)
updated_movie_data = {"year": 1974}
updated_movie = movie_api.update_movie(123, updated_movie_data)
movie_api.delete_movie(123)

all_quotes = quote_api.get_quotes()
quote = quote_api.get_quote_by_id(456)
new_quote_data = {"text": "I'll be back", "movie_id": 123}
new_quote = quote_api.create_quote(new_quote_data)
updated_quote_data = {"text": "I'll be back!", "movie_id": 123}
updated_quote = quote_api.update_quote(456, updated_quote_data)
quote_api.delete_quote(456)

```

For more information on the methods available, see the MovieAPI and QuoteAPI class definitions in the movie_api.py and quote_api.py files.

## Testing

Unit tests for the SDK can be run using pytest. To run the tests, first install pytest:

    ```pip install pytest```
    
    Then run the tests:
    
    ```pytest```


