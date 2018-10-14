import json
from flask import jsonify

class VectorEntry():

  def __init__(self, iid, vector):
    self.id = iid
    self.vector = vector

  def get_as_json(self):
    return jsonify({'id': self.id, 'vector': self.vector})
