# 국내 코로나 현황 for HA

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

<br>

## Installation
### Manual
- HA 설치 경로 아래 custom_components에 covid19_kr폴더 안의 전체 파일을 복사해줍니다.<br>
  `<config directory>/custom_components/covid19_kr/`<br>
- Home-Assistant 를 재시작합니다<br>
### HACS
- HACS > Integretions > 우측상단 메뉴 > Custom repositories 선택
- 'https://github.com/huimang2/covid19_kr' 주소 입력, Category에 'integration' 선택 후, 저장
- HACS > Integretions 메뉴 선택 후, '국내 코로나 현황' 검색하여 설치

<br>

## Usage
### Custom Integration
- 구성 > 통합구성요소 > 통합구성요소 추가하기 > 국내 코로나 현황 선택 > 지역(시·도) 선택후, 확인.

<br>
