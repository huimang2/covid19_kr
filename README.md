# 국내 코로나 현황 for HA

![HAKC)][hakc-shield]
![HACS][hacs-shield]
![Version v1.4][version-shield]

국내 코로나 현황 컴포넌트입니다. <br>
보건복지부 및 각 지자체 홈페이지에서 현황을 크롤링하여 센서로 표시합니다. <br>

통합구성요소를 지원하며, 시/도별 현황 및 도시별 현황을 각각 표시할 수 있습니다. <br>

<br>

## Version history
| Version | Date        | 내용              |
| :-----: | :---------: | ----------------------- |
| v1.0.0  | 2021.08.17  | First version  |
| v1.0.1  | 2021.08.17  | 오타 수정 |
| v1.0.2  | 2020.08.17  | 오타 수정 |
| v1.1.0  | 2020.08.17  | 코드 수정 |
| v1.1.1  | 2020.08.17  | 오류 수정 |
| v1.2.0  | 2020.08.18  | 코드 수정 |
| v1.2.1  | 2020.08.19  | 코드 수정 |
| v1.2.2  | 2020.08.22  | 시도와 도시의 이름이 같을 때 컴포넌트가 생성되지 않는 문제 수정 |
| v1.2.3  | 2020.08.23  | 부산 센서 오류 수정 |

<br>

## Installation
### Manual
- HA 설치 경로 아래 custom_components에 covid19_kr폴더 안의 전체 파일을 복사해줍니다.<br>
  `<config directory>/custom_components/covid19_kr/`<br>
- Home-Assistant 를 재시작합니다<br>
### HACS
- HACS > Integretions > 우측상단 메뉴 > Custom repositories 선택
- 'https://github.com/huimang2/covid19_kr' 주소 입력, Category에 'integration' 선택 후, 저장
- HACS > Integretions 메뉴 선택 후, '[KR] 코로나 현황' 검색하여 설치

<br>

## Usage
### Custom Integration
- 구성 > 통합구성요소 > 통합구성요소 추가하기 > 국내 코로나 현황 선택 > 지역(시·도) 선택후, 확인.

<br>


### 지원현황
| 도·광역시 | 시·군·구 |
| :-----: | :-----: |
| 전국 ||
| 서울 | 강남구, 강동구, 강북구, 강서구, 관악구, 광진구, 구로구, <br> 금천구, 노원구, 도봉구, 동대문구, 동작구, 마포구 , 서대문구, <br> 서초구, 성동구, 성북구, 송파구, 양천구, 영등포구, 용산구, <br> 은평구, 종로구, 중구, 중랑구, 기타 |
| 부산 | 중구, 서구, 동구, 영도구, 부산진구, 동래구, 남구, 북구, 해운대구, 사하구, <br> 금정구, 강서구, 연제구, 수영구, 사상구, 기장군, 기타 |
| 대구 | |
| 인천 | 중구, 동구, 미추홀구, 연수구, 남동구, 부평구, 계양구, <br> 서구, 강화군, 옹진군, 기타 |
| 광주 | |
| 대전 | |
| 울산 | 중구,남구,동구,북구,울주군 |
| 세종 | |
| 경기 | 수원, 고양, 용인, 성남, 부천, 안산, 화성, 남양주, 안양, 평택, <br> 의정부, 파주, 시흥, 김포, 광명, 광주, 군포, 이천, 오산, 하남, <br> 양주, 구리, 안성, 포천, 의왕, 여주, 양평, 동두천, 과천, 가평, <br> 연천 |
| 강원 | 춘천, 원주, 강릉, 동해, 태백, 속초, 삼척, 홍천, 횡성, 영월, <br> 평창, 정선, 철원, 화천, 양구, 인제, 고성, 양양 |
| 충북 | |
| 충남 | |
| 전북 | |
| 전남 | |
| 경북 | 포항, 경주, 김천, 안동, 구미, 영주, 영천, 상주, 문경, 경산, <br> 군위, 의성, 청송, 영양, 영덕, 청도, 고령, 성주, 칠곡, 예천, <br> 봉화, 울진, 울릉 |
| 경남 | 창원, 진주, 통영, 사천, 김해, 밀양, 거제, 양산, 의령, 함안, <br> 창녕, 고성, 남해, 하동, 산청, 함양, 거창, 합천 |
| 제주 | |
| 검역 | |

<br>

## 데이터 수집 사이트
- 전국 / 도·광역시: http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13
- 서울: https://www.seoul.go.kr/coronaV/coronaStatus.do
- 부산: https://www.busan.go.kr/covid19/Corona19.do
- 인천: https://www.incheon.go.kr/covid19/index
- 울산: https://covid19.ulsan.go.kr/index.do
- 경기: https://www.gg.go.kr/contents/contents.do?ciIdx=1150&menuId=2909
- 강원: http://www.provin.gangwon.kr/covid-19.html
- 경북: https://gb.go.kr/corona_main.htm
- 경남: http://xn--19-q81ii1knc140d892b.kr/main/main.do

[version-shield]: https://img.shields.io/badge/version-v1.2.3-orange.svg
[hakc-shield]: https://img.shields.io/badge/HAKC-Enjoy-blue.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-red.svg
