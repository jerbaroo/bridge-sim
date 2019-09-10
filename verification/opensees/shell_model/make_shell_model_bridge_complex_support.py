# Generates a shell model of a bridge and visualizes the vertical translations
#
# Notes:
# * meant for demonstrative purposes
# * the code will break if the input is unintelligent, the internal consistency of the input is not checked

import os
import subprocess as subp

import matplotlib.pyplot as plt
import numpy as np

plt.interactive(False)

# -----------------------------------------------------------------------
# INPUT & CONTROL
# -----------------------------------------------------------------------

model_name = "shell_model_bridge_complex_support.tcl"
os_exe_dir = "c:\\Users\\arpada\\Wok\\OpenSees2.5.0"

# divisions in longitudinal direction
l_boundary = np.array([0, 60])
l_support = np.array([2, 30, 58])
l_load = np.array([15])
l_discr = np.linspace(np.min(l_boundary), np.max(l_boundary), 100)
l_node_incr = 1000

# divisions in transverse direction
t_boundary = np.array([0, 10])
t_support = np.array([1, 9])
t_load = np.array([1])
t_discr = np.linspace(np.min(t_boundary), np.max(t_boundary), 10)

pier_height = 3

# -------------------------------------------------
# UTILS
# -------------------------------------------------


def comb2vec(v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
    """
    Create all possible combinations of two vectors
    """
    vc = np.array(np.meshgrid(v1, v2)).T.reshape(-1, 2).T
    return vc


def get_node_at_xy(set_x, set_y, node_x_vect, node_y_vect, node_n_vect):
    set_node_xy = comb2vec(set_x, set_y)
    n_set_node = set_node_xy.shape[1]
    set_node_n = np.empty(n_set_node)
    for ii in range(n_set_node):
        idx = (set_node_xy[0, ii] == node_x_vect) & (set_node_xy[1, ii] == node_y_vect)
        set_node_n[ii] = node_n_vect[idx]
    return set_node_n, set_node_xy


def unpack(s):
    return " ".join(map(str, s))


def write_header(file):
    file.write("# This a programatically generated file.\n#\n")
    file.write("# Units:\n# \n# dimension: [m]\n# force: [N]\n\n")
    file.write("wipe\n\n")
    file.write("model basic -ndm 3 -ndf 6\n\n")
    return


def write_support(file, nodeTag_sup, nodeTag_deck):
    # fix $nodeTag (ndf $constrValues)
    trans_x = 1
    trans_y = 1
    trans_z = 1
    rot_x = 0
    rot_y = 0
    rot_z = 0
    file.write("\n# Supports\n")
    file.write("# fix $NodeTag x-transl y-transl z-transl x-rot y-rot z-rot\n")
    for nodeTag_ii in nodeTag_sup:
        file.write(f"fix {nodeTag_ii:.0f} {trans_x:.0f} {trans_y:.0f} {trans_z:.0f} {rot_x:.0f} {rot_y:.0f} {rot_z:.0f}\n")

    file.write("\n# Rigid links\n")
    file.write("# rigidLink $type $masterNodeTag $slaveNodeTag\n")
    for ii, nodeTag_ii in enumerate(nodeTag_sup):
        file.write(f"rigidLink beam {nodeTag_ii:.0f} {nodeTag_deck[2*ii - (ii % 2)]:.0f}\n")
        file.write(f"rigidLink beam {nodeTag_ii:.0f} {nodeTag_deck[2*ii + 2 - (ii % 2)]:.0f}\n")
    return


def write_uniaxialMaterial(file, matTag, E):
    """
    Only for linear elastic materials so far

    uniaxialMaterial Elastic $matTag $E <$eta> <$Eneg>
    """
    file.write("\n# Concrete\n")
    for matTag_ii, E_ii in zip(matTag, E):
        file.write(f"uniaxialMaterial Elastic {matTag_ii:.0f} {E_ii:.5e}\n")
    return


def write_ElasticMembranePlateSection(file, secTag, E, nu, h, rho):
    # section ElasticMembranePlateSection $secTag $E $nu $h $rho
    file.write("\n# Cross-sections\n")
    for secTag_ii, E_ii, nu_ii, h_ii, rho_ii in zip(secTag, E, nu, h, rho):
        file.write(f"section ElasticMembranePlateSection {secTag_ii:.0f} {E_ii:.5e} {nu_ii:.5e} {h_ii:.5e} {rho_ii:.5e}\n")
    return


def write_elementShellMITC4(file, node_n, secTag, eleTag_start: int = 1):
    # element ShellMITC4 $eleTag $iNode $jNode $kNode $lNode $secTag
    file.write("\n# Shell elements\n")
    file.write("\n# ShellMITC4 Elements Definition: element ShellMITC4 $eleTag $iNode $jNode $kNode $lNode $secTag\n")
    n_t = node_n.shape[0]
    n_l = node_n.shape[1]
    eleTag = eleTag_start
    for jj in range(n_t-1):
        for ii in range(n_l-1):
            iNode = node_n[jj, ii]
            jNode = node_n[jj, ii + 1]
            kNode = node_n[jj + 1, ii + 1]
            lNode = node_n[jj + 1, ii]
            file.write(f"element ShellMITC4 {eleTag:.0f} {iNode:.0f} {jNode:.0f} {kNode:.0f} {lNode:.0f} {secTag:.0f}\n")
            eleTag += 1
    return


def write_analysis_settings(file):
    file.write("\nsystem BandGeneral\n")
    file.write("numberer RCM\n")
    # file.write("constraints Plain\n")
    file.write("constraints Transformation\n")
    file.write("integrator LoadControl 1\n")
    file.write("algorithm Linear\n")
    file.write("analysis Static\n")


def write_loading(file, nodeTag, Fx=0., Fy=0., Fz=0.):
    file.write("\n# Loading\n")
    file.write("timeSeries Linear 1\n\n")
    file.write("pattern Plain 1 1 {\n")
    for nodeTag_ii in nodeTag:
        file.write(f"   load {nodeTag_ii:.0f} {Fx:.4e} {Fy:.4e} {Fz:.4e} 0 0 0\n")
    file.write("}\n")
    return


def write_recorder(file, nodeTag):
    file.write("\n# Recorder\n")
    file.write(f"recorder Node -file shell_model_bridge_complex_support_transl_z.out -node {unpack(nodeTag)} -dof 3 disp\n")


def write_tcl(model_path):
    with open(model_path, 'w+') as tcl_file:
        # header
        write_header(tcl_file)

        # deck nodes
        tcl_file.write("# node $NodeTag $XCoord $Ycoord $Zcoord\n")
        for ii in range(len(node_n_vect)):
            tcl_file.write(f"node {node_n_vect[ii]:.0f} {node_x_vect[ii]:.4f} {node_y_vect[ii]:.4f} {node_z_vect[ii]:.4f}\n")
        # support nodes
        for ii in range(len(sup_node_n)):
            tcl_file.write(f"node {sup_node_n[ii]:.0f} {sup_node_x_vect[ii]:.4f} {sup_node_y_vect[ii]:.4f} {sup_node_z_vect[ii]:.4f}\n")

        # supports
        write_support(tcl_file, sup_node_n, sup_node_deck_n)

        # geomTransf Linear $transfTag <-jntOffset $dXi $dYi $dXj $dYj>
        # tcl_file.write("\n\ngeomTransf Linear 1\n")

        # material models
        # write_uniaxialMaterial(tcl_file, [1], [2.0000000e+11])
        # section ElasticMembranePlateSection $secTag $E $nu $h $rho
        write_ElasticMembranePlateSection(tcl_file, [1], [2.0000000e+10], [0.2], [0.4], [0])  # check the density

        # elements
        write_elementShellMITC4(tcl_file, node_n, secTag=1)

        # loading
        write_loading(tcl_file, load_node_n, Fx=0, Fy=0, Fz=1e5)

        # analysis settings
        write_analysis_settings(tcl_file)

        # collect results
        write_recorder(tcl_file, node_n_vect)

        # analysis
        tcl_file.write("\nanalyze 1\n")

        tcl_file.write('\nputs "Analysis done"\n')
        tcl_file.write("print node 2")


# -----------------------------------------------------------------------
# PRE-PROCESSING
# -----------------------------------------------------------------------

l_support_deck = np.sort(np.hstack((l_support-2, l_support+2)))
t_support_deck = t_support

l_node = np.unique(np.hstack((l_boundary, l_support_deck, l_load, l_discr)))
t_node = np.unique(np.hstack((t_boundary, t_support_deck, t_load, t_discr)))

node_x, node_y = np.meshgrid(l_node, t_node)
node_z = np.zeros(node_x.shape)
node_n_base = np.arange(1, len(l_node)+1, dtype=int)
node_n = node_n_base
for ii in range(1, len(t_node)):
    node_n = np.vstack((node_n, node_n_base + (ii)*l_node_incr))

node_x_vect = node_x.ravel()
node_y_vect = node_y.ravel()
node_z_vect = node_z.ravel()
node_n_vect = node_n.ravel()

# support nodes
sup_node_deck_n, sup_node_deck_xy = get_node_at_xy(l_support_deck, t_support_deck, node_x_vect, node_y_vect, node_n_vect)
sup_node_xy = comb2vec(l_support, t_support)
sup_node_n = 1e6 + np.arange(sup_node_xy.shape[1]) + 1

sup_node_x_vect = sup_node_xy[0, :].ravel()
sup_node_y_vect = sup_node_xy[1, :].ravel()
sup_node_z_vect = np.ones(sup_node_x_vect.shape)*pier_height

# load nodes
load_node_n, load_node_xy = get_node_at_xy(l_load, t_load, node_x_vect, node_y_vect, node_n_vect)

cwd = os.getcwd()

model_path = os.path.join(os_exe_dir, model_name)
os_exe_path = os.path.join(os_exe_dir, "OpenSees.exe")

# -----------------------------------------------------------------------
# WRITE TCL FILE
# -----------------------------------------------------------------------

write_tcl(model_path=model_path)

# -----------------------------------------------------------------------
#  RUN ANALYSIS
# -----------------------------------------------------------------------

os.chdir(os_exe_dir)
# subp.check_output(f'"{os_exe_path}" "{model_name}"', shell=True, stderr=subp.STDOUT).decode()
subp.check_output(f'"{os_exe_path}" "{model_name}"', shell=True).decode()
os.chdir(cwd)

# -----------------------------------------------------------------------
#  POST-PROCESSING
# -----------------------------------------------------------------------
res_path = os.path.join(os_exe_dir, "shell_model_bridge_complex_support_transl_z.out")

transl_z_vect = np.loadtxt(res_path)

transl_z = np.reshape(transl_z_vect, node_x.shape)

transl_z_max = np.max(transl_z)
idx = np.unravel_index(np.argmax(transl_z), transl_z.shape)

# -----------------------------------------------------------------------
#  VISUALIZATION
# -----------------------------------------------------------------------

# .......................................................................
# Top view
# .......................................................................
fig, ax = plt.subplots()
ax.contour(node_x, node_y, transl_z*1e3, levels=14, linewidths=0.5, colors='k')
cntr = plt.contourf(node_x, node_y, transl_z*1e3, levels=14, cmap="RdBu_r")
cbar = fig.colorbar(cntr, ax=ax)
cbar.set_label('Vertical translation, d_z [mm]')

ax.scatter(sup_node_deck_xy[0, :], sup_node_deck_xy[1, :], marker="o", color="blue", label="support")
ax.scatter(load_node_xy[0, :], load_node_xy[1, :], marker="o", color="red", label="load")

ax.scatter(node_x[idx], node_y[idx], marker="o", facecolors="none", edgecolors="black", label="max d_z")
ax.text(node_x[idx], node_y[idx], f"{transl_z_max*1e3:.3f}mm", style="italic")

ax.legend()
ax.axis('equal')
plt.xlabel("Longitudinal dir., x [m]")
plt.ylabel("Transverse dir., y [m]")
plt.grid(False)

print(f"Maximum vertical translation: {transl_z_max*1e3:.3f} mm")

# .......................................................................
# Side view at the edge
# .......................................................................
sup_node_deck_x = np.unique(sup_node_deck_xy[0, :])
# it should be the line of the supports
node_x_edge = node_x[0, :]
trans_z_edge = transl_z[0, :]
trans_z_edge_max = np.max(trans_z_edge)
idx_max = np.unravel_index(np.argmax(trans_z_edge), trans_z_edge.shape)

nn = len(sup_node_deck_x)
sup_node_deck_trans_z = np.empty(nn)
for ii in range(nn):
    idx = node_x_edge == sup_node_deck_x[ii]
    sup_node_deck_trans_z[ii] = trans_z_edge[idx]

fig, ax = plt.subplots()
ax.plot(node_x_edge, trans_z_edge*1e3, color="green", label="deformed shape")
ax.scatter(sup_node_deck_x, sup_node_deck_trans_z*1e3, marker="o", color="blue", label="deformed support")

ax.scatter(load_node_xy[0, :], np.zeros(load_node_xy.shape[1]), marker="o", color="red", label="load")

ax.plot(node_x_edge, np.zeros(node_x_edge.shape[0]), color="gray", ls="--", label="undeformed shape")
ax.scatter(sup_node_deck_x, np.zeros(sup_node_deck_x.shape[0]), marker="o", facecolors="none", edgecolors="gray")

ax.scatter(node_x_edge[idx_max], trans_z_edge_max*1e3, marker="o", facecolors="none", edgecolors="black", label="max d_z")
ax.text(node_x_edge[idx_max], trans_z_edge_max*1e3, f"{trans_z_edge_max*1e3:.3f}mm", style="italic")

ax.legend()
plt.xlabel("Longitudinal dir., x [m]")
plt.ylabel("Vertical translation, d_z [mm]")
plt.gca().invert_yaxis()
plt.show()
