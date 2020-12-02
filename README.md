![image](https://user-images.githubusercontent.com/45448731/100836430-a14e0500-34b2-11eb-915f-1a19cbf82169.png)
<br>

## 목차  
- [팀원](#팀원)  
- [주제](#주제)  
- [필요성](#필요성)  
- [개발 기술 내용 및 진행과정](#개발-기술-내용-및-진행과정)  
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
<br>

### > 협업 필터링 방식의 문제점
- 데이터를 수집 할 만한 **충분한 이용자가 갖춰진 경우에만 사용 가능**

- 최신 곡의 경우 이를 **추천 할 수 있는 정보가 쌓일 때까지 추천이 어려움**

- 현재 유통되는 음악 추천 프로그램은 대부분 사용자가 월정액을 이용하거나, 곡을 구매 해야지만 제대로 사용할 수 있는 등의 **금전적 제약 조건이 존재**
<br>

### > 협업 필터링 방식의 해결 방법
![image](https://user-images.githubusercontent.com/45448731/100839146-13284d80-34b7-11eb-8723-36f00391e244.png)
- **콘텐츠 기반 필터링** 방법을 통하여 기존 사용자의 데이터 없이 곡을 추천하는 방식 제시
  - 콘텐츠 기반 필터링 방법: 콘텐츠(음악정보)에 대한 분석을 기반으로 추천하는 방법
  
- 사용자 데이터 불균형에 따른 음악 산업 내 격차를 해소할 것으로 기대함
<br>

### 2.
### > 최근 많이 들은 곡 기반 노래 추천의 문제점
<img src="https://user-images.githubusercontent.com/45448731/100839643-e32d7a00-34b7-11eb-976b-b0aeead1d2e5.png" width="800px"/> 
<br>

### > 최근 많이 들은 곡 기반 노래 추천의 해결 방안
- 단순하게 ＂최근 많이 들은 곡”기반 플레이리스트 제시가 아닌 **“사용자 플레이리스트 기반”** 추천 플레이리스트 제공
<br>

### 3.
### > 자동 생성된 플레이리스트의 문제점과 해결방안
![image](https://user-images.githubusercontent.com/45448731/100839942-6949c080-34b8-11eb-813b-ba3422274d65.png)
<br>

---
## 개발 기술 내용 및 진행과정
- [중요한 속성 파악을 위한 데이터 분석 진행](#중요한-속성-파악을-위한-데이터-분석-진행)
- [추천 시스템 모델 훈련 방법](#추천-시스템-모델-훈련-방법)
- 
### 중요한 속성 파악을 위한 데이터 분석 진행
[`데이터 분석.ipynb`](https://github.com/gyeoldere/MuTube/blob/master/%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B6%84%EC%84%9D.ipynb)

- 가수, 소속사, 성별, 작사, 작곡가의 경우 쏠림이 적게 나타남

- 순위가 없는 비율이 전체의 75% 이상을 차지할 정도로 크므로 최고 순위를 고려하지 않을 예정
<br>

### 추천 시스템 모델 훈련 방법
![image](https://user-images.githubusercontent.com/45448731/100840620-829f3c80-34b9-11eb-8251-df6f5c94e3d0.png)  


[`최종모델+기능시연.ipynb`](https://github.com/gyeoldere/MuTube/blob/master/%EC%B5%9C%EC%A2%85%EB%AA%A8%EB%8D%B8%2B%EA%B8%B0%EB%8A%A5%EC%8B%9C%EC%97%B0.ipynb): **데이터 분석 ~ 완료된 클러스터링 데이터 불러오기** 부분 참조

#### 1. 데이터 정제
- 일본어 가사, 중국어 가사 삭제
  - 가사 데이터로 한국어 형태소 분석을 통해 클러스터링 예정이기 때문
  
- 음악이 아닌 데이터(ex. 콘서트 대본) 삭제
- 가사가 N/A 값인 데이터 삭제 `-N/A: Not Applicable 또는 Not Available, 해당 없음/공란 의 의미`
  - 클러스터링 단계에서는 가사만 사용됨
  
- 중복된 가사 제거
- 이모티콘을 포함한 특수문자 모두 제거 
  - 정규식 이용
  
- 아무것도 남지 않은 데이터 N/A로 변경
- N/A 값 모두 제거

#### 2. 토크나이징
- 불용어 지정 - `불용어: 토큰화를 실행하고 난 뒤 의미적 기능을 상실했다고 생각해 제거하는 형태소`

- Okt 형태소 분석기를 사용하여 형태소 단위로 단어 분류 및 일정 수준의 정규화 진행

#### 3. Doc2Vec
> 문장을 벡터화하는 Word2vec의 방식을 확장하여 paragraph(문단, 이 모델에서는 노래 가사 전체)를 벡터화 하는 방식

- Gensim에서 doc2vec와 TaggedDocument를 불러와 사용
```
  - Gensim: 문서 사이의 유사도 계산과 텍스트 분석을 돕는 라이브러리
  - TaggedDocument: 본 단계 이후 클러스터링의 정확도를 높이기 위한 방법으로 Document(토큰화된 단어 데이터)에 tag를 달아줌
```
- 주요 hyperparameter는 vector size = 100, window = 3, epoch = 40, min_count = 0을 사용
```
vector_size:  임베딩 벡터의 크기, 벡터 사이즈가 클 수록 생성된 모델의 성능이 정교해지나 훈련 시간 및 메모리의 크기가 커짐
window: 훈련시 앞 뒤로 고려하는 단어의 개수, 사이즈가 커지면 훈련 시간 증가
epochs: 반복 횟수
min_count: 데이터에 등장하는 단어의 최소 빈도수 – word2vec/doc2vec는 자주 등장하지 않는 단어에 대해서는 제대로 학습이 이루어지지 않는데, 우리의 경우는 모든 단어 고려함
```

#### 4. 클러스터링
> 비지도 학습으로, 데이터를 몇 개의 단위로 분류하는 작업

- 몇몇 클러스터링은 hyperparameter로 몇 개의 클러스터로 배분할 것인지 결정해 주어야 함

- 따라서, **Hierarchical Clustering**을 통해 클러스터링의 경향성을 확인한 뒤, 클러스터의 개수를 정했음

  - Hierarchical Clustering : 덴드로그램(Dendrogram, 계층적 트리 모형) 을 이용하여 개별 개체들을 순차적, 계층적으로 유사한 개체와 통합하여 군집화를 수행하는 알고리즘, 클러스터의 수를 지정하지 않아도 알아서 클러스터링 수행
  
  - 덴드로그램을 적절한 수준에서 자르면 전체 데이터를 몇 개의 군집으로 나눌 수 있게 됨
![image](https://user-images.githubusercontent.com/45448731/100841742-0c033e80-34bb-11eb-8ef7-dbf2f8af3c44.png)

- Hierarchical Clustering을 통하여 정보 (n=10)을 가지고 bottom up(아래-->위) 방식의 Hierarchical Agglomerative clustering(병합 군집)을 수행
  - Agglomerative clustering: top down 방식인 hierarchical clustering 방식과 반대로(bottom up) 진행되지만 결과값은 비슷함

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
