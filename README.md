# Grocery Store

# Intructions to run the applilcation

## Frontend
```
cd frontend
```

### Install dependencies
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```


## Backend
```
cd backend
```

### Set up virtual environment
```
python3 -m venv .env
```


### Activate virtual environment

#### Windows
```
.env\Scripts\activate
```

#### Linux
```
source .env/bin/activate --user
```

### Install dependencies
```
pip install --no-cache -r requirements.txt
```

### Run server
```
python app.py
```

celery -A app.celery worker -l info

celery -A app.celery beat --max-interval 1 -l info


for celery worker:
cd backend/
source wsl_env/bin/activate --user
celery -A app.celery worker -l info



### Login credentials
```json
{
    "email": "admin@email.com",
    "password": "admin"
},
{
    "email": "manager@email.com",
    "password": "manager"
},
{
    "email": "user@email.com",
    "password": "user"
}
```

Access the app at http://localhost:8080

