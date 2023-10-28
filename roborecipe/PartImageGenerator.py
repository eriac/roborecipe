from panda3d_viewer import Viewer, ViewerConfig
from roborecipe.data_type import *
import imageio
import datetime
import os
import pathlib
import shutil
from panda3d.core import BamCache

def clear_panda3d_cashe():
    cashe_dir = BamCache.getGlobalPtr().getRoot()
    print("remove panda3d chashe " + str(cashe_dir))
    shutil.rmtree(cashe_dir)

class MechanicalPartsImageGenerator:
    def __init__(self, comp):
        self.comp = comp

    def get_pkg_name(self):
        return self.comp.id.pkg_name

    def get_m_datetime(self):
        return self.comp.m_datetime

    def write(self, output_base_dir):
        config = ViewerConfig()
        config.set_window_size(800, 800)
        config.enable_shadow(True)
        config.show_axes(False)
        config.show_grid(False)

        viewer = Viewer(window_type='offscreen', config=config)
        viewer.append_group('root')

        mm_to_unit = 0.01
        viewer.append_mesh('root', 'mesh1', self.comp.rigit_body.mesh_filepath, scale={mm_to_unit, mm_to_unit, mm_to_unit})
        viewer.set_material('root', 'mesh1', color_rgba=(0.5, 0.5, 0.0, 1))
 
        viewer.move_nodes('root', {'mesh1': ((0, 0, 0), (1, 0, 0, 0))})

        body_view = self.comp.rigit_body.view
        point_from = (body_view.from_point.x * mm_to_unit, body_view.from_point.y * mm_to_unit, body_view.from_point.z * mm_to_unit)
        point_to = (body_view.to_point.x * mm_to_unit, body_view.to_point.y * mm_to_unit, body_view.to_point.z * mm_to_unit)

        viewer.reset_camera(pos=point_from, look_at=point_to)
        image = viewer.get_screenshot(requested_format='RGB')
        viewer.destroy()

        output_dir = str(output_base_dir) + '/' + self.comp.id.pkg_name + '/images'
        os.makedirs(output_dir, exist_ok = True)

        filepath = output_dir + '/' + self.comp.id.type_name + '_rigid_body.png'
        print('write ' + filepath)
        writer = imageio.get_writer(filepath, mode='I')
        writer.append_data(image)

class AssemblyImageGenerator:
    def __init__(self, comp, item_list, step_view_list):
        self.comp = comp
        self.item_list = item_list
        self.step_view_list = step_view_list

    def get_pkg_name(self):
        return self.comp.id.pkg_name

    def write(self, output_base_dir):
        config = ViewerConfig()
        config.set_window_size(800, 800)
        config.enable_shadow(True)
        config.show_axes(False)
        config.show_grid(False)
        viewer = Viewer(window_type='offscreen', config=config)
        viewer.enable_lights(False)

        #### change lights ####
        viewer._app._lights = [
            viewer._app._make_light_ambient((0.2, 0.2, 0.2)),
            viewer._app._make_light_direct(
                1, (0.3, 0.4, 0.4), pos=(8.0, 8.0, 10.0)),
            viewer._app._make_light_direct(
                2, (0.4, 0.3, 0.4), pos=(8.0, -8.0, 10.0)),
            viewer._app._make_light_direct(
                3, (0.4, 0.4, 0.3), pos=(-8.0, 8.0, 10.0)),
            viewer._app._make_light_direct(
                4, (0.3, 0.3, 0.4), pos=(-8.0, -8.0, 10.0)),
            viewer._app._make_light_direct(
                5, (0.8, 0.8, 0.8), pos=(0.0, 0.0, -10.0)),
        ]
        viewer._app._lights_mask = [True, True, True, True, True, True]
        viewer.enable_lights(True)
        #### end change lights ####

        viewer.append_group('root')
        mm_to_unit = 0.01
        max_step = self._get_max_step()

        self.image_list = []
        for step_no in range(max_step + 1):
            # add object
            for obj_no, item in enumerate(self.item_list):
                mesh_name = 'mesh' + str(obj_no)
                if item.step_no == step_no:
                    # print(mesh_name, item.comp.rigit_body.mesh_filepath)
                    viewer.append_mesh('root', mesh_name, item.comp.rigit_body.mesh_filepath, scale={mm_to_unit, mm_to_unit, mm_to_unit})

            #  set color
            for obj_no, item in enumerate(self.item_list):
                mesh_name = 'mesh' + str(obj_no)
                if item.step_no == step_no:
                    color_rgba = item.comp.category.get_color(True)
                    viewer.set_material('root', mesh_name, color_rgba=color_rgba)
                elif item.step_no < step_no:
                    color_rgba = item.comp.category.get_color(False)
                    viewer.set_material('root', mesh_name, color_rgba=color_rgba)

            # view
            for view_no, view in enumerate(self.step_view_list[step_no]):
                point_from = (view.from_point.x * mm_to_unit, view.from_point.y * mm_to_unit, view.from_point.z * mm_to_unit)
                point_to = (view.to_point.x * mm_to_unit, view.to_point.y * mm_to_unit, view.to_point.z * mm_to_unit)
                viewer.reset_camera(pos=point_from, look_at=point_to)

                image_list = []
                # set position & render
                move_size = 10
                for move_index in range(move_size + 1):
                    rate = 1.0 * (move_size - move_index) / move_size  
                    for obj_no, item in enumerate(self.item_list):
                        if item.step_no == step_no:
                            mesh_name = 'mesh' + str(obj_no)
                            pos = item.transform.position
                            rot = item.transform.rotation
                            move = item.move
                            pos_unit = ((pos.x + move.x * rate) * mm_to_unit, (pos.y + move.y * rate) * mm_to_unit, (pos.z + move.z * rate) * mm_to_unit)
                            rot_unit = (rot.w, rot.x, rot.y, rot.z)
                            viewer.move_nodes('root', {mesh_name: (pos_unit, rot_unit)})
                            # print(pos_unit, rot_unit)
                    image_list.append(viewer.get_screenshot(requested_format='RGB'))
                self.image_list.append([image_list, step_no, view_no])
        viewer.stop()

        image_dir = str(output_base_dir) + '/' + self.comp.id.pkg_name + '/images/'
        os.makedirs(image_dir, exist_ok = True)

        for image_set in self.image_list:
            image_list = image_set[0]
            step_no = image_set[1]
            view_no = image_set[2]

            gif_name = self.comp.id.type_name + '_' + str(step_no) + '_' + str(view_no) + '.gif'
            print('write image ' + image_dir + gif_name)

            last_image = image_list[-1].copy()
            for i in range(10):
                image_list.append(last_image)
            imageio.mimsave(image_dir + gif_name, image_list, duration = 200, loop = 0)

    def _get_max_step(self):
        def key_func(obj):
            return obj.step_no
        return max(self.item_list, key = key_func).step_no


if __name__ == '__main__':
    from roborecipe.AssemblyAnalyzer import *
    import os

    component_path_list = [
        ComponentPathItem('screw_m3', '/home/ubuntu/workspace/roborecipe/sample/screw_m3', '/home/ubuntu/workspace/roborecipe/sample/screw_m3/roborecipe/pan_10.yaml'),
        ComponentPathItem('screw_m3', '/home/ubuntu/workspace/roborecipe/sample/screw_m3', '/home/ubuntu/workspace/roborecipe/sample/screw_m3/roborecipe/hollow_spacer_20.yaml'),
        ComponentPathItem('sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project/roborecipe/bar_plate.yaml'),
        ComponentPathItem('sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project/roborecipe/base_plate.yaml'),
        ComponentPathItem('sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project/roborecipe/side_asm.yaml'),
        ComponentPathItem('sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project/roborecipe/main_asm.yaml'),
    ]
    cll = ComponentListLoader()
    for path_item in component_path_list:
        cll.load(path_item)



    # assembly images
    top_assmebly_id = ComponentIdentifier('sample_project', 'main_asm')

    ata = AssemblyTreeAnalyzer(cll, top_assmebly_id)
    for item in ata.get_position_list():
        print(item.comp.rigit_body.mesh_filepath)

    aig = AssemblyImageGenerator(ata.get_position_list(), ata.get_step_view_list())

    os.makedirs('../out/sample_project/images', exist_ok = True)
    aig.save_image('../out/sample_project/images/main_asm')
