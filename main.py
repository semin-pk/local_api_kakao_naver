from fastapi import FastAPI, Request
import requests
import urllib.parse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 오리진 허용, 필요에 따라 변경 가능
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # 허용할 메서드 목록
    allow_headers=["*"],  # 모든 헤더 허용, 필요에 따라 변경 가능
)
KAKAO_REST_API = 'faa3869240e454c8a6be06fbc2974992'
KAKAO_API_BASE_URL = 'https://dapi.kakao.com/v2/local/search/keyword.json'

NAVER_CLIENT_ID = 'jT8KskzS98tgkvS71Pvi'
NAVER_CLIENT_SECRET = '86kmWUcflG'
NAVER_API_BASE_URL = 'https://openapi.naver.com/v1/search/local.json'


class Storeinfo(BaseModel):
    place_name: str
    address_name: str
    road_address_name: str
    phone: str


@app.post('/kakao/store/list')
async def kakao_searchlist(request:Request):
    data = await request.json()
    query = data.get('keyword', '')
    print(query)  
    header = {
        'Authorization': f'KakaoAK {KAKAO_REST_API}'
    }
    data = {
        'query': query,
        'sort': 'accuracy',
        'size' : 5
    }
    response = requests.get(url=KAKAO_API_BASE_URL, headers=header, params=urllib.parse.urlencode(data))
    response = response.json()
    store_detail = []
    for document in response['documents']:
        store_detail.append({
            'place_name':document['place_name'],
            'address_name':document['address_name'],
            'road_address_name':document['road_address_name'],
            'phone':document['phone']
        })
    return JSONResponse(store_detail)

@app.post('/naver/store/list')
async def naver_searchlist(request:Request):
    data = await request.json()
    query = data.get('keyword', '')
    print(query)  
    header = {
        "X-Naver-Client-Id":NAVER_CLIENT_ID,
        "X-Naver-Client-Secret":NAVER_CLIENT_SECRET
    }
    data = {
        'query': '교대 스타벅스',
        'display' : 5
    }
    response = requests.get(url=NAVER_API_BASE_URL, headers=header, params=urllib.parse.urlencode(data))
    response = response.json()
    store_detail = [] 
    for item in response['items']:
        store_detail.append({
            'place_name':item['title'].replace('<b>', '').replace('</b>', ''),
            'address_name':item['address'],
            'road_address_name':item['roadAddress'],
            'phone':item['telephone']
        })
    return JSONResponse(store_detail)
    
@app.post('/store/insert')
async def storeinsert(storeinfo: Storeinfo):
    if storeinfo:
        store = {
            'place_name':storeinfo.place_name,
            'address_name':storeinfo.address_name,
            'road_address_name':storeinfo.road_address_name,
            'phone':storeinfo.phone
        }
        print(store)
        result = {
                    'check_response':'ok'
                }
    else:
        result = {
                    'check_response': 'error'
                }
    print(result)
    return JSONResponse(result)


    

