from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..  import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login') #instead of schemas we used fastapi import schemas.UserLogin
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    #OAuth2PasswordRequestForm will return username and password, so we will have to use username insead of password 
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    
    #create a token and return a token 
    access_token = oauth2.create_access_token(data={"user_id":user.id})

    return {"token": access_token, "token_tyle": "bearer"}