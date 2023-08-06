"""
Functions to build structures,
"""

import json
from typing import Dict, List, Union

import h5py
import numpy as np
from pymatgen.core import Structure

from dspawpy.io.read import (_sinfo_from_h5, get_lines_without_comment,
                             get_sinfo)


def build_Structures_from_datafile(datafile: Union[str, List[str]]) -> List[Structure]:
    """读取一/多个h5/json文件，返回pymatgen的Structures列表

    Parameters
    ----------
    datafile : 字符串或字符串列表
        aimd.h5/aimd.json文件或包含任意这些文件文件夹；若给定字符串列表，将依次读取数据并合并成一个Structures列表

    Returns
    -------
    List[Structure] : pymatgen structures 列表

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import build_Structures_from_datafile
    # 读取单个文件
    >>> pymatgen_Structures = build_Structures_from_datafile(datafile='aimd1.h5')
    # 给定包含aimd.h5或aimd.json文件的文件夹位置
    >>> pymatgen_Structures = build_Structures_from_datafile(datafile='my_aimd_task')
    # 当datafile为列表时，将依次读取多个文件，合并成一个Structures列表
    >>> pymatgen_Structures = build_Structures_from_datafile(datafile=['aimd1.h5','aimd2.h5'])
    """
    dfs = []
    if isinstance(datafile, list):  # 续算模式，给的是多个文件
        dfs = datafile
    else:  # 单次计算模式，处理单个文件
        if datafile.endswith(".h5") or datafile.endswith(".json"):
            df = datafile
        else:
            raise FileNotFoundError("未找到h5或json文件！")
        dfs.append(df)

    # 读取结构数据
    pymatgen_Structures = []
    for df in dfs:
        # TODO 支持选取特定帧
        structure_list = _get_structure_list(df)
        pymatgen_Structures.extend(structure_list)

    return pymatgen_Structures


def _get_structure_list(df: str = "aimd.h5") -> List[Structure]:
    """get pymatgen structures from single datafile

    Parameters
    ----------
    df : str, optional
        datafile, by default "aimd.h5"

    Returns
    -------
    List[Structure] : list of pymatgen structures

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import get_structure_list
    >>> structure_list = get_structure_list(df='aimd.h5')
    """

    # create Structure structure_list from aimd.h5
    Nstep, elements, positions, lattices, D_mag_fix = get_sinfo(df)
    strs = []
    for i in range(Nstep):
        strs.append(
            Structure(
                lattices[i],
                elements,
                positions[i],
                coords_are_cartesian=False,
                site_properties={
                    "Mags": D_mag_fix["Mags"][i],
                    "AtomFixs": D_mag_fix["AtomFixs"][i],
                },
            )
        )

    return strs


def from_dspaw_as(as_file: str = "structure.as") -> Structure:
    """从DSPAW的as结构文件中读取结构信息

    Parameters
    ----------
    as_file : str
        DSPAW的as结构文件, 默认'structure.as'

    Returns
    -------
    Structure
        pymatgen的Structure对象

    Examples
    --------
    >>> from dspawpy.io.structure import from_dspaw_as
    >>> S1 = from_dspaw_as(as_file='structure00.as')
    """
    D = {}
    lines = get_lines_without_comment(as_file, "#")
    N = int(lines[1])
    lattice = []
    for line in lines[3:6]:
        vector = line.split()
        lattice.extend([float(vector[0]), float(vector[1]), float(vector[2])])

    lattice = np.asarray(lattice).reshape(3, 3)
    is_direct = lines[6].strip().split()[0].startswith("Direct")
    elements = []
    positions = []
    others = []
    line6s = []  # Cartesian/Direct Mag Fix_x ...
    for i in range(N):
        atom = lines[i + 7].strip().split()
        elements.append(atom[0])
        positions.extend([float(atom[1]), float(atom[2]), float(atom[3])])

        if len(atom) > 4:
            other = atom[4:]
            others.append(other)
            line6 = lines[6]
            line6s.append(line6)

    D.setdefault("others", others)
    D.setdefault("line6s", line6s)

    coords = np.asarray(positions).reshape(-1, 3)
    if others == [] and line6s == []:
        return Structure(
            lattice, elements, coords, coords_are_cartesian=(not is_direct)
        )
    else:
        return Structure(
            lattice,
            elements,
            coords,
            coords_are_cartesian=(not is_direct),
            site_properties=D,
        )


def from_hzw(hzw_file) -> Structure:
    """从hzw结构文件中读取结构信息

    Parameters
    ----------
    hzw_file : str
        hzw结构文件，以 .hzw 结尾

    Returns
    -------
    Structure
        pymatgen的Structure对象

    Examples
    --------
    >>> from dspawpy.io.structure import from_hzw
    >>> S1 = from_hzw(hzw_file='Si.hzw')
    """
    lines = get_lines_without_comment(hzw_file, "%")
    number_of_probes = int(lines[0])
    if number_of_probes != 0:
        raise ValueError("dspaw only support 0 probes hzw file")
    lattice = []
    for line in lines[1:4]:
        vector = line.split()
        lattice.extend([float(vector[0]), float(vector[1]), float(vector[2])])

    lattice = np.asarray(lattice).reshape(3, 3)
    N = int(lines[4])
    elements = []
    positions = []
    for i in range(N):
        atom = lines[i + 5].strip().split()
        elements.append(atom[0])
        positions.extend([float(atom[1]), float(atom[2]), float(atom[3])])

    coords = np.asarray(positions).reshape(-1, 3)
    return Structure(lattice, elements, coords, coords_are_cartesian=True)


def to_file(structure: Structure, filename: str, fmt, coords_are_cartesian=True):
    """往结构文件中写入信息

    Parameters
    ----------
    structure : Structure
        pymatgen的Structure对象
    filename : str
        结构文件名
    fmt : str
        结构文件类型，支持 "json","as","hzw"
    coords_are_cartesian : bool
        坐标是否为笛卡尔坐标，默认为True

    Examples
    --------
    >>> from dspawpy.io.structure import to_file
    >>> to_file(structure, filename='Si.json', fmt='json')
    >>> to_file(structure, filename='Si.as', fmt='as')
    >>> to_file(structure, filename='Si.hzw', fmt='hzw')
    """
    if fmt == "json":
        to_dspaw_json(structure, filename, coords_are_cartesian)
    elif fmt == "as":
        to_dspaw_as(structure, filename, coords_are_cartesian)
    elif fmt == "hzw":
        to_hzw(structure, filename)


def from_dspaw_atominfo(hpath, index: int = None) -> Structure:
    if not isinstance(hpath, str):  # for compatibility with aimd2pdb.py
        atominfo = hpath
        lattice = np.asarray(atominfo["Lattice"]).reshape(3, 3)
        elements = []
        positions = []
        for atom in atominfo["Atoms"]:
            elements.append(atom["Element"])
            positions.extend(atom["Position"])

        coords = np.asarray(positions).reshape(-1, 3)
        is_direct = atominfo["CoordinateType"] == "Direct"
        return Structure(
            lattice, elements, coords, coords_are_cartesian=(not is_direct)
        )
    Nstep, elements, positions, lattices = _sinfo_from_h5(hpath, index)
    return Structure(lattices[0], elements, positions[0], coords_are_cartesian=True)


def from_dspaw_atominfo_json(atominfo: dict) -> Structure:
    lattice = np.asarray(atominfo["Lattice"]).reshape(3, 3)
    elements = []
    positions = []
    for atom in atominfo["Atoms"]:
        elements.append(atom["Element"])
        positions.extend(atom["Position"])

    coords = np.asarray(positions).reshape(-1, 3)
    is_direct = atominfo["CoordinateType"] == "Direct"
    return Structure(lattice, elements, coords, coords_are_cartesian=(not is_direct))


def from_dspaw_atominfos(aimd_dir: str) -> List[Structure]:
    structures = []
    if isinstance(aimd_dir, list) or isinstance(aimd_dir, np.ndarray):
        for atominfo in aimd_dir:
            structures.append(from_dspaw_atominfo(atominfo))
    elif aimd_dir.endswith(".h5"):
        aimd = h5py.File(aimd_dir)
        steps = int(np.array(aimd.get("/Structures/FinalStep"))[0])
        for i in range(steps):
            structures.append(from_dspaw_atominfo(aimd_dir, i + 1))
    elif aimd_dir.endswith(".json"):
        with open(aimd_dir, "r") as fin:
            aimd = json.load(fin)
        for atominfo in aimd["Structures"]:
            structures.append(from_dspaw_atominfo_json(atominfo))
    else:
        print("file - " + aimd_dir + " :  Unsupported format!")
        return

    return structures


def to_dspaw_as(structure: Structure, filename: str, coords_are_cartesian=True):
    """write dspaw as file
    If converted from as file, will copy the mag and fix info,
        otherwise, those info will be ignored!
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Total number of atoms\n")
        file.write("%d\n" % len(structure))

        file.write("Lattice\n")
        for v in structure.lattice.matrix:
            file.write("%.6f %.6f %.6f\n" % (v[0], v[1], v[2]))

        i = 0
        for site in structure:
            if i == 0:
                if "line6s" in site.properties:
                    file.write("%s\n" % site.properties["line6s"])
                else:
                    if coords_are_cartesian:
                        file.write("Cartesian\n")
                    else:
                        file.write("Direct\n")
            i += 1

            coords = site.coords if coords_are_cartesian else site.frac_coords
            if "others" in site.properties:
                sp = " ".join(site.properties["others"])  # flatten str list
                file.write(
                    "%s %.6f %.6f %.6f %s\n"
                    % (site.species_string, coords[0], coords[1], coords[2], sp)
                )
            else:  # the most common case
                file.write(
                    "%s %.6f %.6f %.6f\n"
                    % (site.species_string, coords[0], coords[1], coords[2])
                )


def to_hzw(structure: Structure, filename: str):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("% The number of probes \n")
        file.write("0\n")
        file.write("% Uni-cell vector\n")

        for v in structure.lattice.matrix:
            file.write("%.6f %.6f %.6f\n" % (v[0], v[1], v[2]))

        file.write("% Total number of device_structure\n")
        file.write("%d\n" % len(structure))
        file.write("% Atom site\n")

        for site in structure:
            file.write(
                "%s %.6f %.6f %.6f\n"
                % (site.species_string, site.coords[0], site.coords[1], site.coords[2])
            )


def to_dspaw_dict(structure: Structure, coords_are_cartesian=True) -> Dict:
    lattice = structure.lattice.matrix.flatten().tolist()
    atoms = []
    for site in structure:
        coords = site.coords if coords_are_cartesian else site.frac_coords
        atoms.append({"Element": site.species_string, "Position": coords.tolist()})

    coordinate_type = "Cartesian" if coords_are_cartesian else "Direct"
    return {"Lattice": lattice, "CoordinateType": coordinate_type, "Atoms": atoms}


def to_dspaw_json(structure: Structure, filename: str, coords_are_cartesian=True):
    d = to_dspaw_dict(structure, coords_are_cartesian)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(d, file, indent=4)


def to_pdb(structures: List[Structure], pdb_filename: str):
    with open(pdb_filename, "w", encoding="utf-8") as file:
        for i, s in enumerate(structures):
            file.write("MODEL         %d\n" % (i + 1))
            file.write("REMARK   Converted from Structures\n")
            file.write("REMARK   Converted using dspawpy\n")
            lengths = s.lattice.lengths
            angles = s.lattice.angles
            file.write(
                "CRYST1{0:9.3f}{1:9.3f}{2:9.3f}{3:7.2f}{4:7.2f}{5:7.2f}\n".format(
                    lengths[0], lengths[1], lengths[2], angles[0], angles[1], angles[2]
                )
            )
            for j, site in enumerate(s):
                file.write(
                    "%4s%7d%4s%5s%6d%4s%8.3f%8.3f%8.3f%6.2f%6.2f%12s\n"
                    % (
                        "ATOM",
                        j + 1,
                        site.species_string,
                        "MOL",
                        1,
                        "    ",
                        site.coords[0],
                        site.coords[1],
                        site.coords[2],
                        1.0,
                        0.0,
                        site.species_string,
                    )
                )
            file.write("TER\n")
            file.write("ENDMDL\n")
