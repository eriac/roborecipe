#!/usr/bin/python3
import pathlib
import glob
import os
import datetime
import xml.etree.ElementTree as ET
import shutil

class PackagePathItem:
    def __init__(self, pkg_name, pkg_base_path):
        self.pkg_name = pkg_name
        self.pkg_base_path = pkg_base_path
    def __str__(self):
        return '(' + self.pkg_name + ', ' + self.pkg_base_path + ')'

class ComponentPathItem:
    def __init__(self, pkg_name, pkg_base_path, comp_file_path, m_datetime):
        self.pkg_name = pkg_name
        self.pkg_base_path = pkg_base_path
        self.comp_file_path = comp_file_path
        self.m_datetime = m_datetime
    def __str__(self):
        return '(' + self.pkg_name + ', ' + self.pkg_base_path + ', ' + self.comp_file_path + ', ' + str(self.m_datetime) + ')'

class DirectoryLoader:
    def __init__(self, root_path):
        target_directory = pathlib.Path(root_path).resolve()
        self.pkg_list = self._get_valid_package_list(target_directory)

        self.package_component_list = []
        for p in self.pkg_list:
            for c in self._get_component_list(p[1]):
                m_data_time = datetime.datetime.fromtimestamp(os.path.getmtime(c))
                self.package_component_list.append(ComponentPathItem(p[0], p[1], c, m_data_time))

    def get_component_path_list(self):
        return self.package_component_list

    def get_pkg_list(self):
        pkg_path_list = []
        for p in self.pkg_list:
            pkg_path_list.append(PackagePathItem(p[0], p[1]))
        return pkg_path_list

    def copy_resouces_dir(self, pkg_set, output_dir):
        for p in self.pkg_list:
            if p[0] in pkg_set:
                source_dir = p[1] + '/resources'
                target_dir = str(output_dir) + '/' + p[0] + '/resources'
                if os.path.isdir(source_dir):
                    print('copy ' + source_dir)
                    shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
            print('skip copy resouces: ' + p[0])

    def _get_valid_package_list(self, target_directory):
        package_path_list = glob.glob(str(target_directory) + '/*/package.xml', recursive = True)

        output_list = []
        for package_path in package_path_list:
            name = self._get_package_name(package_path)
            if name is not None:
                package_base_dir = str(pathlib.Path(package_path).parent)
                output_list.append([name, package_base_dir])
        return output_list

    def _get_package_name(self, package_path):
        tree = ET.parse(package_path)
        elem = tree.getroot().find("name")
        if elem is not None:
            return elem.text
        RED = '\033[31m'
        END = '\033[0m'
        print(RED + package_path + ': <name> not found' + END)
        return None

    def _get_component_list(self, pkg_path):
        return glob.glob(pkg_path + '/roborecipe/*.yaml', recursive = True)

    def _get_modify_datetime(self, dir_path):
        file_list = glob.glob(dir_path + '/**/*', recursive = True)
        m_datetime_list = []
        for file_path in file_list:
            m_data_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            m_datetime_list.append(m_data_time)
        return max(m_datetime_list)

class OutputDirectoryDatetimeItem:
    def __init__(self, pkg_name, image_m):
        self.pkg_name = pkg_name
        self.image_m = image_m

class OutputDirectorySearch:
    def __init__(self, output_base_dir):
        pkg_list = glob.glob(str(output_base_dir) + '/*/', recursive = True)
        self.image_datetime_dict = {}
        for pkg_path in pkg_list:
            m_datetime = self._get_m_datetime(pkg_path + 'images/')
            if m_datetime is not None:
                self.image_datetime_dict[pathlib.Path(pkg_path).name] = m_datetime

    def need_update_image(self, pkg_name, source_datetime):
        # print('######## ' + pkg_name + ' #########')
        if pkg_name not in self.image_datetime_dict:
            # print('not in list')
            return True
        else:
            # print('check ' + str(self.image_datetime_dict[pkg_name]) + ' < ' + str(source_datetime))
            return self.image_datetime_dict[pkg_name] < source_datetime

    def _get_m_datetime(self, dir_path):
        file_list = glob.glob(dir_path + '/**/*', recursive = True)
        m_datetime_list = []
        for file_path in file_list:
            m_data_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            m_datetime_list.append(m_data_time)
        if file_list:
            return max(m_datetime_list)
        else:
            return None

if __name__ == '__main__':
    dl = DirectoryLoader('../sample')
    for component in dl.get_component_path_list(): 
        print(component)

    out_ds = OutputDirectorySearch('../out')
    print(out_ds.need_update_image('screw_m3', datetime.datetime(2023, 4, 1)))
    print(out_ds.need_update_image('screw_m3', datetime.datetime(2023, 10, 1)))
    print(out_ds.need_update_image('screw_m4', datetime.datetime(2023, 4, 1)))

    dl.copy_resouces_dir(set(['screw_m3','sample_project']), '../out')