#Encoding=UTF8

import pymongo
from src import Config

conn = pymongo.MongoClient(Config.config['mongo_url'])

def get_user(userId, password):
    db = conn.VoiceImageDB
    coll = db.user_profile
    return coll.find_one({'user_id': userId, 'password': password})

def get_user_by_id(userId):
    db = conn.VoiceImageDB
    coll = db.user_profile
    rec = coll.find_one({'user_id': userId})
    return rec;

def register_user(user):
    db = conn.VoiceImageDB
    coll = db.user_profile
    coll.insert_one(user)
    
def get_server_users():
    db = conn.VoiceImageDB
    coll = db.server_usage
    doc = coll.find_one()
    if doc is None:
        servers = Config.config['servers']
        doc = {}
        for server in servers:
            doc[server['name']] = 0
        coll.insert_one(doc)
        
    return doc

def increase_server_usage(server_name, count):
    db = conn.VoiceImageDB
    coll = db.server_usage
    doc = coll.find_one()
    if doc is not None:
        doc[server_name] = doc[server_name] + count
        coll.save(doc)
        
def save_image(image):
    db = conn.VoiceImageDB
    coll = db.voice_images
    coll.save(image)
    
def get_unprocessed(num):
    images = []
    db = conn.VoiceImageDB
    coll = db.voice_images
    unpro = coll.find({'processed': False})
    for doc in unpro:
        images.append(doc)
    
    return images

def save_person(person):
    db = conn.VoiceImageDB
    coll = db.user_facename
    coll.save(person)

def get_person_id(user_id, name):
    person_ids = set()
    db = conn.VoiceImageDB
    coll = db.person_list
    unpro = coll.find({'user_id': user_id, 'name': name})
    for doc in unpro:
        person_ids.add(doc['person_id'])
    
    return person_ids
    
def get_similar_persons(user_id, persons):
    person_ids = set()
    for p in persons:
        person_ids = get_person_id(user_id, p)
    
    similars = get_similar_candidates(user_id, person_ids)
    similees = get_similee_candidates(user_id, person_ids)
    
    return person_ids | similars | similees
    
def get_similee_candidates(user_id, person_id):
    similees = set()
    db = conn.VoiceImageDB
    coll = db.person_list

    doc = coll.find_one({'user_id': user_id, 'person_id': person_id})
    if not doc:
        return similees
    
    candidates = doc['candidates']
    if not candidates:
        return similees
    
    candi = [i['personId'] for i in candidates]
    for c in candi:
        similees.add(c)
        
    return similees
    
def get_similee_candidates_rec(user_id, person_ids):
    similees = person_ids
    index = 0
    
    while index < len(similees):
        person_id = similees[index]
        simi = get_similee_candidates(user_id, person_id)
        for si in simi:
            if not si in similees:
                similees.append(si)
                
        index = index + 1
        
    return similees
    
def get_similar_candidates(user_id, person_id):
    similars = set()
    db = conn.VoiceImageDB
    coll = db.person_list
    unpro = coll.find({'user_id': user_id})
    for doc in unpro:
        candidates = doc['candidates']
        if not candidates:
            continue
        
        candi = [i['personId'] for i in candidates]
        if person_id in candi:
            similars.add(doc['person_id'])

    return similars
    
def get_similar_candidates_rec(user_id, person_ids):
    similars = person_ids
    index = 0
    
    while index < len(similars):
        person_id = similars[index]
        simi = get_similar_candidates(user_id, person_id)
        for si in simi:
            if not si in similars:
                similars.append(si)
                
        index = index + 1

    return similars

if __name__ == "__main__":
    print(get_similee_candidates_rec('wang', ['d6ca4db4-f1a3-49c1-8609-b111ecc4df57']))
    print(get_similar_candidates_rec('wang', ['082aca8c-c441-4cc3-a696-9d13ea391f6d']))
    
    
    
    
