from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

from .. database import get_db, engine
from .. import models, schemas, oauth2

# for complex application we can use this prefix so that we can remove /post from everoute and its added by default
router= APIRouter(
    prefix="/posts",
    tags=['Posts']
)



@router.get("/",  response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = "") :
    # cursor.execute(""" SELECT * FROM posts""")
    # posts  = cursor.fetchall()
    print(limit)
    # this is to get all the posts in the db 
    # posts = db.query(models.Post).all()
    #limit the # of resutls , offset is for skip , for optional use filter for keyword 
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #in SQL alchamey, by default the join is innter join, so we have to pass a flag for otter join. Also, we need to import from sqlalchemy import func to count 
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #this is get only post that user created. example note taking app where the user notes are personal 
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts


#pass status code in decortator everytime you create a post 
@router.post("/",  status_code=status.HTTP_201_CREATED, response_model=schemas.Post )
def create_posts(post:schemas.postCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # # can also use cursor.execute and then use f string to insert, but that is security issue (SQL ijection, use can write a SQL qurey in the data back)
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone() #This will return new post created 
    # conn.commit() #commit all changes or it wont save in the DB
    

    # this is very inefficient way of getting elements of the post. instead we can just unpack the dictionary by using the pydentic model and two **post.dict() or post.model_dump()
    #new_post=  models.Post(title=post.title, content = post.content, published = post.published)

    print(current_user.id)
    new_post = models.Post(owner_id =current_user.id, **post.model_dump()) #owner_id is fetched form the current user and then attached with the post 
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #retrive new post with the id and default details 
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
#incdluding : int will confirm on user end if correct values are being sent in this case it needs to be int, it will also convert from str to int 
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #the reason we do as int is if the user send back the string, it will response as not a valid entry 
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),)) #sometimes there are issue so we put comma after the str(id)
    # post = cursor.fetchone()
    # print(current_user)
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")
    
    print(post)
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post= cursor.fetchone()
    # conn.commit()
        # if deleted_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with the id: {id} was not found.')
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with the id: {id} was not found.')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not Authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.postCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # if updated_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} was not found.')

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {id} was not found.')
    
    if post.owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not Authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
