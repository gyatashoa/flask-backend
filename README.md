
# Doctr Machine Learning Model Api

This repository consist of a flask backend and Machine Learning model ( it uses the Gaussian Naive Bayes Algorithm ) built with
scikit learn. This is used in predicting in predicting a disease,its probability and required prescription


## Run Server Locally

Clone the project

```bash
  git clone https://github.com/gyatashoa/flask-backend
```

Go to the project directory

```bash
  cd flask-backend-master
```
create .env file

```bash
    touch .env
```

set up environmental variables in .env file

``` 
    SECRET_KEY=12345678
    POSTGRES_DB_URI=sqlite:///db.sqlite3
```

create .flaskenv file

```bash
    touch .flaskenv
```

set up flask config with .flaskenv file

```
    export FLASK_ENV=development
    export FLASK_APP=src
```

Install required python modules

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  flask run
```


## API Reference

#### Get all symptoms

```http
  GET /api/v1/predictions/symptoms
```

| Result | Type     | Description                |
| :-------- | :------- | :------------------------- |
| symptoms | `array` | array of all symptoms |

#### Make a predictions

```http
  POST /api/v1/predictions/predict
```

| Request Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `symptoms as key`      | `JSON` | The symptoms you would like to predict |


| Results | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Disease`      | `String` | Predicted disease |
| `probability` | `Float`| Models probability of predicted disease|
|`prescriptions`|`Array` | All prescriptions|




## Documentation

[Documentation](https://linktodocumentation)


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [@Asamoah Yeboah Felix](https://www.github.com/gyatashoa)

## 🚀 About Me
My name Asamoah Yeboah Felix, A final year Computer Science student at KNUST

