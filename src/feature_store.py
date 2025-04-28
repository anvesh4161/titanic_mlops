import redis
import json

class RedisFeatureStore:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.StrictRedis(
            host=host, 
            port=port, 
            db=db, 
            decode_responses=True
            )
        
    # Storing row by row
    def store_features(self, entity_id, features):
        """
        Store features in Redis.
        :param entity_id: Unique identifier for the entity.
        :param features: Dictionary of features to store.
        """
        key = f"entity:{entity_id}:features"
        self.client.set(key, json.dumps(features))

    # Getting rows one at a time
    def get_features(self, entity_id):
        key = f"entity:{entity_id}:features"
        features = self.client.get(key)
        if features:
            return json.loads(features)
        else:
            return None
        
    # Storing the data in a batch        
    def store_batch_features(self, batch_data):
        for entity_id, features in batch_data.items():
            self.store_features(entity_id, features)

    # Getting the data in a batch    
    def get_batch_features(self, entity_ids):
        batch_features = {}
        for entity_id in entity_ids:
            batch_features[entity_id] = self.get_features(entity_id)
        return batch_features
    
    def get_all_entity_ids(self):
        keys = self.client.keys("entity:*:features")
        # entity, entity_id and feature are splitted
        entity_ids = [key.split(":")[1] for key in keys]
        return entity_ids
        

    
