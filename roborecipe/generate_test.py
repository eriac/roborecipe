#!/usr/bin/python3
from roborecipe.DirectoryLoader import * 
from roborecipe.AssemblyAnalyzer import * 
from roborecipe.TopPageGenerator import * 
from roborecipe.PartsPageGenerator import *
from roborecipe.PartImageGenerator import *

if __name__ == '__main__':
    dl = DirectoryLoader('../sample')
    out_ds = OutputDirectorySearch('../out')
    component_path_list = []
    for component in dl.get_component_path_list(): 
        component_path_list.append(component)

    cll = ComponentListLoader()
    for path_item in component_path_list:
        cll.load(path_item)

    top_assembly_id = ComponentIdentifier('sample_project', 'main_asm')
    ata = AssemblyTreeAnalyzer(cll, top_assembly_id)
    ada = AssemblyDependencyAnalyzer(cll, top_assembly_id)

    # top page
    tg = TopPageGenerator(top_assembly_id, ata, ada)
    tg.write('../out')

    # package copy
    used_pkg_name_set = ada.get_pkg_name_set()
    dl.copy_resouces_dir(used_pkg_name_set, '../out')

    # part page (screw)
    for item in ata.get_quantity_list(ComponentCategoryEnum.SCREW):
        # image
        mpig = MechanicalPartsImageGenerator(item.comp)
        if out_ds.need_update_image(mpig.get_pkg_name(), mpig.get_m_datetime()):
            mpig.write('../out')
        else:
            print('skip image')

        # html
        mpg = MechanicalPartsPageGenerator(item.comp)
        mpg.write('../out')

    # part page (laser_cut)
    for item in ata.get_quantity_list(ComponentCategoryEnum.LASER_CUT):
        # image
        mpig = MechanicalPartsImageGenerator(item.comp)
        if out_ds.need_update_image(mpig.get_pkg_name(), mpig.get_m_datetime()):
            mpig.write('../out')
        else:
            print('skip image')

        # html
        mpg = ProcessPartsPageGenerator(item.comp)
        mpg.write('../out')

    # part page (assembly)
    for item in ada.get_list():
        # image
        ata = AssemblyTreeAnalyzer(cll, item.comp.id)
        aig = AssemblyImageGenerator(item.comp, ata.get_position_list(), ata.get_step_view_list())
        asm_m_datetime = AssemblyDependencyAnalyzer(cll, item.comp.id).get_m_datetime()

        if out_ds.need_update_image(aig.get_pkg_name(), asm_m_datetime):
            aig.write('../out')
        else:
            print('skip image')

        # html
        apg = AssemblyPageGenerator(item.comp)
        apg.write('../out')