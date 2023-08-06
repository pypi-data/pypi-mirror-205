# -*- coding: utf-8 -*-

"""
This is the implementation for the detail sphere_base
"""

from sphere_base.sphere.sphere import Sphere
from sphere_base.sphere_overlay.sov_conf import *
from sphere_base.sphere_overlay.sphere_nodes.edge_sphere_item import SphereEdge
import random
from sphere_base.utils import dump_exception


class OverlaySphere(Sphere):
    Edge_class = SphereEdge

    def __init__(self, universe, position=None, texture_id=None):
        super().__init__(universe, position, texture_id)

        self.set_node_class_selector(self.get_node_class_from_data)
        self._close_event_listeners = []
        self.billboard_id = random.randint(30, 31)

    def get_model(self):
        self.model = self.uv.models.get_model('holo_sphere')

    def get_node_class_from_data(self, data):
        if 'op_code' not in data:
            return self.Node
        return get_class_from_type(data['op_code'], SPHERE_NODE_EDITOR)

    def create_new_node(self, node_type=0, mouse_ray_collision_point=None):
        node = None

        # calculate the cumulative angle based on the mouse position
        orientation = self.calc.find_angle(mouse_ray_collision_point, self.orientation)

        try:

            if node_type:
                node = get_class_from_type(node_type, SPHERE_NODE_EDITOR)(self, orientation_offset=orientation)
            else:
                node = self.Node(self, orientation)

        except Exception as e:
            dump_exception(e)

        self.history.store_history("node created", True)
        return node

    # def draw(self):
    #     """
    #     Render the sphere_base and all the items on it.
    #     """
    #
    #     if self.animation != 0:
    #         self.rotate_sphere(self.animation)
    #
    #     self.model.draw(self, texture_id=self.texture_id, color=self.color)
    #
    #     for item in self.items:
    #         if item.type == "node":
    #             item.draw()
    #         elif item.type == "edge":
    #             item.draw()
    #
    #     if self.edge_drag.dragging:
    #         self.edge_drag.draw()
