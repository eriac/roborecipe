#!/usr/bin/python3
import pathlib
import glob

class DirectorySearch:
    def __init__(self, root_path):
        target_directory = pathlib.Path(root_path).resolve()
        self.pkg_list = self._get_package_list(target_directory)

        self.component_list = []
        for p in self.pkg_list:
            for c in self._get_component_list(p):
                self.component_list.append([p,c])

    def getComponentPathPairList(self):
        return self.component_list

    def getPackagePathList(self):
        return self.pkg_list

    def _get_package_list(self, target_directory):
        return glob.glob(str(target_directory) + '/*/package.xml', recursive = True)

    def _get_component_list(self, pkg_path):
        pkg_dir = pathlib.Path(pkg_path+"/..").resolve()
        return glob.glob(str(pkg_dir) + '/*/*.roborecipe', recursive = True)

if __name__ == '__main__':
    ds = DirectorySearch('../sample')
    for component in ds.getComponentPathPairList(): 
        print(component)
