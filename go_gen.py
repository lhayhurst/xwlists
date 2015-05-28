import xwingmetadata

__author__ = 'lhayhurst'

for shipname in xwingmetadata.ships.keys():
    shiptext = ' "' + shipname + '": func () Ship { return Ship{ Name: " ' + shipname + '", Attack: 3, Agility: 1, Hull: 3, Shields: 5, canAttack: true,}},'
    print shiptext

