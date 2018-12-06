import sys, json, logging
from annoy import AnnoyIndex
from api.VectorEntry import VectorEntry
from api.VectorResultEntry import VectorResultEntry
from api.Index import Index
from core.VectorHandler import VectorHandler
from flask import Flask, Response, abort, request, jsonify
from flask_restplus import Resource, Api

app = Flask(__name__)
vector_handler = VectorHandler()
api = Api(app, version='1.0', title='Annoy API',
    description='Spotify Annoy REST API',)

@api.route('/<string:index_id>')
class CreateIndex(Resource):

  def put(self, index_id):
    return self.create_index(index_id)

  def post(self, index_id):
    return self.create_index(index_id)

  def delete(self, index_id):
    if vector_handler.delete_index(index_id) == True:
      return make_response(True), 200
    else:
      return make_response(False), 500

  def create_index(self, index_id):
    if request.json:
      index = Index(index_id, request.json['dimensions'], request.json['metric'])
    else:
      index = Index(index_id)
    if vector_handler.create_index(index) == True:
      return make_response(True), 201
    return make_response(False), 500

@api.route('/<string:index_id>/_build')
class BuildIndex(Resource):
  def post(self, index_id):
    valid_response_condition(request)
    if vector_handler.build_index(index_id, request.json['n_trees']) == True:
      return make_response(True), 200
    return make_response(False), 500

@api.route('/<string:index_id>/_save')
class SaveIndex(Resource):
  def post(self, index_id):
    if vector_handler.save_index_to_disk(index_id) == True:
      return make_response(True), 200
    return make_response(False), 500

@api.route('/<string:index_id>/_load')
class LoadIndex(Resource):
  def post(self, index_id):
    valid_response_condition(request)
    if vector_handler.load_index_from_disk(index_id, request.json['dimensions']) == True:
      return make_response(True), 200
    return make_response(False), 500

@api.route('/<string:index_id>/_unload')
class UnloadIndex(Resource):
  def post(self, index_id):
    if vector_handler.unload_index(index_id) == True:
      return make_response(True), 200
    return make_response(False), 500

@api.route('/<string:index_id>/<int:doc_id>')
class AddDocumentToIndex(Resource):
  def post(self, index_id, doc_id):
    valid_response_condition(request)
    document = VectorEntry(index_id, doc_id, request.json['vector'])
    if vector_handler.add_vector(document) == True:
      return make_response(True), 201
    return make_response(False), 500

@api.route('/<string:index_id>/_vector')
class FindApproximateNearestNeighborsByVector(Resource):
  def post(self, index_id):
    valid_response_condition(request)
    results = list(map(lambda x: x.get_as_json(), vector_handler.get_nns_by_vector(index_id, request.json['vector'], request.json['size'], request.json['search_k'])))
    return results, 200

@api.route('/<string:index_id>/_item')
class FindApproximateNearestNeighborsByItem(Resource):
  def post(self, index_id):
    valid_response_condition(request)
    results = list(map(lambda x: x.get_as_json(), vector_handler.get_nns_by_item(index_id, request.json['id'], request.json['size'], request.json['search_k'])))
    return results, 200

def valid_response_condition(request):
  if not request.json:
    return make_response(False), 500

def make_response(acknowledged):
  return {'acknowledged': acknowledged}
