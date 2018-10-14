import json
from flask import jsonify

class VectorResultEntry():

  def __init__(self, iid, distance):
    self.id = iid
    self.distance = distance

  def get_as_json(self):
    return jsonify({'id': self.id, 'distance': self.distance})
