
# from pydantic_settings import BaseSettings, SettingsConfigDict
# import os


# #the point of this is to verify the enviormwent variable and set the proper format 
# class Settings(BaseSettings):
    
#     database_hostname: str
#     database_port: str
#     database_password: str
#     database_name: str
#     database_username: str
#     secret_key: str
#     algorithm: str
#     access_token_expire_minutes: int
#     # model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

#     class Config:
#         _env_file = '.env'




# # settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
# settings = Settings()
