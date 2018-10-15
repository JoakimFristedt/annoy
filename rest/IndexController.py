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

@app.route(base_path + '/create', methods=['POST'])
def create_index():
  if not request.json:
      abort(400)
  status = vector_handler.create_index(request.json['id'], request.json['dimensions'])
  if status == True:
    return jsonify({'acknowledged': True}), 201
  return jsonify({'acknowledged': False}), 500

@app.route(base_path + '/add', methods=['POST'])
def add_vector():
  if not request.json:
      abort(400)
  vector = VectorEntry(request.json['index'], request.json['id'], request.json['vector'])
  if vector_handler.add_vector(vector) == True:
    return make_response(True), 201
  return make_response(False), 500

@app.route(base_path + '/nns', methods=['POST'])
def get_nns_by_vector():
  if not request.json:
      abort(400)
  results = list(map(lambda x: x.get_as_json(), vector_handler.get_nns_by_vector(request.json['index'], request.json['vector'], request.json['items'])))
  return jsonify(results), 200

@app.route(base_path + '/build', methods=['POST'])
def build_annoy_index():
  if not request.json:
      abort(400)
  if vector_handler.build_index(request.json['index']) == True:
    return make_response(True), 200
  return make_response(False), 500

@app.route(base_path + '/save', methods=['POST'])
def save_annoy_index():
  if not request.json:
      abort(400)
  if vector_handler.save_index_to_disk(request.json['index']) == True:
    return make_response(True), 200
  return make_response(False), 500

@app.route(base_path + '/load', methods=['POST'])
def load_annoy_index():
  if not request.json:
      abort(400)
  if vector_handler.load_index_from_disk(request.json['index'], request.json['dimensions']) == True:
    return make_response(True), 200
  return make_response(False), 500

def make_response(acknowledged):
  return jsonify({'acknowledged': acknowledged})
