import json
import sys
from flask import Flask, Response, abort, request, jsonify
from api.VectorEntry import VectorEntry
from api.VectorResultEntry import VectorResultEntry
from core.VectorHandler import VectorHandler
from annoy import AnnoyIndex

app = Flask(__name__)
vector_handler = VectorHandler()
base_path = '/v1/annoy/index'

@app.route(base_path + '/add', methods=['POST'])
def add_vector():
  if not request.json:
      abort(400)
  vector = VectorEntry(request.json['id'], request.json['vector'])
  vector_handler.add_vector(vector)
  return vector.get_as_json(), 201

@app.route(base_path + '/nns', methods=['POST'])
def get_nns_by_vector():
  if not request.json:
      abort(400)
  results = vector_handler.get_nns_by_vector(request.json['vector'])
  return jsonify({'result': results}), 200

@app.route(base_path + '/build')
def build_annoy_index():
  vector_handler.build_index()
  return jsonify({'acknowledge': True}), 200
