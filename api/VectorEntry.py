import json
from flask import jsonify

class VectorEntry():

  def __init__(self, index, iid, vector):
    self.index = index
    self.id = iid
    self.vector = vector

  def get_as_json(self):
    return {'index': self.index, 'id': self.id, 'vector': self.vector}
