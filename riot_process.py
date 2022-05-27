import json
from typing import Type
import os

ddragon_path = 'ddragon/12.10.1/data/ko_KR/'

champions = os.popen('ls '+ddragon_path+'champion/').read().split('\n')[:-1]
champions.remove('Thresh.json')
champions = dict(zip([champ.split('.')[0] for champ in champions], champions))


class Champion:
    def __init__(self, name: str):
        self.json = json.load(open(ddragon_path+'champion/'+champions[name]))
        self.hp = self.json['data'][name]['stats']['hp']
        self.hpGrowth = self.json['data'][name]['stats']['hpperlevel']
        self.armor = self.json['data'][name]['stats']['armor']
        self.spellblock = self.json['data'][name]['stats']['spellblock']
        self.armorGrowth = self.json['data'][name]['stats']['armorperlevel']
        self.spellblockGrowth = self.json['data'][name]['stats']['spellblockperlevel']
    def getDefence(self, level: int):
        return [(self.armor + level*self.armorGrowth), (self.spellblock + level*self.spellblockGrowth)]
    def getOldDefence(self, level: int):
        return [(self.armor + level*(self.armorGrowth-1.2)), (self.spellblock + level*(self.spellblockGrowth-0.8))]
    def getNewOldHP(self, level: int):
        return [(self.hp + level*self.hpGrowth), ((self.hp-70) + level*(self.hpGrowth-12))]


def defenceCalc(champ: Type[Champion], lev: int): # [ [AD_reduce(%), AP_reduce(%)], [old_AD_reduce(%), old_AP_reduce(%)] ]
    return list(map(lambda n: (list(map(lambda i: i/float(i+100)*100, n))), zip(champ.getDefence(lev), champ.getOldDefence(lev))))

def effectiveHealth(champ: Type[Champion], lev: int):
    defence = defenceCalc(champ, lev)
    HP = champ.getNewOldHP(lev)
    return [[HP[j]/(1-defence[j][i]/100) for i in range(2)] for j in range(2)]

def p_diff(after_patch: list, before_patch: list):
    return [round(after_patch[i]/before_patch[i], 2) for i in range(len(after_patch))]

def diff(cname: str, lev: int):
    champ = Champion(cname)

    oldDefence = champ.getOldDefence(lev)
    defence = champ.getDefence(lev)

    print(f"--------------------< {(champ.json['data'][cname]['name']+', '+champ.json['data'][cname]['title']).center(14, ' ')} >--------------------")
    print('========================================================================')

    print(f'Armor: [{oldDefence[0]:.1f}] -> [{defence[0]:.1f}]')
    print(f'SpellBlock: [{oldDefence[1]:.1f}] -> [{defence[1]:.1f}]')
    
    after_patch, before_patch = defenceCalc(champ, lev)

    print(f'AD_reduce(%): [{before_patch[0]:.2f}%] -> [{after_patch[0]:.2f}%] ({p_diff(after_patch, before_patch)[0]:.2f} times)')
    print(f'AP_reduce(%): [{before_patch[1]:.2f}%] -> [{after_patch[1]:.2f}%] ({p_diff(after_patch, before_patch)[1]:.2f} times)')

    print('========================================================================')
    
    hp = champ.getNewOldHP(lev)
    effHP = effectiveHealth(champ, lev)
    print(f'HP: [{hp[1]}] -> [{hp[0]}] ({p_diff([hp[0]], [hp[1]])[0]} times)')
    print(f'EffectiveHP(only AD): [{effHP[1][0]:.1f}] -> [{effHP[0][0]:.1f}] ({p_diff(effHP[0], effHP[1])[0]:.2f} times)')
    print(f'EffectiveHP(only AP): [{effHP[1][1]:.1f}] -> [{effHP[0][1]:.1f}] ({p_diff(effHP[0], effHP[1])[1]:.2f} times)')
    print(f'EffectiveHP(Average): [{sum(effHP[1])/2:.1f}] -> [{sum(effHP[0])/2:.1f}] ({sum(p_diff(effHP[0], effHP[1]))/2:.2f} times)')

    print('========================================================================')


if __name__ == '__main__':
    while True:
        cname = input('ChampionName = ')
        if cname in champions:
            lev = int(input(f'{cname} at level = '))
            if(lev in range(1, 19)):
                diff(cname, lev)
            else:
                print('Wrong Level (must be 1~18 int)')
        else:
            print('Wrong Name')
