#########
# This is a work in progress tool to generate "glue" between surfaces
# Code is roughly based on the Bullet Constraints addon

import bpy
import bmesh
import math

import subprocess
import sys

try:
    import shapely.geometry as sply
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "shapely", "-y", "--no-cache-dir"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "shapely", "--no-cache-dir"])
    import shapely.geometry as sply


import mathutils
from mathutils import Vector
# from bpy.props import *

bl_info = {
    "name": "Glue Tool",
    "author": "Connor",
    "version": (0, 0, 0, 1),
    "blender": (4, 3, 0),
    "location": "Properties",
    "description": "Tool to generate constraints.",
    "warning": "Work in progress",
    "wiki_url":
    "https://github.com/ConX164",
    "tracker_url":
    "https://github.com/ConX164",
    "category": "Object"}


class Bullet_Tools(bpy.types.Panel):
    bl_label = "Glue Tool"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'physics'

    def draw(self, context):
        layout = self.layout
        scene = context.window_manager.bullet_tool

        # object = context.object
        # if object.type == 'MESH' or 'EMPTY':

        row = layout.row()
        row.operator("bullet.x_connect", icon="MOD_SKIN")
        #row.operator("bullet.intersect_area", icon="MOD_SKIN")

        """row = layout.row()
        row.prop(scene, "bullet_tool_neighbours")
        row.prop(scene, "bullet_tool_search_radius")"""

        # Show Object Settings
        """row = layout.row()
        row.prop(scene, "bullet_tool_show_obj")
        row.active = False
        if context.window_manager.bullet_tool.bullet_tool_show_obj is True:
            row.active = True
        row.prop(scene, "bullet_tool_friction")
        row.prop(scene, "bullet_tool_use_margin")

        row = layout.row()
        row.active = False
        if context.window_manager.bullet_tool.bullet_tool_show_obj is True:
            row.active = True
        row.prop(scene, "bullet_tool_bounciness")
        row.prop(scene, "bullet_tool_collmargin")"""

        # Show Constraint Settings
        row = layout.row()
        row.prop(scene, "bullet_tool_Constraint_type")
        # Show Break Options
        row = layout.row()
        row.prop(scene, "bullet_tool_breakable")
        row.prop(scene, "bullet_tool_break_threshold")
        row.prop(scene, "bullet_tool_pressure")

        # Config
        row = layout.row()
        row.prop(scene, "bullet_tool_max_angle")
        row.prop(scene, "bullet_tool_max_distance")
        row.prop(scene, "bullet_tool_min_area")
        """"# Show Iterations Options
        row = layout.row()
        row.prop(scene, "bullet_tool_show_it")
        row.active = False
        if context.window_manager.bullet_tool.bullet_tool_show_it is True:
            row.active = True
        row.prop(scene, "bullet_tool_over_iteration")
        row.prop(scene, "bullet_tool_iteration")"""
        # For Constraint Types

        """"# Show Iterations Options
        row = layout.row()
        row.prop(scene, "bullet_tool_show_lim")
        ac = False
        row.active = False
        if context.window_manager.bullet_tool.bullet_tool_show_lim is True:
            ac = True
            row.active = True

        if (context.window_manager.bullet_tool.bullet_tool_Constraint_type
                == 'HINGE'):
            col = layout.column(align=True)
            col.active = False
            if ac is True:
                col.active = True
            col.label(text="Limits:")

            row = col.row()
            sub = row.row()
            sub.scale_x = 0.5
            sub.prop(scene, "bullet_tool_use_limit_ang_z", toggle=True)
            sub = row.row()
            sub.active = (context.window_manager.bullet_tool
                          .bullet_tool_use_limit_ang_z)
            sub.prop(scene, "bullet_tool_limit_ang_z_lower", text="Lower")
            sub.prop(scene, "bullet_tool_limit_ang_z_upper", text="Upper")

        elif (context.window_manager.bullet_tool.bullet_tool_Constraint_type
                == 'SLIDER'):
            col = layout.column(align=True)
            col.active = False
            if ac is True:
                col.active = True
            col.label(text="Limits:")

            row = col.row()
            sub = row.row()
            sub.scale_x = 0.5
            sub.prop(scene, "bullet_tool_use_limit_lin_x", text='X Axis',
                     toggle=True)
            sub = row.row()
            sub.active = (context.window_manager.bullet_tool
                          .bullet_tool_use_limit_ang_z)
            sub.prop(scene, "bullet_tool_limit_lin_x_lower", text="Lower")
            sub.prop(scene, "bullet_tool_limit_lin_x_upper", text="Upper")

        elif (context.window_manager.bullet_tool.bullet_tool_Constraint_type
              == 'PISTON'):
            col = layout.column(align=True)
            col.active = False
            if ac is True:
                col.active = True
            col.label(text="Limits:")

            row = col.row()
            sub = row.row()
            sub.scale_x = 0.5
            sub.prop(scene, "bullet_tool_use_limit_lin_x", toggle=True)
            sub = row.row()
            sub.active = (context.window_manager.bullet_tool
                          .bullet_tool_use_limit_lin_x)
            sub.prop(scene, "bullet_tool_limit_lin_x_lower", text="Lower")
            sub.prop(scene, "bullet_tool_limit_lin_x_upper", text="Upper")

            col = layout.column(align=True)
            col.active = False
            if ac is True:
                col.active = True

            row = col.row()
            sub = row.row()
            sub.scale_x = 0.5
            sub.prop(scene, "bullet_tool_use_limit_ang_x", toggle=True)
            sub = row.row()
            sub.active = (context.window_manager.bullet_tool
                          .bullet_tool_use_limit_ang_x)
            sub.prop(scene, "bullet_tool_limit_ang_x_lower", text="Lower")
            sub.prop(scene, "bullet_tool_limit_ang_x_upper", text="Upper")

        elif (context.window_manager.bullet_tool.bullet_tool_Constraint_type
                in {'GENERIC', 'GENERIC_SPRING'}):
            col = layout.column(align=True)
            col.active = False
            if ac is True:
                col.active = True
            col.label(text="Limits:")

            row = col.row()

            sub = row.row()
            sub.scale_x = 0.5
            sub.prop(scene, "bullet_tool_use_limit_lin_x", toggle=True)
            sub = row.row()
            sub.active = (context.window_manager.bullet_tool
                          .bullet_tool_use_limit_lin_x)
            sub.prop(scene, "bullet_tool_limit_lin_x_lower", text="Lower")
            sub.prop(scene, "bullet_tool_limit_lin_x_upper", text="Upper")

            row = col.row()
            sub = row.row()
            sub.scale_x = 0.5
            sub.prop(scene, "bullet_tool_use_limit_lin_y", toggle=True)
            sub = row.row()
            sub.active = (context.window_manager.bullet_tool
                          .bullet_tool_use_limit_lin_y)
            sub.prop(scene, "bullet_tool_limit_lin_y_lower", text="Lower")
            sub.prop(scene, "bullet_tool_limit_lin_y_upper", text="Upper")

            row = col.row()
            sub = row.row()
            sub.scale_x = 0.5
            sub.prop(scene, "bullet_tool_use_limit_lin_z", toggle=True)
            sub = row.row()
            sub.active = (context.window_manager.bullet_tool
                          .bullet_tool_use_limit_lin_z)
            sub.prop(scene, "bullet_tool_limit_lin_z_lower", text="Lower")
            sub.prop(scene, "bullet_tool_limit_lin_z_upper", text="Upper")

            col = layout.column(align=True)
            col.active = False
            if ac is True:
                col.active = True

            row = col.row()
            sub = row.row()
            sub.scale_x = 0.5
            sub.prop(scene, "bullet_tool_use_limit_ang_x", toggle=True)
            sub = row.row()
            sub.active = (context.window_manager.bullet_tool
                          .bullet_tool_use_limit_ang_x)
            sub.prop(scene, "bullet_tool_limit_ang_x_lower", text="Lower")
            sub.prop(scene, "bullet_tool_limit_ang_x_upper", text="Upper")

            row = col.row()
            sub = row.row()
            sub.scale_x = 0.5
            sub.prop(scene, "bullet_tool_use_limit_ang_y", toggle=True)
            sub = row.row()
            sub.active = (context.window_manager.bullet_tool
                          .bullet_tool_use_limit_ang_y)
            sub.prop(scene, "bullet_tool_limit_ang_y_lower", text="Lower")
            sub.prop(scene, "bullet_tool_limit_ang_y_upper", text="Upper")

            row = col.row()
            sub = row.row()
            sub.scale_x = 0.5
            sub.prop(scene, "bullet_tool_use_limit_ang_z", toggle=True)
            sub = row.row()
            sub.active = (context.window_manager.bullet_tool
                          .bullet_tool_use_limit_ang_z)
            sub.prop(scene, "bullet_tool_limit_ang_z_lower", text="Lower")
            sub.prop(scene, "bullet_tool_limit_ang_z_upper", text="Upper")

            if (context.window_manager.bullet_tool.bullet_tool_Constraint_type
                    == 'GENERIC_SPRING'):
                col = layout.column(align=True)
                col.active = False
                if ac is True:
                    col.active = True
                col.label(text="Springs:")

                row = col.row()
                sub = row.row()
                sub.scale_x = 0.1
                sub.prop(scene, "bullet_tool_use_spring_x", toggle=True,
                         text="X")
                sub = row.row()
                sub.active = (context.window_manager.bullet_tool
                              .bullet_tool_use_spring_x)
                sub.prop(scene, "bullet_tool_spring_stiffness_x")
                sub.prop(scene, "bullet_tool_spring_damping_x")

                row = col.row()
                sub = row.row()
                sub.scale_x = 0.1
                sub.prop(scene, "bullet_tool_use_spring_y", toggle=True,
                         text="Y")
                sub = row.row()
                sub.active = (context.window_manager.bullet_tool
                              .bullet_tool_use_spring_y)
                sub.prop(scene, "bullet_tool_spring_stiffness_y")
                sub.prop(scene, "bullet_tool_spring_damping_y")

                row = col.row()
                sub = row.row()
                sub.scale_x = 0.1
                sub.prop(scene, "bullet_tool_use_spring_z", toggle=True,
                         text="Z")
                sub = row.row()
                sub.active = (context.window_manager.bullet_tool
                              .bullet_tool_use_spring_z)
                sub.prop(scene, "bullet_tool_spring_stiffness_z")
                sub.prop(scene, "bullet_tool_spring_damping_z")"""

        row = layout.row()
        row.operator("bullet.update", icon="FILE_REFRESH")
        row.prop(scene, "bullet_tool_mult")

        row = layout.row()
        row.operator("bullet.simplify", icon="MOD_DECIM")

        row = layout.row()
        row.prop(scene, "bullet_tool_max_merge_angle")
        row.prop(scene, "bullet_tool_clean_verts")
        row.prop(scene, "bullet_tool_edge_angle")

        row = layout.row()
        row.operator("bullet.remove_constraints", icon="X")


# Add Constraints for Bullet Viewport Branch
def constraint_empty(loc, ob1, ob2, empties_collection, area):
    empty_name = "Glue constraint " + ob1.name + " to " + ob2.name
    empty = bpy.data.objects.new(empty_name, None)
    empty.location = loc
    bpy.data.collections[empties_collection.name].objects.link(empty)
    bpy.context.view_layer.objects.active = empty

    empty.empty_display_size = 0.2
    bpy.ops.rigidbody.constraint_add(type=str(bpy.context.window_manager.bullet_tool.bullet_tool_Constraint_type))
    empty.rigid_body_constraint.object1 = ob1
    empty.rigid_body_constraint.object2 = ob2
    empty.rigid_body_constraint.use_breaking = (bpy.context.window_manager.bullet_tool.bullet_tool_breakable)
    empty.rigid_body_constraint.disable_collisions = False
    empty.rigid_body_constraint.breaking_threshold = area
    empty.constraints.new(type='CHILD_OF').target = ob1

    # Keep a record of which empty is connected to which objects, to allow the
    # user to select objects and delete the conected empties. Use a dictionary
    # so each object can store the names of multiple empties.
    if "empties" not in ob1:
        ob1["empties"] = {"0": empty_name}
    else:
        empties_dic = ob1["empties"]
        index = len(empties_dic)
        empties_dic[str(index)] = empty_name

    if "empties" not in ob2:
        ob2["empties"] = {"0": empty_name}
    else:
        empties_dic = ob2["empties"]
        index = len(empties_dic)
        empties_dic[str(index)] = empty_name

    update(bpy.context.selected_objects)  # Check This


# Grease Pencil function

# Restore selection and active object
def restore_active_and_sel(ob, objs):
    bpy.ops.object.select_all(action='DESELECT')

    for obj in objs:
        if not (obj is None):
            obj.select_set(state=True)

    if not (ob is None):
        bpy.context.view_layer.objects.active = ob
    # ob.select_set(state=True)


# Restore selection without an active object
def restore_sel(objs):
    bpy.ops.object.select_all(action='DESELECT')

    for obj in objs:
        if not (obj is None):
            obj.select_set(state=True)


# Create Dictionary of Bounding Spheres
def spheres(objs):
    sphereDict = {}
    for obj in objs:
        maxRadius = 0
        for vertex in obj.data.vertices:
            radius = vertex.co.length
            if radius > maxRadius:
                maxRadius = radius
        sphereDict[obj] = maxRadius
    return sphereDict


# Check and glue surfaces
def glue(obj1, obj2, collection, temp, bounds, wm):
    if (obj1.matrix_world.translation - obj2.matrix_world.translation).length <= (bounds[obj1] + bounds[obj2]):
        mesh1 = obj1.data
        mesh2 = obj2.data
        pairs = []
        angleThreshold = math.cos(math.radians(wm.bullet_tool.bullet_tool_max_angle))

        # Detect Alignment
        for face1 in mesh1.polygons:
            for face2 in mesh2.polygons:
                if abs((obj2.matrix_world.to_3x3() @ face2.normal).normalized().dot(
                        (obj1.matrix_world.to_3x3() @ face1.normal).normalized())) >= angleThreshold:
                    n = obj1.matrix_world.to_3x3() @ face1.normal
                    distance = abs(((obj1.matrix_world @ mesh1.vertices[face1.vertices[0]].co) - (
                                obj2.matrix_world @ mesh2.vertices[face2.vertices[0]].co)).dot(n) / math.sqrt(n.dot(n)))
                    if distance <= wm.bullet_tool.bullet_tool_max_distance:
                        pairs.append((face1, face2))

        intersectCenter = mathutils.Vector((0, 0, 0))
        # Flatten and Area Calculation
        for pair in pairs:
            face1, face2 = pair
            f1Norm = obj1.matrix_world.to_3x3() @ face1.normal
            v1 = f1Norm.orthogonal().normalized()
            v2 = f1Norm.normalized().cross(v1)
            origin = obj1.matrix_world @ mesh1.vertices[face1.vertices[0]].co

            flat1 = []
            flat2 = []

            for vertex in face1.vertices:
                offsetVertex = (obj1.matrix_world @ mesh1.vertices[vertex].co) - origin
                a = offsetVertex.project(v1)
                b = offsetVertex.project(v2)
                flat1.append((a.length * projectSign(a, v1), b.length * projectSign(b, v2)))
            for vertex in face2.vertices:
                offsetVertex = (obj2.matrix_world @ mesh2.vertices[vertex].co) - origin
                a = offsetVertex.project(v1)
                b = offsetVertex.project(v2)
                flat2.append((a.length * projectSign(a, v1), b.length * projectSign(b, v2)))

            poly1 = sply.Polygon(flat1)
            poly2 = sply.Polygon(flat2)

            intersectPoly = sply.Polygon.intersection(poly1, poly2)
            intersectArea = intersectPoly.area
            overlapPercent = intersectArea / min(poly1.area, poly2.area)

            # self.report({'INFO'}, f"{poly1} :::: {list(face1.vertices)}")
            if overlapPercent >= wm.bullet_tool.bullet_tool_min_area:
                intersectCenter = origin + v1 * intersectPoly.centroid.x + v2 * intersectPoly.centroid.y
                if wm.bullet_tool.bullet_tool_pressure:
                    constraint_empty(intersectCenter, obj1, obj2, collection,
                                     wm.bullet_tool.bullet_tool_break_threshold * intersectArea)
                else:
                    constraint_empty(intersectCenter, obj1, obj2, collection,
                                     wm.bullet_tool.bullet_tool_break_threshold)
                temp.report({'INFO'}, f"{intersectCenter}")


def rewrap(inList, index):
    newList = []
    for i in range(index - len(inList), index):
        newList.append(inList[i])
    return newList


def mergeLists(list1, list2):
    newList = []
    d1 = 0
    joined = False
    for i in range(0, len(list1)):
        if d1 > 0:
            d1 -= 1
            continue
        for j in range(0, len(list2)):
            if (list1[i] == list2[j]) and joined:
                return []
            if (list1[i - 1] == list2[j]) and (list1[i] == list2[j - 1]):
                listA = rewrap(list1, i)
                listB = rewrap(list2, j)
                listBr = listB[:]
                listBr.reverse()
                for c in range(1, min(len(listA), len(listB))):
                    if listA[c] != listBr[c]:
                        d1 = c - 1
                        break
                newList.extend(listA[d1:])
                newList.extend(listB[1:-1 - d1])
                joined = True
                break

            elif (list1[i - 1] == list2[j - 1]) and (list1[i] == list2[j]):
                listA = rewrap(list1, i)
                listB = rewrap(list2, j)
                listB.reverse()
                listBr = listB[:]
                listBr.reverse()
                for c in range(1, min(len(listA), len(listB))):
                    if listA[c] != listBr[c]:
                        d1 = c - 1
                        break
                newList.extend(listA[d1:])
                newList.extend(listB[1:-1 - d1])
                joined = True
                break
    return newList


def mergeGroups(value1, value2, groupDict, data):
    data[groupDict[value1]].extend(data[groupDict[value2]])
    tempIndex = groupDict[value2]
    for key in data[groupDict[value2]]:
        groupDict[key] = groupDict[value1]
    data.pop(tempIndex)


def group(value, key, groupDict, data, count):
    if key in groupDict:
        if value not in groupDict:
            groupDict[value] = groupDict[key]
            data[groupDict[key]].append(value)
        elif groupDict[value] != groupDict[key]:
            mergeGroups(value, key, groupDict, data)
    elif value in groupDict:
        groupDict[key] = groupDict[value]
        data[groupDict[value]].append(key)
    else:
        groupDict[key] = count
        groupDict[value] = count
        data[count] = ([key, value])
        count += 1
    return count


def leaveOne(testingPoints, groupData):
    onePresent = False
    for ID in sorted(groupData, reverse=True):
        if ID in testingPoints:
            if onePresent:
                testingPoints.pop(ID)
            else:
                onePresent = True


def copyData(data, groupData, newData):
    for index in groupData:
        data[index] = newData


class OBJECT_OT_Bullet_Simplify(bpy.types.Operator):
    bl_idname = "bullet.simplify"
    bl_label = "Simplify Faces"

    bl_description = "Simplifies face geometry by removing shared edges"

    def execute(self, context):

        simplifyCount = 0
        sel_obs = context.selected_objects
        # obj = context.object
        bpy.ops.object.select_all(action='DESELECT')
        angleThreshold = math.cos(math.radians(context.window_manager.bullet_tool.bullet_tool_max_merge_angle))
        for obj in sel_obs:
            obj.select_set(True)
            context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode="EDIT")
            bm = bmesh.from_edit_mesh(obj.data)
            facesLib = []
            for polygon in obj.data.polygons:
                facesLib.append(polygon.vertices[:])
            testLib = {}
            for i in range(len(facesLib)):
                testLib[i] = facesLib[i]

            grouping = {}
            groupData = {}
            groupCount = 0
            for i in range(len(facesLib)):
                if i in testLib:
                    for j in range(len(facesLib)):
                        if j in testLib:
                            if i == j:
                                continue
                            if (facesLib[i] != facesLib[j]) and (abs((obj.data.polygons[i].normal).normalized().dot(
                                    obj.data.polygons[j].normal.normalized())) >= angleThreshold):
                                mergedFace = mergeLists(facesLib[i], facesLib[j])
                                if mergedFace:
                                    simplifyCount += 1
                                    self.report({'INFO'},
                                                f"***{i}::{j}::{facesLib[i]}::::{facesLib[j]}::::{mergedFace}")
                                    groupCount = group(j, i, grouping, groupData, groupCount)
                                    copyData(facesLib, groupData[grouping[i]], mergedFace[:])
                                    leaveOne(testLib, groupData[grouping[i]])

            confirmedFaces = selectIndividuals(groupData, len(facesLib), grouping)
            # [facesLib.pop(index) for index in grouping]
            # self.report({'INFO'}, f"1:::::{grouping}")
            # self.report({'INFO'}, f"2:::::{groupData}")
            # self.report({'INFO'}, f"3:::::{grouping}")
            # self.report({'INFO'}, f"4:::::{facesLib}")
            materialData = []
            for index in confirmedFaces:
                materialData.append(obj.data.polygons[index].material_index)
            [bm.faces.remove(face) for face in bm.faces]

            self.report({'INFO'}, f"5:::::{materialData}")

            bm.verts.ensure_lookup_table()
            [bm.faces.new([bm.verts[i] for i in facesLib[index]]) for index in confirmedFaces]

            bm.faces.ensure_lookup_table()
            for i in range(len(confirmedFaces)):
                bm.faces[i].material_index = materialData[i]

            [bm.verts.remove(vert) for vert in bm.verts if not vert.link_faces]
            [bm.edges.remove(edge) for edge in bm.edges if not edge.link_faces]

            if context.window_manager.bullet_tool.bullet_tool_clean_verts:
                for vert in bm.verts:
                    if len(vert.link_edges) == 2:
                        # self.report({'INFO'}, f"CODE 1")
                        # angle = math.degrees(vert.calc_edge_angle())
                        # self.report({'INFO'}, f"CODE 3: {angle}")
                        if abs(math.degrees(
                                vert.calc_edge_angle())) <= context.window_manager.bullet_tool.bullet_tool_edge_angle:
                            # self.report({'INFO'}, f"CODE 2")
                            bmesh.ops.dissolve_verts(bm, verts=[vert])

            bmesh.update_edit_mesh(obj.data)

        bpy.ops.object.mode_set(mode="OBJECT")

        # restore_active_and_sel(obj, sel_obs)
        self.report({'INFO'}, f"Merged Faces::{simplifyCount}")
        return {'FINISHED'}


def selectIndividuals(groups, length, mapping):
    newList = []
    for subgroup in groups:
        newList.append(groups.get(subgroup)[0])
    for i in range(length):
        if i not in mapping:
            newList.append(i)
    return newList


class OBJECT_OT_Bullet_X_Connect(bpy.types.Operator):
    bl_idname = "bullet.x_connect"
    bl_label = "Generate Constraints"

    bl_description = "Glue faces together"

    def execute(self, context):

        sel_obs = context.selected_objects
        obj = context.object
        bpy.ops.object.select_all(action='DESELECT')

        mesh_obs = []
        for ob in sel_obs:
            if ob.type == 'MESH':
                mesh_obs.append(ob)

        # Make a new collection for all the empties we're going to create
        collection = bpy.data.collections.new("Glue Constraints")
        context.scene.collection.children.link(collection)

        # Create Spherical Bounds
        boundsDict = spheres(sel_obs)

        # Iterate through selection and glue
        searchList = sel_obs[:]
        temp = []
        for mainObj in sel_obs[:-1]:
            searchList.remove(mainObj)
            for testObj in searchList:
                glue(mainObj, testObj, collection, self, boundsDict, context.window_manager)

        restore_active_and_sel(obj, sel_obs)
        update(sel_obs)

        # Remove the collection if nothing was put in it
        if len(collection.all_objects) == 0:
            bpy.context.scene.collection.children.unlink(collection)
            bpy.data.collections.remove(collection)

        return {'FINISHED'}


def projectSign(p, v):
    if (p.x != 0 and v.x != 0):
        return p.x * v.x / abs(p.x * v.x)
    elif (p.y != 0 and v.y != 0):
        return p.y * v.y / abs(p.y * v.y)
    elif (p.z != 0 and v.z != 0):
        return p.z * v.z / abs(p.z * v.z)
    else:
        return 1


class OBJECT_OT_Bullet_intersect_Area(bpy.types.Operator):
    bl_idname = "bullet.intersect_area"
    bl_label = "Find Overlap"

    bl_description = "Allow multiple constraints between objects. Uses " \
                     "Neighbour Limit and Search Radius values (set below)."

    def execute(self, context):
        selected_objects = context.selected_objects
        obj1 = selected_objects[0]
        obj2 = selected_objects[1]
        mesh1 = obj1.data
        mesh2 = obj2.data

        pairs = []

        # Detect Alignment
        for face1 in mesh1.polygons:
            for face2 in mesh2.polygons:
                if abs(face2.normal.normalized().dot(face1.normal.normalized())) > 0.98:
                    n = obj1.matrix_world.to_3x3() @ face1.normal
                    distance = abs(((obj1.matrix_world @ mesh1.vertices[face1.vertices[0]].co) - (
                                obj2.matrix_world @ mesh2.vertices[face2.vertices[0]].co)).dot(n) / math.sqrt(n.dot(n)))
                    if distance < 0.5:
                        pairs.append((face1, face2))

        maxArea = 0
        intersectCenter = mathutils.Vector((0, 0, 0))
        # Flatten and Area Calculation
        for pair in pairs:
            face1, face2 = pair
            f1Norm = obj1.matrix_world.to_3x3() @ face1.normal
            v1 = f1Norm.orthogonal().normalized()
            v2 = f1Norm.normalized().cross(v1)
            origin = obj1.matrix_world @ mesh1.vertices[face1.vertices[0]].co

            flat1 = []
            flat2 = []

            for vertex in face1.vertices:
                offsetVertex = (obj1.matrix_world @ mesh1.vertices[vertex].co) - origin
                a = offsetVertex.project(v1)
                b = offsetVertex.project(v2)
                flat1.append((a.length * projectSign(a, v1), b.length * projectSign(b, v2)))
            for vertex in face2.vertices:
                offsetVertex = (obj2.matrix_world @ mesh2.vertices[vertex].co) - origin
                a = offsetVertex.project(v1)
                b = offsetVertex.project(v2)
                flat2.append((a.length * projectSign(a, v1), b.length * projectSign(b, v2)))

            poly1 = sply.Polygon(flat1)
            poly2 = sply.Polygon(flat2)

            intersectPoly = sply.Polygon.intersection(poly1, poly2)
            area = intersectPoly.area

            # self.report({'INFO'}, f"{poly1} :::: {list(face1.vertices)}")
            if area > maxArea:
                maxArea = area
                intersectCenter = origin + v1 * intersectPoly.centroid.x + v2 * intersectPoly.centroid.y

        self.report({'INFO'}, f"{maxArea}, {intersectCenter}")

        return {'FINISHED'}


def update(objs):
    wm = bpy.context.window_manager

    """def up_rigid_body():
        # obj.rigid_body.use_deactivation = False
        orb = obj.rigid_body

        if wm.bullet_tool.bullet_tool_show_obj is True:
            orb.use_margin = wm.bullet_tool.bullet_tool_use_margin
            orb.collision_margin = wm.bullet_tool.bullet_tool_collmargin
            orb.restitution = wm.bullet_tool.bullet_tool_bounciness
            orb.friction = wm.bullet_tool.bullet_tool_friction"""

    def up_rigid_constraint():
        con = obj.rigid_body_constraint
        con.use_breaking = wm.bullet_tool.bullet_tool_breakable
        con.type = wm.bullet_tool.bullet_tool_Constraint_type
        con.breaking_threshold *= wm.bullet_tool.bullet_tool_mult

    def empty_size(empty):
        size = 0.5

        if empty.rigid_body_constraint.type == 'FIXED':
            empty.scale = (size, size, size)
            empty.empty_display_size = size
            empty.empty_display_type = 'PLAIN_AXES'
        if empty.rigid_body_constraint.type == 'POINT':
            empty.scale = (size, size, size)
            empty.empty_display_size = size
            empty.empty_display_type = 'SPHERE'
        if empty.rigid_body_constraint.type == 'HINGE':
            empty.scale = (0.0, 0.0, size * 3)
            empty.empty_display_size = size
            empty.empty_display_type = 'PLAIN_AXES'
        if empty.rigid_body_constraint.type == 'SLIDER':
            empty.scale = (size * 3, 0.0, 0.0)
            empty.empty_display_size = size
            empty.empty_display_type = 'PLAIN_AXES'
        if empty.rigid_body_constraint.type == 'PISTON':
            empty.scale = (size * 3, 0.0, 0.0)
            empty.empty_display_size = size
            empty.empty_display_type = 'PLAIN_AXES'
        if empty.rigid_body_constraint.type == 'GENERIC':
            empty.scale = (size, size, size)
            empty.empty_display_size = size
            empty.empty_display_type = 'PLAIN_AXES'
        if empty.rigid_body_constraint.type == 'GENERIC_SPRING':
            empty.scale = (size, size, size)
            empty.empty_display_size = size
            empty.empty_display_type = 'PLAIN_AXES'

    for obj in objs:
        # Only Allow Mesh or Empty
        if obj.type == 'MESH':

            # Check for Constraints
            if obj.rigid_body_constraint:
                up_rigid_constraint()

                # obj.rigid_body_constraint.disable_collisions=0
        elif obj.type == 'EMPTY':
            if obj.rigid_body_constraint:
                up_rigid_constraint()
                empty_size(obj)


class OBJECT_OT_Bullet_Update(bpy.types.Operator):
    bl_idname = "bullet.update"
    bl_label = "Update Selected"

    bl_description = "Update Settings to Selected"

    def execute(self, context):
        update(bpy.context.selected_objects)

        return {'FINISHED'}


class OBJECT_OT_Bullet_remove_constraints(bpy.types.Operator):
    bl_idname = "bullet.remove_constraints"
    bl_label = "Remove Constraints"
    bl_description = "Remove Constraints on Selected"

    def execute(self, context):

        bdo = bpy.data.objects
        scene = context.scene
        act_ob = context.active_object
        if act_ob is not None:
            # If the active object is one of our empties which we are going
            # to remove,  set it to none now, otherwise later when we try to
            # restore the active object, Blender will give an exception as the
            # object has been removed.
            if act_ob.name.startswith("BCT constraint"):
                act_ob = None

        sel_ob_names = []
        for sel_ob in context.selected_objects:
            sel_ob_names.append(sel_ob.name)

        # We can't use a for loop as we will be removing items from
        # the list as we go through it. Use a while loop.
        index = 0
        while index < len(sel_ob_names):
            ob_name = sel_ob_names[index]
            if ob_name.startswith("BCT constraint"):
                # The object is one of the empties created by BCT
                # to join two objects together. Find the collection it
                # belongs to so the collection can be removed after
                # last empty is removed from it.
                ob = bdo.get(ob_name)
                if ob is not None:
                    c = None
                    for c in ob.users_collection:
                        if c.name.startswith("BCT empties"):
                            break

                    del (sel_ob_names[index])
                    bdo.remove(bdo[ob_name], do_unlink=True)

                    if c is not None:
                        if len(c.objects) == 0:
                            bpy.data.collections.remove(c)
            else:

                # As we are not going to remove the current object,
                # increment the index so that next time through the loop
                # we won't look at the same object. (If an object is
                # removed we don't need to do this as all subsequent
                # objects move down a position)
                index += 1

                # We have either got an object with its own rigidbody
                # constraint, or an object which is constrained by an
                # empty with rigidbody constraints. Check if the object
                # has its own constraint, and if not find the empty which
                # is constraining it.
                ob = bdo.get(ob_name)
                if ob is not None:
                    if ob.rigid_body_constraint:

                        # The object has its own constraint.
                        context.view_layer.objects.active = ob
                        if bpy.ops.rigidbody.constraint_remove.poll():
                            bpy.ops.rigidbody.constraint_remove()
                        else:
                            # We must change the context to avoid an
                            # exception. Change it back straight after.
                            bpy.context.area.type = 'VIEW_3D'
                            bpy.ops.rigidbody.constraint_remove()
                            bpy.context.area.type = 'PROPERTIES'
                    else:
                        # Get the list of all empties connected to this object,
                        # which we have previously stored
                        if "empties" in ob:
                            for key in ob["empties"]:
                                empty = scene.objects.get(ob["empties"][key])

                                if empty is not None:
                                    # Find the collection the empty belongs to
                                    # so it can be deleted after last empty is
                                    # removed.
                                    c = None
                                    for c in empty.users_collection:
                                        if c.name.startswith("BCT empties"):
                                            break

                                    # Remove the empty, but first remove its
                                    # name from the object dictionary where it
                                    # was stored. Also take a note of its name
                                    # (see next comment).
                                    empty_name = empty.name
                                    bdo.remove(bdo[empty.name], do_unlink=True)

                                    # The empty we just deleted might be in our
                                    # list of selected objects if it happened
                                    # to be selected when the user pressed the
                                    # remove button. In other words, we might
                                    # have had two references to it - one from
                                    # the dictionary attached to the object,
                                    # and another from it having been selected.
                                    # Go through the rest of the list and if
                                    # the name of the empty is found, remove
                                    # it from the list so we don't try to
                                    # remove the already-removed empty when
                                    # we reach that point in the list.
                                    j = index
                                    while j < len(sel_ob_names):
                                        if sel_ob_names[j] == empty_name:
                                            del (sel_ob_names[j])
                                            break
                                        else:
                                            j += 1

                                    if c is not None:
                                        if len(c.objects) == 0:
                                            bpy.data.collections.remove(c)

                                # Whether we found the empty or not, remove
                                # the reference to it from the obejct. If we
                                # found it, we deleted it, if we didn't find
                                # it, the object shouldn't refer to it.
                                del ob["empties"][key]

        if act_ob is None:
            # If one of the empties we deleted was the active object,
            # Blender will make the physics panel disappear (it disappears
            # when there is no active object), which will make the BCT UI
            # disappear too. To stop it disappearing, set one of the selected
            # objects as active, or if all selected objects were removed,
            # set the first object in the scene active, if there is one.
            if len(context.selected_objects) > 0:
                new_active_ob = scene.objects.get(sel_ob_names[0])
                context.view_layer.objects.active = new_active_ob
            else:
                vl_obs = context.view_layer.objects
                if len(vl_obs) > 0:
                    vl_obs.active = vl_obs[0]

        return {'FINISHED'}


# Properties Test
class BulletToolProps(bpy.types.PropertyGroup):
    bool = bpy.props.BoolProperty
    float = bpy.props.FloatProperty
    int = bpy.props.IntProperty

    """bullet_tool_show_obj: bool(
        name="", default=False, description='Enable Object Settings Update')
    bullet_tool_show_con: bool(
        name="", default=True, description='Enable Type Settings Update')
    bullet_tool_show_break: bool(
        name="", default=True, description='Enable Break Threshold Update')
    bullet_tool_show_it: bool(name="", default=False,description='Enable Override Iterations Update')
    bullet_tool_show_lim: bool(
        name="Enable Update Limits & Springs",
        default=False,
        description='Enable Limits Update')"""
    """bullet_tool_use_margin: bool(
        name="Collision Margin", default=True, description='Collision Margin')
    bullet_tool_collmargin: float(
        name="Margin",
        default=0.0005,
        min=0.0,
        max=1,
        description="Collision Margin")
    bullet_tool_bounciness: float(
        name="Bounciness",
        default=0.0,
        min=0.0,
        max=10000,
        description="Bounciness")
    bullet_tool_friction: float(
        name="Friction", default=0.5, min=0.0, max=100, description="Friction")
    bullet_tool_iteration: int(name="Iterations", default=60, min=1, max=1000)
    bullet_tool_over_iteration: bool(
        name="Override Iterations",
        default=False,
        description='Override Iterations')"""
    bullet_tool_breakable: bool(
        name="Breakable",
        default=False,
        description='Enable breakable Constraints')
    bullet_tool_break_threshold: float(name="Break Threshold", default=10, min=0.0, max=10000,
                                       description="Break Threshold. Strength of Object. Break Threshold""= Mass * Threshold")
    bullet_tool_max_angle: float(name="Max Angle", default=2, min=0.0, max=30,
                                 description="Maximum Angle Between Faces to be Considered Touching")
    bullet_tool_max_distance: float(name="Max Distance", default=0.01, min=0.0, max=1,
                                    description="Maximum Distance Between Faces to be Considered Touching")
    bullet_tool_min_area: float(name="Min Area Percentage", default=0.001, min=0.0, max=1,
                                description="Minimum Overlapping Area Percentage to be Considered Touching")
    bullet_tool_mult: float(name="Threshold Multiplier", default=1, min=0.0, max=100000,
                            description="Multiplication to Apply to Breaking Threshold when Updating")
    bullet_tool_pressure: bool(name="Pressure", default=True, description='Calculate Break Threshold from Face Area')
    bullet_tool_max_merge_angle: float(name="Face Angle", default=1, min=0.0, max=30,
                                       description="Maximum Angle Between Faces to Merge")
    bullet_tool_edge_angle: float(name="Edge Angle", default=0.5, min=0.0, max=30,
                                  description="Maximum Bend Angle to Merge")
    bullet_tool_clean_verts: bool(name="Clean Vertices", default=True,
                                  description="Merge Vertices in Addition to Faces")

    """bullet_tool_multiplier: bool(
        name="Multiply",
        default=False,
        description='Break Threshold = Break Threshold * Multiplier')"""
    """bullet_tool_search_radius: float(
        name="Search Radius",
        default=3.0,
        min=0.0,
        max=10000,
        description="Near Search radius")

    bullet_tool_neighbours: int(
        name="Neighbour Limit",
        default=3,
        min=1,
        max=60,
        description="Number of Neighbour to Check. More = Slower")

    # for GPencil
    # bullet_tool_gpencil_mode: bool(
    #     name="GPencil Mode",
    #     default=False,
    #     description="Disabled =  Edit constraints, Enabled = Edit and "
    #                 "Generate Constraints")
    bullet_tool_gpencil_dis: float(
        name="GPencil Distance",
        default=1.0,
        min=0.0,
        max=100,
        description="Distance for GPencil")"""

    # props for Constraints
    """bullet_tool_use_limit_ang_x: bool(name="X Angle", default=False)
    bullet_tool_limit_ang_x_lower: float(
        name="Limit Angle X lower", default=-45.0, min=-360, max=360)
    bullet_tool_limit_ang_x_upper: float(
        name="Limit Angle X upper", default=45.0, min=-360, max=360)

    bullet_tool_use_limit_ang_y: bool(name="Y Angle", default=False)
    bullet_tool_limit_ang_y_lower: float(
        name="Limit Angle Y lower", default=-45.0, min=-360, max=360)
    bullet_tool_limit_ang_y_upper: float(
        name="Limit Angle Y upper", default=45.0, min=-360, max=360)

    bullet_tool_use_limit_ang_z: bool(name="Z Angle", default=False)
    bullet_tool_limit_ang_z_lower: float(
        name="Limit Angle Z lower", default=-45.0, min=-360, max=360)
    bullet_tool_limit_ang_z_upper: float(
        name="Limit Angle Z upper", default=45.0, min=-360, max=360)

    bullet_tool_use_limit_lin_x: bool(name="X Axis", default=False)
    bullet_tool_limit_lin_x_lower: float(
        name="Limit Linear X lower", default=-45.0, min=-10000.0, max=10000)
    bullet_tool_limit_lin_x_upper: float(
        name="Limit Linear X upper", default=45.0, min=-10000.0, max=10000)

    bullet_tool_use_limit_lin_y: bool(name="Y Axis", default=False)
    bullet_tool_limit_lin_y_lower: float(
        name="Limit Linear Y lower", default=-45.0, min=-10000.0, max=10000)
    bullet_tool_limit_lin_y_upper: float(
        name="Limit Linear Y upper", default=45.0, min=-10000.0, max=10000)

    bullet_tool_use_limit_lin_z: bool(name="Z Axis", default=False)
    bullet_tool_limit_lin_z_lower: float(
        name="Limit Linear Z lower", default=-45.0, min=-10000.0, max=10000)
    bullet_tool_limit_lin_z_upper: float(
        name="Limit Linear Z upper", default=45.0, min=-10000.0, max=10000)

    bullet_tool_use_spring_x: bool(name="Use Spring X", default=False)
    bullet_tool_spring_stiffness_x: float(
        name="Stiffness", default=10.0, min=-0.0, max=100)
    bullet_tool_spring_damping_x: float(
        name="Damping", default=0.5, min=-0.0, max=1)

    bullet_tool_use_spring_y: bool(name="Use Spring X", default=False)
    bullet_tool_spring_stiffness_y: float(
        name="Stiffness", default=10.0, min=-0.0, max=100)
    bullet_tool_spring_damping_y: float(
        name="Damping", default=0.5, min=-0.0, max=1)

    bullet_tool_use_spring_z: bool(name="Use Spring X", default=False)
    bullet_tool_spring_stiffness_z: float(
        name="Stiffness", default=10.0, min=-0.0, max=100)
    bullet_tool_spring_damping_z: float(
        name="Damping", default=0.5, min=-0.0, max=1)"""

    itemlist = [('FIXED', 'Fixed', 'FIXED'),
                ('POINT', 'Point', 'POINT'),
                ('HINGE', 'Hinge', 'HINGE'),
                ('SLIDER', 'Slider', 'SLIDER'),
                ('PISTON', 'Piston', 'PISTON'),
                ('GENERIC', 'Generic', 'GENERIC'),
                ('GENERIC_SPRING', 'Generic Spring', 'GENERIC_SPRING')
                ]

    bullet_tool_Constraint_type: bpy.props.EnumProperty(
        items=itemlist,
        name="Constraint_type")
    # bpy.context.scene['bullet_tool_Constraint_type'] = 0


classes = [BulletToolProps,
           Bullet_Tools,
           OBJECT_OT_Bullet_X_Connect,
           OBJECT_OT_Bullet_Update,
           OBJECT_OT_Bullet_remove_constraints,
           OBJECT_OT_Bullet_intersect_Area,
           OBJECT_OT_Bullet_Simplify
           ]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.WindowManager.bullet_tool = bpy.props.PointerProperty(
        type=BulletToolProps)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.WindowManager.bullet_tool


if __name__ == "__main__":
    register()
