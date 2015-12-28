import json

class Tome:
    def __init__(self, json_data, tourney ):
        self.data = json_data
        self.tournament_name = None
        self.tourney = tourney
        self.validate_data()


    ENTITY_GROUP_MAP = 'entityGroupMap'
    ENTITIES         = 'entities'
    METADATA_VERSION = 'metadataVersion'
    TEMP_KEYS        = 'tempKeys'
    TOME_VERSION     = '1.0.5'
    TOURNAMENT       = 'Tournament:#'
    NAME             = 'name'
    ROUND_LENGTH     = 'round_length'
    FORMAT_PK        = 'format_pk'
    PRIMARY_KEY      = 'pk'
    CURRENT_ROUND    = 'current_round'
    ENTITY_ASPECT    = 'entity_aspect'
    PARENT_PKEY      = 'parent_pk'
    SETTINGS_PK      = 'settings_pk'

    def validate_data(self):
        #validate to level keys
        expected_keys = [Tome.ENTITY_GROUP_MAP, Tome.METADATA_VERSION, Tome.TEMP_KEYS]
        for ek in expected_keys:
            if not ek in self.data.keys():
                raise Exception("TOME data missing top level key " + ek )
        if not Tome.TOME_VERSION == self.data[Tome.METADATA_VERSION]:
            raise Exception("wrong TOME data version, expected  " +  Tome.TOME_VERSION + ", received " + self.data[Tome.METADATA_VERSION])

        #validate tournament info
        entity_group_map = self.data[Tome.ENTITY_GROUP_MAP]
        if not entity_group_map.has_key( Tome.TOURNAMENT):
            raise Exception("no data found for tournament key")
        tournament_info = entity_group_map[Tome.TOURNAMENT]
        if not tournament_info.has_key( Tome.ENTITIES ):
            raise Exception("tournament info has no entities key")

        #a tournament can have multiple segements (ie a swiss followed by a cut)
        #these segments are stored as 'entities' inside the tournament info
        tournament_segments = tournament_info[Tome.ENTITIES]

        if not len( tournament_segments > 0 ):
            raise Exception("empty tournament segments found")

        self.tournament_segments = {}
        for segment in tournament_segments:
            #each segment should have a name, a key, a type, format format key
            #for now, just stash these away, as we'll have to come back and validate them later
            pk = segment[Tome.PRIMARY_KEY]
            self.tournament_segments[pk] = segment

        if not tournament_info.has_key( Tome.NAME ):
            raise Exception("no name found for tournament")
        self.tournament_name = tournament_info[Tome.Name]




if __name__ == "__main__":
    fh = open("static/tome.json", 'r')
    strdata = fh.read().replace('\n', '')
    print strdata
    data = json.loads(strdata)
    t = Tome( data )
