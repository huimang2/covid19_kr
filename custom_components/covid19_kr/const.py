"""Const for covid19_kr"""

DOMAIN = "covid19_kr"
BRAND = "HUIMANG2"
MODEL = "COVID-19(KR)"
SW_VERSION = "1.1.1"
ATTRIBUTION = "30분에 1번씩 보건복지부 크롤링"

SENSORS = {
    "신규확진자": "mdi:emoticon-sad-outline",
    "누적확진자": "mdi:emoticon-neutral-outline",
    "격리자": "mdi:emoticon-cry-outline",
    "격리해제": "mdi:emoticon-happy-outline",
    "사망자": "mdi:emoticon-dead-outline",
}

ATTRIBUTE = [ "국내발생", "해외유입", "합계" ]

DEFAULT_URL = "http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13"
SIDO_LIST = {
    "전국": {
        "city": [],
        "url": "",
        "selector": "#content > div > div.data_table.midd.mgt24 > table > tbody > tr > td:nth-child({})",
    },
    "서울": {
        "city": ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구 ", " 서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구", "기타"],
        "url": "https://www.seoul.go.kr/coronaV/coronaStatus.do",
        "selector": "#move-cont1 > div:nth-child(3) > table.tstyle-status.pc.pc-table > tbody > tr:nth-child({}) > td"
    },
    "부산": {
        "city": ["중구", "서구", "동구", "영도구", "부산진구", "동래구", "남구", "북구", "해운대구", "사하구", "금정구", "강서구", "연제구", "수영구", "사상구", "기장군", "기타"], 
        "url": "https://www.busan.go.kr/covid19/Corona19.do",
        "selector": "#covid-state-area > div > div.covid-state-table > table:nth-child(1) > tbody > tr:nth-child({}) > td:nth-child(n+2)"
    },
    "대구": {
        "city": [], 
        "url": ""
    },
    "인천": {
        "city": ["중구", "동구", "미추홀구", "연수구", "남동구", "부평구", "계양구", "서구", "강화군", "옹진군", "기타"], 
        "url": "https://www.incheon.go.kr/covid19/index",
        "selector": "#content > div > div > div > div > div:nth-child(2) > div > table > tr:nth-child({}) > td:nth-child(n+3)"
    },
    "광주": {
        "city": [], 
        "url": ""
    },
    "대전": {
        "city": [], 
        "url": ""
    },
    "울산": {
        "city": ["중구","남구","동구","북구","울주군"], 
        "url": "https://covid19.ulsan.go.kr/index.do",
        "selector": "body > div.corona_wrap > div > div > div.localarea_box > table > tbody > tr:nth-child({}) > td"
    },
    "세종": {
        "city": [], 
        "url": ""
    },
    "경기": {
        "city": ["수원", "고양", "용인", "성남", "부천", "안산", "화성", "남양주", "안양", "평택", "의정부", "파주", "시흥", "김포", "광명", "광주", "군포", "이천", "오산", "하남", "양주", "구리", "안성", "포천", "의왕", "여주", "양평", "동두천", "과천", "가평", "연천"], 
        "url": "https://www.gg.go.kr/contents/contents.do?ciIdx=1150&menuId=2909",
        "selector": "#result > div.mt-4.py-4.w-100 > div > div > dl:nth-child(n+2) > dd > *:nth-child({})"
    },
    "강원": {
        "city": ["춘천", "원주", "강릉", "동해", "태백", "속초", "삼척", "홍천", "횡성", "영월", "평창", "정선", "철원", "화천", "양구", "인제", "고성", "양양"], 
        "url": "http://www.provin.gangwon.kr/covid-19.html",
        "selector": "#main > div.inner > div.condition > div > table > tbody > tr:nth-child(2n) > td:not([rowspan])"
    },
    "충북": {
        "city": [], 
        "url": ""
    },
    "충남": {
        "city": [], 
        "url": ""
    },
    "전북": {
        "city": [], 
        "url": ""
    },
    "전남": {
        "city": [], 
        "url": ""
    },
    "경북": {
        "city": ["포항", "경주", "김천", "안동", "구미", "영주", "영천", "상주", "문경", "경산", "군위", "의성", "청송", "영양", "영덕", "청도", "고령", "성주", "칠곡", "예천", "봉화", "울진", "울릉"], 
        "url": "https://gb.go.kr/corona_main.htm",
        "selector": "#contents > div.status > div:nth-child(2) > div > dl:nth-child(n+3) > dd > {}"
    },
    "경남": {
        "city": ["창원", "진주", "통영", "사천", "김해", "밀양", "거제", "양산", "의령", "함안", "창녕", "고성", "남해", "하동", "산청", "함양", "거창", "합천"], 
        "url": "http://xn--19-q81ii1knc140d892b.kr/main/main.do",
        "selector": "#subCnt > div.cont.corona_map > div.city_board > div > div.table.type1.pt10 > table > tbody > tr:nth-child({}) > td:nth-child(n+3)"
    },
    "제주": {
        "city": [], 
        "url": ""
    },
    "검역": {
        "city": [], 
        "url": ""
    },
}
