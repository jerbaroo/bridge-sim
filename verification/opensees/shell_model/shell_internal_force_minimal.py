"""
    Testing the ShellMITC4 element on a simple model: translations, internal forces, strains

    Units:
     length [m]
     force  [N]

     ^ y
     |
     |
     0---> x


     7     8     9
    o-----o-----o
    |     |     |
    |     |     |
    o-----o-----o
    |4    |5    |6
    |     |     |
    o-----o-----o
    1     2     3
"""

import os
import glob
import subprocess as subp

import matplotlib.pyplot as plt
import numpy as np

plt.close('all')
plt.interactive(False)

# ----------------------------------------------------------------------------------------------------------------------
# INPUT & CONTROL
# ----------------------------------------------------------------------------------------------------------------------

model_name = "shell_model_03.tcl"
template_name = "shell_model_03_template.tcl"
os_exe_dir = "c:\\Users\\arpada\\Wok\\OpenSees3.0.3"

F_total = 1000
force_type = "uniform"
# force_type = "concentrated"

# the same discretization will be used in y direction as well
n_elem_x = 20

x_start = 0
x_end = 2
y_start = 0
y_end = 2

# dims = ["y"]
dims = ["x", "y"]
# dims = ["x", "y", "z"]

# ----------------------------------------------------------------------------------------------------------------------
# PRE-PROCESSING
# ----------------------------------------------------------------------------------------------------------------------

# This is how OS structures the ouputs source: https://opensees.berkeley.edu/community/viewtopic.php?f=2&t=64493&p=110032&hilit=ShellMITC4#p110032; https://opensees.berkeley.edu/community/viewtopic.php?f=2&t=64252&p=109351&hilit=ShellMITC4#p109351
# [Nxx, Nyy, Nxy, Mxx, Myy, Mxy, Vxz, Vyz]; in the x-y local coordinate system of the element
internal_force_dict = {0: "Nxx", 1: "Nyy", 2: "Nxy", 3: "Mxx", 4: "Myy", 5: "Mxy", 6: "Vxz", 7: "Vyz"}
internal_force_unit_dict = {0: "N/m", 1: "N/m", 2: "N/m", 3: "Nm/m", 4: "Nm/m", 5: "Nm/m", 6: "N/m", 7: "N/m"}
# [11-strain, 22-strain, 12-shear, 11-curvature, 22-curvature, 12-curvature, 13-shear, 23-shear]; in the x-y local coordinate system of the element
strain_dict = {0: "strain_11", 1: "strain_22", 2: "shear_12", 3: "curvature_11", 4: "curvature_22", 5: "curvature_12", 6: "shear_13", 7: "shear_23"}

n_internal_force = len(internal_force_dict)


prev_analysis_files = glob.glob(os.path.join(os_exe_dir, f"{model_name[:-4]}*.out"))
for prev_analysis_file in prev_analysis_files:
    os.remove(prev_analysis_file)

if divmod(n_elem_x, 2)[1] != 0:
    n_elem_x = n_elem_x + 1

n_elem_y = n_elem_x # for simplicity

dim_dict = {"x": 0, "y": 1, "z": 2}

dim_num = [dim_dict[dim] for dim in dims]

# .......................................................................
# Nodes
# .......................................................................
node_x = np.linspace(x_start, x_end, n_elem_x+1)
node_y = np.linspace(y_start, y_end, n_elem_y+1)

node_X, node_Y = np.meshgrid(node_x, node_y)

node_xx = node_X.ravel()
node_yy = node_Y.ravel()
node_zz = np.zeros(node_xx.shape)

n_node = np.prod(node_X.shape)
node_nr = np.arange(1, n_node+1, dtype=int)

n_node = len(node_nr)

# .......................................................................
# Elements
# .......................................................................
n_elem = n_elem_x*n_elem_y

M = node_nr.reshape((n_elem_x+1, n_elem_y+1))
node_i = M[:-1, :-1].ravel()
node_j = node_i + 1
node_k = node_j + (n_elem_x + 1)
node_l = node_i + (n_elem_x + 1)
elems_nodes = np.vstack((node_i, node_j, node_k, node_l)).T

if force_type == "uniform":
    loaded_nodes = M[-1, :]
    n_loaded_nodes = len(loaded_nodes)
    f = F_total/(n_loaded_nodes - 1)
    load_on_nodes = np.ones(len(loaded_nodes))*f
    load_on_nodes[[0, -1]] = f/2
elif force_type == "concentrated":
    loaded_nodes = [M[-1, int(n_elem_x/2)]]
    n_loaded_nodes = [1]
    load_on_nodes = [F_total]
else:
    raise ValueError

# .......................................................................
# Rest
# .......................................................................
n_dim = len(dims)

# paths
template_path = os.path.join(os_exe_dir, template_name)
model_path = os.path.join(os_exe_dir, model_name)
os_exe_path = os.path.join(os_exe_dir, "OpenSees.exe")

cwd = os.getcwd()

# ----------------------------------------------------------------------------------------------------------------------
#  WRITE TCL FILE
# ----------------------------------------------------------------------------------------------------------------------

with open(template_path, "rt") as file_in:
    with open(model_path, "w+") as file_out:
        for line in file_in:
            mod_line = line.replace("<<TOT_NODE_NR>>", str(n_node))
            mod_line = mod_line.replace("<<TOT_ELEM_NR>>", str(n_elem))
            mod_line = mod_line.replace("<<MODEL_NAME>>", model_name[:-4])

            node_block = [f"node {node_nr[ii]:.0f} {node_xx[ii]:.4f} {node_yy[ii]:.4f} {node_zz[ii]:.4f}\n" for ii in range(n_node)]
            node_block = "".join(node_block)
            mod_line = mod_line.replace("<<NODE>>", node_block)

            support_block = [f"fix {ii+1:.0f} 1 1 1 1 1 1\n" for ii in range(n_elem_x + 1)]
            support_block = "".join(support_block)
            mod_line = mod_line.replace("<<SUPPORT>>", support_block)

            element_block = [f"element ShellMITC4 {node_nr[ii]:.0f} {elem_nodes[0]:.0f} {elem_nodes[1]:.0f} {elem_nodes[2]:.0f} {elem_nodes[3]:.0f} 1\n" for ii, elem_nodes in enumerate(elems_nodes)]
            element_block = "".join(element_block)
            mod_line = mod_line.replace("<<ELEMENT>>", element_block)

            load_block = [f"\tload {loaded_node:.0f} {load_on_node:.4e} {load_on_node:.4e} 0 0 0 0\n" for loaded_node, load_on_node in zip(loaded_nodes, load_on_nodes)]
            load_block = "".join(load_block)
            mod_line = mod_line.replace("<<LOAD>>", load_block)

            file_out.write(mod_line)

# ----------------------------------------------------------------------------------------------------------------------
#  RUN ANALYSIS
# ----------------------------------------------------------------------------------------------------------------------

os.chdir(os_exe_dir)
subp.check_output(f'"{os_exe_path}" "{model_name}"', shell=True, stderr=subp.STDOUT).decode()
os.chdir(cwd)

# ----------------------------------------------------------------------------------------------------------------------
#  POST-PROCESSING
# ----------------------------------------------------------------------------------------------------------------------

# .......................................................................
# Translations
# .......................................................................
transl_mx = np.empty((n_node, n_dim))
for ii, dim in enumerate(dims):
    res_path = os.path.join(os_exe_dir, f"{model_name[:-4]}_transl_{dim}.out")

    transl_mx[:, ii] = np.loadtxt(res_path)

idx_max_transl = np.argmax(transl_mx, axis=0)
max_transl = transl_mx[idx_max_transl, dim_num]

# .......................................................................
# Internal forces
# .......................................................................
# Q: ??are the internal force given at the nodes or integration points??

res_path = os.path.join(os_exe_dir, f"{model_name[:-4]}_internal_force.out")
element_internal_force_mx = np.loadtxt(res_path)
element_internal_force_mx = element_internal_force_mx.reshape((n_elem, -1, 8))

node_internal_force_mx = np.empty((n_node, 8))
for ii, node in enumerate(node_nr):
    idx_row, idx_col = np.where(elems_nodes == node)
    node_internal_force_mx[ii, :] = np.mean(element_internal_force_mx[idx_row, idx_col], axis=0)

# .......................................................................
# Strains
# .......................................................................
# Q: ?? strains at what point along the thickness of the element ??
# Q: ?? are the strains in the local coordinate system or principal strains??

element_strain_mx = np.empty((n_elem, 8*4))
n_comp = 8
for ii in range(4):
    res_path = os.path.join(os_exe_dir, f"{model_name[:-4]}_strain_integrationpoint={ii+1}.out")
    element_strain_mx_ii = np.loadtxt(res_path)
    element_strain_mx_ii = element_strain_mx_ii.reshape((n_elem, 8))
    idx1 = ii*n_comp
    idx2 = (ii+1)*n_comp
    element_strain_mx[:, idx1:idx2] = element_strain_mx_ii

element_strain_mx = element_strain_mx.reshape((n_elem, -1, 8))

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# this step is incorrect (treats the strain results as they correspond to nodes)
# it should be corrected once the integration point locations are known
node_strain_mx = np.empty((n_node, 8))
for ii, node in enumerate(node_nr):
    idx_row, idx_col = np.where(elems_nodes == node)
    node_strain_mx[ii, :] = np.mean(element_strain_mx[idx_row, idx_col], axis=0)
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# ----------------------------------------------------------------------------------------------------------------------
#  VISUALIZATION
# ----------------------------------------------------------------------------------------------------------------------

# .......................................................................
# Translations
# .......................................................................
for ii, dim in enumerate(dims):
    Z = transl_mx[:, ii].reshape((n_elem_x+1, n_elem_y+1))*1e3

    fig, ax = plt.subplots()
    ax.contour(node_X, node_Y, Z, levels=14, linewidths=0.5, colors='k')
    cntr = plt.contourf(node_X, node_Y, Z, levels=14, cmap="RdBu_r")
    cbar = fig.colorbar(cntr, ax=ax)
    cbar.set_label(f"Translation, {dim} [mm]")

    ax.scatter(node_xx, node_yy, marker=".", facecolors="none", edgecolors="black", label="node")

    idx_max_transl_ii = idx_max_transl[ii]
    max_transl_ii = float(max_transl[ii])
    tx = node_xx[idx_max_transl_ii]
    ty = node_yy[idx_max_transl_ii]
    ax.scatter(tx, ty, marker="o", facecolors="red", edgecolors="black", label="max")
    ax.text(tx, ty, f"{max_transl_ii * 1e3:.3f}mm", style="italic")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_title("Translations")

# .......................................................................
# Internal forces
# .......................................................................

internal_force_nums = [0, 1, 2]
for ii in internal_force_nums:
    internal_force = internal_force_dict[ii]
    internal_force_unit = internal_force_unit_dict[ii]
    Z = node_internal_force_mx[:, ii].reshape((n_elem_x+1, n_elem_y+1))

    fig, ax = plt.subplots()
    ax.contour(node_X, node_Y, Z, levels=14, linewidths=0.5, colors='k')
    cntr = plt.contourf(node_X, node_Y, Z, levels=14, cmap="RdBu_r")
    cbar = fig.colorbar(cntr, ax=ax)
    cbar.set_label(f"Internal force, {internal_force} [{internal_force_unit}]")

    ax.scatter(node_xx, node_yy, marker=".", facecolors="none", edgecolors="black", label="node")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_title("Internal forces")


# .......................................................................
# Strains
# .......................................................................

strain_nums = [0, 1, 2]
for ii in strain_nums:
    strain = strain_dict[ii]
    Z = node_strain_mx[:, ii].reshape((n_elem_x+1, n_elem_y+1))

    fig, ax = plt.subplots()
    ax.contour(node_X, node_Y, Z, levels=14, linewidths=0.5, colors='k')
    cntr = plt.contourf(node_X, node_Y, Z, levels=14, cmap="RdBu_r")
    cbar = fig.colorbar(cntr, ax=ax)
    cbar.set_label(f"Strain, {strain} [-]")

    ax.scatter(node_xx, node_yy, marker=".", facecolors="none", edgecolors="black", label="node")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_title("Strains")

plt.show()

