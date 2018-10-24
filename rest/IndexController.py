import sys, json, logging
from annoy import AnnoyIndex
from api.VectorEntry import VectorEntry
from api.VectorResultEntry import VectorResultEntry
from core.VectorHandler import VectorHandler
from flask import Flask, Response, abort, request, jsonify

app = Flask(__name__)
vector_handler = VectorHandler()
base_path = '/v1/annoy/index'

@app.route(base_path + '/list')
def list_indices():
  indices = list(vector_handler.list_indices())
  return jsonify({'indices': indices}), 200

@app.route(base_path + '/create', methods=['POST'])
def create_index():
  valid_response_condition(request)
  status = vector_handler.create_index(request.json['id'], request.json['dimensions'], request.json['metric'])
  if status == True:
    return make_response(True), 201
  return make_response(False), 201

@app.route(base_path + '/size', methods=['POST'])
def list_index_size():
  valid_response_condition(request)
  size = vector_handler.get_index_size(request.json['id'])
  return jsonify({'size': size})

@app.route(base_path + '/add', methods=['POST'])
def add_vector():
  valid_response_condition(request)
  vector = VectorEntry(request.json['index'], request.json['id'], request.json['vector'])
  if vector_handler.add_vector(vector) == True:
    return make_response(True), 201
  return make_response(False), 500

@app.route(base_path + '/nns/vector', methods=['POST'])
def get_nns_by_vector():
  valid_response_condition(request)
  results = list(map(lambda x: x.get_as_json(), vector_handler.get_nns_by_vector(request.json['index'], request.json['vector'], request.json['size'], request.json['search_k'])))
  return jsonify(results), 200

@app.route(base_path + '/nns/item', methods=['POST'])
def get_nns_by_item():
  valid_response_condition(request)
  results = list(map(lambda x: x.get_as_json(), vector_handler.get_nns_by_item(request.json['index'], request.json['id'], request.json['size'], request.json['search_k'])))
  return jsonify(results), 200

@app.route(base_path + '/build', methods=['POST'])
def build_annoy_index():
  valid_response_condition(request)
  if vector_handler.build_index(request.json['index'], request.json['n_trees']) == True:
    return make_response(True), 200
  return make_response(False), 500

@app.route(base_path + '/save', methods=['POST'])
def save_annoy_index():
  valid_response_condition(request)
  if vector_handler.save_index_to_disk(request.json['index']) == True:
    return make_response(True), 200
  return make_response(False), 500

@app.route(base_path + '/load', methods=['POST'])
def load_annoy_index():
  valid_response_condition(request)
  if vector_handler.load_index_from_disk(request.json['index'], request.json['dimensions']) == True:
    return make_response(True), 200
  return make_response(False), 500

@app.route(base_path + '/unload', methods=['POST'])
def unload_annoy_index():
  valid_response_condition(request)
  if vector_handler.unload_index(request.json['index']) == True:
    return make_response(True), 200
  return make_response(False), 500

@app.errorhandler(404)
def page_not_found(e):
  app.logger.error('Error for request: ' + str(e))
  return jsonify(error=404, text=str(e)), 404

@app.errorhandler(400)
def page_not_found(e):
  app.logger.error('Error for request: ' + str(e))
  return jsonify(error=400, text=str(e)), 400

def valid_response_condition(request):
  if not request.json:
      abort(400)

def make_response(acknowledged):
  return jsonify({'acknowledged': acknowledged})
