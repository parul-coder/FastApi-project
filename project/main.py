from fastapi import FastAPI,Depends,status,Response, HTTPException
from . import schemas,models
from sqlalchemy.orm import Session 
from database import engine,SessionLocal


app = FastAPI()

models.Base.metadata.create_all(bind = engine)

@app.get('/')
def view():
	return 'Welcome to FastAPI Project '


#dependencies
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()



#inserting values to the tables

@app.post('/blog', status_code = status.HTTP_201_CREATED)
def create(data:schemas.Blog, db:Session = Depends(get_db)):
	new_blog = models.Blog(title = data.title, body = data.body)
	db.add(new_blog)
	db.commit()
	db.refresh(new_blog)
	return new_blog


# getting  all values from the tables

@app.get('/blog')
def get_blogs(db: Session = Depends(get_db)):
	blogs = db.query(models.Blog).all()
	return blogs


# getting particular values from table 


@app.get('/blog/{id}',status_code = 200)
def show(id, response : Response, db: Session = Depends(get_db)):
	blog = db.query(models.Blog).filter(models.Blog.id == id).first()

	if not blog:
		raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail = f"blog with {id} didn't exists")
		# response.status_code = status.HTTP_404_NOT_FOUND
		# return {'details':f"blog with {id} didn't exist"}

	return blog



# delete the data from db

@app.delete('/blog/{id}',status_code = status.HTTP_204_NO_CONTENT)
def remove(id, db:Session = Depends(get_db)):

	db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session = False)

	db.commit()
	return 'deleted successfully'



# update the data into db

@app.put('/blog/{id}',status_code = status.HTTP_202_ACCEPTED)
def updated(id, request:schemas.Blog, db:Session = Depends(get_db)):
	db.query(models.Blog).filter(models.Blog.id == id).update({models.Blog.title : request.title}, synchronize_session=False)

	# to update whole request body schema data
	#db.query(models.Blog).filter(models.Blog.id == id).update(request)
	db.commit()
	return 'updated successfully'
