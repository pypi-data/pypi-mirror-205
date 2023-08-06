"""
Functions to build structures
"""

from typing import List, Union

import numpy as np
from pymatgen.core import Structure

from dspawpy.io.read import get_lines_without_comment, get_sinfo


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
        if (
            datafile.endswith(".h5")
            or datafile.endswith(".json")
            or datafile.endswith(".as")
        ):
            df = datafile
        else:
            raise FileNotFoundError("未找到h5或json文件！")
        dfs.append(df)

    # 读取结构数据
    pymatgen_Structures = []
    for df in dfs:
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
        if D_mag_fix:
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
        else:
            strs.append(
                Structure(
                    lattices[i],
                    elements,
                    positions[i],
                    coords_are_cartesian=False,
                )
            )
    return strs


def _from_dspaw_as(as_file: str = "structure.as") -> Structure:
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


def _from_hzw(hzw_file) -> Structure:
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
