from annoy import AnnoyIndex
from api.VectorEntry import VectorEntry
from api.Index import Index
from api.VectorResultEntry import VectorResultEntry
from core.Properties import Properties

indices = {}
properties = Properties()

class VectorHandler():

  def list_indices(self):
    return indices.keys()

  def create_index(self, index):
    if indices and index.index_id in indices:
      return False
    annoy_index = AnnoyIndex(index.dimensions, metric=index.metric)
    indices[index.index_id] = annoy_index
    return True

  def delete_index(self, index):
    if index in indices: 
      del indices[index]
      return True
    else:
      return False

  def get_index_size(self, index_id):
    if index_id not in indices:
      return False
    index = indices[index_id]
    return index.get_n_items()

  def add_vector(self, vector_entry):
    if vector_entry.index not in indices:
      index = AnnoyIndex(len(vector_entry.vector))
      indices[vector_entry.index] = index
    index = indices[vector_entry.index]
    index.add_item(vector_entry.id, vector_entry.vector)
    return True

  def build_index(self, index_id, n_trees):
    if index_id not in indices:
      return False
    index = indices[index_id]
    index.build(n_trees)
    return True

  def get_nns_by_item(self, index_id, query_id, size, search_k):
    if index_id not in indices:
      return False
    index = indices[index_id]
    result = index.get_nns_by_item(query_id, size, search_k, True)
    return self.get_vector_result_entries_from_nns(result, index_id)

  def get_nns_by_vector(self, index_id, query_vector, size, search_k):
    if index_id not in indices:
      return False
    index = indices[index_id]
    result = index.get_nns_by_vector(query_vector, size, search_k, True)
    return self.get_vector_result_entries_from_nns(result, index_id)

  def get_vector_result_entries_from_nns(self, result, index_id):
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
    index.save(self._get_full_index_path(index_id))
    return True

  def unload_index(self, index_id):
    if index_id not in indices:
      return False
    index = indices[index_id]
    return index.unload()

  def load_index_from_disk(self, index_id, dimensions):
    index = AnnoyIndex(dimensions)
    index.load(self._get_full_index_path(index_id))
    indices[index_id] = index
    return True

  def _get_full_index_path(self, index_id):
    return properties.get_data_dir() + '/' + index_id + '.ann'
