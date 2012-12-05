import turbogears
from rpg import model
from rpg.model import Equipment, Feature, Trainer

turbogears.update_config(configfile="dev.cfg",
    modulename="rpg.config")

# populate base equipment

Equipment(name='Red Gloves', type='Gloves', strength=5,
    speed=0, defence=0, conditioning=0, cost=0,
    filename='rpg/static/images/equipment/gloves_red.png', offset_x=39, offset_y=397)

Equipment(name='Red Boots', type='Boots', strength=0,
    speed=5, defence=0, conditioning=0, cost=0,
    filename='rpg/static/images/equipment/shoes_red.png', offset_x=79, offset_y=508)

Equipment(name='Red Trunks', type='Trunks', strength=0,
    speed=0, defence=5, conditioning=5, cost=0,
    filename='rpg/static/images/equipment/shorts_red.png', offset_x=79, offset_y=400)
    
Equipment(name='5lb Weights', type='Gym', strength = 1)

Equipment(name='Running Shoes', type='Gym', conditioning = 1)

Equipment(name='Sparring Gear', type='Gym', speed = 1, defence = 1, conditioning = 1)

Trainer(name='Craig Kost', points=5, salary = 100, hirefee = 100)

#populate trainers
Trainer(name='Punchy McGee', points=6, level = 2, salary = 500, hirefee=200)

Trainer(name = 'Jack Maybourne', points = 7, level = 2, salary = 700, hirefee = 600)

Trainer(name = 'Aaron Chrichton', points = 10, level = 3, salary = 1000, hirefee = 1000)

Trainer(name='Manny Stewart', points =30, level = 20, salary = 100000, hirefee=20000)



# populate gym equipment

Equipment(name='Medicine Ball', type='Gym', conditioning = 3, defence = 2, level = 2, cost = 200)

Equipment(name='Skipping Rope', type='Gym', speed = 2, conditioning = 1, level = 2, cost = 200)

Equipment(name='Speed Bag', type='Gym', speed = 3, strength = 2, conditioning = 1, level = 5, cost = 350)

Equipment(name='Heavy Bag', type='Gym', strength = 3, speed = 1, conditioning = 2, level = 5, cost = 350)

Equipment(name='Weight Machine', type='Gym', strength = 5, conditioning = 2, level = 6, cost = 400)


# populate gloves

Equipment(name='Blue Gloves', type='Gloves', strength=10,
    speed=0, defence=0, conditioning=0, cost=100, level=1,
    filename='rpg/static/images/equipment/gloves_blue.png', offset_x=39, offset_y=397)

Equipment(name='White Gloves', type='Gloves', strength=20,
    speed=0, defence=5, conditioning=0, cost=250, level=5,
    filename='rpg/static/images/equipment/gloves_white.png', offset_x=39, offset_y=397)

Equipment(name='Black Gloves', type='Gloves', strength=25,
    speed=5, defence=5, conditioning=0, cost=500, level=10,
    filename='rpg/static/images/equipment/gloves_black.png', offset_x=39, offset_y=397)

# populate boots

Equipment(name='Blue Boots', type='Boots', strength=0,
    speed=10, defence=0, conditioning=0, cost=100, level=1,
    filename='rpg/static/images/equipment/shoes_blue.png', offset_x=79, offset_y=508)

Equipment(name='White Boots', type='Boots', strength=0,
    speed=15, defence=5, conditioning=0, cost=200, level=5,
    filename='rpg/static/images/equipment/shoes_white.png', offset_x=79, offset_y=508)

Equipment(name='Black Boots', type='Boots', strength=5,
    speed=20, defence=5, conditioning=0, cost=500, level=10,
    filename='rpg/static/images/equipment/shoes_black.png', offset_x=79, offset_y=508)

# populate trunks

Equipment(name='Blue Trunks', type='Trunks', strength=0,
    speed=0, defence=10, conditioning=10, cost=150, level=1,
    filename='rpg/static/images/equipment/shorts_blue.png', offset_x=79, offset_y=400)

Equipment(name='White Trunks', type='Trunks', strength=0,
    speed=5, defence=15, conditioning=10, cost=250, level=5,
    filename='rpg/static/images/equipment/shorts_white.png', offset_x=79, offset_y=400)

Equipment(name='Yellow Trunks', type='Trunks', strength=5,
    speed=15, defence=15, conditioning=15, cost=550, level=10,
    filename='rpg/static/images/equipment/shorts_yellow.png', offset_x=79, offset_y=400)

# populate Feature

# populate bodies

Feature(name='White', type='Body',
    filename='rpg/static/images/features/body_white.png', offset_x=29, offset_y=90)

Feature(name='Yellow', type='Body',
    filename='rpg/static/images/features/body_yellow.png', offset_x=29, offset_y=90)

Feature(name='Brown', type='Body',
    filename='rpg/static/images/features/body_brown.png', offset_x=29, offset_y=90)

Feature(name='Black', type='Body',
    filename='rpg/static/images/features/body_black.png', offset_x=29, offset_y=90)

# populate hair

Feature(name='Bald', type='Hair',
    filename='', offset_x=0, offset_y=0)

Feature(name='Spikey', type='Hair',
    filename='rpg/static/images/features/hair_spike.png', offset_x=20, offset_y=30)

Feature(name='Turban', type='Hair',
    filename='rpg/static/images/features/hair_turban.png', offset_x=23, offset_y=15)

Feature(name='Fro', type='Hair',
    filename='rpg/static/images/features/hair_fro.png', offset_x=13, offset_y=44)

Feature(name='Whispy', type='Hair',
    filename='rpg/static/images/features/hair_whisp.png', offset_x=20, offset_y=69)

# populate eyes

Feature(name='Angry', type='Eyes',
    filename='rpg/static/images/features/eyes_angry.png', offset_x=59, offset_y=162)

Feature(name='Blue', type='Eyes',
    filename='rpg/static/images/features/eyes_blue.png', offset_x=79, offset_y=157)

Feature(name='Cool', type='Eyes',
    filename='rpg/static/images/features/eyes_cool.png', offset_x=50, offset_y=162)

Feature(name='Furrow', type='Eyes',
    filename='rpg/static/images/features/eyes_furrow.png', offset_x=54, offset_y=123)

Feature(name='Mean', type='Eyes',
    filename='rpg/static/images/features/eyes_mean.png', offset_x=53, offset_y=157)

Feature(name='Regular', type='Eyes',
    filename='rpg/static/images/features/eyes_reg.png', offset_x=60, offset_y=161)

# populate face

Feature(name='None', type='Face',
    filename='', offset_x=0, offset_y=0)

Feature(name='Beard', type='Face',
    filename='rpg/static/images/features/face_beard.png', offset_x=55, offset_y=187)

# populate mouth

Feature(name='None', type='Mouth',
    filename='', offset_x=0, offset_y=0)

Feature(name='Straight', type='Mouth',
    filename='rpg/static/images/features/mouth_straight.png', offset_x=113, offset_y=219)

Feature(name='Teeth', type='Mouth',
    filename='rpg/static/images/features/mouth_teeth.png', offset_x=81, offset_y=210)

model.hub.commit()
