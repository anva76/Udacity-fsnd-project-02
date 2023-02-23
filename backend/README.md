# Backend - Trivia API

## Setting up the Backend

### Prerequisites

* **Python 3.7 or higher** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

* **Virtual Environment** - It is recommended to use a python virtual environment for running the backend Flask code. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

* **PostgreSQL Server** - For this project, a connection to a running PostgreSQL server is required. The simplest scenario is to run the server locally. Please refer to the [PostgreSQL administration docs](https://www.postgresql.org/docs/current/admin.html) and [install](https://www.postgresql.org/download/) a relevant binary package for your platform.

### Installing PIP Dependencies

In your terminal, navigate to the `/backend` directory and create a virtual environment by executing:

```bash
virtualenv venv
```
Then activate the newly created environment:

```bash
source venv/bin/activate
```
Install PIP dependencies:

```bash
pip install -r requirements.txt
```

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

Before running the backend server, please ensure that you are in the `/backend` folder and your virtual environment is activated as described above.

The backend application loads its secrets as environment variables from an `.env` file. Please create one in the `/backend` folder as shown in the following example:

```bash
DB_HOST=your_db_host
DB_USER=your_db_user
DB_PASSWORD=your_password
DB_NAME=postgre_database_name
TEST_DB_NAME=postgre_test_database_name
```
To run the backend Flask server, execute:

```bash
python app.py
```

## API documentation

### API Endpoints

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains the dictionary of categories.

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports",
        "7": "TV series",
        "8": "Cinema"
    },
    "success": true
}
```

`GET '/categories/<int:category_id>/questions'`

- Fetches the list of questions for a given category.
- Request Arguments: `category_id` - passed as a url paremeter.
- Returns: a list of questions, current category, total number of questions.

```json
{
    "current_category": "Science",
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
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
    "total_questions": 2
}
```
`GET '/questions?page=<n>'`

- Fetches the list of questions for a given page.
- Request Arguments: `page` - passed as a url parameter
- Returns: a list of questions, dictionary of categories, current category, total number of questions, actual page.
The actual page parameter may be different from the requested page if it is out of range.


```json
{
    "actual_page": 1,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": "",
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
        },

    ],
    "success": true,
    "total_questions": 21
}
```

`DELETE '/questions/<int:question_id>'`

- Sends a request to delete a question based on a question id number.
- Request Arguments: `question_id` - passed as a url parameter
- Returns: If the transaction is successful, only a success indicator is returned.

```json
{
    "success": true
}
```

`POST '/questions'`

- Sends a request to add a new question.
- Request Arguments: `question`, `answer`, `difficulty`, `category` - all passed in the body of a JSON request.

```json
{
    "question":"Who was the singer in The Doors band?",
    "answer":"Jim Morisson",
    "difficulty": 2,
    "category": 5
}
```
- Returns: the question id of a newly created item.

```json
{
    "question_id": 43,
    "success": true
}
```

`POST '/questions'`

- Sends a request to search for a specific question by search term.
- Request Arguments: `search_term` - passed in the body of a JSON request.

```json
{
    "search_term":"Tom Hanks"
}
```
- Returns: a list of questions matching the search criteria, total number of matching questions, current category.

```json
{
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
    ],
    "current_category": "",
    "success": true,
    "total_questions": 1
}
```

`POST '/categories'`

- Sends a request to add a new category.
- Request Arguments: `category` - passed in the body of a JSON request.

```json
{
    "category":"Cinema"
}
```
- Returns:  the category id of a newly created item.

```json
{
    "category_id": 8,
    "success": true
}
```

`DELETE '/categories/<int:category_id>'`

- Sends a request to delete a category based on a category id.
- Request Arguments: `category_id` - passed as a url parameter.
- Returns: If the transaction is successful, only a success indicator is returned.

```json
{
    "success": true
}
```

`POST '/quizzes'`

- Fetches the next random question taking into account a list of previous questions and current category.
- Request Arguments: `quiz_category`, `previous_questions` - all passed in the body of a JSON request.
If the category id is 0, the next question is chosen from all categories.

```json
{
    "quiz_category":{"id":2,"type":"Art"},
    "previous_questions":[16,18]
}
```
- Returns: a dictionary with question details.

```json
{
    "question": {
        "answer": "Mona Lisa",
        "category": 2,
        "difficulty": 3,
        "id": 17,
        "question": "La Giaconda is better known as what?"
    },
    "success": true
}
```
### Error handling
If an API request is successful, a `success` indicator equal to `true` as well as an HTTP status code of 200 will be included in each server response. In case of an error, the success parameter will be equal to `false`. In addition, an error message and code will be provided.

```json
{
    "error": 404,
    "message": "Not found",
    "success": false
}
```

## Testing

In your terminal, navigate to the `/backend` folder and activate your virtual environment as described above.

The backend application loads its secrets as environment variables from an `.env` file. Please create one in the `/backend` folder as shown above.

Finally, execute the following commands to perform testing:

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_app.py
```
