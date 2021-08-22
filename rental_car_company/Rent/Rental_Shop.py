from Car.Instrument_Panel import *
import datetime
import pandas as pd

class car_rent:
    bcar=[]
    open_shop=datetime.date(2021,5,1)
    sonata1 = Sonata()
    sonata2 = Sonata()
    sonata3 = Sonata()
    tucson1 = Tucson()
    tucson2 = Tucson()
    bongo1 = Bongo()
    bongo2 = Bongo()
    tesla1 = Tesla_S()
    tesla2 = Tesla_S()
    tesla3 = Tesla_S()
    carcollection=[sonata1,sonata2,sonata3,tucson1,tucson2,bongo1,bongo2,
                   tesla1,tesla2,tesla3]
    def new_old(a):
        if(a.new_or_old>0):
            return "old"
        else:
            return "new"

    car=['승용차','승용차','승용차','suv','suv','트럭','트럭','전기승용차','전기승용차','전기승용차']
    model=['Sonata','Sonata','Sonata','Tucson','Tucson','Bongo','Bongo','Tesla_S','Tesla_S','Tesla_S']
    ran=[sonata1.mileage,sonata2.mileage,sonata3.mileage,tucson1.mileage,tucson2.mileage,bongo1.mileage,bongo2.mileage,
         tesla1.mileage,tesla2.mileage,tesla3.mileage]
    wf=[sonata1.w_fuel,sonata2.w_fuel,sonata3.w_fuel,tucson1.w_fuel,tucson2.w_fuel,bongo1.w_fuel,bongo2.w_fuel,
        tesla1.w_fuel,tesla2.w_fuel,tesla3.w_fuel]
    nwod=[new_old(sonata1),new_old(sonata2),new_old(sonata3),new_old(tucson1),new_old(tucson2),new_old(bongo1),new_old(bongo2),
          new_old(tesla1),new_old(tesla2),new_old(tesla3)]
    ren=['-','-','-','-','-','-','-','-','-','-']
    re=['-','-','-','-','-','-','-','-','-','-']
    us=['-','-','-','-','-','-','-','-','-','-']
    ph=['-','-','-','-','-','-','-','-','-','-']
    dd={'차종':car,'모델명':model,'평균주행거리':ran,'평균주유량':wf,'신차or중고차':nwod,
        '대여일':ren,'반납일':re,'대여자':us,'휴대폰번호':ph}

    df=pd.DataFrame(data=dd)
    pd.set_option('mode.chained_assignment', None)  # <==== 경고를 끈다
  
    def rent(self,x): #렌탈

        if (car_rent.df['대여일'][x-1] == '-' and car_rent.df['반납일'][x-1] == '-') or \
                (car_rent.df['대여일'][x-1]!='-' and car_rent.df['반납일'][x-1]!= '-'):  # 가능
            ix = x - 1  # dataframe index

            now = input("대여일 작성(####-##-## 꼴) : ")
            nd=now.replace('-',' ')
            nd=nd.split()
            nd=datetime.date(int(nd[0]),int(nd[1]),int(nd[2])) #계산
            self.rent_t=nd
            n = input("대여자분 성함 작성 > ")
            c = input("휴대폰번호 작성 > ")
            car_rent.df["대여자"][x - 1] = n
            car_rent.df["휴대폰번호"][x - 1] = c
            car_rent.df["대여일"][x - 1] = now
            car_rent.bcar.append(x)
            if car_rent.df['반납일'][x-1] !='-': #반납됐던차 다시 빌리는경우 저번 반납 시간 리셋
                car_rent.df['반납일'][x - 1]='-'
        else:
            print("이미 대여중 ")

    def getw_mileage(x,y): #한주간 운행거리합
        car_rent.df['평균주행거리'][x]=y

    def getw_fuel(x,y): #한주간 주유량
        car_rent.df['평균주유량'][x]=y


    def car_return(self,x): #반납
        if car_rent.df['대여일'][x-1]!='-':
            if car_rent.df['반납일'][x-1] == '-':
                ix=x-1
                now = input("반납일 작성(####-##-## 꼴) : ")
                nd = now.replace('-', ' ')
                nd = nd.split()
                nd = datetime.date(int(nd[0]), int(nd[1]), int(nd[2]))  # 계산
                self.return_t = nd
                car_rent.df["반납일"][x - 1] = now
                car_rent.bcar.remove(x)

                interval=self.return_t-self.rent_t

                m=car_rent.carcollection[x - 1].mileage/int(interval.days)
                f=car_rent.carcollection[x - 1].w_fuel/int(interval.days)


                car_rent.getw_mileage(x-1,m)
                car_rent.getw_fuel(x - 1, f)

            else:
                print("이미반납했습니다 ")
        else:
            print("안빌렸습니다 ")




    def remain_car(self): #현재 차고에 남은 차량(대여가능여부)

        for i in range(len(car_rent.df)):
            if car_rent.df['반납일'][i]!='-': #가능

                print(i+1,"번째 ",car_rent.df.values[i])
            elif car_rent.df['대여일'][i]=='-': #가능

                print(i+1,"번째 ",car_rent.df.values[i])
            else:
                continue


    def plus_car(self): #차추가
        print("1. 승용차(sonata)")
        print("2. suv(tucson)")
        print("3. 트럭(bongo)")
        print("4. 전기승용차(tesla_s)")

        ct=int(input("차종 입력 > "))

        t = ['승용차', 'suv', '트럭', '전기승용차']
        tt=['Sonata','Tucson','Bongo','Tesla_s']
        if ct-1==0: # sonata
            new= Sonata()
        elif ct-1==1: # tucson
            new=Tucson()
        elif ct-1==2: # bongo
            new=Bongo()
        else: # tesla_s
            new=Tesla_S()

        car_rent.carcollection.append(new)
        car_rent.car.append(t[ct-1])
        car_rent.model.append(tt[ct-1])
        car_rent.ran.append(new.mileage)
        car_rent.wf.append(new.w_fuel)
        car_rent.nwod.append(car_rent.new_old(new))
        car_rent.ren.append('-')
        car_rent.re.append('-')
        car_rent.us.append('-')
        car_rent.ph.append('-')
        ndd = {'차종': t[ct-1], '모델명': tt[ct-1], '평균주행거리': new.mileage, '평균주유량': new.w_fuel, '신차or중고차': car_rent.new_old(new),
              '대여일': '-', '반납일': '-', '대여자': '-', '휴대폰번호': '-'}

        car_rent.df.loc[len(car_rent.df)] = ndd

    def scrap_car(self,z): #폐차

        car_rent.df.drop(index=z-1,inplace=True)
        car_rent.df=car_rent.df.reset_index(drop=True)
        car_rent.carcollection.pop(z-1)
        car_rent.car.pop(z-1)
        car_rent.model.pop(z-1)
        car_rent.ran.pop(z-1)
        car_rent.wf.pop(z-1)
        car_rent.nwod.pop(z-1)
        car_rent.ren.pop(z-1)
        car_rent.re.pop(z-1)
        car_rent.us.pop(z-1)
        car_rent.ph.pop(z-1)

    def car_match(self): #차 매칭
        print("원하시는 차종이 무엇인가요?  ")
        print("1. 승용차")
        print("2. suv")
        print("3. 트럭")
        print("4. 전기승용차")

        x=int(input("> "))
        t=['승용차','suv','트럭','전기승용차']
        x=t[x-1]
        for i in range(len(car_rent.df)):
            if x == car_rent.df['차종'][i]:
                print(i+1,"번째 ",car_rent.df.values[i])

    def car_monitor(self):
        print("       차종 모델 평균주행거리 평균주유량 신차or중고차 대여일 반납일 대여자 휴대폰번호 ")

        for i in range(len(car_rent.df)):
            print(i+1,"번째 ",car_rent.df.values[i])






