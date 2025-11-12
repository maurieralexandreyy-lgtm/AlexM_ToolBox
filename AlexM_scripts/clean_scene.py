import maya.cmds as cmds

def find_duplicate_names(mode="object"):
    if mode == "shape":
        all_objects = cmds.ls(type="shape", long=True)
    else:
        all_objects = cmds.ls(long=True)

    name_map = defaultdict(list)
    for obj in all_objects:
        short_name = obj.split('|')[-1]
        name_map[short_name].append(obj)

    duplicates = {name: paths for name, paths in name_map.items() if len(paths) > 1}
    return duplicates

def select_duplicate_objects(mode="object"):
    duplicates = find_duplicate_names(mode)
    flat_list = [item for sublist in duplicates.values() for item in sublist]
    if flat_list:
        cmds.select(flat_list, replace=True)
    else:
        cmds.select(clear=True)
        cmds.warning(f"No duplicate {mode} names found.")

def fix_duplicate_objects(mode="object"):
    duplicates = find_duplicate_names(mode)
    rename_count = defaultdict(int)

    for name, paths in duplicates.items():
        for i, obj in enumerate(paths):
            if i == 0:
                continue
            rename_count[name] += 1
            new_name = f"{name}_{rename_count[name]+1:02d}"
            try:
                if mode == "shape":
                    cmds.rename(obj, new_name)
                else:
                    new_obj = cmds.rename(obj, new_name)
                    shapes = cmds.listRelatives(new_obj, shapes=True, fullPath=True) or []
                    for shape in shapes:
                        new_shape_name = new_obj.split('|')[-1] + 'Shape'
                        cmds.rename(shape, new_shape_name)
            except Exception as e:
                cmds.warning(f"Could not rename {obj}: {e}")

def rename_shapes_by_name():
    selection = cmds.ls(selection=True, long=True) or []
    if not selection:
        cmds.warning("No objects selected.")
        return

    for obj in selection:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
        for shape in shapes:
            obj_name = obj.split('|')[-1]
            new_shape_name = obj_name + "Shape"
            try:
                cmds.rename(shape, new_shape_name)
            except Exception as e:
                cmds.warning(f"Could not rename shape {shape}: {e}")

def clean_scene_ui():
    if cmds.window("cleanSceneWin", exists=True):
        cmds.deleteUI("cleanSceneWin")

    window = cmds.window("cleanSceneWin", title="Clean Scene Objects", sizeable=False)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)

    cmds.text(label="Name Clash", align="center", height=20)
    cmds.separator(height=1)
    clash_type = cmds.radioButtonGrp("clashType", label="Type :", labelArray2=["Object", "Shape"], numberOfRadioButtons=2, select=1)
    clash_action = cmds.radioButtonGrp("clashAction", label="Action :", labelArray2=["Select", "Fix"], numberOfRadioButtons=2, select=1)

    def apply_action(*args):
        action = cmds.radioButtonGrp(clash_action, query=True, select=True)
        clash_mode = cmds.radioButtonGrp(clash_type, query=True, select=True)
        mode_str = "object" if clash_mode == 1 else "shape"

        if action == 1:
            select_duplicate_objects(mode=mode_str)
        elif action == 2:
            fix_duplicate_objects(mode=mode_str)
    
    cmds.separator(height=10)
    cmds.button(label="Rename shape by name", command=lambda x: rename_shapes_by_name(), height=30)
    cmds.separator(height=10)
    cmds.rowLayout(numberOfColumns=2)
    cmds.button(label="Apply", command=apply_action, h=30, w=160)
    cmds.button(label="Cancel", command=lambda *args: cmds.deleteUI(window, window=True), h=30, w=160)

    cmds.setParent("..")
    cmds.showWindow(window)

clean_scene_ui()

