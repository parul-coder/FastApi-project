
from fastapi import FastAPI, Depends
from . import schemas,models
from database import engine,Base

app = FastAPI()


models.Base.metadata.create_all(bind = engine)

@app.get('/')
def show():
	return 'welcome to crud test'




@app.post('/blog')
def create(request:schemas.Blog):
	pass
