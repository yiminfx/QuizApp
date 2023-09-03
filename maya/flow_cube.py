import maya.standalone
maya.standalone.initialize(name='python')

import maya.cmds as cmds

def build_house():
    # Create the base of the house
    base = cmds.polyCube(width=10, height=1, depth=10)[0]

    # Create the walls of the house
    wall1 = cmds.polyCube(width=10, height=5, depth=1)[0]
    cmds.move(0, 2.5, -5, wall1)

    wall2 = cmds.polyCube(width=1, height=5, depth=10)[0]
    cmds.move(-5, 2.5, 0, wall2)

    wall3 = cmds.duplicate(wall1)[0]
    cmds.move(0, 2.5, 5, wall3)

    wall4 = cmds.duplicate(wall2)[0]
    cmds.move(5, 2.5, 0, wall4)

    # Create the roof of the house
    roof_vertices = [(0, 10, -5), (5, 10, 0), (0, 10, 5), (-5, 10, 0)]
    roof_face = cmds.polyCreateFacet(p=roof_vertices)[0]
    cmds.move(0, 7.5, 0, roof_face)

def main():
    try:
        # Build the house
        build_house()

        # Get the user's document folder
        document_folder = cmds.internalVar(userAppDir=True)

        # Define the export paths
        maya_export_path = document_folder + "house_model.ma"
        obj_export_path = document_folder + "house_model.obj"

        # Save the Maya scene
        cmds.file(rename=maya_export_path)
        cmds.file(save=True, type="mayaAscii")

        # Load the OBJ export plugin
        cmds.loadPlugin("objExport")

        # Select all objects
        cmds.select(all=True)

        # Export the selection as OBJ
        cmds.file(obj_export_path, force=True, options="groups=0;ptgroups=0;materials=0;smoothing=1;normals=1", type="OBJexport", pr=True, es=True)

        print("House model exported as Maya scene file and OBJ to:", document_folder)
    except Exception as e:
        print("Error:", e)
    finally:
        maya.standalone.uninitialize()

if __name__ == "__main__":
    main()
