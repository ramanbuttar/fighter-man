import random

def fight(fighter1, fighter2):
   
    hp1 = fighter1.getHP()
    hp2 = fighter2.getHP()
    roundwinners=[]
    
    for i in range(0,12):
        roundwinners.append('-')
    
    #while fighter1.hp > 0 and fighter2.hp > 0:
    
    for round in range(0, 12):
        rhp1 = hp1
        rhp2 = hp2

        if fighter1.getSpeed() > fighter2.getSpeed():

            hp2 -= attack(fighter1, fighter2)

            if hp2 < 1:
                roundwinners[round] = 2
                return (1, roundwinners)

            hp1 -= attack(fighter2, fighter1)

            if hp1 < 1:
                roundwinners[round] = -2
                return (-1, roundwinners)

        else:

            hp1 -= attack(fighter2, fighter1)

            if hp1 < 1:
                roundwinners[round] = -2
                return (-1, roundwinners)

            hp2 -= attack(fighter1, fighter2)


            if hp2 < 1:
                roundwinners[round] = 2
                return (1, roundwinners)
                    
        if (rhp1 - hp1) > (rhp2 - hp2):
            roundwinners[round] = 1
            
        elif (rhp2 - hp2) > (rhp1 - hp1):
            roundwinners[round] = -1
            
        else:
            roundwinners[round] = 0

    return checkScores(roundwinners)

#check scorecard
def checkScores(scores):
    wins = scores.count(1)
    losses = scores.count(-1)
    
    if wins > losses:
        return 1
        
    elif wins < losses:
        return -1
        
    else:
        return 0
                
             
#calculate the amount of damage done by an attack
def attack(attacker, defender):

    a_str = attacker.getStrength()
    a_spd = attacker.getSpeed()
    d_def = defender.getDefence()
    d_spd = defender.getSpeed()
    

    #chance to score critical hit
    crit = (a_str + a_spd)/100

    #chance to defend attack
    dodge = (d_spd+d_def-a_spd)/100
    block = (d_spd+d_def)/100

    #dice
    a_rnd = random.randint(0, 100)
    d_rnd = random.randint(0, 100)

    #check for crit
    if a_rnd < crit:
        attackPower = a_str/2

    else:
        attackPower = (a_str-(a_rnd%10))/4

    #return damage done
    if d_rnd < dodge:
        return 0
    if d_rnd < block:
        return attackPower/2
    else:
        return attackPower

def calcEXP(fighter1, fighter2):
    if fighter1.level > fighter2.level:
        expdif = (fighter1.level-fighter2.level)*2000
        expdif += (fighter1.exp-fighter2.exp)
        expbonus = int(expdif/100)*(-1)
        
    elif fighter1.level < fighter2.level:
        expdif = (fighter2.level-fighter1.level)*2000
        expdif += (fighter2.exp-fighter1.exp)
        expbonus = int(expdif/100)

    else:
        expbonus = 0
        
    exp = 100 + expbonus

    return exp

