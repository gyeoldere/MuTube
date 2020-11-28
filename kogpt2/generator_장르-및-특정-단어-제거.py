# -*- coding: utf-8 -*-
import os
import torch
from gluonnlp.data import SentencepieceTokenizer
from kogpt2.model.sample import sample_sequence
from kogpt2.utils import get_tokenizer
from kogpt2.utils import download, tokenizer
from kogpt2.model.torch_gpt2 import GPT2Config, GPT2LMHeadModel
import gluonnlp
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--temperature', type=float, default=0.7,
                    help="temperature 를 통해서 글의 창의성을 조절합니다. 1에 가까울수록 창의적") 
parser.add_argument('--top_p', type=float, default=0.9,
                    help="top_p 를 통해서 글의 표현 범위를 조절합니다.")
parser.add_argument('--top_k', type=int, default=40,
                    help="top_k 를 통해서 글의 표현 범위를 조절합니다.")
parser.add_argument('--text_size', type=int, default=30,#20,
                    help="결과물의 길이를 조정합니다.")
parser.add_argument('--loops', type=int, default=-1,
                    help="글을 몇 번 반복할지 지정합니다. -1은 무한반복입니다.")
parser.add_argument('--tmp_sent', type=str, default="사랑",
                    help="글의 시작 문장입니다.")
parser.add_argument('--load_path', type=str, default="./checkpoint/KoGPT2_checkpoint_37000.tar",
                    help="학습된 결과물을 저장하는 경로입니다.")

args = parser.parse_args()
'''
pytorch_kogpt2 = {
    'url':
    'checkpoint/pytorch_kogpt2_676e9bcfa7.params',
    'fname': 'pytorch_kogpt2_676e9bcfa7.params',
    'chksum': '676e9bcfa7'
}
'''
pytorch_kogpt2 = {
    'url':
    'https://kobert.blob.core.windows.net/models/kogpt2/pytorch/pytorch_kogpt2_676e9bcfa7.params',
    'fname': 'pytorch_kogpt2_676e9bcfa7.params',
    'chksum': '676e9bcfa7'
}

kogpt2_config = {
    "initializer_range": 0.02,
    "layer_norm_epsilon": 1e-05,
    "n_ctx": 1024,
    "n_embd": 768,
    "n_head": 12,
    "n_layer": 12,
    "n_positions": 1024,
    "vocab_size": 50000
}

def auto_enter(text):
    text = (text.replace("   ", "\n"))
    text = text.split("\n")

    text = [t.lstrip() for t in text if t != '']
    return "\n\n".join(text)

def main(temperature = 0.7, top_p = 0.8, top_k = 40, tmp_sent = "", text_size = 100, loops = 0, load_path = ""):
    ctx = 'cuda'
    cachedir = '~/kogpt2/'
    save_path = './checkpoint/'
    # download model
    model_info = pytorch_kogpt2
    model_path = download(model_info['url'],
                          model_info['fname'],
                          model_info['chksum'],
                          cachedir=cachedir)
    # download vocab
    vocab_info = tokenizer
    vocab_path = download(vocab_info['url'],
                          vocab_info['fname'],
                          vocab_info['chksum'],
                          cachedir=cachedir)
    # Device 설정
    device = torch.device(ctx)
    # 저장한 Checkpoint 불러오기
    checkpoint = torch.load(load_path, map_location=device)

    # KoGPT-2 언어 모델 학습을 위한 GPT2LMHeadModel 선언
    kogpt2model = GPT2LMHeadModel(config=GPT2Config.from_dict(kogpt2_config))
    kogpt2model.load_state_dict(checkpoint['model_state_dict'])

    kogpt2model.eval()
    vocab_b_obj = gluonnlp.vocab.BERTVocab.from_sentencepiece(vocab_path,
                                                              mask_token=None,
                                                              sep_token=None,
                                                              cls_token=None,
                                                              unknown_token='<unk>',
                                                              padding_token='<pad>',
                                                              bos_token='<s>',
                                                              eos_token='</s>')

    tok_path = get_tokenizer()
    model, vocab = kogpt2model, vocab_b_obj
    tok = SentencepieceTokenizer(tok_path)

    if loops:
        num = 1
    else:
        num = 0

    try:
        load_path.split("/")[-2]
    except:
        pass
    else:
        load_path = load_path.split("/")[-2]

    
    print("ok : ",load_path)

    if not(os.path.isdir("samples/"+ load_path)):
        os.makedirs(os.path.join("samples/"+ load_path))

    name_list=[]
    
    while 1:
        sent =''
        if tmp_sent == "":
            tmp_sent = input('input : ')
        sent = sent+tmp_sent

        toked = tok(sent)
        

        if len(toked) > 1022:
            break

        sent = sample_sequence(model, tok, vocab, sent, text_size, temperature, top_p, top_k)
        sent = sent.replace("//", "\n") # 비효율적이지만 엔터를 위해서 등장
        sent = sent.replace("</s>", "") 
        sent = auto_enter(sent)
        
        
        #print(tmp_sent,len(tmp_sent))        
        
        
        #-- 장르가 포함되면
        ## 제거할 장르 list # 아이돌 노래만 모아서 '아이돌'이라는 단어는 남겨두었음
        genre=['pop','팝','댄스','dance','클럽','club','외힙','힙합','hiphop','hop','트로트','일렉','rnb','알앤비','알엔비','락','록','밴드','rock','피아노','첼로','바이올린','연주곡','뉴에이지','newage','new age','ccm','송가','재즈','째즈','jazz','클래식','트로피칼','트로피컬','레게','여자','여왕','여성','걸그룹','남자','남성','보이그룹','인디','발라드','랩','rap','래퍼','ost','디스코','동요','영화','드라마','크리스마스','christmas','어쿠스틱','jpop','일본','애니','재지','헤비메탈','라틴','블루스','펑크','funk','솔로','그룹','해외','국내','리믹스','remix','기타','신스']

        ## 맨 앞에 장르 이름이 오는 경우를 제외한다: - input 다음단어 ~끝까지 검사
        genre_state=0 #장르 있는 경우 반복문으로 돌아가기 위함
        
        for i in genre:
            if i in sent[len(tmp_sent):len(sent)]:
                #print('genre inside')#동작 확인용
                genre_state=1
                break #장르 검사 for문 탈출용
                
        if genre_state==1:
            continue #아래 코드 실행 X
        
        
       
        
        #--특정 단어 뒤에 가수 이름 나올때 존재 - ex) pop의 거장 OOO
        #--숫자있을경우 pass (xx년대 삭제, 오류 추정 키워드 삭제,x월의,x탄,part x ~~ 삭제)
        # ᄂ,ᄋ,ᄏ,ᄒ은 'ㄴ,ㅇ,ㅋ,ㅎ'이아님(옛한글)
        # 그외 이상한 단어/영어조합
        keyword=['거장','황제','작곡가','의 명곡','의명곡','트렌드세터','아티스트','의 음악','음악가',' 신','흐름 ','숙적','형님','누님','스타','주도한','리릭시스트','가수','저격수','작사가','프로듀서','예찬','사수','제왕','아이콘','신에서','dj','보컬리스트','마지막','예찬론자','레전드','대가','신화','대명사','대세','대부','선구자','뮤지션','레이블','0','1','2','3','4','5','6','7','8','9','시밤','음악 신나는','산뜻한 산뜻한','하아요','누굴까','ss','ᄋ','ᄒ','ᄂ','ᄏ','월','번째','번 째','세대','에브리데이 에브리데이','탄','part','잘생기','잘생긴','땐네','속반','브랜드','료를','이양','oo','싸월드','top','힙존','미츠','자세 가을','아른비','가을뜻','마다','탐미','카페의상','오는몰래','카페 cafe','클래시아','의요한','사운드로','4대','람덤','수놓','nct','exo','엑소','4요','uture','쿠방','tkdgy','nbn','ns','am','쿨다운','퇴근길 브런치','포레스트 캠프','에ck','0분','할로윈','우리에','잘톤','시간에','주는돈','우리꺼','런치여행','여친','남친','한번쯤쿵','시절이송','oul','죽임','죽이','비붐','이기는','노바','슬슬장','고도듯한','위에서뻥','모음2','모음1','느낌 여유','안좋은','도색','시부야','림을','리지웃','합의','kg','노래 신나는','플레이야','계의','세습','째줄','후회노','노매장','렉하','리듬보컬','악동','하루부터곡','사운드의 하면','의하면','준억','예후','숙명','꺼내듣기','보자','줄거리','사골국','trance','사이키델릭','충만한바람','주는옴','의가의','동양','사홍길','의든','luv song','new york','루츠','세터지는','영국민','no','le','ed','es','er','el','ey','la','지ist','가의길','사의길','가즈아','마음 메탈','르진','의진','드를','이상업','망향','파이','x','의경','아이 ','준넘','으로우는','문신','맨오브','의에서','aomg','이자칫','반렛','가보쟈','업타운',' 외','에칠','집성','콜라보 ','을 미치게','을싸','념지','끌어낸 ','단이','처음다는','태호','댄서블','가명','드는','드루와','꺼내버림','잠든','총포','내빈다','씬을','전그','그라운드']
        
        ## 맨 앞에 위에서 지정한 단어가 오는 경우 제외- input 다음단어~끝까지 검사
        keyword_state=0 #장르 있는 경우 반복문으로 돌아가기 위함
        
        for i in keyword:
            if i in sent[len(tmp_sent):len(sent)]:
                #print('keyword inside',sent)#동작 확인용
                keyword_state=1
                break #장르 검사 for문 탈출용
                
        if keyword_state==1:
            continue #아래 코드 실행 X
        
        
        #숫자 있는것 빼버려서 제외
        '''
        #-- 가끔 마지막단어가 숫자로 나올때가 있는데 이를 없앰 ex) : 신나는 음악모음 2
        for i in range(0,len(sent)):
            try:
                int(sent[len(sent)-1]) #마지막글자를 숫자로 바꾸는게 오류가 나지 않는다?? :숫자 
                sent=sent[:len(sent)-1] #숫자제거
                #print('del num')#동작 확인용
            except:
                break # 검사종료
        '''
        
        
        #-- 플레이리스트 이름에 엔터 or <unk> 있는 경우 space로 바꿈
        sent=sent.replace('\n',' ').replace('<unk>',' ')
        
        
        #-- 공백 2개일경우 1개로 바꿈
        sent=sent.replace('  ',' ')

        
        #-- 마지막글자 공백 제거
        if(sent[len(sent)-1]==' '): #마지막글자 공백일경우
            sent=sent[:len(sent)-1] #공백제거
        
        
        
        #-- 중복 이름 생성x
        if sent in name_list:
            continue #아래 코드 실행 X
        
        # 중복x->list에 추가
        name_list.append(sent)
        print(sent)

        
        
        #
        now = [int(n) for n in os.listdir("./samples/" + load_path)]
        
        try:
            now = max(now)
        except:
            now = 1

        f = open("samples/"+ load_path + "/" + str(now + 1), 'w', encoding="utf-8")
        
        head = [load_path, tmp_sent, text_size, temperature, top_p, top_k]
        head = [str(h) for h in head]
        f.write(",".join(head))
        f.write(",")
        f.write(sent)
        f.close()

        #tmp_sent = ""

        if num != 0:
            num += 1
            if num >= loops:
                print("good")
                return

if __name__ == "__main__":
    # execute only if run as a script
    main(temperature=args.temperature, top_p=args.top_p, top_k=args.top_k, tmp_sent=args.tmp_sent, text_size=args.text_size, loops=args.loops+1, load_path=args.load_path)