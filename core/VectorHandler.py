from annoy import AnnoyIndex
from api.VectorEntry import VectorEntry
from api.VectorResultEntry import VectorResultEntry

indices = {}

class VectorHandler():

  def list_indices(self):
    return indices.keys()

  def create_index(self, iid, dimensions):
    if indices and iid in indices:
      return False
    index = AnnoyIndex(dimensions)
    indices[iid] = index
    return True

  def add_vector(self, vector_entry):
    if vector_entry.index not in indices:
      print(indices[vector_entry.index])
      return False
    index = indices[vector_entry.index]
    index.add_item(vector_entry.id, vector_entry.vector)
    return True

  def build_index(self, index_id):
    if index_id not in indices:
      return False
    index = indices[index_id]
    index.build(-1)
    return True

  def get_nns_by_item(self, index_id, query_id, size):
    if index_id not in indices:
      return False
    index = indices[index_id]
    result = index.get_nns_by_item(query_id, size, -1, True)
    return VectorHandler.get_vector_result_entries_from_nns(result, index_id)

  def get_nns_by_vector(self, index_id, query_vector, size):
    if index_id not in indices:
      return False
    index = indices[index_id]
    result = index.get_nns_by_vector(query_vector, size, -1, True)
    return VectorHandler.get_vector_result_entries_from_nns(result, index_id)

  def get_vector_result_entries_from_nns(result, index_id):
    ids = result[0]
    distances = result[1]
    vector_entries = []
    for i in range(0, len(ids)):
      vector_result = VectorResultEntry(index_id, ids[i], distances[i])
      vector_entries.append(vector_result)
    return vector_entries

  def save_index_to_disk(self, index_id):
    if index_id not in indices:
      return False
    index = indices[index_id]
    index.save('/tmp/' + index_id) # read base path from property?
    return True

  def load_index_from_disk(self, index_id, dimensions):
    index = AnnoyIndex(dimensions)
    index.load('/tmp/' + index_id)
    indices[index_id] = index
    return True
