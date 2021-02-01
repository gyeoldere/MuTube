개발 관련 정리: https://github.com/minji-o-j/KoGPT2-finetuning
# KoGPT2-finetuning
# KoGPT2 이용하여 플레이리스트 이름 생성하기
---
- [데이터 수집](#데이터-수집)
---
## 데이터 수집 
### - 태그별 플레이리스트 목록 크롤링  



[`crawling_all.py`](https://github.com/minji-o-j/KoGPT2-finetuning/blob/main/crawling/melon%20playlist/crawling_all.py) : 크롤링 사용 코드
<br><br>

- 각각의 태그마다 고유 번호 존재
![image](https://user-images.githubusercontent.com/45448731/98686741-43933500-23ac-11eb-8d0f-18114fdd1003.png)
<br>

- 찾아본 결과 46985까지 태그 번호가 존재하며, 중간에 빈 숫자가 있더라도 자동으로 넘어가게끔 구현
- 페이지는 플레이리스트개수가10000개 이상이더라도 **10000번까지 로드**되며 이후는 흰 화면이 뜸
<br><br>



## 전처리

### - 데이터 수집 단계

- 플레이리스트에 특수문자가 존재하는 경우가 많았음  
![image](https://user-images.githubusercontent.com/45448731/98688269-016af300-23ae-11eb-82df-6cfc6c12a3dd.png)
<br>

- 특수문자만 제거(`isalnum()`함수 이용)-> **의미없는 단어 생기거나 의도하던 의미와 달라지는 경우 발생**  
  - R&B->RB  
  - S͚O͚F͚T͚ ʙᴛs&ɪᴜ sᴏɴɢs°•[휴식, 공부, 잠] -> SOFTʙᴛsɪᴜsᴏɴɢs휴식공부잠  
  - [취향존중]2020년 10월 신곡 정리[24일 신곡 업데이트] -> 취향존중2020년10월신곡정리24일신곡업데이트  
  
- 따라서 특수문자를 제거하는 대신 **자주 등장하는 특수문자 변경**  

  - 삭제해도 문맥에 이상이 없는 특수문자(‘♬’, ‘♪’, ‘!’ 등) 제거 후 저장  

  - ‘_’는 띄어쓰기로, “[playlist]”, “<playlist>”, “(playlist)”는 “playlist”로 변경 후 저장  

  - R&B의 경우 rnb로 통일  

    

- 이후 `isalnum()` 함수를 이용하여 **특수문자가 없는 플레이리스트만 수집** -> 약 87000개  

  - `isalnum()`함수는 공백도 특수문자로 취급하기 때문에 공백을 없앤 플레이리스트 이름에서 검사 후 원본 이름을 넣는 식으로 수정  

<br><br>

### - 데이터 수집 이후

- 앞에 'NEW', 'Update'라는 수식어를 붙인 경우가 많아서 엑셀에서 맨 앞에 NEW 또는 Update 라는 단어가 있을 경우는 이 단어만 없앰   

