import os
import importlib.util
_moduleList = {}
_modList = {}

def pages_view():
    _moduleList.clear()
    for root, dirs, __ in os.walk(r'./'):
        for dir in dirs:
            if dir == 'views':
                for filename in os.listdir('views'):
                    _file = os.path.join('views', filename)
                    if os.path.isfile(_file):
                        filename = filename.strip('.py')
                        if filename != '__init__':
                            _moduleList[filename] = importlib.util.spec_from_file_location(
                                filename, _file)
    return _moduleList

class WiewModel:
    def __init__(self) -> None:
        pass
    def route(self):
        pass
    def view(self):
        pass

def routing()->WiewModel:
    _modList.clear()
    for view in pages_view():
        page = pages_view().get(view).loader.load_module().View()
        route = page.route
        _modList[route] = page
    print('urls->', _modList)
    return _modList

if __name__ == '__main__':
    pass
