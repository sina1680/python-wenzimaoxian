#这是一个文字冒险游戏
#作者：孙健
#联系方式:QQ 28472517
#开始创建于2018.09.26

import random
import math
def change_player(mapSize):
    player['locationX']=math.floor((mapSize-1)/2)
    player['locationY']=math.floor((mapSize-1)/2)
    player['locationID']=math.floor(math.pow(mapSize,2)/2)+1
#玩家数据中心
player={
    'name':'小明',
    'hp':10,
    'maxhp':10,
    'gold':0,
    'items':[],
    'level':1,
    'xp':0,
    'xpForNextLevel':100,
    'locationX':0,
    'locationY':0,
    'locationID':0,
    'exploredAreas':1
 }

#初始化游戏地图和游戏区域
gameMap ={}
mapSize = 5
map_Num = math.floor(math.pow(mapSize,2))
areaTpye = ["沙漠","平原","山丘","山脉","森林","沼泽","荒地","地牢"]
change_player(mapSize)
#在游戏地图中生成一个区域
def makeArea(id,x,y):
    area={
        'mapID':id,
        'x':x,
        'y':y,
        'type': random.choice(areaTpye),
        'explored':False
        }
    return area

#生成游戏地图
def makeMap(rows,columns):
    thisRow=0
    thisCol=0
    thisArea = 1
    for r in range(0,rows):
        for c in range(0,columns):
            gameMap[thisArea]=makeArea(thisArea,thisRow,thisCol)
            if gameMap[thisArea]["mapID"]==player['locationID']:
                gameMap[thisArea]['type']='老家'
                gameMap[thisArea]['explored']=True
            thisArea += 1
            thisCol += 1
        thisRow += 1
        thisCol = 0
#生成玩家
def makePlayer():
    player["name"] = input("请输入游戏主角名字: ")
    print ("\n你的游戏主角名字叫 {0}. 你的生命值是满的 ({1} 点), 你有 {2} 个金币. 你身上没有任何东西.".format(player["name"], player["hp"],player["gold"]))
    print ("\t%s 是一个一级角色, 需要获得 %s 点经验才能升级. 这样做我们会获得更多最大生命值. 你可以在探索和战斗中获得经验." % (player["name"],player["xpForNextLevel"]))
    print ("\t你的冒险开始于你的家乡，去探索更多土地吧...")
def hitEnter():
	input("\n回车键继续.")
# 获取地区描述
def description():
    isExplored = "已探索"
    if gameMap[player["locationID"]]["explored"] == False:
        isExplored = "未探索"
    print ("\n当前位置: " + gameMap[player["locationID"]]["type"])
    print ("(X: " + str(player["locationX"]) + ", Y: " + str(player["locationY"]) + ") 该区域状态： " + isExplored + "." + str(player["locationID"])+"号地区")

# 绕地图移动.
def movePlayer(direction):
    if direction == 'n':
        if player['locationY']+1 <= mapSize-1:
            player['locationY'] += 1
            player['locationID'] += mapSize
        else:
            player['locationY'] = 0
            player['locationID'] = (player['locationID']+mapSize)-map_Num
    elif direction == 's':
        if player['locationY'] -1 >= 0:
            player['locationY'] -=1
            player['locationID'] -= mapSize
        else:
            player["locationY"] = mapSize-1
            player["locationID"] = (player['locationID']-mapSize)+map_Num
    elif direction == "e":
        if player["locationX"] + 1 <= mapSize-1:
            player["locationX"] += 1
            player["locationID"] += 1
        else:
            player["locationX"] = 0
            player["locationID"] -= mapSize-1
            
    else:
        if player["locationX"] - 1 >= 0:
            player["locationX"] -= 1
            player["locationID"] -= 1
        else:
            player["locationX"] = mapSize-1
            player["locationID"] += mapSize-1
    description()
#添加经验
def addXp(num):
    player['xp'] += num
    print('\n%s 获得了 %s 点经验值。'% (player['name'],num))
    if player['xp'] >= player['xpForNextLevel']:
        player['level'] += 1
        player['maxhp'] += 5
        player['hp'] = player['maxhp']
        print('恭喜你，升级了 -- %s 现在是 %s 级了！'% (player['name'],player['level']))
#添加金币
def addGold(num):
    player['gold'] += num
    print('\n%s 拾取了 %s 个金币。'% (player['name'],num))
def healhp():
    print('你增加了 %s 点生命值。'%(player['maxhp']-player['hp']))
    player['hp'] = player['maxhp']
def dofight():
    monsterType = ["哥布林","兽人","强盗","僵尸","骷髅","史莱姆","小鬼","巨型蝙蝠","大甲虫","狼","熊"]
    myRace = random.choice(monsterType)
    theMonster = {
        'race':myRace,
        'hit_points':random.randrange(1,4),
        'treasure':random.randrange(0,5)
        }
    print('\n%s 出现在你的面前。\n'%theMonster['race'])
    return theMonster

def getAction():
    print('\n可用命令')
    actionString = ""
    if gameMap[player["locationID"]]["explored"] == False:
        actionString += "\nx = 探索该地区。"
    if player["locationID"] == 13 and player["hp"] < player["maxhp"]:
        actionString += "\nr = 恢复休息。"
    print(actionString)
    print('n = 去北面 / s = 去南面 / w = 去西边 / e = 去东边.')
    print('i = 查看物品和金币')
    print('c = 查看角色状态')
    choice = input('请输入命令并回车').lower()
    print ("--------------------------------这是美丽的分割线--------------------------------")
    if choice == "i":
        print ("你目前携带: " + "%s" % ", ".join(map(str, player["items"])))
        print ("金币: " + str(player["gold"])+" 个")
    #移动
    elif choice == "n" or choice == "e" or choice == "w" or choice == "s":
        movePlayer(choice)
    #探索地区
    elif choice == "x":
        if gameMap[player["locationID"]]["explored"] == False:
            player["exploredAreas"] += 1
            sumNum = random.randrange(1,4)
            if sumNum == 1:
                print('\n你找到了金币')
                gold=random.randrange(5,10)
                addGold(gold)
                addXp(int(math.floor(gold/12)))
            elif sumNum ==2:
                print ("天哪，你遇到了怪物!")
                theMonster=dofight()
                damage = theMonster['hit_points']
                print ("你受到了 " + str(damage) + " 点伤害.")
                player["hp"] -= damage
                if player["hp"] > 0:
                    addXp(damage*5)
                    if theMonster['treasure'] >0:
                        addGold(theMonster['treasure'])
            else:
                print('你看看了四周，没有发现什么有趣的东西。')
                addXp(1)
            gameMap[player["locationID"]]["explored"] = True
        else:
            print('这里已经探索了，没什么好探索的。')
    elif choice == "r" and player["locationID"] == 13 and player["hp"] < player["maxhp"]:
        healhp()
    elif choice == 'c':
        print(player['name'] + ' /等级: '+ str(player['level'])+ "级  经验值: " + str(player["xp"]) + "点 (还需要" + str(player["xpForNextLevel"]) + "点升级)")
        print ("生命值: " + str(player["hp"]) + " 点 (最大生命值: " + str(player["maxhp"]) + " 点)")
    elif choice == 'm':
        
        for i in range(0,mapSize):
            for j in range(map_Num-(i+1)*mapSize,map_Num-i*mapSize):
                print(gameMap[j+1]['type']+'('+str(gameMap[j+1]['mapID']).zfill(2)+'号)  ',end='')
            print('\n')
    else:
        print('抱歉，我不知道你在说什么。')
    print ("--------------------------------这是美丽的分割线--------------------------------")
makeMap(mapSize,mapSize)
makePlayer()
still_alive = True
description()
hitEnter()
#游戏循环
while still_alive:
    getAction()
    if player["exploredAreas"] == map_Num:
        print ("你已经探索了该地图所有区域!\n现在进入一个全新的地图...")
        hitEnter()
        mapSize = mapSize+2
        map_Num = math.floor(math.pow(mapSize,2))
        change_player(mapSize)
        gamemap = {}
        makeMap(mapSize,mapSize)
        player["exploredAreas"] = 1
        
        description()
        if player["hp"] <= 0: # 玩家死亡
            print ("\n你挂了.")
            still_alive = False
