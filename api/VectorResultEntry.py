import json
from flask import jsonify

class VectorResultEntry():

  def __init__(self, index, iid, distance):
    self.index = index
    self.id = iid
    self.distance = distance

  def get_as_json(self):
    return {'index': self.index, 'id': self.id, 'distance': self.distance}
