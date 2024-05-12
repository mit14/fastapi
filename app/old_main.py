from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body

#importing pydantic lib for POST API validation 
from pydantic import BaseModel
from typing import Optional
from random import randrange

import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

#creating a new class and passing all mandatory elements of the API POST requerst. 
class Post(BaseModel):
    title: str
    content: str
    # = is for the optional feild, set a default value 
    published: bool = True
    #rating: Optional[int] = None

#connection to db
while True:
    try:
        #conn = psycopg2.connect(host, database, user, password, column name mapping )
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='KhiaraLeo@1412', cursor_factory= RealDictCursor )
        cursor = conn.cursor()
        print("database connection was successful")
        break
    except Exception as error:
        print("Connection to DB failed")
        print("Error:", error)
        time.sleep(2)



my_post = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "Fav food", "content": "My fav food", "id": 2}]



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts  = cursor.fetchall()
    print(posts)
    return {"data": posts}



#pass status code in decortator everytime you create a post 
@app.post("/posts",  status_code=status.HTTP_201_CREATED )
def create_posts(post:Post):
    # can also use cursor.execute and then use f string to insert, but that is security issue (SQL ijection, use can write a SQL qurey in the data back)
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) """, (post.title, post.content, post.published))


    # #post here is in the pydantic structure/format
    # print(post)
    # #converted the post to a python dictionary, and we can send back as return 
    # #print(post.dict())
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,10000000000)
    # my_post.append(post_dict)
    # return {"data": post_dict}
#title str, contect str,



@app.get("/post/{id}")
#incdluding : int will confirm on user end if correct values are being sent in this case it needs to be int, it will also convert from str to int 
def get_post(id: int, response: Response):
    post = [p for p in my_post if p['id']==id ]
    #import response to send status code, also pass in the variable 
    if not post:
        #response.status_code = 404 ////////////this was the hard coding way 
        # response.status_code = status.HTTP_404_NOT_FOUND  #imported status and select the code you find okay 
        # return {'message': f'post with {id} was not found.'}

        #easier than above, import HTTP Exception and pass two parameters
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found.')
    return {"data": post}


@app.delete("/post/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # can raise an exception like this but this is not the proper way, instead i can pass the status code in the decorator 
    #raise HTTPException(status_code= status.HTTP_204_NO_CONTENT)
    #we dont send data back when using 204, so send the response instead 
    return Response(status_code=status.HTTP_204_NO_CONTENT)