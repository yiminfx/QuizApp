import maya.cmds as cmds


# 1: select blendshapde node of the mesh and print out its blendshapes
def find_shapes_node(selected_mesh):
    if cmds.objExists(selected_mesh):
        history_nodes = cmds.listHistory(selected_mesh)
        
        if history_nodes:
            for node in history_nodes:
                node_type = cmds.nodeType(node)
                if node_type == 'blendShape':
                    return node
        else:
            print("No blendShape node found in the history of {}.".format(selected_mesh))
            return None
    else:
        print("Selected mesh does not exist.")
        return None

# Get the currently selected mesh
selected_mesh = cmds.ls(selection=True)
if selected_mesh:
    shapes_node = find_shapes_node(selected_mesh[0])
    if shapes_node:
        cmds.select(shapes_node)
        
        blendshapes = cmds.listConnections(shapes_node, type='shape')

        for index, blendshape in enumerate(blendshapes):
            if ('transform' not in blendshape and 'head' not in blendshape):
                print (blendshape) 

                cmds.setAttr(f'shapes.{blendshape}', 1)
                
                duplicated_mesh = cmds.duplicate(selected_mesh , name=f"dup_{blendshape}")
                # Offset the duplicate in the x-axis
                cmds.move(20 * index, 0, 0, duplicated_mesh, relative=True)

                cmds.setAttr(f'shapes.{blendshape}', 0)



    else:
        print("No 'shapes' node (blendShape) found connected to {}.".format(selected_mesh[0]))
else:
    print("Please select a mesh.")

