from annoy import AnnoyIndex
from api.VectorEntry import VectorEntry
from api.VectorResultEntry import VectorResultEntry

index = AnnoyIndex(300)

class VectorHandler():

  def add_vector(self, vector_entry):
    index.add_item(vector_entry.id, vector_entry.vector)
    return vector_entry

  def build_index(self):
    index.build(-1)

  def get_nns_by_vector(self, query_vector):
    result = index.get_nns_by_vector(query_vector, 100, -1, True)
    ids = result[0]
    distances = result[1]
    vector_entries = []
    for i in range(0, len(ids)):
      vector_entries.append({'id': ids[i], 'distance': distances[i]})
    return vector_entries
