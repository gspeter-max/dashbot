
import datetime 
from pydantic import BaseModel
from enum import Enum
import typing 
from pydantic import Field
from yarl import Query

class APIAuthType(str, Enum):
    NONE = 'none'
    APIKEY = 'apikey'
    BEARER = 'bearer'
    BASIC = 'basic'
    JWT =  'jwt'
    DIGEST = 'digest'

class AuthApiKeyModel(BaseModel):
    key : str
    location : str = 'header'
    name : str = 'x-api-key'

class AuthBearerModel(BaseModel):
    token : str 

class AuthBasicAuthModel(BaseModel):
    username : str 
    password : str 

class AuthJwtModel(BaseModel):
    secret : str 
    privateKey : typing.Optional[str] 
    payload : str 
    addTokenTo : str
    algorithm : str
    isSecretBase64Encoded : bool
    headerPrefix : str
    queryParamkey : str
    header : str

class AuthDigestModel(BaseModel):
    username : str
    password : str
    realm : str
    nonce : str
    algorithm : str
    qop : str
    opaque : str


class AutoModel( BaseModel ):
    type : APIAuthType
    apikey : typing.Optional[AuthApiKeyModel] = None
    bearer : typing.Optional[AuthBearerModel] = None
    basic : typing.Optional[AuthBasicAuthModel] = None
    jwt : typing.Optional[AuthJwtModel] = None
    digest : typing.Optional[AuthDigestModel] = None 

class HTTPVerb(str, Enum):
    get = 'GET'
    head = 'HEAD'
    post = 'POST'
    put = 'PUT'
    patch = 'PATCH'
    delete = 'DELETE'
    options = 'OPTIONS'

class NameValueModel( BaseModel ):
    name : str
    value : typing.Any

class ContentType(str, Enum):
    json = 'application/json'
    text = 'text/plain'
    formdata = 'multipart/from-data'

class FormDataModel(BaseModel):
    name : str
    value : str
    type : str

class requestArgumentClass( BaseModel ):
    method : HTTPVerb = Field(HTTPVerb.get)
    url : str = ''
    headers : typing.Optional[typing.List[NameValueModel]] = None
    params : typing.Optional[typing.List[NameValueModel]] = None 
    authModel: typing.Optional[AutoModel] = Field(default_factory= lambda : AutoModel(type = APIAuthType.NONE))
    isHeaderEnabledList : typing.Optional[typing.List[bool]]
    isParamEnabledList : typing.Optional[typing.List[bool]]
    bodyContentType : ContentType = Field( default=ContentType.json )
    body : typing.Optional[str]
    query : typing.Optional[str]
    formData : typing.Optional[typing.List[FormDataModel]]

class responseArgumentClass( BaseModel ):
    statusCode : typing.Optional[int]
    headers : typing.Optional[typing.Dict[str,str]]
    requestHeaders : typing.Optional[typing.Dict[str,str]]
    body : typing.Optional[str]
    formattedBody : typing.Optional[str]
    bodyBytes : typing.Optional[bytes]
    time : typing.Optional[datetime.timedelta]
    sseOutput : typing.Optional[typing.List[str]]
