from datetime import *
import pkg_resources
pkg_resources.require("SQLObject>=0.8,<=0.10.0")
from turbogears.database import PackageHub
# import some basic SQLObject classes for declaring the data model
# (see http://www.sqlobject.org/SQLObject.html#declaring-the-class)
from sqlobject import SQLObject, SQLObjectNotFound, RelatedJoin
# import some datatypes for table columns from SQLObject
# (see http://www.sqlobject.org/SQLObject.html#column-types for more)
from sqlobject import StringCol, UnicodeCol, IntCol, DateTimeCol, ForeignKey, RelatedJoin, DateCol, BoolCol
from turbogears import identity

__connection__ = hub = PackageHub('rpg')

# your data model

class Chat(SQLObject):
    user = StringCol(notNone=True, default='')
    message = UnicodeCol(notNone=True, default='')
    room = StringCol(notNone=True, default='')
    target = StringCol(default='')
    time = DateTimeCol(default=datetime.now())

#the fighter
class Fighter(SQLObject):
    name = StringCol(notNone=True, default='', alternateID=True, alternateMethodName='by_fighter_name')

    trainer = ForeignKey('Trainer', notNone=False, default=None)
	
    #stat bonuses from attribute points
    trainer_points = IntCol(default=0)
    trainer_strength = IntCol(default=0)
    trainer_speed = IntCol(default=0)
    trainer_defence = IntCol(default=0)
    trainer_conditioning = IntCol(default=0)

    hp = IntCol(default=100)

    level = IntCol(default=1)
    exp = IntCol(default=0)

    #related gear
    gloves = ForeignKey('Equipment')
    boots = ForeignKey('Equipment')
    trunks = ForeignKey('Equipment')
	
    #related equipment
	# equipement_set = 0 when not set 1 when set
    equipment_set = BoolCol(default=False)
    equipment1 = ForeignKey('Equipment')
    equipment2 = ForeignKey('Equipment')
    equipment3 = ForeignKey('Equipment')

    #fight record
    wins = IntCol(default=0)
    losses = IntCol(default=0)
    draws = IntCol(default=0)

    #fighter appearance stuff
    body = ForeignKey('Feature')
    eyes = ForeignKey('Feature')
    hair = ForeignKey('Feature')
    mouth = ForeignKey('Feature')
    face = ForeignKey('Feature')
	
    def getStrength(self):
        strength = 10+self.level
        strength += self.gloves.strength
        strength += self.boots.strength
        strength += self.trunks.strength
        strength += self.equipment1.strength
        strength += self.equipment2.strength
        strength += self.equipment3.strength
        strength += self.trainer_strength
        return strength
		
    def getSpeed(self):
        speed = 10+self.level
        speed += self.gloves.speed
        speed += self.boots.speed
        speed += self.trunks.speed
        speed += self.equipment1.speed
        speed += self.equipment2.speed
        speed += self.equipment3.speed
        speed += self.trainer_speed
        return speed
		
    def getDefence(self):
        defence = 10+self.level
        defence += self.gloves.defence
        defence += self.boots.defence
        defence += self.trunks.defence
        defence += self.equipment1.defence
        defence += self.equipment2.defence
        defence += self.equipment3.defence
        defence += self.trainer_defence
        return defence
		
    def getConditioning(self):
        conditioning = 10+self.level
        conditioning += self.gloves.conditioning
        conditioning += self.boots.conditioning
        conditioning += self.trunks.conditioning
        conditioning += self.equipment1.conditioning
        conditioning += self.equipment2.conditioning
        conditioning += self.equipment3.conditioning
        conditioning += self.trainer_conditioning
        return conditioning

    def getHP(self):
        return (10+self.level+self.getConditioning())


class Trainer(SQLObject):
    name = StringCol(notNone=True, default='')
    hirefee = IntCol(default=0)
    salary = IntCol(default=0)
    points = IntCol(default=0)
    level = IntCol(default=1)

#equipment
class Equipment(SQLObject):
    name = StringCol(notNone=True, default='')
    type = StringCol(notNone=True, default='')

    #bonus to stats
    strength = IntCol(default=0)
    speed = IntCol(default=0)
    defence = IntCol(default=0)
    conditioning=IntCol(default=0)

    cost = IntCol(default=0) #cost in the shop

    owner = RelatedJoin('User')

    #imaging stuff
    filename = StringCol(default = '')

    #offsets
    offset_x = IntCol(default = 0)
    offset_y = IntCol(default = 0)
    
    level = IntCol(default=1) #level requirement


#appearance stuff
class Feature(SQLObject):
    type = StringCol(default='')
    name = StringCol(default='')
    filename = StringCol(default='')
    offset_x = IntCol(default = 0)
    offset_y = IntCol(default = 0)

#auction stuff
class Auction(SQLObject):
    owner = StringCol(default='')
    item = ForeignKey('Equipment')
    expiry = DateCol(default = datetime.now() + timedelta(days=1)) 
    buyer = StringCol(default='')
    bid = IntCol(default = 0)
    buyout = IntCol(default = 0)
    
#feed info
class Feed(SQLObject):
    owner = StringCol(default='')
    msg = StringCol(default='')
    category = StringCol(default='')
    time = DateTimeCol(default=datetime.now())

# the identity model

class Visit(SQLObject):
    """
    A visit to your site
    """
    class sqlmeta:
        table = 'visit'

    visit_key = StringCol(length=40, alternateID=True,
                          alternateMethodName='by_visit_key')
    created = DateTimeCol(default=datetime.now)
    expiry = DateTimeCol()

    def lookup_visit(cls, visit_key):
        try:
            return cls.by_visit_key(visit_key)
        except SQLObjectNotFound:
            return None
    lookup_visit = classmethod(lookup_visit)


class VisitIdentity(SQLObject):
    """
    A Visit that is link to a User object
    """
    visit_key = StringCol(length=40, alternateID=True,
                          alternateMethodName='by_visit_key')
    user_id = IntCol()


class Group(SQLObject):
    """
    An ultra-simple group definition.
    """
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = 'tg_group'

    group_name = UnicodeCol(length=16, alternateID=True,
                            alternateMethodName='by_group_name')
    display_name = UnicodeCol(length=255)
    created = DateTimeCol(default=datetime.now)

    # collection of all users belonging to this group
    users = RelatedJoin('User', intermediateTable='user_group',
                        joinColumn='group_id', otherColumn='user_id')

    # collection of all permissions for this group
    permissions = RelatedJoin('Permission', joinColumn='group_id',
                              intermediateTable='group_permission',
                              otherColumn='permission_id')


class User(SQLObject):
    """
    Reasonably basic User definition.
    Probably would want additional attributes.
    """
    # names like "Group", "Order" and "User" are reserved words in SQL
    # so we set the name to something safe for SQL
    class sqlmeta:
        table = 'tg_user'

    user_name = UnicodeCol(length=16, alternateID=True,
                           alternateMethodName='by_user_name')
    email_address = UnicodeCol(length=255, alternateID=True,
                               alternateMethodName='by_email_address')
    display_name = UnicodeCol(length=255)
    password = UnicodeCol(length=40)
    created = DateTimeCol(default=datetime.now)

    ###User's Fighter###
    fighter = ForeignKey('Fighter')

    ###Inventory###
    gear = RelatedJoin('Equipment')

    money = IntCol(default = 100)

    ###User's Default Chat Room###
    chat_room = StringCol(default='main')

    # groups this user belongs to
    groups = RelatedJoin('Group', intermediateTable='user_group',
                         joinColumn='user_id', otherColumn='group_id')

    def _get_permissions(self):
        perms = set()
        for g in self.groups:
            perms |= set(g.permissions)
        return perms

    def _set_password(self, cleartext_password):
        """Runs cleartext_password through the hash algorithm before saving."""
        password_hash = identity.encrypt_password(cleartext_password)
        self._SO_set_password(password_hash)

    def set_password_raw(self, password):
        """Saves the password as-is to the database."""
        self._SO_set_password(password)


class Permission(SQLObject):
    """
    A relationship that determines what each Group can do
    """
    permission_name = UnicodeCol(length=16, alternateID=True,
                                 alternateMethodName='by_permission_name')
    description = UnicodeCol(length=255)

    groups = RelatedJoin('Group',
                         intermediateTable='group_permission',
                         joinColumn='permission_id',
                         otherColumn='group_id')
