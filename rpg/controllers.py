import turbogears as tg
from turbogears import controllers, expose, flash, identity, redirect, paginate
from turbogears import widgets, validate, error_handler
from cherrypy import request, response

from datetime import *

from kid import Element

from rpg.widgets import *
from rpg.model import *
from sqlobject.sqlbuilder import AND, OR

from rpg.fight import fight, calcEXP
import image_gen as ImageGen

add_user_form = widgets.TableForm(fields=AddUserFields(), validator=AddUserSchema(), action="./addUser", submit_text="Register User")

class Root(controllers.RootController):

############### LOGIN and LOGOUT ###############
    @expose(template="rpg.templates.login")
    def index(self, forward_url=None, previous_url=None, *args, **kw):

        if not identity.current.anonymous and identity.was_login_attempted() \
                and not identity.get_identity_errors():
            #raise redirect(tg.url(forward_url or previous_url or './', kw))
            raise redirect('./home')

        forward_url = None
        previous_url = request.path

        if identity.was_login_attempted():
            msg = _("The credentials you supplied were not correct or "
                "did not grant access to this resource.")
        elif identity.get_identity_errors():
            msg = _("You must provide your credentials before accessing "
                "this resource.")
        else:
            msg = _("Please log in.")
            forward_url = request.headers.get("Referer", "./")

        response.status = 403
        return dict(message=msg, previous_url=previous_url, logging_in=True,
            original_parameters=request.params, forward_url=forward_url)

    @expose()
    def logout(self, **data):
        identity.current.logout()
        raise redirect("./")

#############################################################################

    def strongly_expire(func):
        """Decorator that sends headers that instruct browsers and proxies not to cache."""
        def newfunc(*args, **kwargs):
            response.headers['Expires'] = 'Sun, 19 Nov 1978 05:00:00 GMT'
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
            response.headers['Pragma'] = 'no-cache'
            return func(*args, **kwargs)
        return newfunc

    @expose(template="rpg.templates.home")
    @identity.require(identity.not_anonymous())
    def home(self, **data):
        news = Feed.selectBy(owner = me()).orderBy('time').reversed().limit(10)      
        
        return dict(fighter=my_fighter(), news=news, tabber=widgets.Tabber(), today=date.today())

    @expose(template="rpg.templates.chat")
    @identity.require(identity.not_anonymous())
    def chat(self, **data):
        return dict(room=identity.current.user.chat_room)

    @expose(allow_json=True)
    @strongly_expire
    @identity.require(identity.not_anonymous())
    def getChat(self, **data):
        try:
            num = int(data['num'])
            msgs = [chat for chat in Chat.select(AND(Chat.q.id > num, Chat.q.room == data['room'], OR(Chat.q.user == identity.current.user.user_name, Chat.q.target == '', Chat.q.target == identity.current.user.user_name)), orderBy=Chat.q.id)]
            return dict(msgs=msgs, room=data['room'])
        except:
            raise redirect(tg.url('/home'))

    @expose()
    @identity.require(identity.not_anonymous())
    def saveChat(self, **data):
        try:
            split = data['msg'].split(" ", 2)
            if (split[0] == "/join"):
                identity.current.user.chat_room = split[-1]
            elif (split[0] == "/msg"):
                if (len(split) >= 3):
                    Chat(user=me(), room=data['room'], target=split[1], message=split[2], time = datetime.now())
            else:
                Chat(user=me(), message=data['msg'], room=data['room'], time = datetime.now())
            return dict()
        except:
            raise redirect(tg.url('/home'))

    @expose(allow_json=True)    
    @strongly_expire
    @identity.require(identity.not_anonymous())
    def getActiveUsers(self, **data):
        try:
            active = User.select(AND(Visit.q.visit_key == VisitIdentity.q.visit_key, VisitIdentity.q.user_id == User.q.id, User.q.chat_room == str(data['room'])), distinct=True)
            users = [u.user_name for u in active]
            return dict(users=users)
        except:
            raise redirect(tg.url('/home'))

    @expose(template="rpg.templates.register")
    def register(self, **data):
        if data.get('tg_errors', False):
            flash('There was a problem with the entered data!')
        return dict(form=add_user_form, heading="New User Registration", form_values=None)

    @expose()
    @validate(form=add_user_form)
    @error_handler(register)
    def addUser(self, **data):
        fighter = addFighter(data['display_name']) #create fighter to associate with user
        u = User(user_name=data['user_name'], email_address=data['email'],
            display_name=data['display_name'], password=data['password1'], fighter=fighter)
        
        #populate inventory
        u.addEquipment(Equipment.get(1))
        u.addEquipment(Equipment.get(2))
        u.addEquipment(Equipment.get(3))
        u.addEquipment(Equipment.get(4))
        u.addEquipment(Equipment.get(5))
        u.addEquipment(Equipment.get(6))

        if data.get('notify', False):
            flash('User registered! You will be notified.')
        else:
            flash('User registered!')

        # log in the new user
        ident = identity.current_provider.validate_identity(u.user_name, u.password, request.tg_visit.key)
        identity.set_current_identity(ident)

        raise redirect(tg.url('./home'))

####Fight Test Stuff####
    @expose(template="rpg.templates.fightresults")
    @identity.require(identity.not_anonymous())
    def rumble(self, **data):
        try:          
            fighter1 = my_fighter()
            fighter2 = Fighter.get(int(data['opponent_id']))
            
            purse = 0
            
            exp = 0
            
            opp = User.selectBy(display_name = fighter2.name)[0]

            if (fighter1 != fighter2) and (abs(fighter1.level-fighter2.level) < 3) and (cur_user().money >= calcBet(fighter2)):

                #sim the fight
                result, scores = fight(fighter1, fighter2)    

                #update fight record
                if result == 1: #if win
                    exp = calcEXP(fighter1, fighter2)
                    purse = calcPurse(fighter2)
                    
                    cur_user().money += purse
                    
                    fighter1.exp += exp

                    #check for a level up
                    if(checkLevel(fighter1)):
                        flash('You gained a level!')
                        Feed(owner=me(),
                            msg = 'Congratulations, you are now level %d!' % my_fighter().level,
                            category='Fight', time = datetime.now())

                    fighter1.wins += 1
                    fighter2.losses += 1
                    
                    #create result feed for opponent
                    fightFeed(opp.user_name, 'lose', fighter1.name, 0)
                    Feed(owner=me(), msg='Your fighter defeated %s! Gained %d Experience and won $%d' %(fighter2.name, exp, purse),
                        category = 'Fight', time = datetime.now())

                elif result == -1: #if loss
                    fighter1.losses += 1
                    fighter2.wins += 1
                    bet = calcBet(fighter2)
                    
                    cur_user().money -= bet
                    opp.money += bet
                    
                    #create result feed for opponent
                    fightFeed(opp.user_name, 'win', fighter1.name, bet)
                    Feed(owner=me(), msg='Your fighter lost to %s.' %fighter2.name,
                        category = 'Fight', time = datetime.now())
                    
                else: #draw
                    fighter1.draws += 1
                    fighter2.draws += 1
                    
                    #create result feed for opponent
                    fightFeed(opp.user_name, 'draw', fighter1.name, 0)
                    Feed(owner=me(), msg='Your fighter drew with %s.' %fighter2.name,
                        category = 'Fight', time = datetime.now())
                    
                    
                return dict(player = fighter1.name, opponent = fighter2.name, result = result, scorecard = scores, winnings=purse, expgain = exp)
            else:
                if fighter1 == fighter2:
                    flash('You can\'t fight yourself.....')
                
                elif cur_user().money < calcBet(fighter2):
                    flash("You do not have enough money to fight")
                    
                else:
                    flash("You do not meet the level requirements to fight this opponent")
                    
                
                raise redirect('./arena')
        except KeyError:
            raise redirect('./home')
        

    #find opponent
    @expose(template="rpg.templates.arena")
    @identity.require(identity.not_anonymous())
    @paginate('fighters', limit=10)
    def arena(self, **data):
        try:
            fighters = Fighter.select(Fighter.q.id != my_fighter().id)
            fightergrid = widgets.PaginateDataGrid(fields=[
                ('Name', linkFighter),
                ('Level', 'level'),
                ('Fighting Fee', calcBet),
                ('Prize Money', calcPurse)])
            
            if data.get('opp', False):
                opp = Fighter.by_fighter_name(data['opp'])
            else:
                opp = None
                
            return dict(fighters=fighters, grid=fightergrid, me=my_fighter(), opponent=opp)
        except SQLObjectNotFound:
            flash("Unknown fighter")
            raise redirect(tg.url('/arena'))
        except:
            raise redirect(tg.url('/home'))

####Gym Test Stuff####
    @expose(template="rpg.templates.gym")
    @strongly_expire
    @identity.require(identity.not_anonymous())
    def gym(self, **data):
        fighter = my_fighter()

        bodies = Feature.selectBy(type = 'Body')
        hair = Feature.selectBy(type = 'Hair')
        eyes = Feature.selectBy(type = 'Eyes')
        mouths = Feature.selectBy(type = 'Mouth')
        faces = Feature.selectBy(type = 'Face')     
		
        equipment = []        
        for g in cur_user().gear:
            if g.type == "Gym":
                equipment.append(g)
				
        gear = []        
        for g in cur_user().gear:
            if g.type != 'Gym':
                gear.append(g)
        
        return dict(fighter=fighter, equipment=equipment, inventory=gear, bodies=bodies, eyes=eyes, hair=hair, mouths=mouths, faces=faces, tabber=widgets.Tabber())
    
    @expose(allow_json=True)
    @strongly_expire
    @identity.require(identity.not_anonymous())
    def getEquipmentStats(self, equipment=None, **data):           
        result = dict()
        for g in cur_user().gear:
            if equipment == g.name:
                strength=g.strength
                speed=g.speed
                defence=g.defence
                conditioning=g.conditioning
                result = dict(strength=strength, speed=speed, defence=defence, conditioning=conditioning)
        return result

    #train using equipment
    @expose()
    @identity.require(identity.not_anonymous())
    def setTrainingEquipment(self, equipment1=None, equipment2=None, equipment3=None, **data):
        # get fighter
        fighter = my_fighter()

        # check if fighter's gear has already been set for the day
        if fighter.equipment_set:
            flash('Equipment already set for the day, nice try :P')
        # check if equipment is all different, no duplicates allowed
        elif equipment1==equipment2 or equipment1==equipment3 or equipment2==equipment3:
            flash('You must train using distinct equipment')
        # check if equipment is still in inventory, if so then set
        else:
            e1 = None
            e2 = None
            e3 = None

            for g in cur_user().gear:
                if g.name == equipment1:
                    e1 = g
                elif g.name == equipment2:
                    e2 = g
                elif g.name == equipment3:
                    e3 = g

            if e1 and e2 and e3:
                if e1.level > fighter.level or e3.level > fighter.level or e3.level > fighter.level:
                    flash('You are trying to equip an item that\'s level is too high.')
                else:
                    fighter.equipment1 = e1
                    fighter.equipment2 = e2
                    fighter.equipment3 = e3
                    # set flag saying equipment is set for the day
                    fighter.equipment_set = True
                    flash('Training equipment set for the day!')
            else:
                flash('One or more of the equipment items are not in your inventory, are you sure you didn\'t sell it just now?')				

        raise redirect(tg.url('./gym'))

    #apply attribute allocation
    @expose()
    @identity.require(identity.not_anonymous())
    def train(self, **data):
        try:
            fighter = my_fighter()
            if not fighter.trainer == None:
                fighter.trainer_points = int(data['points'])
                fighter.trainer_strength = int(data['strength'])
                fighter.trainer_speed = int(data['speed'])
                fighter.trainer_defence = int(data['defence'])
                fighter.trainer_conditioning = int(data['conditioning'])

                flash('Finished training, points allocated!')
                raise redirect(tg.url('./gym'))
            else:
                fighter.trainer_strength = 0
                fighter.trainer_speed = 0
                fighter.trainer_defence = 0
                fighter.trainer_conditioning = 0
                flash('Nice try, you don\'t have a trainer')
                raise redirect(tg.url('./gym'))
        except:
            raise redirect(tg.url('./gym'))
    
####Gear Stuff####
    #go to shop
    @expose(template="rpg.templates.shop")
    @identity.require(identity.not_anonymous())
    def shop(self, **data):
        if data.get('filter', False):
            shopfilter = data['filter']
	    if ((shopfilter != 'All') and (shopfilter != 'Gloves') and (shopfilter != 'Boots') and (shopfilter != 'Trunks')):
		shopfilter = "All"
        else:
            shopfilter = "All"
    
        if shopfilter == "All": 
            goods = Equipment.select(OR(Equipment.q.type == 'Gloves',
                Equipment.q.type == 'Boots', Equipment.q.type == 'Trunks'),
                orderBy=Equipment.q.type)
        else:
            goods = Equipment.select(Equipment.q.type == shopfilter)
            
        gymequip = Equipment.selectBy(type = 'Gym')                
        
        return dict(equipment = goods, trainers = Trainer.select(), fighter = my_fighter(),
            inventory = cur_user().gear, tabber=widgets.Tabber(),
            gym = gymequip)

	#buy gear from shop
    @expose()
    @identity.require(identity.not_anonymous())
    def hiretrainer(self, **data):
        try:
            trainer = Trainer.get(int(data['trainer_id']))

            if (my_fighter().level >= trainer.level):
                if cur_user().money >= trainer.hirefee: #not owned and have enough money
                    if my_fighter().trainer != None:
                        Feed(owner=me(), msg = 'You fired %s and hired %s to train your fighter.' %(my_fighter().trainer.name, trainer.name), category = 'Shop', time = datetime.now())
                        flash('You fired %s and hired %s to train your fighter.' %(my_fighter().trainer.name, trainer.name))
                    else:				
                        Feed(owner=me(), msg = 'You hired %s to train your fighter.' %trainer.name, category = 'Shop', time = datetime.now())
                        flash(trainer.name + ' hired!')
                    
                    my_fighter().trainer = trainer
                    cur_user().money -= trainer.hirefee
                    my_fighter().trainer_points = trainer.points
                    my_fighter().trainer_strength = 0
                    my_fighter().trainer_speed = 0
                    my_fighter().trainer_defence = 0
                    my_fighter().trainer_conditioning = 0
                else: #not enough minerals
                    flash('You don\'t have enough money to hire this trainer.')
            else: #not same level as trainer
                flash('You need to reach level ' + str(trainer.level) + ' to hire this trainer.')
    
            raise redirect('./shop')
        except SQLObjectNotFound:
            flash("Unknown Trainer")
            raise redirect('./shop')
        except:
            raise redirect('./shop')
		
    @expose()
    @identity.require(identity.not_anonymous())
    def firetrainer(self, nextpage='./shop', **data):
        if (my_fighter().trainer != None):
            Feed(owner=me(), msg = 'You fired %s.' %my_fighter().trainer.name,
                category = 'Shop', time = datetime.now())        
            my_fighter().trainer = None
            my_fighter().trainer_points = 0
            my_fighter().trainer_strength = 0
            my_fighter().trainer_speed = 0
            my_fighter().trainer_defence = 0
            my_fighter().trainer_conditioning = 0
            flash('Trainer fired!')
        raise redirect(nextpage)

    #equip gear on fighter
    @expose()
    @identity.require(identity.not_anonymous())
    def equipgear(self, **data):
        try:
            fighter = my_fighter()
            inventory = cur_user().gear
            gear = Equipment.get(int(data['gear_id']))

            #check if the fighter owns the gear and equip
            if gear in inventory and fighter.level >= gear.level:
                if gear.type == 'Gloves':
                    fighter.gloves = gear
                elif gear.type == 'Boots':
                    fighter.boots = gear
                elif gear.type == 'Trunks':
                    fighter.trunks = gear
        
            #update the fighter's stats to accomodate new gear
            createFighterImage(fighter)

            result = []
            for i in inventory:
                if i.type != "Gym":
                    if ((fighter.gloves == i) or (fighter.boots == i) or (fighter.trunks == i)):
                        result.append({"id":i.id, "link":True})
                    else:
                        result.append({"id":i.id, "link":False})
            return dict(inventory=result)
        except:
            return dict()

    #buy gear from shop
    @expose()
    @identity.require(identity.not_anonymous())
    def buygear(self, **data):
        try:
            gear = Equipment.get(int(data['gear_id']))
            inventory = cur_user().gear
            
            #check if you have this item in the auction already
            dupcheck = Auction.select(AND(Auction.q.owner == me(), Auction.q.itemID == Equipment.q.id, Equipment.q.name == gear.name)).count()
            
            if dupcheck != 0:
                flash('You already own this item and have put it up for auction')

            #check if user already owns the gear
            elif cur_user().money >= gear.cost: #not owned and have enough money
                if gear in inventory:
                    flash('You already own this item')
                else:
                    cur_user().addEquipment(gear)
                    cur_user().money -= gear.cost
                    flash(gear.name + ' purchased!')
                    Feed(owner = me(), msg='Bought %s at the shop for $%d' %(gear.name, (gear.cost)),
                        category = 'Shop', time = datetime.now())
                    
            else: #not enough minerals
                flash('You don\'t have enough money to purchase this.')
    
            raise redirect('./shop')
        except KeyError:
            raise redirect('./home')

    #sell gear at shop
    @expose()
    @identity.require(identity.not_anonymous())
    def sellgear(self, **data):
        try:
            gear = Equipment.get(int(data['gear_id']))
            inventory = cur_user().gear

            if gear in inventory and (not inUse(gear)):
                cur_user().removeEquipment(gear)
                cur_user().money += (gear.cost/3)
                flash('Item sold!')
                Feed(owner = me(), msg='Sold %s at the shop for $%d' %(gear.name, (gear.cost/3)),
                    category = 'Shop', time = datetime.now())

            else:
                flash('Items which are currently in use may not be sold')

            raise redirect('./shop')
        except:
            raise redirect('./shop')


####Auction stuff####
    #go to auctions
    @expose(template="rpg.templates.auctions")
    @identity.require(identity.not_anonymous())
    @paginate('auctions', limit=10)
    def auction(self, **data):
        try:
            if data.get('filter', False):
                auctionfilter = data['filter']
		if ((auctionfilter != 'All') and (auctionfilter != 'Gloves') and (auctionfilter != 'Boots') and (auctionfilter != 'Trunks')):
               	    auctionfilter = "All"
            else:
                auctionfilter = "All"
    
            if auctionfilter == "All":    
                auctions = Auction.select()
            else:
                #auctions = Auction.select(Auction.itemID.q.type == auctionfilter)
                auctions = Auction.select(AND(Auction.q.itemID == Equipment.q.id, Equipment.q.type == auctionfilter))

            auctioncount = auctions.count()
            mybids = Auction.select(Auction.q.buyer==me())
            myauctions = Auction.select(Auction.q.owner==me())

            auctionsgrid = widgets.PaginateDataGrid(fields=[
                (' ', auctionButton),
                ('Item', itemName),
                ('Type', itemType),
                ('Level', itemLevel),
                ('Strength', itemStrength),
                ('Speed', itemSpeed),
                ('Defence', itemDefence),
                ('Conditioning', itemConditioning),
                ('Highest Bid', 'bid'),
                ('Expires On', 'expiry'),
                ('Seller', 'owner')])
            
            
            viewgrid = widgets.DataGrid(fields=[
                ('Item', itemName),
                ('Type', itemType),
                ('Level', itemLevel),
                ('Strength', itemStrength),
                ('Speed', itemSpeed),
                ('Defence', itemDefence),
                ('Conditioning', itemConditioning),
                ('Highest Bid', 'bid'),
                ('Expires On', 'expiry'),
                ('Seller', 'owner')])
                
            owngrid = widgets.DataGrid(fields=[
                ('Item', itemName),
                ('Type', itemType),
                ('Level', itemLevel),
                ('Strength', itemStrength),
                ('Speed', itemSpeed),
                ('Defence', itemDefence),
                ('Conditioning', itemConditioning),
                ('Highest Bid', 'bid'),
                ('Expires On', 'expiry'),
                ('Seller', 'owner'),
                (' ', cancelAuction)])
            
            return dict(auctioncount = auctioncount, auctions = auctions, auctiongrid = auctionsgrid,
                mybids = mybids, myauctions = myauctions, tabber=widgets.Tabber(),
                inventory = cur_user().gear, viewgrid = viewgrid, owngrid = owngrid)
            
        except:
            raise redirect('./auction')

    #place bid
    @expose()
    @identity.require(identity.not_anonymous())
    def placebid(self, **data):
        try:
            auction = Auction.get(int(data['auctionID']))
            mybids = Auction.select(Auction.q.buyer==me())
            bid = int(data['bid'])
    
            if auction.owner == me() or auction.item in cur_user().gear:
                flash('Cannot bid on your own auctions or items that you already own.')
            
            elif auction in mybids:
                flash('Cannot bid on the same item more than once.')
                
            elif bid <= auction.bid+25:
                flash('Your bid must be at least $25 more than the current highest bid!')
            
            elif cur_user().money >= bid:
                #refund old bidder's money and notify
                if auction.buyer != '':
                    old_bidder = User.by_user_name(auction.buyer)
                    old_bidder.money += bid
                    Feed(owner=auction.buyer, msg = 'You were outbid on %s' % auction.item.name,
                        category='auction', time = datetime.now())
                
                #update auction to reflect new buyer and deduct payment
                auction.buyer = me()
                auction.bid = bid
                cur_user().money -= bid
                flash('Bid successfully placed')
            else:
                flash('Insufficient Funds')
	    raise redirect('./auction')
        except KeyError:
            flash('Bid could not be placed: Bid must be a numeric value and an item must be selected!')
            raise redirect('./auction')
	except:
	    raise redirect('./auction')
        
    #create auction
    @expose()
    @identity.require(identity.not_anonymous())
    def createauction(self, **data):
        try:
            inventory = cur_user().gear
            
            startingbid = int(data['startbid'])
            
            length = int(data['auctionlength'])
            
            if length < 1 or length > 7:
                flash('Auctions may only last up to 7 days')
            
            elif startingbid < 1:
                flash('Starting bid must be at least 1')
            
            else:
                item = Equipment.selectBy(name=data['auctionitem'])[0]       
                if ((item in inventory) and (not inUse(item))):
                    auction = Auction(item=item, owner=me(),
                        bid=startingbid, expiry=(datetime.now() + timedelta(days=length)))
                    cur_user().removeEquipment(item)
                    Feed(owner=me(), msg = 'Created auction for %s' %item.name,
                        category = 'Auction', time = datetime.now())
                    flash('Auction created successfully')
                else:
                    flash('You cannot auction off gear that is in use')
            raise redirect('./auction')
        except ValueError:
            flash('Auction could not be created: Starting bid must be a numeric value')
            raise redirect('./auction')
        except:
            raise redirect('./auction')
            
            
    #cancel auctions
    @expose()
    @identity.require(identity.not_anonymous())
    def cancelauction(self, **data):
        try:
            auction = Auction.get(int(data['auction']))
            
            if auction.owner == me():
            
                if cur_user().money >= int(auction.item.cost*0.05):
                    #if somebody was bidding
                    if auction.buyer != '':
                        #refund bidder's money
                        bidder = User.by_user_name(auction.buyer)
                        bidder.money += bid
                        Feed(owner=auction.buyer,
                            msg = 'The auction for %s was cancelled' % auction.item.name,
                            category='auction', time = datetime.now())
                        
                    #give item back to user
                    cur_user().addEquipment(auction.item)
                    
                    #charge cancellation fee
                    cur_user().money -= int(0.05*auction.item.cost)
                    
                    #create feed entry/flash msg
                    Feed(owner = me(), msg = 'You cancelled your auction for %s' %auction.item.name,
                        category = 'Auction', time = datetime.now())
                       
                    flash('Auction Cancelled.')
                        
                    #remove auction
                    auction.destroySelf()
                    
                else:
                    flash('You don\'t have enough money to pay the cancellation fee...')
                
            else:
                flash('That auction isn\'t yours...')
                
            raise redirect('/auction')
            
        except:
            raise redirect('/home')
            


####Apearance Stuff####
    @expose()
    @strongly_expire
    @identity.require(identity.not_anonymous())
    def updateimage(self, **data):
        try:
            fighter = my_fighter()

            fighter.body = Feature.selectBy(name=data['body'], type='Body')[0]
            fighter.eyes = Feature.selectBy(name=data['eyes'], type='Eyes')[0]
            fighter.hair = Feature.selectBy(name=data['hair'], type='Hair')[0]
            fighter.mouth = Feature.selectBy(name=data['mouth'], type='Mouth')[0]
            fighter.face = Feature.selectBy(name=data['face'], type='Face')[0]

            createFighterImage(fighter)
            return dict()
        except KeyError:
            raise redirect(tg.url('/home'))

#check if the fighter has gained a level
def checkLevel(fighter):
    if fighter.exp > 2000:
        fighter.level += 1
        fighter.exp = fighter.exp%2000
        return True

    return False

#create a fighter and equip starter gear
def addFighter(fighter_name):
    fighter = Fighter(
        name=fighter_name,
		#trainer=Trainer.get(1), # remove comment to remove trainer
        gloves=Equipment.get(1),
        boots=Equipment.get(2),
        trunks=Equipment.get(3),
        equipment1=Equipment.get(4),
        equipment2=Equipment.get(5),
        equipment3=Equipment.get(6),
        mouth=Feature.selectBy(name='None', type='Mouth')[0],
        body=Feature.selectBy(name='White', type='Body')[0],
        hair=Feature.selectBy(name='Bald', type='Hair')[0],
        face=Feature.selectBy(name='None', type='Face')[0],
        eyes=Feature.selectBy(name='Regular', type='Eyes')[0])
    createFighterImage(fighter)
    return fighter

#check if item is in use
def inUse(gear):
    fighter = my_fighter()
    if gear == fighter.gloves or gear == fighter.boots or gear == fighter.trunks or gear == fighter.equipment1 or gear == fighter.equipment2 or gear == fighter.equipment3:
        return True
        
    else:
        return False

#create image of fighter
def createFighterImage(fighter):
    ImageGen.update_fighter_image(fighter)

    return

#fighter links in datagrid
#based on linking method found in Introduction to Widgets
#at http://docs.turbogears.org/1.0/IntroductionToWidgets
def linkFighter(fighter):
    link = Element('a', href=tg.url('/arena?opp=%s') % fighter.name)
    link.text = fighter.name
    return link
    
def cancelAuction(auction):
    link = Element('a', href=tg.url('/cancelauction?auction=%s') % auction.id)
    link.text = 'Cancel'
    return link


#fighting money calcs
def calcPurse(opponent):
    winnings = 100*opponent.level
    if opponent.level > my_fighter().level:
        winnings += (opponent.level-my_fighter().level)*100
        
    winnings += ((opponent.exp - my_fighter().exp)/100)
    
    return winnings
        
def calcBet(opponent):
    
    bet = (100*opponent.level)/2
    
    bet += ((opponent.exp - my_fighter().exp)/100)

    return bet


#create feed entry for fight result
def fightFeed(name, result, opponent, prize):
    if result == 'win':
        Feed(owner=name, msg="Your fighter defeated %s, you earned $%d" %(opponent, prize),
            category = 'Fight', time = datetime.now())
        
    elif result == 'lose':
         Feed(owner=name, msg="Your fighter lost against %s" % opponent,
            category = 'Fight', time = datetime.now())
         
    else:
         Feed(owner=name, msg="Your fighter drew against %s" %(opponent, prize),
            category = 'Fight', time = datetime.now())
        

####helpers for foreignkey attributes in auctions grid####
def auctionButton(auction):
    button = Element('input',type='radio', name='auctionID', id='auctionID',
        value=str(auction.id), onclick='minBid(%s)' % auction.bid)
    return button
    
def itemName(auction):
    return auction.item.name
    
def itemType(auction):
    return auction.item.type
    
def itemLevel(auction):
    return auction.item.level
    
def itemStrength(auction):
    return auction.item.strength
    
def itemSpeed(auction):
    return auction.item.speed
    
def itemDefence(auction):
    return auction.item.defence
    
def itemConditioning(auction):
    return auction.item.conditioning

#user helper functions    
    
def cur_user():
    return identity.current.user

def my_fighter():
    return identity.current.user.fighter

def me():
    return identity.current.user.user_name
