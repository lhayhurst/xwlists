import random
import re
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from myapp import db_connector
from xwingmetadata import XWingMetaData
import xwingmetadata


__author__ = 'lhayhurst'

import time
from decl_enum import DeclEnum
from sqlalchemy import Column, Integer, String, DateTime, Table, desc, Float, asc, func, Date
from sqlalchemy import ForeignKey


#TABLES

tourney_table = "tourney"
list_table = "list"
ship_table = "ship"
pilot_table = "pilot"
ship_pilot_table = "ship_pilot"
ship_type_table = "ship_type"
upgrade_table = "ship_upgrade"
ship_pilot_upgrade_table = "ship_pilot_upgrade_table"
tourney_list_table = "tourney_list"


Base = db_connector.get_base()

class Faction(DeclEnum):
    IMPERIAL = "Imperial", "Imperial"
    REBEL    = "Rebel", "Rebel"

class UpgradeType(DeclEnum):
    TITLE = xwingmetadata.TITLE, xwingmetadata.TITLE
    DROID = xwingmetadata.DROID, xwingmetadata.DROID,
    CREW  = xwingmetadata.CREW, xwingmetadata.CREW
    EPT   = xwingmetadata.EPT, xwingmetadata.EPT
    MOD    = xwingmetadata.MOD, xwingmetadata.MOD
    SYSTEM = xwingmetadata.SYSTEM, xwingmetadata.SYSTEM
    BOMB_MINES = xwingmetadata.BOMB, xwingmetadata.BOMB
    CANNON = xwingmetadata.CANNON, xwingmetadata.CANNON
    TURRET = xwingmetadata.TURRET, xwingmetadata.TURRET
    TORPEDO = xwingmetadata.TORPEDO, xwingmetadata.TORPEDO
    MISSILE = xwingmetadata.MISSILE, xwingmetadata.MISSILE

class ShipType(DeclEnum):
    XWING = "X-Wing", "X-Wing"
    YWING = "Y-Wing", "Y-Wing"
    AWING = "A-Wing", "A-Wing"
    BWING = "B-Wing", "B-Wing"
    EWING = "E-Wing", "E-Wing"
    YT1300 = "YT-1300", "YT-1300"
    YT2400 = "YT-2400", "YT-2400"
    HWK290 = "HWK-290", "HWK-290"
    Z95 = "Z-95 Headhunter", "Z-95 Headhunter"
    TIEFIGHTER = "TIE Fighter", "TIE Fighter"
    TIEADVANCED = "TIE Advanced", "TIE Advanced"
    TIEINTERCEPTOR = "TIE Interceptor", "Tie Interceptor"
    FIRESPRAY = "Firespray-31", "Firespray-31"
    LAMDA = "Lambda Shuttle", "Lambda Shuttle"
    TIEBOMBER = "TIE Bomber", "TIE Bomber"
    TIEDEFENDER = "TIE Defender", "TIE Defender"
    TIEPHANTOM = "TIE Phantom", "TIE Phantom"
    DECIMATOR = "VT-49 Decimator", "VT-49 Decimator"

class Pilot(Base):
    __tablename__ = pilot_table
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    cost = Column(Integer)

class ShipPilot(Base):
    __tablename__ = ship_pilot_table
    id = Column(Integer, primary_key=True)
    ship_type = Column(ShipType.db_type())
    pilot_id = Column(Integer, ForeignKey('{0}.id'.format(pilot_table)))
    pilot = relationship(Pilot.__name__, uselist=False)



class Ship(Base):
    __tablename__ = ship_table
    id = Column(Integer, primary_key=True)
    ship_pilot_id = Column(Integer, ForeignKey('{0}.id'.format(ship_pilot_table)))
    list_id = Column(Integer, ForeignKey('{0}.id'.format(list_table)))  #parent
    ship_pilot = relationship(ShipPilot.__name__, uselist=False)
    upgrades = relationship( "ShipUpgrade", back_populates="ship")

    def get_upgrade(self, upgrade_name ):

        ret = []

        num_upgrades = 1

        if "." in upgrade_name:
            a = upgrade_name.split('.')
            upgrade_name = a[0]
            num_upgrades = int(a[1])

        for upgrade in self.upgrades:
            if upgrade.upgrade_type.description == upgrade_name:
                ret.append( upgrade.upgrade)

        if num_upgrades > len(ret):
            return ""
        elif len(ret) == 0:
            return ""
        print ret
        return ret[ num_upgrades - 1  ]


class ShipUpgrade(Base):
    __tablename__ = upgrade_table
    id = Column(Integer, primary_key=True)
    ship_id = Column(Integer, ForeignKey('{0}.id'.format(ship_table)))
    upgrade_type = Column(UpgradeType.db_type())
    upgrade = Column(String(128))
    ship = relationship( Ship.__name__, back_populates="upgrades")


class List(Base):
    __tablename__ = list_table
    id = Column(Integer, primary_key=True)
    name   = Column(String(128))
    faction     = Column(Faction.db_type())
    ships       = relationship(Ship.__name__)
    points      = Column(Integer)


class Tourney(Base):
    __tablename__ = tourney_table
    id = Column(Integer, primary_key=True)
    tourney_name  = Column(String(128))
    tourney_date  = Column(Date)
    tourney_type  = Column(String(128))
    tourney_lists = relationship( "TourneyList", back_populates="tourney", order_by="asc(TourneyList.tourney_standing)")

class TourneyList(Base):
    __tablename__ = tourney_list_table
    id               = Column( Integer, primary_key=True)
    tourney_id       = Column(Integer, ForeignKey('{0}.id'.format(tourney_table)))
    list_id          = Column(Integer, ForeignKey('{0}.id'.format(list_table)))
    player_name      = Column(String(128))
    tourney_standing = Column(Integer)
    image            = Column(String(128))
    list             = relationship( List.__name__, uselist=False)
    tourney          = relationship( Tourney.__name__, back_populates="tourney_lists")

    def player_name_stripped(self):
        regex = re.compile('[^a-zA-Z ]')
        return regex.sub('', self.player_name)





class PersistenceManager:

    db_connector = None

    def __init__(self, db_connector):
        self.db_connector = db_connector

    def create_schema(self):
        self.db_connector.get_base().metadata.create_all(self.db_connector.get_engine())

    def drop_schema(self):
        self.db_connector.get_base().metadata.drop_all(self.db_connector.get_engine())


    def populate_reference_tables(self):
        #return True
        session = self.db_connector.get_session()

        pilots = {}
        ship_pilots = []

        m = XWingMetaData()
        all_ships = m.ships_full()
        for ship in all_ships:
            for pilot in all_ships[ship]:
                p = Pilot(name=pilot['name'], cost=pilot['cost'])
                pilots[ pilot['name'] ] = p
        session.add_all( pilots.values() )
        session.commit()

        for ship in all_ships:
            for pilot in all_ships[ship]:
                p =  pilots[pilot['name']]
                sp = ShipPilot( ship_type=ShipType.from_string(ship), pilot=p, pilot_id=p.id)
                ship_pilots.append(sp)
        session.add_all( ship_pilots )
        session.commit()

    def get_tourney(self,tourney_name):
        return self.db_connector.get_session().query(Tourney).filter_by(tourney_name=tourney_name).first()

    def get_tourney_by_id(self,tourney_id):
        return self.db_connector.get_session().query(Tourney).filter_by(id=tourney_id).first()


    def delete_tourney(self, tourney_name):
        tourney = self.get_tourney( tourney_name)
        for list in tourney.tourney_lists:
            self.db_connector.get_session().delete(list)
        self.db_connector.get_session().delete(tourney)
        self.db_connector.get_session().commit()

    def delete_tourney_list_details(self, tourney_list):

        for ship in tourney_list.list.ships:
            self.db_connector.get_session().delete(ship)
        self.db_connector.get_session().delete(tourney_list.list)
        tourney_list.list = None
        self.db_connector.get_session().commit()


    def get_tourney_list(self,tourney_list_id):
        return self.db_connector.get_session().query(TourneyList).filter_by(id=tourney_list_id).first()

    def get_ship_pilot(self, ship_type, pilot):
        return \
        self.db_connector.get_session().query(ShipPilot, Pilot).filter_by(ship_type=ShipType.from_string(ship_type)). \
            filter(ShipPilot.pilot_id == Pilot.id). \
            filter(pilot == Pilot.name).first()[0]


    def get_random_tourney_list(self, tourney):
        session = self.db_connector.get_session()
        query = session.query(Tourney, TourneyList).\
                        filter(TourneyList.tourney_id == Tourney.id).\
                        filter(TourneyList.list_id == None )
        rowcount = int(query.count())
        randomRow = query.offset( int( rowcount * random.random() ) ).first()
        return randomRow[1]

    def get_tourney_summary(self):
        session = self.db_connector.get_session()
        tourney_lists = session.query(TourneyList).all()

        ret = {}

        for tl in tourney_lists:
            tourney_name = tl.tourney.tourney_name
            if not ret.has_key(tourney_name):
                ret[tourney_name] = { 'num_entered' : 0, 'num_not_entered' : 0, 'tourney': tl.tourney}
            if tl.list_id is None:
                ret[tourney_name]['num_not_entered'] += 1
            else:
                ret[tourney_name]['num_entered'] += 1
        return ret


