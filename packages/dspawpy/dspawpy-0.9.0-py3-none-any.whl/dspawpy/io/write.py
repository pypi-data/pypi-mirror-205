"""
Functions to write files
"""

import json
import os

import numpy as np

from dspawpy.io.read import (_get_lammps_non_orthogonal_box, _sinfo_from_h5,
                             _sinfo_from_json, load_h5)


def write_xyz_traj(
    datafile="aimd.h5",
    ai=None,
    ele=None,
    index=None,
    xyzfile="aimdTraj.xyz",
):
    """保存xyz格式的轨迹文件

    Parameters
    ----------
    datafile : str or list
        DSPAW计算完成后保存的h5/json文件或包含它们的文件夹路径
    ai : int
        原子编号列表（体系中的第几号原子，不是质子数）
    ele : str
        元素，例如 'C'，'H'，'O'，'N'
    index : int
        优化过程中的第几步

    Returns
    -------
    xyzfile: str
        写入xyz格式的轨迹文件，默认为aimdTraj.xyz

    Example
    -------
    >>> from dspawpy.analysis.aimdtools import write_xyz_traj
    >>> write_xyz_traj(datafile='aimd.h5', ai=[1,2,3], index=1, xyzfile='aimdTraj.xyz')
    """
    if isinstance(datafile, list):
        for i, df in enumerate(datafile):
            write_xyz_traj(df, ai, ele, index, str(i + 1) + xyzfile)
        return f"{xyzfile} 文件已保存！"
    # search datafile in the given directory
    elif os.path.isdir(datafile):
        directory = datafile  # specified datafile is actually a directory
        print("您指定了一个文件夹，正在查找相关h5或json文件...")
        if os.path.exists(os.path.join(directory, "aimd.h5")):
            datafile = os.path.join(directory, "aimd.h5")
            print("Reading aimd.h5...")
        elif os.path.exists(os.path.join(directory, "aimd.json")):
            datafile = os.path.join(directory, "aimd.json")
            print("Reading aimd.json...")
        else:
            raise FileNotFoundError("未找到aimd.h5/aimd.json文件！")
    if datafile.endswith(".h5"):
        Nstep, eles, poses, lats, line6s = _sinfo_from_h5(datafile, index, ele, ai)
    elif datafile.endswith(".json"):
        Nstep, eles, poses, lats, line6s = _sinfo_from_json(datafile, index, ele, ai)
    else:
        raise TypeError("仅支持读取h5或json文件！")

    # 写入文件
    with open(xyzfile, "w") as f:
        # Nstep
        for n in range(Nstep):
            # 原子数不会变，就是不合并的元素总数
            f.write("%d\n" % len(eles))
            # lattice
            f.write(
                'Lattice="%f %f %f %f %f %f %f %f %f" Properties=species:S:1:pos:R:3 pbc="T T T"\n'
                % (
                    lats[n, 0, 0],
                    lats[n, 0, 1],
                    lats[n, 0, 2],
                    lats[n, 1, 0],
                    lats[n, 1, 1],
                    lats[n, 1, 2],
                    lats[n, 2, 0],
                    lats[n, 2, 1],
                    lats[n, 2, 2],
                )
            )
            # position and element
            for i in range(len(eles)):
                f.write(
                    "%s %f %f %f\n"
                    % (eles[i], poses[n, i, 0], poses[n, i, 1], poses[n, i, 2])
                )
    print(f"{xyzfile} 文件已保存！")


def write_dump_traj(
    datafile="aimd.h5",
    ai=None,
    ele=None,
    index=None,
    dumpfile="aimdTraj.dump",
):
    """保存为lammps的dump格式的轨迹文件，暂时只支持正交晶胞

    Parameters
    ----------
    datafile : str or list
        DSPAW计算完成后保存的h5/json文件或包含它们的文件夹路径
    ai : int
        原子编号列表（体系中的第几号原子，不是质子数）
    ele : str
        元素，例如 'C'，'H'，'O'，'N'
    index : int
        优化过程中的第几步

    Returns
    -------
    dumpfile: str
        写入dump格式的轨迹文件，默认为aimdTraj.dump

    Example
    -------
    >>> from dspawpy.analysis.aimdtools import write_dump_traj
    >>> write_dump_traj(datafile='aimd.h5', ai=[1,2,3], index=1, dumpfile='aimdTraj.dump')
    """
    if isinstance(datafile, list):
        for i, df in enumerate(datafile):
            write_dump_traj(df, ai, ele, index, str(i + 1) + dumpfile)
        return f"{dumpfile} 文件已保存！"
    # search datafile in the given directory
    elif os.path.isdir(datafile):
        directory = datafile  # specified datafile is actually a directory
        print("您指定了一个文件夹，正在查找相关h5或json文件...")
        if os.path.exists(os.path.join(directory, "aimd.h5")):
            datafile = os.path.join(directory, "aimd.h5")
            print("Reading aimd.h5...")
        elif os.path.exists(os.path.join(directory, "aimd.json")):
            datafile = os.path.join(directory, "aimd.json")
            print("Reading aimd.json...")
        else:
            raise FileNotFoundError("未找到aimd.h5/aimd.json文件！")
    if datafile.endswith(".h5"):
        Nstep, eles, poses, lats, line6s = _sinfo_from_h5(datafile, index, ele, ai)
    elif datafile.endswith(".json"):
        Nstep, eles, poses, lats, line6s = _sinfo_from_json(datafile, index, ele, ai)
    else:
        raise TypeError("仅支持读取h5或json文件！")

    # 写入文件
    with open(dumpfile, "w") as f:
        for n in range(Nstep):
            box_bounds = _get_lammps_non_orthogonal_box(lats[n])
            f.write("ITEM: TIMESTEP\n%d\n" % n)
            f.write("ITEM: NUMBER OF ATOMS\n%d\n" % (len(eles)))
            f.write("ITEM: BOX BOUNDS xy xz yz xx yy zz\n")
            f.write(
                "%f %f %f\n%f %f %f\n %f %f %f\n"
                % (
                    box_bounds[0][0],
                    box_bounds[0][1],
                    box_bounds[0][2],
                    box_bounds[1][0],
                    box_bounds[1][1],
                    box_bounds[1][2],
                    box_bounds[2][0],
                    box_bounds[2][1],
                    box_bounds[2][2],
                )
            )
            f.write("ITEM: ATOMS type x y z id\n")
            for i in range(len(eles)):
                f.write(
                    "%s %f %f %f %d\n"
                    % (eles[i], poses[n, i, 0], poses[n, i, 1], poses[n, i, 2], i + 1)
                )
    print(f"{dumpfile} 文件已保存！")


def write_VESTA(in_filename: str, data_type, out_filename="DS-PAW.vesta"):
    """从包含电子体系信息的json或h5文件中读取数据并写入VESTA格式的文件中

    Parameters
    ----------
    in_filename : str
        包含电子体系信息的json或h5文件路径
    data_type: str
        数据类型，支持 "rho", "potential", "elf", "pcharge", "boundcharge"
    out_filename : str
        输出文件路径, 默认 "DS-PAW.vesta"

    Returns
    --------
    out_filename : file
        VESTA格式的文件

    Examples
    --------
    >>> from dspawpy.io.write import write_VESTA
    >>> write_VESTA("DS-PAW.json", "rho")
    """
    if in_filename.endswith(".h5"):
        data = load_h5(in_filename)
        if data_type.lower() == "rho" or data_type.lower() == "boundcharge":
            write_VESTA_format(data, ["/Rho/TotalCharge"], out_filename)
        elif data_type.lower() == "potential":
            write_VESTA_format(
                data,
                [
                    "/Potential/TotalElectrostaticPotential",
                ],
                out_filename,
            )
        elif data_type.lower() == "elf":
            write_VESTA_format(data, ["/ELF/TotalELF"], out_filename)
        elif data_type.lower() == "pcharge":
            write_VESTA_format(data, ["/Pcharge/1/TotalCharge"], out_filename)
        else:
            raise NotImplementedError("仅支持rho/potential/elf/pcharge/boundcharge")

    elif in_filename.endswith(".json"):
        with open(in_filename, "r") as fin:
            data = json.load(fin)
        if data_type.lower() == "rho" or data_type.lower() == "boundcharge":
            write_VESTA_format_json(
                data["AtomInfo"], [data["Rho"]["TotalCharge"]], out_filename
            )
        elif data_type.lower() == "potential":
            write_VESTA_format_json(
                data["AtomInfo"],
                [
                    data["Potential"]["TotalElectrostaticPotential"],
                ],
                out_filename,
            )
        elif data_type.lower() == "elf":
            write_VESTA_format_json(
                data["AtomInfo"], [data["ELF"]["TotalELF"]], out_filename
            )
        elif data_type.lower() == "pcharge":
            write_VESTA_format_json(
                data["AtomInfo"], [data["Pcharge"][0]["TotalCharge"]], out_filename
            )
        else:
            raise NotImplementedError("仅支持rho/potential/elf/pcharge/boundcharge")

    else:
        raise NotImplementedError("仅支持json或h5格式文件")


def write_delta_rho_vesta(AB, A, B, output="delta_rho.vesta"):
    """电荷密度差分可视化

    DeviceStudio暂不支持大文件，临时写成可以用VESTA打开的格式

    Parameters
    ----------
    AB : str
        AB的电荷密度文件路径，可以是h5或json格式
    A : str
        A的电荷密度文件路径，可以是h5或json格式
    B : str
        B的电荷密度文件路径，可以是h5或json格式
    output : str
        输出文件路径，默认 "delta_rho.vesta"

    Returns
    -------
    output : file
        电荷差分（AB-A-B）后的电荷密度文件，

    Examples
    --------
    >>> from dspawpy.io.write import write_delta_rho_vesta
    >>> write_delta_rho_vesta('AB.h5', 'A.h5', 'B.h5', 'delta_rho.vesta')
    >>> write_delta_rho_vesta('AB.json', 'A.json', 'B.json', 'delta_rho.vesta')
    # 甚至可以混写
    >>> write_delta_rho_vesta('AB.h5', 'A.json', 'B.json', 'delta_rho.vesta')
    """
    print(f"读取{AB}...")
    if AB.endswith(".h5"):
        dataAB = load_h5(AB)
        rhoAB = np.array(dataAB["/Rho/TotalCharge"])
        nGrids = dataAB["/AtomInfo/Grid"]
        atom_symbol = dataAB["/AtomInfo/Elements"]
        atom_pos = dataAB["/AtomInfo/Position"]
        latticeConstantMatrix = dataAB["/AtomInfo/Lattice"]
        atom_pos = np.array(atom_pos).reshape(-1, 3)
    elif AB.endswith(".json"):
        atom_symbol = []
        atom_pos = []
        with open(AB, "r") as f1:
            dataAB = json.load(f1)
            rhoAB = np.array(dataAB["Rho"]["TotalCharge"])
            nGrids = dataAB["AtomInfo"]["Grid"]
        for i in range(len(dataAB["AtomInfo"]["Atoms"])):
            atom_symbol.append(dataAB["AtomInfo"]["Atoms"][i]["Element"])
            atom_pos.append(dataAB["AtomInfo"]["Atoms"][i]["Position"])
        atom_pos = np.array(atom_pos)

        latticeConstantMatrix = dataAB["AtomInfo"]["Lattice"]
    else:
        raise ValueError(f"file format must be either h5 or json: {AB}")

    print(f"读取{A}...")
    if A.endswith(".h5"):
        dataA = load_h5(A)
        rhoA = np.array(dataA["/Rho/TotalCharge"])
    elif A.endswith(".json"):
        with open(A, "r") as f2:
            dataA = json.load(f2)
            rhoA = np.array(dataA["Rho"]["TotalCharge"])
    else:
        raise ValueError(f"file format must be either h5 or json: {A}")

    print(f"读取{B}...")
    if B.endswith(".h5"):
        dataB = load_h5(B)
        rhoB = np.array(dataB["/Rho/TotalCharge"])
    elif B.endswith(".json"):
        with open(B, "r") as f3:
            dataB = json.load(f3)
            rhoB = np.array(dataB["Rho"]["TotalCharge"])
    else:
        raise ValueError(f"file format must be either h5 or json: {B}")

    print(f"计算电荷差分...")
    rho = rhoAB - rhoA - rhoB
    rho = np.array(rho).reshape(nGrids[0], nGrids[1], nGrids[2])

    element = list(set(atom_symbol))
    element = sorted(set(atom_symbol), key=atom_symbol.index)
    element_num = np.zeros(len(element))
    for i in range(len(element)):
        element_num[i] = atom_symbol.count(element[i])

    latticeConstantMatrix = np.array(latticeConstantMatrix)
    latticeConstantMatrix = latticeConstantMatrix.reshape(3, 3)

    print(f"写入文件{output}...")
    with open(output, "w") as out:
        out.write("DS-PAW_rho\n")
        out.write("    1.000000\n")
        for i in range(3):
            for j in range(3):
                out.write("    " + str(latticeConstantMatrix[i, j]) + "    ")
            out.write("\n")
        for i in range(len(element)):
            out.write("    " + element[i] + "    ")
        out.write("\n")

        for i in range(len(element_num)):
            out.write("    " + str(int(element_num[i])) + "    ")
        out.write("\n")
        out.write("Direct\n")
        for i in range(len(atom_pos)):
            for j in range(3):
                out.write("    " + str(atom_pos[i, j]) + "    ")
            out.write("\n")
        out.write("\n")

        for i in range(3):
            out.write("  " + str(nGrids[i]) + "  ")
        out.write("\n")

        ind = 0
        for i in range(nGrids[0]):
            for j in range(nGrids[1]):
                for k in range(nGrids[2]):
                    out.write("  " + str(rho[i, j, k]) + "  ")
                    ind = ind + 1
                    if ind % 5 == 0:
                        out.write("\n")

    print(f"成功写入 {output}")


def write_atoms(fileobj, hdf5):
    fileobj.write("DS-PAW Structure\n")
    fileobj.write("  1.00\n")
    lattice = np.asarray(hdf5["/AtomInfo/Lattice"]).reshape(-1, 1)  # 将列表lattice下的多个列表整合
    fileobj.write(
        "%10.6f %10.6f %10.6f\n" % (lattice[0][0], lattice[1][0], lattice[2][0])
    )
    fileobj.write(
        "%10.6f %10.6f %10.6f\n" % (lattice[3][0], lattice[4][0], lattice[5][0])
    )
    fileobj.write(
        "%10.6f %10.6f %10.6f\n" % (lattice[6][0], lattice[7][0], lattice[8][0])
    )

    elements = hdf5["/AtomInfo/Elements"]
    elements_set = []
    elements_number = {}
    for e in elements:
        if e in elements_set:
            elements_number[e] = elements_number[e] + 1
        else:
            elements_set.append(e)
            elements_number[e] = 1

    for e in elements_set:
        fileobj.write("  " + e)
    fileobj.write("\n")

    for e in elements_set:
        fileobj.write("%5d" % (elements_number[e]))
    fileobj.write("\n")
    if hdf5["/AtomInfo/CoordinateType"][0] == "Direct":
        fileobj.write("Direct\n")
    else:
        fileobj.write("Cartesian\n")
    for i, p in enumerate(hdf5["/AtomInfo/Position"]):
        fileobj.write("%10.6f" % p)
        if (i + 1) % 3 == 0:
            fileobj.write("\n")
    fileobj.write("\n")


def write_VESTA_format(hdf5: dict, datakeys: list, filename):
    with open(filename, "w") as file:
        write_atoms(file, hdf5)
        for key in datakeys:
            d = np.asarray(hdf5[key]).reshape(-1, 1)  # 将列表hdf5[key]下的多个列表整合
            file.write("%5d %5d %5d\n" % tuple(hdf5["/AtomInfo/Grid"]))
            i = 0
            while i < len(d):
                for j in range(10):
                    file.write("%10.5f " % d[i])
                    i += 1
                    if i >= len(d):
                        break
                file.write("\n")

            file.write("\n")


def write_atoms_json(fileobj, atom_info):
    fileobj.write("DS-PAW Structure\n")
    fileobj.write("  1.00\n")
    lattice = atom_info["Lattice"]

    fileobj.write("%10.6f %10.6f %10.6f\n" % (lattice[0], lattice[1], lattice[2]))
    fileobj.write("%10.6f %10.6f %10.6f\n" % (lattice[3], lattice[4], lattice[5]))
    fileobj.write("%10.6f %10.6f %10.6f\n" % (lattice[6], lattice[7], lattice[8]))

    elements = [atom["Element"] for atom in atom_info["Atoms"]]
    elements_set = []
    elements_number = {}
    for e in elements:
        if e in elements_set:
            elements_number[e] = elements_number[e] + 1
        else:
            elements_set.append(e)
            elements_number[e] = 1

    for e in elements_set:
        fileobj.write("  " + e)
    fileobj.write("\n")

    for e in elements_set:
        fileobj.write("%5d" % (elements_number[e]))
    fileobj.write("\n")
    if atom_info["CoordinateType"] == "Direct":
        fileobj.write("Direct\n")
    else:
        fileobj.write("Cartesian\n")
    for atom in atom_info["Atoms"]:
        fileobj.write("%10.6f %10.6f %10.6f\n" % tuple(atom["Position"]))
    fileobj.write("\n")


def write_VESTA_format_json(atom_info: dict, data: list, filename):
    with open(filename, "w") as file:
        write_atoms_json(file, atom_info)
        for d in data:
            file.write("%5d %5d %5d\n" % tuple(atom_info["Grid"]))
            i = 0
            while i < len(d):
                for j in range(10):
                    file.write("%10.5f " % d[i])
                    i += 1
                    if i >= len(d):
                        break
                file.write("\n")

            file.write("\n")
