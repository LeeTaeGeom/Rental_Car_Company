class Car:
    def __init__(self, max_fuel, fuel_economy, max_passengers=0, max_load=0):
        self.max_fuel = max_fuel
        self.max_passengers=max_passengers
        self.max_load=max_load
        self.passengers=0
        self.load=0
        self.new_or_old = 0 #중고인지아닌지
        self.movex=[]   # 이동거리 리스트 move할때마다
        self.movefuel_1km=[] #move할때마다 1km당 드는 fuel
        self.mileage = 0
        self.fuel = self.max_fuel
        if self.max_load==0:
            self.fuel_economy = fuel_economy - (self.passengers / self.max_passengers) * fuel_economy * 0.1
        elif self.max_passengers==0:
            self.fuel_economy = fuel_economy - (self.load / self.max_load) * fuel_economy * 0.1
        else:
            self.fuel_economy = fuel_economy - (self.passengers / self.max_passengers) * fuel_economy * 0.1 - (self.load / self.max_load) * fuel_economy * 0.1
        self.fuel_economy_100=self.fuel_economy
        self.range = self.fuel_economy * self.fuel
        self.w_fuel=0
    def fill_up(self): #연료/배터리 가득 채우기
        self.w_fuel += self.max_fuel - self.fuel
        self.fuel=self.max_fuel


    def fill(self,x): #연료/배텨리 x만큼 채우기, 최대 용량을 초과할 수 없음
        if(self.fuel+x>self.max_fuel):
            print("넘쳐요 넘쳐. full로만 채울게요 ")
            self.w_fuel += self.max_fuel - self.fuel
            self.fuel=self.max_fuel
        else:
            self.fuel+=x
            self.w_fuel+=x

    def ride(self,x): #자동차에 승객(화물)이 x만큼 탑승 max_passengers max_load 넘으면안됨-> 넘으면 안태우고 그냥가는걸로
        if(self.passengers+x>self.max_passengers):
           print("탑승가능한 인원보다 많습니다. 안태우겠습니다 ")
        elif(self.passengers+x<0):
            print("그만큼 내릴 사람이 없습니다. 그냥 남은사람도 안내릴게요 ")
        else:
            self.passengers+=x
            self.check_fuel_economy()

    def check_fuel_economy(self):
        if self.max_load == 0:
            self.fuel_economy = self.fuel_economy - (self.passengers / self.max_passengers) * self.fuel_economy * 0.1
        elif self.max_passengers == 0:
            self.fuel_economy = self.fuel_economy - (self.load / self.max_load) * self.fuel_economy * 0.1
        else:
            self.fuel_economy=self.fuel_economy-(self.passengers/self.max_passengers)*self.fuel_economy*0.1-(self.load/self.max_load)*self.fuel_economy*0.1


    def get_range(self): #현재 연료량(배터리)로 주행가능거리
        self.range=self.fuel_economy*self.fuel
        range=self.range
        return range

    def get_fuel_economy_100(self):
        xsum=0
        usefuel=0
        for i in reversed(range(len(self.movex))):
            xsum += self.movex[i]
            if xsum >= 100:
                break
        if(xsum-100>0):
            for j in reversed(range(len(self.movefuel_1km))):
                if(j>i):
                    usefuel+=self.movex[j]*self.movefuel_1km[j]
                elif(j==i):
                    usefuel+=(self.movex[j]-(xsum-100))*self.movefuel_1km[j]
                else:
                    break
        else: #xsum-100==0 , xsum-100<0
            for j in reversed(range(len(self.movefuel_1km))):
                if(j>=i):
                    usefuel+=self.movex[j]*self.movefuel_1km[j]
                else:
                    break
        if(xsum<100):
            ans=xsum/usefuel # fuel_economy=distance/fuel 식이기때문
        else:
            ans=100/usefuel # 100km 넘을때부터 계기판확인시점에서부터 100km이전사이의 fuel_economy
        return ans

    def move(self,x): #현상태에서 x거리만큼 주행, fuel이 부족해 x만큼 못가면 주의를 주고 주행시작 그리고 fuel이 다떨어지면 멈춤, 주행이끝나고 fuel, mileage, range, fuel_economy_100이 업데이트 됨
        self.new_or_old+=1
        if self.get_range()<x:
            print("연료가 부족해서 ",x,"만큼은 못갑니다. 대신 ",self.range,"만큼 갑니다 ")
            self.mileage+=self.range
            self.movex.append(x)    #거리 기록
            self.movefuel_1km.append(1/self.fuel_economy) # x거리갈때까지 1km마다 사용되는 기름 양
            self.fuel_economy_100=self.get_fuel_economy_100() # fuel_economy_100
            self.fuel=0
            self.range=self.get_range()
        else:
            self.mileage+=x
            self.movex.append(x) #거리 기록
            self.movefuel_1km.append(1 / self.fuel_economy)  # x거리갈때까지 1km마다 사용되는 기름 양
            self.fuel_economy_100=self.get_fuel_economy_100() # fuel_economy_100
            self.range-=x
            self.fuel=self.range/self.fuel_economy

    def get_mileage(self): #주행거리 반환
        mileage=self.mileage
        return mileage


    def show_dash(self):

        print("총 운행거리 : ",self.get_mileage())# 총 운행거리
        print("현재 연료량 : ",self.fuel)# 현재 연료량/배터리량
        print("현재 연료량으로 주행가능거리 : ",self.get_range())# 현재 연료량/배터리량으로 주행가능거리
        print("최근 100km 주행 간 연비 : ",self.fuel_economy_100)# 최근 100km 주행 간 연비(총 주행이 100km가 안되면 현시점까지의 연비)
        print("탑승인원(운전자 제외) or 싣고 있는 짐 무게 : ",self.passengers,"명 ",self.load,"kg")# 탑승(인원) 또는 무게 : 몇명, 몇kg
        print()

class Sonata(Car): #승용차 리터, km/l, 명
    def __init__(self):
        super().__init__(max_fuel=55,fuel_economy=12,max_passengers=4)

    def show_dash(self):
        print("총 운행거리 : ",self.get_mileage())# 총 운행거리
        print("현재 연료량 : ",self.fuel)# 현재 연료량/배터리량
        print("현재 연료량으로 주행가능거리 : ",self.get_range())# 현재 연료량/배터리량으로 주행가능거리
        print("최근 100km 주행 간 연비 : ",self.fuel_economy_100)# 최근 100km 주행 간 연비(총 주행이 100km가 안되면 현시점까지의 연비)
        print("탑승인원(운전자 제외) : ",self.passengers,"명 ")# 탑승(인원) : 몇명
        print()


class Tucson(Car): #SUV명 리, km/l, 명 + kg
    def __init__(self):
        super().__init__(max_fuel=60, fuel_economy=10, max_passengers=5,max_load=500)
    def ride(self,x,y):
        if (self.passengers + x > self.max_passengers):
            print("탑승가능한 인원보다 많습니다. 안태우겠습니다 ")
        elif (self.passengers + x < 0):
            print("그만큼 내릴 사람이 없습니다. 그냥 남은사람도 안내릴게요 ")
        else:
            self.passengers += x

        if (self.load + y > self.max_load):
            print("실을수있는 화물보다 많습니다. 싣지않겠습니다 ")
        elif (self.load + y < 0):
            print("그만큼 내릴 화물이 없습니다. 그냥 남은화물도 안내릴게요 ")
        else:
            self.load += y
        self.check_fuel_economy()

class Bongo(Car): #트럭 리터, km/l터, kg
    def __init__(self):
        super().__init__(max_fuel=55,fuel_economy=11,max_load=700)
    def ride(self,x):
        if (self.load + x > self.max_load):
            print("실을수있는 화물보다 많습니다. 싣지않겠습니다 ")
        elif (self.load + x < 0):
            print("그만큼 내릴 화물이 없습니다. 그냥 남은화물도 안내릴게요 ")
        else:
            self.load += x
            self.check_fuel_economy()

    def show_dash(self):

        print("총 운행거리 : ",self.get_mileage())# 총 운행거리
        print("현재 연료량 : ",self.fuel)# 현재 연료량/배터리량
        print("현재 연료량으로 주행가능거리 : ",self.get_range())# 현재 연료량/배터리량으로 주행가능거리
        print("최근 100km 주행 간 연비 : ",self.fuel_economy_100)# 최근 100km 주행 간 연비(총 주행이 100km가 안되면 현시점까지의 연비)
        print("싣고 있는 짐 무게 : ",self.load,"kg")#  무게 : 몇kg
        print()


class Tesla_S(Car): #전기 자동차 kwh, km/kwh, 명
    max_charge = 450 #전기라 따로 선언함
    charge_economy = 1 #전기라 따로 선언함
    def __init__(self):
        super().__init__(Tesla_S.max_charge, Tesla_S.charge_economy, max_passengers=5)

    def show_dash(self):
        print("총 운행거리 : ",self.get_mileage())# 총 운행거리
        print("현재 배터리 량 : ",self.fuel)# 현재 연료량/배터리량
        print("현재 배터리 량으로 주행가능거리 : ",self.get_range())# 현재 연료량/배터리량으로 주행가능거리
        print("최근 100km 주행 간 연비 : ",self.fuel_economy_100)# 최근 100km 주행 간 연비(총 주행이 100km가 안되면 현시점까지의 연비)
        print("탑승인원(운전자 제외) : ",self.passengers,"명 ")# 탑승(인원) 몇명
        print()
    def move(self,x): #현상태에서 x거리만큼 주행, fuel이 부족해 x만큼 못가면 주의를 주고 주행시작 그리고 fuel이 다떨어지면 멈춤, 주행이끝나고 fuel, mileage, range, fuel_economy_100이 업데이트 됨
        self.new_or_old+=1
        if self.get_range()<x:
            print("배터리가 부족해서 ",x,"만큼은 못갑니다. 대신 ",self.range,"만큼 갑니다 ")
            self.mileage+=self.range
            self.movex.append(x)    #거리 기록
            self.movefuel_1km.append(1/self.fuel_economy) # x거리갈때까지 1km마다 사용되는 기름 양
            self.fuel_economy_100=self.get_fuel_economy_100() # fuel_economy_100
            self.fuel=0
            self.range=self.get_range()
        else:
            self.mileage+=x
            self.movex.append(x) #거리 기록
            self.movefuel_1km.append(1 / self.fuel_economy)  # x거리갈때까지 1km마다 사용되는 기름 양
            self.fuel_economy_100=self.get_fuel_economy_100() # fuel_economy_100
            self.range-=x
            self.fuel=self.range/self.fuel_economy

#테슬라 맨처음에 생성자서 넘겨줄때 변수를 charge로 정해두고 fuel랑 의미하는게같아서 car클래스에서는 fuel 변수로 사용될예정



