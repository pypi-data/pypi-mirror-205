import requests
import fake_useragent
import json
class GoodModsLab:
    def __init__(self):
        self.__headers = {"User-agent":str(fake_useragent.FakeUserAgent.random)}
        self.__session = requests.Session()
    def __repr__(self):
        return "<Synchronous API for GoodModsLab>"
    def getbyid(self, id:int) -> (dict | None):
        rs = self.__session.get(f"http://goodmodslab.ru:8000/api/v.1.1/mods/{id}", headers=self.__headers, params={"client_id":"2"}).text
        a = json.loads(rs)
        if a == {"message":"Модификация не найдена"}:
            return None
        return a
    def sort(self, a:list):
        def funcSort(x):
            return -x["likes_count"]
        return sorted(a, key=funcSort)
    def foreachmods(self, game:str = None) -> (list | None):
        if game == None:
            rs = self.__session.get(f"http://goodmodslab.ru:8000/api/v.1.1/mods", headers=self.__headers, params={"client_id":"2"}).text.replace("[", '', 1)[::-1].replace("]", '', 1)[::-1]
            if rs == ['']:
                return None
            rs = str(rs).split("},{")
            a=[]
            for i in rs:
                a.append(json.loads("{"+i.replace('}', '').replace('{', "")+"}"))
            return a
        rs = self.__session.get(f"http://goodmodslab.ru:8000/api/v.1.1/mods", headers=self.__headers, params={"client_id":"2", "game":game}).text.replace("[", '', 1)[::-1].replace("]", '', 1)[::-1]
        rs = str(rs).split("},{")
        a=[]
        for i in rs:
                a.append(json.loads("{"+i.replace('}', '').replace('{', "")+"}"))
        return a
    def getphoto(self, url:str):
        a = url.split("/")
        rs = self.__session.get(f"http://goodmodslab.ru:8000/api/v.1.0/{a[1]}", headers=self.__headers, params={"name" : a[2], "package":"71f1c0659e47746cbb0b394ca386b5b9"}).url
        return rs
    def getfile(self, id:int):
        rs = self.__session.get(f"http://goodmodslab.ru:8000/api/v.1.1/mods/download/{id}", headers=self.__headers, params={"client_id" : 2, "access_token":"none"}).url
        return rs