import json
from typing import Type
import os

ddragon_path = 'ddragon/12.10.1/data/ko_KR/'

champions = os.popen('ls '+ddragon_path+'champion/').read().split('\n')[:-1]
champions = dict(zip([champ.split('.')[0] for champ in champions], champions))


class Champion:
    def __init__(self, name: str):
        self.json = json.load(open(ddragon_path+'champion/'+champions[name]))
        self.armor = self.json['data'][name]['stats']['armor']
        self.spellblock = self.json['data'][name]['stats']['spellblock']
        self.armorGrowth = self.json['data'][name]['stats']['armorperlevel']
        self.spellblockGrowth = self.json['data'][name]['stats']['spellblockperlevel']
    def getDefence(self, level: int):
        return ((self.armor + level*self.armorGrowth), (self.spellblock + level*self.spellblockGrowth))
    def getOldDefence(self, level: int):
        return ((self.armor + level*(self.armorGrowth-1.2)), (self.spellblock + level*(self.spellblockGrowth-0.8)))

def defenceCalc(champ: Type[Champion], lev: int):
    return list(map(lambda n: (list(map(lambda i: i/float(i+100)*100, n))), zip(champ.getDefence(lev), champ.getOldDefence(lev))))

p_diff = {}

for name in champions:
    champ = Champion(name)
    after_patch, before_patch = defenceCalc(champ, 18)
    p_diff[name] = [round(after_patch[i]/before_patch[i], 2) for i in range(2)]

if __name__ == '__main__':
    while True:
        cname = input('ChampionName = ')
        try:
            print(f'Level 18 dmg_reduce_percent ratio : {p_diff[cname]}')
        except:
            print('Wrong Champion Name')

