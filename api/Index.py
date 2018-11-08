class Index(object):

  def __init__(self, index_id, dimensions=None, metric=None):
    self.index_id = index_id
    if dimensions is None:
      self.dimensions = 300
    else:
      self.dimensions = dimensions
    if metric is None:
      self.metric = 'angular'
    else:
      self.metric = metric
