#!/usr/bin/env python
import pickle
import sys
import os
import pprint
import qt
MXCUBE_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
sys.path.insert(0, MXCUBE_ROOT)
app = qt.QApplication([])

from BlissFramework.Utils import PropertyBag
#from BlissFramework import Configuration

if __name__ == '__main__':
  if len(sys.argv) > 2:
    try:
      cfg = open(sys.argv[2], 'r')
      gui = open(sys.argv[1], 'r')
    except Exception as e:
      print('Could not open file', e)
  else:
    print('Usage: %s <.gui file> <cfg file> > new .gui file' % sys.argv[0])

  gui_config = eval(gui.read())
  #config_obj = Configuration.Configuration()
  #config_obj.load(gui_config)
  cfg = eval(cfg.read())

  def find(item_name, config=gui_config):
    for x in config:
      if x["name"]==item_name:
        return x, pickle.loads(x["properties"])
      cfg, item = find(item_name, x["children"]) 
      if item:
        return cfg,item
    return None, None

  for item in cfg:
    for item_name, item_cfg in item.items():
      # look for property object for item in .gui file
      gui_cfg_item, gui_item = find(item_name)  

      if gui_item is None:
        sys.stderr.write('No item'+item_name+'found in .gui file'+sys.argv[1]+'\n')
      else:
        # assign properties
        sys.stderr.write('[%s]\n' % item_name)
        for prop_name, prop_value in item_cfg.items():
          sys.stderr.write('  -> setting value for property %s to %s\n' %(prop_name,prop_value))
          try:
            gui_item.properties[prop_name].setValue(prop_value)
          except KeyError:
            pass
        # re-dump PropertyBag
        gui_cfg_item["properties"]=pickle.dumps(gui_item)

  print(repr(gui_config))
