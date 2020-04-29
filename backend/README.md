# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT


## API DOCUMENTATION
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

### Endpoints
- GET '/api/categories'
- GET '/api/questions'
- DELETE '/api/questions/<int:question_id>'
- POST '/api/questions'
- POST '/api/questions/search'
- GET '/api/categories/<int:category_id>/questions'
- POST '/api/quizzes'


#### GET '/api/categories'
TEST: 
`
curl localhost:3000/api/categories
`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```JSON
{
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
}
```


#### GET '/api/questions'
TEST: 
`
curl localhost:3000/api/questions
`
 - Fetches a dictionary which is storing the key values of "categories", "current_category", "questions", "success", and "total_questions".
 - Request Arguments: None
 - Returns on success: An object with 5 keys.
    - "success"
        - True or False. Indicates if an error has occured or not.
    - "categories"
        - Contains the result similar to '/api/categories'.
    - "current_category"
        - Currently unused. For future functionality.
    - "questions"
        - Contains the entire dataset (returned as a list) of questions with keys "id", "question", "answer", "category"
        - "category is stored as the numerical representation. e.g. it would return '1' rather than 'Science'. 
    - "total_questions"
        - Returns the total number of questions in the database.
```JSON
{
    "categories": {
        "1": "Science", 
        "2": "Art", 
        "3": "Geography", 
        "4": "History", 
        "5": "Entertainment", 
        "6": "Sports"
    }, 
    "current_category": null, 
    "questions": [
        {
            "answer": "Apollo 13", 
            "category": 5, 
            "difficulty": 4, 
            "id": 2, 
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }, 
        {
            "answer": "Tom Cruise", 
            "category": 5, 
            "difficulty": 4, 
            "id": 4, 
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        }...
    ],
    "success": true, 
    "total_questions": 19
}
```
- Returns on failure:
```JSON
{
    'success': False,
    'error_code': 404,
    'message': 'resource not found'
}
```


#### DELETE '/api/questions/<int:question_id>'
TEST: 
`
curl -X DELETE localhost:3000/api/questions/6
`
- Deletes a question based on the id provided.
- Request Arguments: The id.
- Returns on Success: 4 key values.
    - "success"
        - True or False. Indicates if an error has occured or not.
    - "deleted"
        - the id of the question just deleted.
    - "question"
        - The values of the just deleted question.
    - "total_questions"
        - Returns the total number of questions in the database after the deletion.
```JSON
{
    "deleted": 6, 
    "question": {
        "answer": "Edward Scissorhands", 
        "category": 5, 
        "difficulty": 3, 
        "id": 6, 
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    "success": true, 
    "total_questions": 18
}
```
- Return on Failure: one of the below.
```JSON
{
    'success': False,
    'error_code': 404,
    'message': 'resource not found'
}
```
```JSON
{
    'success': False,
    'error_code': 422,
    'message': 'unprocessable'
}
```


#### POST '/api/questions'
TEST: 
`
curl -X POST -H "Content-Type: application/json" --data '{"question":"What is the airspeed velocity of a swallow?","answer":"An African or European swallow?","category":"5","difficulty":5}' localhost:3000/api/questions
`
- Creates and stores a new questionin the database. The id is auto generated.
- Request Arguments:
    - question, stored as a string
    - answer, stored as a string
    - category, an integer, but stored as a string. Refer to GET categories above.
    - difficulty, stored as an intiger from 1-5.
- Returns on Success: 4 key values.
    - "success"
        - True or False. Indicates if an error has occured or not.
    - "created"
        - the id of the question just created.
    - "question_info"
        - The values of the just created question.
    - "total_questions"
        - Returns the total number of questions in the database after the deletion.
```JSON
{
    "created": 24, 
    "question_info": {
        "answer": "An African or European swallow?", 
        "category": 5, 
        "difficulty": 5, 
        "id": 24, 
        "question": "What is the airspeed velocity of a swallow?"
    }, 
    "success": true, 
    "total_questions": 19
}
```
- Return on Failure: one of the below
```JSON
{
    'success': False,
    'error_code': 400,
    'message': 'bad request'
}
```
```JSON
{
    'success': False,
    'error_code': 422,
    'message': 'unprocessable'
}
```


#### POST '/api/questions/search'
TEST: 
`
curl -X POST -H "Content-Type: application/json" --data '{"searchTerm":"swallow"}' localhost:3000/api/questions/search
`
- Searches the database for questions containing the given string, 'serachTerm'.
- Request Arguments:
    - "searchTerm", a string. 
- Returns on Success: 4 key values.
    - "success"
        - True or False. Indicates if an error has occured or not.
    - "current_category"
        - Currently unused. For future functionality.
    - "questions"
        - Contains the dataset (returned as a list) of questions with keys "id", "question", "answer", and "category", which match the search term.
    - "total_questions"
        - Returns the total number of questions in the database.
```JSON
{
    "current_category": null, 
    "questions": [
        {
            "answer": "Maya Angelou", 
            "category": 4, 
            "difficulty": 2, 
            "id": 5, 
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
         }, 
        {
            "answer": "George Washington Carver", 
            "category": 4, 
            "difficulty": 2, 
            "id": 12, 
            "question": "Who invented Peanut Butter?"
        }, 
        {
            "answer": "Alexander Fleming", 
            "category": 1, 
            "difficulty": 3, 
            "id": 21, 
            "question": "Who discovered penicillin?"
        }
    ], 
    "success": true, 
    "total_questions": 3
}
```
- Result on Failure:
```JSON
{
    'success': False,
    'error_code': 422,
    'message': 'unprocessable'
}
```


#### GET '/api/categories/<int:category_id>/questions'
TEST: 
`
curl localhost:3000/api/categories/6/questions
`
- Fetches questions of a specific category in a dictionary which is storing the key values of "categories", "current_category", "questions", "success", and "total_questions".
 - Request Arguments: The category id.
 - Returns on success: An object with 5 keys.
    - "success"
        - True or False. Indicates if an error has occured or not.
    - "categories"
        - Contains the result similar to '/api/categories'.
    - "current_category"
        - Currently unused. For future functionality.
    - "questions"
        - Contains the entire dataset (returned as a list) of questions with keys "id", "question", "answer", "category"
        - "category is stored as the numerical representation. e.g. it would return '1' rather than 'Science'. 
    - "total_questions"
        - Returns the total number of questions in the database.
```JSON
{
    "current_category": 6, 
    "questions": [
    {
        "answer": "Brazil", 
        "category": 6, 
        "difficulty": 3, 
        "id": 10, 
        "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
        "answer": "Uruguay", 
        "category": 6, 
        "difficulty": 4, 
        "id": 11, 
        "question": "Which country won the first ever soccer World Cup in 1930?"
    }
    ], 
    "success": true, 
    "total_questions": 2
}
```
- Return on Failure:
```JSON
{
    'success': False,
    'error_code': 422,
    'message': 'unprocessable'
}
```


#### POST '/api/quizzes'
TEST: 
` curl -X POST -H "Content-Type: application/json" --data '{"previous_questions":[22],"quiz_category":{"type":"Science","id":"1"}}' localhost:3000/api/quizzes
`
- Fetches a question based on the chosen category (0 is all). The ids of previously asked questions can be sent as a list so they will not be repeated.
- Request Arguments: The category id, and id of previously asked questions. 
- Returns on success: An object with 5 keys.
    - "success"
        - True or False. Indicates if an error has occured or not.
    - "questions"
        - Contains a question with keys "id", "question", "answer", and "category".
    - "previous_questions"
        - list of previous questions asked.
```JSON
{
    'success': True, 
    'question': {
        'id': 21, 
        'question': 'Who discovered penicillin?', 
        'answer': 'Alexander Fleming', 
        'category': 1, 
        'difficulty': 3
        }, 
    'previous_questions': [22]
}
```
- Return on Failure:
```JSON
{
  "error_code": 400, 
  "message": "bad request", 
  "success": false
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```