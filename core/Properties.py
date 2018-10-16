import os

class Properties():

  def get_data_dir(self):
    if 'DATA_DIR' in os.environ:
      return os.environ['DATA_DIR']
    else:
      return '/tmp'
