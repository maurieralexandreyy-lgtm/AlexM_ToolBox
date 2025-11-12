def open_main_toolbox():
    # --- Création de la fenêtre principale ---
    if cmds.window("main_toolbox", exists=True):
        cmds.deleteUI("main_toolbox")

    window = cmds.window("main_toolbox", title="Main Toolbox", sizeable=True)
    form = cmds.formLayout()

    scroll = cmds.scrollLayout(parent=form, horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
    main_column = cmds.columnLayout(adjustableColumn=True, columnOffset=["both", 10], rowSpacing=10)

    cmds.separator(height=10, style="in")

    ''' ============================================================
         RIGGING & SETUP
        ============================================================ '''

    cmds.frameLayout(label="Rigging & Setup", borderStyle="etchedIn", collapsable=True,
                     marginHeight=8, marginWidth=5, labelAlign="center")

    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)

    cmds.button(label="Create Blend Joints", command=lambda x: bd_jt.create_blend_joint_ui(),
                height=30, backgroundColor=[0.6, 0.7, 0.9])
    cmds.button(label="Joints Bound by Curve", command=lambda x: jt_cv.joints_on_curve(),
                height=30, backgroundColor=[0.6, 0.7, 0.9])
    cmds.button(label="Compensate Group", command=lambda x: cmp_g.compensate_grp(),
                height=30, backgroundColor=[0.6, 0.7, 0.9])

    cmds.setParent('..')  # ferme columnLayout
    cmds.setParent('..')  # ferme frameLayout

    ''' ============================================================
         OPTIMIZSATION
        ============================================================ '''

    cmds.frameLayout(label="Optimization", borderStyle="etchedIn", collapsable=True,
                     marginHeight=8, marginWidth=5, labelAlign="center")

    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)

    cmds.button(label="Clean Scene", command=lambda x: cn_sc.clean_scene_ui(),
                height=30, backgroundColor=[0.6, 0.9, 0.6])
    cmds.button(label="Object Selector", command=lambda x: slct.object_selector_ui(),
                height=30, backgroundColor=[0.6, 0.9, 0.6])

    cmds.setParent('..')  # ferme columnLayout
    cmds.setParent('..')  # ferme frameLayout

    ''' ============================================================
         QUICK TOOLS
        ============================================================ '''

    cmds.frameLayout(label="Quick tools", borderStyle="etchedIn", collapsable=True,
                     marginHeight=8, marginWidth=5, labelAlign="center")

    cmds.columnLayout(adjustableColumn=True, rowSpacing=5)

    cmds.button(label="Copy XYZ Transform", command=lambda x: c_xyz.copy_xyz(),
                height=30, backgroundColor=[0.9, 0.6, 0.6])
    
    cmds.setParent('..')  # ferme columnLayout
    cmds.setParent('..')  # ferme frameLayout

    cmds.separator(height=10, style="in")

    cmds.setParent('..')  # ferme main_column
    cmds.setParent('..')  # ferme scrollLayout

    cmds.formLayout(form, edit=True, attachForm=[(scroll, 'top', 0), (scroll, 'left', 0), (scroll, 'bottom', 0), (scroll, 'right', 0)])
    cmds.showWindow(window)
