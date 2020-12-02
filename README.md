![image](https://user-images.githubusercontent.com/45448731/100836430-a14e0500-34b2-11eb-915f-1a19cbf82169.png)
<br>

## 목차  
- [팀원](#팀원)  
- [주제](#주제)  
- [필요성](#필요성)  
- [프로젝트 일정](#프로젝트-일정)   
- 
---
## 팀원 
이름|역할|비고 
:---:|:---:|:---:
[이한결](https://github.com/gyeoldere)|팀 총괄|팀장
이승민|플레이리스트 생성|
[정민지](https://github.com/minji-o-j)|플레이리스트 제목 생성|
[한우정](https://github.com/dnwjddl)|데이터 전처리 및 분석|
<br>

---
## 주제
- 플레이리스트 기반 새로운 플레이리스트 생성
- 플레이리스트 제목 생성  

![image](https://user-images.githubusercontent.com/45448731/96713427-88463480-13db-11eb-9f64-14eeeeabc5ab.png)
<br>

---
## 필요성
### 1.
### > 기존 협업 필터링 방식  
![image](https://user-images.githubusercontent.com/45448731/100837868-c479b400-34b4-11eb-889b-80328ec81f26.png)
- **User-based Recommendation**: 나와 유사한 성향을 지닌 사람을 기반으로 그 사람이 들은 노래를 추천해줌
- **Item-based Recommendation**: 내가 이전에 들은 노래(혹은 좋아요 누른 노래)를 기반으로 그 노래와 유사한 다른 노래를 추천해주는 방식

### > 협업 필터링 방식의 문제점
- 데이터를 수집 할 만한 **충분한 이용자가 갖춰진 경우에만 사용 가능**
- 최신 곡의 경우 이를 **추천 할 수 있는 정보가 쌓일 때까지 추천이 어려움**
- 현재 유통되는 음악 추천 프로그램은 대부분 사용자가 월정액을 이용하거나, 곡을 구매 해야지만 제대로 사용할 수 있는 등의 **금전적 제약 조건이 존재**

### > 협업 필터링 방식의 해결 방법
![image](https://user-images.githubusercontent.com/45448731/100839146-13284d80-34b7-11eb-8723-36f00391e244.png)


---
## 프로젝트 일정
<img src="https://user-images.githubusercontent.com/45448731/100837059-cf801480-34b3-11eb-8021-3e142db708e8.png" width="800px"/>  

#### 진행 상황
- **계획 설정**: 9/17~10/10
- **기본 설계**: 9/29~11/12
- **상세 설계**: 11/03~11/16
- **구현**: 11/16~11/27
- **최종 발표 준비**: 11/27~12/02
<br>

---
## 
- [`main.py`](https://github.com/gyeoldere/MuTube/blob/master/main.py) : data 크롤링 코드   
- [`아이돌 노래_2016_2020.tsv`](https://github.com/gyeoldere/MuTube/blob/master/%EC%95%84%EC%9D%B4%EB%8F%8C%20%EB%85%B8%EB%9E%98_2016_2020.tsv) : 우리 팀 Dataset (2016년 ~ 2020년 아이돌 노래)
