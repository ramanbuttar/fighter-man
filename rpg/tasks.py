import turbogears
from rpg import model
from rpg.model import User, Fighter, Trainer, Feed, Auction

from datetime import *

turbogears.update_config(configfile="dev.cfg",
    modulename="rpg.config")

from turbogears.database import PackageHub

from sqlobject import connectionForURI

hub = PackageHub("rpg")
con = connectionForURI(hub.uri)
#MyClass._connection = con

####scheduler tasks####
#auction expiry
def checkExpiry():
    auctions = Auction.select()
    
    #check if any auctions have expired
    for auction in auctions:
        if date.today() >= auction.expiry:
            expiryAction(auction)
            
            
    model.hub.commit()
    return

#act on expired auction
def expiryAction(auction):
    owner = User.by_user_name(auction.owner)
    #if no buyer was found
    if auction.buyer == '':
        owner.addEquipment(auction.item)
        
        #create feed entry
        sellfeed = Feed(owner = auction.owner,
            msg = "No buyer could be found for %s." % auction.item.name,
            category = 'auction', time = datetime.now())

    #if buyer is found
    else:
        buyer = User.by_user_name(auction.buyer)
        buyer.addEquipment(auction.item)
        owner.money += auction.bid
        
        #create feed entries
        buyfeed = Feed(owner = auction.buyer, 
            msg = "You won the bid for %s!" % auction.item.name,
            category = 'auction', time = datetime.now())
            
        sellfeed = Feed(owner = auction.owner,
            msg = "Your auction for %s sold!" % auction.item.name,
            category='auction', time = datetime.now())

    #remove auction
    auction.destroySelf()
    model.hub.commit()
    return
    
#per diem
def perDiem():
    users = User.select()
    for user in users:
        payment =  (user.fighter.level*100)
        user.money += payment
        Feed(owner=user.user_name, msg = "Earned $%d from sponsors." %payment,
            category='Other', time = datetime.now())
        
    model.hub.commit()
    return
        
#pay trainer
def payTrainer():
    #for each user
    for user in User.select():
        #print 'im at least here'
        if user.fighter.trainer == None:
            return
            
        else:
            #if user has more money than trainer salary
            if user.money > user.fighter.trainer.salary:
                #deduct the trainer salary from user money
                user.money -= user.fighter.trainer.salary
                notfire = Feed(owner=user.user_name, msg = 'Payed trainer $%d.' %user.fighter.trainer.salary,
                    category = 'Other', time = datetime.now())
            
            #otherwise
            else:
                #change trainer back to default trainer
                user.fighter.trainer = None
                user.fighter.trainer_points = 0
                user.fighter.trainer_strength = 0
                user.fighter.trainer_speed = 0
                user.fighter.trainer_defence = 0
                user.fighter.trainer_conditioning = 0
                
                #generate feed message                         
                fire = Feed(owner=user.user_name, msg = 'You don\'t have enough money to pay your trainer\'s salary, your trainer quit!', category = 'Other', time = datetime.now())
                
    model.hub.commit()        
    return

def schedule():
        
    #turbogears.scheduler.add_interval_task(action=perDiem, taskname='do_something', initialdelay=5, interval=10)           
        
    turbogears.scheduler.add_weekday_task(action=perDiem,
        taskname='perDiem', weekdays=range(1,8), timeonday=(1,0))

    turbogears.scheduler.add_weekday_task(action=checkExpiry,
        taskname='checkExpiry', weekdays=range(1,8), timeonday=(1, 0))
        
    turbogears.scheduler.add_weekday_task(action=payTrainer,
        taskname='payTrainer', weekdays=range(1,8), timeonday=(1, 0))
