"""
Functions to read properties from structure or output files
"""

import json
import os
import re

import h5py
import numpy as np
from pymatgen.core.lattice import Lattice
from pymatgen.core.structure import Structure
from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine
from pymatgen.electronic_structure.core import Orbital, Spin
from pymatgen.electronic_structure.dos import CompleteDos, Dos
from pymatgen.phonon.bandstructure import PhononBandStructureSymmLine
from pymatgen.phonon.dos import PhononDos


def get_lines_without_comment(filename: str, comment: str = "#"):
    lines = []
    """Filter out comment lines"""
    with open(filename) as file:
        while True:
            line = file.readline()
            if line:
                line = re.sub(comment + r".*$", "", line)  # remove comment
                line = line.strip()
                if line:
                    lines.append(line)
            else:
                break

    return lines


def get_ele_from_h5(hpath: str = "aimd.h5"):
    """从h5文件中读取元素列表；
    多离子步并不会在每个离子步的Structure中保存元素信息，只能读取初始结构的元素信息

    Parameters
    ----------
    hpath : str
        h5文件路径

    Returns
    -------
    ele : list
        元素列表, Natom x 1

    Examples
    --------
    >>> from dspawpy.io.utils import get_ele_from_h5
    >>> ele = get_ele_from_h5(hpath='aimd.h5')
    ['H', 'H', 'O']
    """
    data = h5py.File(hpath)
    Elements_bytes = np.array(data.get("/AtomInfo/Elements"))
    tempdata = np.array([i.decode() for i in Elements_bytes])
    ele = "".join(tempdata).split(";")

    return ele


def get_sinfo(datafile: str, scaled=False, index=None, ele=None, ai=None):
    """Wrapper to get structure information from h5/json/as file

    从datafile中读取结构信息

    Parameters
    ----------
    datafile : str
        h5文件或json结果文件路径
    scaled : bool, optional
        是否返回分数坐标，默认False
    index : int or list or str, optional
        运动轨迹中的第几步，从1开始计数
        如果要切片，用字符串写法： '1, 10'
        默认为None，返回所有步
    ele : list, optional
        元素列表, Natom x 1
        默认为None，从h5文件中读取
    ai : int or list or str, optional
        多离子步中的第几个离子步，从1开始计数
        如果要切片，用字符串写法： '1, 10'
        默认为None，返回所有离子步

    Returns
    -------
    Nstep : int
        总离子步数（几个构型）
    pos : np.ndarray
        坐标分量数组，Natom x 3
    ele : list
        元素列表, Natom x 1
    latv : np.ndarray
        晶胞矢量数组，3 x 3
    D_mag_fix : dict
        磁矩、自由度相关信息

    Examples
    --------
    >>> from dspawpy.io.read import get_sinfo
    """
    if datafile.endswith(".h5"):
        assert os.path.exists(datafile), f"{os.path.abspath(datafile)} does not exist!"
        Nstep, eles, pos, latv, D_mag_fix = _sinfo_from_h5(
            hpath=datafile, index=index, ele=ele, ai=ai, return_scaled=scaled
        )
    elif datafile.endswith(".json"):
        assert os.path.exists(datafile), f"{os.path.abspath(datafile)} does not exist!"
        Nstep, eles, pos, latv, D_mag_fix = _sinfo_from_json(
            jpath=datafile, return_scaled=scaled
        )
    else:
        raise ValueError("datafile must be .h5 / .json file!")

    return Nstep, eles, pos, latv, D_mag_fix


def pel_from_as(spath: str, scaled=False):
    """Extract structure information from .as file

    从DSPAW的as结构文件中读取坐标、元素列表，和晶胞信息

    Parameters
    ----------

    spath : str
        结构文件路径

    Returns
    -------

    pos : np.ndarray
        坐标分量数组，Natom x 3
    ele : list
        元素列表, Natom x 1
    latv : np.ndarray
        晶胞矢量数组，3 x 3

    Examples
    --------

    >>> from dspawpy.io.read import pel_from_as
    >>> pos, ele, latv = pel_from_as(spath='structure.as', scaled=False)
    >>> pos
    array([[ 0.        ,  0.        ,  9.06355632],
           [ 1.59203323,  0.91916082, 10.62711265],
           [ 1.59203323,  0.91916082,  7.5       ]])
    >>> ele
    ['Mo', 'S', 'S']
    >>> latv
    array([[ 3.18406646,  0.        ,  0.        ],
           [-1.59203323,  2.75748245,  0.        ],
           [ 0.        ,  0.        , 30.        ]])

    if scaled=True, return scaled coordinates
    >>> spos, ele, latv = pel_from_as(spath='structure.as', scaled=True)
    >>> spos
    array([[0.        , 0.        , 0.30211854],
           [0.66666667, 0.33333333, 0.35423709],
           [0.66666667, 0.33333333, 0.25      ]])
    >>> ele
    ['Mo', 'S', 'S']
    >>> latv
    array([[ 3.18406646,  0.        ,  0.        ],
           [-1.59203323,  2.75748245,  0.        ],
           [ 0.        ,  0.        , 30.        ]])
    """
    with open(spath, "r") as f:
        lines = f.readlines()
        Natom = int(lines[1])  # 原子总数
        ele = [line.split()[0] for line in lines[7 : 7 + Natom]]  # 元素列表

        # 晶格矢量
        latv = np.array([line.split()[0:3] for line in lines[3:6]], dtype=float)
        # xyz坐标分量
        coord = np.array(
            [line.split()[1:4] for line in lines[7 : 7 + Natom]], dtype=float
        )
        # coordinates type
        if lines[6].startswith("C"):  # 笛卡尔 --> 分数坐标
            spos = np.linalg.solve(latv.T, np.transpose(coord)).T
        elif lines[6].startswith("D"):
            spos = coord
        else:
            raise ValueError(f"{spath}中的坐标类型未知！")

        if scaled:
            pos = spos
        else:
            pos = np.dot(spos, latv)

    return pos, ele, latv


def _sinfo_from_h5(
    hpath: str,
    index=None,
    ele=None,
    ai=None,
    return_scaled: bool = False,
):
    print(f"Reading {os.path.abspath(hpath)} ...")
    hf = h5py.File(hpath)  # 加载h5文件
    Total_step = len(np.array(hf.get("/Structures"))) - 2  # 总步数

    if ele is not None and ai is not None:
        raise ValueError("暂不支持同时指定元素和原子序号")
    # 步数
    if index is not None:
        if isinstance(index, int):  # 1
            indices = [index]

        elif isinstance(index, list) or isinstance(ai, np.ndarray):  # [1,2,3]
            indices = index

        elif isinstance(index, str):  # ':', '-3:'
            indices = __parse_indices(index, Total_step)

        else:
            raise ValueError("请输入正确格式的index")

        Nstep = len(indices)
    else:
        Nstep = Total_step
        indices = list(range(1, Nstep + 1))

    # 读取元素列表，这个列表不会随步数改变，也不会“合并同类项”
    Elements = np.array(get_ele_from_h5(hpath), dtype=object)

    # 开始读取晶胞和原子位置
    lattices = np.empty((Nstep, 3, 3))  # Nstep x 3 x 3
    location = []
    if ele is not None:  # 如果用户指定元素
        if isinstance(ele, str):  # 单个元素符号，例如 'Fe'
            ele_list = np.array(ele, dtype=object)
            location = np.where(Elements == ele_list)[0]
        # 多个元素符号组成的列表，例如 ['Fe', 'O']
        elif isinstance(ele, list) or isinstance(ele, np.ndarray):
            for e in ele:
                loc = np.where(Elements == e)[0]
                location.append(loc)
            location = np.concatenate(location)
        else:
            raise TypeError("请输入正确的元素或元素列表")
        elements = Elements[location]

    elif ai is not None:  # 如果用户指定原子序号
        if isinstance(ai, int):  # 1
            ais = [ai]
        elif isinstance(ai, list) or isinstance(ai, np.ndarray):  # [1,2,3]
            ais = ai
        elif isinstance(ai, str):  # ':', '-3:'
            ais = __parse_indices(ai, Total_step)
        else:
            raise ValueError("请输入正确格式的ai")
        ais = [i - 1 for i in ais]  # python从0开始计数，但是用户从1开始计数
        elements = Elements[ais]
        location = ais

    else:  # 如果都没指定
        elements = Elements
        location = list(range(len(Elements)))

    elements = elements.tolist()  # for pretty output

    mags = []  # must be Nstep x Natom x ?

    poses = np.empty(shape=(len(indices), len(elements), 3))
    for i, ind in enumerate(indices):  # 步数
        lats = np.array(hf.get("/Structures/Step-" + str(ind) + "/Lattice"))
        lattices[i] = lats
        # [x1,y1,z1,x2,y2,z2,x3,y3,z3], ...
        # 结构优化时输出的都是分数坐标，不管CoordinateType写的是啥！
        pos = np.array(hf.get("/Structures/Step-" + str(ind) + "/Position"))
        wrapped_pos = pos - np.floor(pos)  # wrap into [0,1)
        wrapped_pos = wrapped_pos.flatten().reshape(-1, 3).T  # reshape

        try:  # 自旋计算
            mag = np.array(hf.get("/Structures/Step-" + str(ind) + "/Mag"))
            if mag == None:
                mag = np.zeros(shape=(len(elements), 1))
        except Exception as e:
            print(e)
            mag = np.zeros(shape=(len(elements), 1))
        mags.append(mag)

    try:  # fix atom
        atomfixs = np.array(hf.get("/AtomInfo/Fix")).astype(bool).flatten()
        assert atomfixs.shape == (12,)  # np.ndarray (Natom x 3, )
        atomfixs = atomfixs.reshape(-1, 3)  # (Natom, 3)
    except Exception as e:
        print(e)
        atomfixs = np.full(shape=(len(elements), 3), fill_value=False)

    mags = np.array(mags).reshape(Nstep, len(elements), -1)
    # repeat atomfixs to Nstep x Natom x 3
    atomfixs = np.repeat(atomfixs[np.newaxis, :, :], Nstep, axis=0).tolist()

    D_mag_fix = {"Mags": mags, "AtomFixs": atomfixs}
    print(
        f"This function does not handle lattice fix info, \n you must manually set it before starting new calculations.."
    )

    if return_scaled:  # Fractional coordinates
        for i, ind in enumerate(indices):  # 步数
            for j, sli in enumerate(location):
                poses[i, j, :] = np.dot(wrapped_pos[:, sli], np.eye(3, 3))
    else:  # Cartesian coordinates
        for i, ind in enumerate(indices):  # 步数
            for j, sli in enumerate(location):
                poses[i, j, :] = np.dot(wrapped_pos[:, sli], lats)

    return Nstep, elements, poses, lattices, D_mag_fix


def _sinfo_from_json(
    jpath: str,
    index=None,
    ele=None,
    ai=None,
    return_scaled=False,
):
    """从json指定的路径读取结构相关数据

    输入:
    - jpath: json文件路径
    - ai: 原子序号（体系中的第几个原子，不是质子数）
    - ele: 元素，例如 'C'，'H'，'O'，'N'
    - index: 运动轨迹中的第几步，从1开始

    输出：
    - Nstep: 总共要保存多少步的信息, int
    - elements: 元素列表, list, Natom x 1
    - positions: 原子位置, list, Nstep x Natom x 3
    - lattices: 晶胞, list, Nstep x 3 x 3
    """
    print(f"Reading {os.path.abspath(jpath)}...")
    with open(jpath, "r") as f:
        data = json.load(f)  # 加载json文件

    if "Structures" in data:
        Total_step = len(data["Structures"])  # aimd.json
    else:
        Total_step = len(data)  # relax.json, neb01.json

    if ele is not None and ai is not None:
        raise ValueError("暂不支持同时指定元素和原子序号")
    # 步数
    if index is not None:
        if isinstance(index, int):  # 1
            indices = [index]

        elif isinstance(index, list) or isinstance(ai, np.ndarray):  # [1,2,3]
            indices = index

        elif isinstance(index, str):  # ':', '-3:'
            indices = __parse_indices(index, Total_step)

        else:
            raise ValueError("请输入正确格式的index")

        Nstep = len(indices)
    else:
        Nstep = Total_step
        indices = list(range(1, Nstep + 1))  # [1,Nstep+1)

    # 预先读取全部元素的总列表，这个列表不会随步数改变，也不会“合并同类项”
    # 这样可以避免在循环内部频繁判断元素是否符合用户需要

    if "Structures" in data:
        Nele = len(data["Structures"][0]["Atoms"])  # relax.json
        total_elements = np.empty(shape=(Nele), dtype=object)  # 未合并的元素列表
        for i in range(Nele):
            element = data["Structures"][0]["Atoms"][i]["Element"]
            total_elements[i] = element
    else:
        Nele = len(data[0]["Atoms"])
        total_elements = np.empty(shape=(Nele), dtype=object)  # 未合并的元素列表
        for i in range(Nele):
            element = data[0]["Atoms"][i]["Element"]
            total_elements[i] = element

    Natom = len(total_elements)

    # 开始读取晶胞和原子位置
    # 在data['Structures']['%d' % index]['Atoms']中根据元素所在序号选择结构
    if ele is not None:  # 用户指定要某些元素
        location = []
        if isinstance(ele, str):  # 单个元素符号，例如 'Fe'
            ele_list = list(ele)
        # 多个元素符号组成的列表，例如 ['Fe', 'O']
        elif isinstance(ele, list) or isinstance(ele, np.ndarray):
            ele_list = ele
        else:
            raise TypeError("请输入正确的元素或元素列表")
        for e in ele_list:
            location.append(np.where(total_elements == e)[0])
        location = np.concatenate(location)

    elif ai is not None:  # 如果用户指定原子序号，也要据此筛选元素列表
        if isinstance(ai, int):  # 1
            ais = [ai]
        elif isinstance(ai, list) or isinstance(ai, np.ndarray):  # [1,2,3]
            ais = ai
        elif isinstance(ai, str):  # ':', '-3:'
            ais = __parse_indices(ai, Total_step)
        else:
            raise ValueError("请输入正确格式的ai")
        ais = [i - 1 for i in ais]  # python从0开始计数，但是用户从1开始计数
        location = ais
        # read lattices and poses

    else:  # 如果都没指定
        location = list(range(Natom))

    # 满足用户需要的elements列表
    elements = np.empty(shape=(Natom,), dtype=object)
    for i in range(len(location)):
        elements[i] = total_elements[location[i]]

    # Nstep x Natom x 3, positions are all fractional
    positions = np.empty(shape=(len(indices), len(elements), 3))
    lattices = np.empty(shape=(Nstep, 3, 3))  # Nstep x 3 x 3
    mags = []  # Nstep x Natom x ?
    Atomfixs = []  # Nstep x Natom x 3

    if "Structures" in data:  # relax.json
        for i, ind in enumerate(indices):  # for every ionic step
            lat = data["Structures"][ind - 1]["Lattice"]
            lattices[i] = np.array(lat).reshape(3, 3)
            mag_for_each_step = []
            fix_for_each_step = []
            for j, sli in enumerate(location):
                ati = data["Structures"][ind - 1]["Atoms"][sli]
                positions[i, j, :] = ati["Position"][:]

                mag_for_each_atom = ati["Mag"][:]
                mag_for_each_step.append(mag_for_each_atom)

                fix_for_each_atom = ati["Fix"][:]
                if fix_for_each_atom == []:
                    fix_for_each_atom = [0, 0, 0]
                fix_for_each_atom = [bool(i) for i in fix_for_each_atom]
                fix_for_each_step.append(fix_for_each_atom)

            mags.append(mag_for_each_step)
            Atomfixs.append(fix_for_each_step)
            if not return_scaled:
                positions = np.dot(positions, lattices[i])
    else:
        for i, ind in enumerate(indices):  # for every ionic step
            lat = data[ind - 1]["Lattice"]
            lattices[i] = np.array(lat).reshape(3, 3)
            mag_for_each_step = []
            fix_for_each_step = []
            for j, sli in enumerate(location):
                ati = data[ind - 1]["Atoms"][sli]
                positions[i, j, :] = ati["Position"][:]

                mag_for_each_atom = ati["Mag"][:]
                mag_for_each_step.append(mag_for_each_atom)

                fix_for_each_atom = ati["Fix"][:]
                if fix_for_each_atom == []:
                    fix_for_each_atom = [0, 0, 0]
                fix_for_each_atom = [bool(i) for i in fix_for_each_atom]
                fix_for_each_step.append(fix_for_each_atom)

            mags.append(mag_for_each_step)
            Atomfixs.append(fix_for_each_step)
            if not return_scaled:
                positions = np.dot(positions, lattices[i])

    elements = elements.tolist()
    Mags = np.array(mags)  # (Nstep, Natom, ?) or (Nstep, 0,)

    D_mag_fix = {"Mags": Mags, "AtomFixs": Atomfixs}
    print(
        f"This function does not handle lattice fix info, \n you must manually set it before starting new calculations.."
    )

    return Nstep, elements, positions, lattices, D_mag_fix


def __parse_indices(index: str, total_step) -> list:
    """解析用户输入的原子序号字符串

    输入：
        - index: 用户输入的原子序号/元素字符串，例如 '1:3,5,7:10'
    输出：
        - indices: 解析后的原子序号列表，例如 [1,2,3,4,5,6,7,8,9,10]
    """
    assert ":" in index, "如果不想切片索引，请输入整数或者列表"
    blcs = index.split(",")
    indices = []
    for blc in blcs:
        if ":" in blc:  # 切片
            low = blc.split(":")[0]
            if not low:
                low = 1  # 从1开始
            else:
                low = int(low)
                assert low > 0, "索引从1开始！"
            high = blc.split(":")[1]
            if not high:
                high = total_step
            else:
                high = int(high)
                assert high <= total_step, "索引超出范围！"

            for i in range(low, high + 1):
                indices.append(i)
        else:  # 单个数字
            indices.append(int(blc))
    return indices


def _get_lammps_non_orthogonal_box(lat: np.ndarray):
    """计算用于输入lammps的盒子边界参数，用于生成dump结构文件

    Parameters
    ----------
    lat : np.ndarray
        常见的非三角3x3矩阵

    Returns
    -------
    box_bounds:
        用于输入lammps的盒子边界
    """
    # https://docs.lammps.org/Howto_triclinic.html
    A = lat[0]
    B = lat[1]
    C = lat[2]
    assert np.cross(A, B).dot(C) > 0, "Lat is not right handed"

    # 将常规3x3矩阵转成标准的上三角矩阵
    alpha = np.arccos(np.dot(B, C) / (np.linalg.norm(B) * np.linalg.norm(C)))
    beta = np.arccos(np.dot(A, C) / (np.linalg.norm(A) * np.linalg.norm(C)))
    gamma = np.arccos(np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B)))

    ax = np.linalg.norm(A)
    a = np.array([ax, 0, 0])

    bx = np.linalg.norm(B) * np.cos(gamma)
    by = np.linalg.norm(B) * np.sin(gamma)
    b = np.array([bx, by, 0])

    cx = np.linalg.norm(C) * np.cos(beta)
    cy = (np.linalg.norm(B) * np.linalg.norm(C) - bx * cx) / by
    cz = np.sqrt(abs(np.linalg.norm(C) ** 2 - cx**2 - cy**2))
    c = np.array([cx, cy, cz])

    # triangluar matrix in lammmps cell format
    # note that in OVITO, it will be down-triangular one
    # lammps_lattice = np.array([a,b,c]).T

    # write lammps box parameters
    # https://docs.lammps.org/Howto_triclinic.html#:~:text=The%20inverse%20relationship%20can%20be%20written%20as%20follows
    lx = np.linalg.norm(a)
    xy = np.linalg.norm(b) * np.cos(gamma)
    xz = np.linalg.norm(c) * np.cos(beta)
    ly = np.sqrt(np.linalg.norm(b) ** 2 - xy**2)
    yz = (np.linalg.norm(b) * np.linalg.norm(c) * np.cos(alpha) - xy * xz) / ly
    lz = np.sqrt(np.linalg.norm(c) ** 2 - xz**2 - yz**2)

    # "The parallelepiped has its “origin” at (xlo,ylo,zlo) and is defined by 3 edge vectors starting from the origin given by a = (xhi-xlo,0,0); b = (xy,yhi-ylo,0); c = (xz,yz,zhi-zlo)."
    # 令原点在(0,0,0)，则 xlo = ylo = zlo = 0
    xlo = ylo = zlo = 0
    # https://docs.lammps.org/Howto_triclinic.html#:~:text=the%20LAMMPS%20box%20sizes%20(lx%2Cly%2Clz)%20%3D%20(xhi%2Dxlo%2Cyhi%2Dylo%2Czhi%2Dzlo)
    xhi = lx + xlo
    yhi = ly + ylo
    zhi = lz + zlo
    # https://docs.lammps.org/Howto_triclinic.html#:~:text=This%20bounding%20box%20is%20convenient%20for%20many%20visualization%20programs%20and%20is%20calculated%20from%20the%209%20triclinic%20box%20parameters%20(xlo%2Cxhi%2Cylo%2Cyhi%2Czlo%2Czhi%2Cxy%2Cxz%2Cyz)%20as%20follows%3A
    xlo_bound = xlo + np.min([0, xy, xz, xy + xz])
    xhi_bound = xhi + np.max([0, xy, xz, xy + xz])
    ylo_bound = ylo + np.min([0, yz])
    yhi_bound = yhi + np.max([0, yz])
    zlo_bound = zlo
    zhi_bound = zhi
    box_bounds = np.array(
        [
            [xlo_bound, xhi_bound, xy],
            [ylo_bound, yhi_bound, xz],
            [zlo_bound, zhi_bound, yz],
        ]
    )

    return box_bounds


def load_h5(dir_h5: str) -> dict:
    """遍历读取h5文件中的数据，保存为字典格式

    慎用此函数，因为会读取很多不需要的数据，耗时很长。

    Parameters
    ----------
    dir_h5 : str
        h5文件路径

    Returns
    -------
    datas: dict
        数据字典

    Examples
    --------
    >>> from dspawpy.io.read import load_h5
    >>> datas = load_h5(dir_h5)
    """

    def get_names(key, h5_object):
        names.append(h5_object.name)

    def is_dataset(name):
        for name_inTheList in names:
            if name_inTheList.find(name + "/") != -1:
                return False
        return True

    def get_datas(key, h5_object):
        if is_dataset(h5_object.name):
            data = np.asarray(h5_object)
            if data.dtype == "|S1":  # 转成字符串 并根据";"分割
                byte2str = [str(bi, "utf-8") for bi in data]
                string = ""
                for char in byte2str:
                    string += char
                data = np.array([elem for elem in string.strip().split(";")])
            # "/group1/group2/.../groupN/dataset" : value
            datas[h5_object.name] = data.tolist()

    with h5py.File(dir_h5, "r") as fin:
        names = []
        datas = {}
        fin.visititems(get_names)
        fin.visititems(get_datas)

        return datas


def load_h5_todict(dir_h5: str) -> dict:
    """与上一个函数区别在于合并了部分同类数据，例如

    /Structures/Step-1/* 和 /Structures/Step-2/* 并入 /Structures/ 组内
    """

    def create_dict(L: list, D: dict):
        if len(L) == 2:
            D[L[0]] = L[1]
            return
        else:
            if not (L[0] in D.keys()):
                D[L[0]] = {}
            create_dict(L[1:], D[L[0]])

    datas = load_h5(dir_h5)

    groups_value_list = []
    for key in datas.keys():
        tmp_list = key[1:].strip().split("/")  # [1:] 截去root
        tmp_list.append(datas[key])
        # groups_value_list[i]结构: [group1, group2, ..., groupN, dataset, value]
        groups_value_list.append(tmp_list)

    groups_value_dict = {}
    for data in groups_value_list:
        create_dict(data, groups_value_dict)

    return groups_value_dict


def get_dos_data(dos_dir: str):
    if dos_dir.endswith(".h5"):
        dos = load_h5(dos_dir)
        if dos["/DosInfo/Project"][0]:
            return get_complete_dos(dos)
        else:
            return get_total_dos(dos)

    elif dos_dir.endswith(".json"):
        with open(dos_dir, "r") as fin:
            dos = json.load(fin)

        if dos["DosInfo"]["Project"]:
            return get_complete_dos_json(dos)
        else:
            return get_total_dos_json(dos)

    else:
        print("file - " + dos_dir + " :  Unsupported format!")
        return


def get_total_dos(dos: dict) -> Dos:
    # h5 -> Dos Obj
    energies = np.asarray(dos["/DosInfo/DosEnergy"])
    if dos["/DosInfo/SpinType"][0] == "none":
        densities = {Spin.up: np.asarray(dos["/DosInfo/Spin1/Dos"])}
    else:
        densities = {
            Spin.up: np.asarray(dos["/DosInfo/Spin1/Dos"]),
            Spin.down: np.asarray(dos["/DosInfo/Spin2/Dos"]),
        }

    efermi = dos["/DosInfo/EFermi"][0]

    return Dos(efermi, energies, densities)


def get_complete_dos(dos: dict) -> CompleteDos:
    # h5 -> CompleteDos Obj
    total_dos = get_total_dos(dos)
    structure = get_structure(dos, "/AtomInfo")
    N = len(structure)
    pdos = [{} for i in range(N)]
    number_of_spin = 1 if dos["/DosInfo/SpinType"][0] == "none" else 2

    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down
        atomindexs = dos["/DosInfo/" + spin_key + "/ProjectDos/AtomIndexs"][0]
        orbitindexs = dos["/DosInfo/" + spin_key + "/ProjectDos/OrbitIndexs"][0]
        for atom_index in range(atomindexs):
            for orbit_index in range(orbitindexs):
                orbit_name = Orbital(orbit_index)
                Contribution = dos[
                    "/DosInfo/"
                    + spin_key
                    + "/ProjectDos"
                    + str(atom_index + 1)
                    + "/"
                    + str(orbit_index + 1)
                ]
                if orbit_name in pdos[atom_index].keys():
                    pdos[atom_index][orbit_name].update({spin: Contribution})
                else:
                    pdos[atom_index][orbit_name] = {spin: Contribution}

    pdoss = {structure[i]: pd for i, pd in enumerate(pdos)}

    return CompleteDos(structure, total_dos, pdoss)


def get_total_dos_json(dos: dict) -> Dos:
    # json -> Dos Obj
    energies = np.asarray(dos["DosInfo"]["DosEnergy"])
    if dos["DosInfo"]["SpinType"] == "none":
        densities = {Spin.up: np.asarray(dos["DosInfo"]["Spin1"]["Dos"])}
    else:
        densities = {
            Spin.up: np.asarray(dos["DosInfo"]["Spin1"]["Dos"]),
            Spin.down: np.asarray(dos["DosInfo"]["Spin2"]["Dos"]),
        }
    efermi = dos["DosInfo"]["EFermi"]
    return Dos(efermi, energies, densities)


def get_complete_dos_json(dos: dict) -> CompleteDos:
    # json -> CompleteDos Obj
    total_dos = get_total_dos_json(dos)
    structure = get_structure_json(dos["AtomInfo"])
    N = len(structure)
    pdos = [{} for i in range(N)]
    number_of_spin = 1 if dos["DosInfo"]["SpinType"] == "none" else 2

    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down
        project = dos["DosInfo"][spin_key]["ProjectDos"]
        for p in project:
            atom_index = p["AtomIndex"] - 1
            o = p["OrbitIndex"] - 1
            orbit_name = Orbital(o)
            if orbit_name in pdos[atom_index].keys():
                pdos[atom_index][orbit_name].update({spin: p["Contribution"]})
            else:
                pdos[atom_index][orbit_name] = {spin: p["Contribution"]}
    pdoss = {structure[i]: pd for i, pd in enumerate(pdos)}

    return CompleteDos(structure, total_dos, pdoss)


def get_structure(hdf5: dict, key: str) -> Structure:
    # load_h5 -> Structure Obj
    lattice = np.asarray(hdf5[key + "/Lattice"]).reshape(3, 3)
    elements = hdf5[key + "/Elements"]
    positions = hdf5[key + "/Position"]
    coords = np.asarray(positions).reshape(-1, 3)
    is_direct = hdf5[key + "/CoordinateType"][0] == "Direct"
    return Structure(lattice, elements, coords, coords_are_cartesian=(not is_direct))


def get_structure_json(atominfo) -> Structure:
    lattice = np.asarray(atominfo["Lattice"]).reshape(3, 3)
    elements = []
    positions = []
    for atom in atominfo["Atoms"]:
        elements.append(atom["Element"])
        positions.extend(atom["Position"])

    coords = np.asarray(positions).reshape(-1, 3)
    is_direct = atominfo["CoordinateType"] == "Direct"
    return Structure(lattice, elements, coords, coords_are_cartesian=(not is_direct))


def get_structure_from_json(jsonfile: str) -> Structure:
    with open(jsonfile, "r") as file:
        j = json.load(file)
    lattice = np.asarray(j["AtomInfo"]["Lattice"]).reshape(3, 3)
    elements = j["AtomInfo"]["Elements"]
    positions = j["AtomInfo"]["Position"]
    coords = np.asarray(positions).reshape(-1, 3)
    is_direct = j["AtomInfo"]["CoordinateType"][0] == "Direct"
    return Structure(lattice, elements, coords, coords_are_cartesian=(not is_direct))


def get_band_data_h5(band: dict, iwan=False):
    if iwan:
        bd = "WannBandInfo"
    else:
        bd = "BandInfo"
    number_of_band = band[f"/{bd}/NumberOfBand"][0]
    number_of_kpoints = band[f"/{bd}/NumberOfKpoints"][0]
    if (
        band[f"/{bd}/SpinType"][0] == "none"
        or band[f"/{bd}/SpinType"][0] == "non-collinear"
    ):
        number_of_spin = 1
    else:
        number_of_spin = 2

    symmetry_kPoints_index = band[f"/{bd}/SymmetryKPointsIndex"]

    efermi = band[f"/{bd}/EFermi"][0]
    eigenvals = {}
    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down

        if f"/{bd}/" + spin_key + "/BandEnergies" in band:
            data = band[f"/{bd}/" + spin_key + "/BandEnergies"]
        elif f"/{bd}/" + spin_key + "/Band" in band:
            data = band[f"/{bd}/" + spin_key + "/Band"]
        else:
            print("Band key error")
            return
        band_data = np.array(data).reshape((number_of_kpoints, number_of_band)).T
        eigenvals[spin] = band_data

    kpoints = np.asarray(band[f"/{bd}/CoordinatesOfKPoints"]).reshape(
        number_of_kpoints, 3
    )

    structure = get_structure(band, "/AtomInfo")
    labels_dict = {}

    for i, s in enumerate(band[f"/{bd}/SymmetryKPoints"]):
        labels_dict[s] = kpoints[symmetry_kPoints_index[i] - 1]

    # read projection data
    projections = None
    if f"/{bd}/IsProject" in band.keys():
        if band[f"/{bd}/IsProject"][0]:
            projections = {}
            number_of_orbit = len(band[f"/{bd}/Orbit"])
            projection = np.zeros(
                (number_of_band, number_of_kpoints, number_of_orbit, len(structure))
            )

            for i in range(number_of_spin):
                spin_key = "Spin" + str(i + 1)
                spin = Spin.up if i == 0 else Spin.down

                atomindexs = band[f"/{bd}/" + spin_key + "/ProjectBand/AtomIndex"][0]
                orbitindexs = band[f"/{bd}/" + spin_key + "/ProjectBand/OrbitIndexs"][0]
                for atom_index in range(atomindexs):
                    for orbit_index in range(orbitindexs):
                        project_data = band[
                            f"/{bd}/"
                            + spin_key
                            + "/ProjectBand/1/"
                            + str(atom_index + 1)
                            + "/"
                            + str(orbit_index + 1)
                        ]
                        projection[:, :, orbit_index, atom_index] = (
                            np.asarray(project_data)
                            .reshape((number_of_kpoints, number_of_band))
                            .T
                        )
                projections[spin] = projection

    return structure, kpoints, eigenvals, efermi, labels_dict, projections


def get_band_data_json(band: dict, iwan=False):
    if iwan:
        bd = "WannBandInfo"
    else:
        bd = "BandInfo"

    number_of_band = band[f"{bd}"]["NumberOfBand"]
    number_of_kpoints = band[f"{bd}"]["NumberOfKpoints"]
    if "Spin2" in band[f"{bd}"]:
        number_of_spin = 2
    else:
        number_of_spin = 1

    symmetry_kPoints_index = band[f"{bd}"]["SymmetryKPointsIndex"]

    if "EFermi" in band[f"{bd}"]:
        efermi = band[f"{bd}"]["EFermi"]
    else:
        efermi = 0  # for wannier

    eigenvals = {}
    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down

        if "BandEnergies" in band[f"{bd}"][spin_key]:
            data = band[f"{bd}"][spin_key]["BandEnergies"]
        elif "Band" in band[f"{bd}"][spin_key]:
            data = band[f"{bd}"][spin_key]["Band"]
        else:
            print("Band key error")
            return

        band_data = np.array(data).reshape((number_of_kpoints, number_of_band)).T

        eigenvals[spin] = band_data

    kpoints = np.asarray(band[f"{bd}"]["CoordinatesOfKPoints"]).reshape(
        number_of_kpoints, 3
    )

    structure = get_structure_json(band["AtomInfo"])
    labels_dict = {}

    for i, s in enumerate(band[f"{bd}"]["SymmetryKPoints"]):
        labels_dict[s] = kpoints[symmetry_kPoints_index[i] - 1]

    # read projection data
    projections = None
    if "IsProject" in band[f"{bd}"].keys():
        if band[f"{bd}"]["IsProject"]:
            projections = {}
            number_of_orbit = len(band[f"{bd}"]["Orbit"])
            projection = np.zeros(
                (number_of_band, number_of_kpoints, number_of_orbit, len(structure))
            )

            for i in range(number_of_spin):
                spin_key = "Spin" + str(i + 1)
                spin = Spin.up if i == 0 else Spin.down

                data = band[f"{bd}"][spin_key]["ProjectBand"]
                for d in data:
                    orbit_index = d["OrbitIndex"] - 1
                    atom_index = d["AtomIndex"] - 1
                    project_data = d["Contribution"]
                    projection[:, :, orbit_index, atom_index] = (
                        np.asarray(project_data)
                        .reshape((number_of_kpoints, number_of_band))
                        .T
                    )

                projections[spin] = projection

    return structure, kpoints, eigenvals, efermi, labels_dict, projections


def get_band_data(band_dir: str, efermi: float = None) -> BandStructureSymmLine:
    # modify BandStructureSymmLine.efermi after it was created will cause error
    if band_dir.endswith(".h5"):
        band = load_h5(band_dir)
        raw = h5py.File(band_dir, "r").keys()
        if "/WannBandInfo/NumberOfBand" in raw:
            (
                structure,
                kpoints,
                eigenvals,
                rEf,
                labels_dict,
                projections,
            ) = get_band_data_h5(band, iwan=True)
        elif "/BandInfo/NumberOfBand" in raw:
            (
                structure,
                kpoints,
                eigenvals,
                rEf,
                labels_dict,
                projections,
            ) = get_band_data_h5(band, iwan=False)
        else:
            print("BandInfo or WannBandInfo key not found in h5file!")
            return
    elif band_dir.endswith(".json"):
        with open(band_dir, "r") as fin:
            band = json.load(fin)
        if "WannBandInfo" in band.keys():
            (
                structure,
                kpoints,
                eigenvals,
                rEf,
                labels_dict,
                projections,
            ) = get_band_data_json(band, iwan=True)
        elif "BandInfo" in band.keys():
            (
                structure,
                kpoints,
                eigenvals,
                rEf,
                labels_dict,
                projections,
            ) = get_band_data_json(band, iwan=False)
        else:
            print("BandInfo or WannBandInfo key not found in json file!")
            return
    else:
        print("file - " + band_dir + " :  Unsupported format!")
        return

    if efermi:  # 从h5直接读取的费米能级可能是错的，此时需要用户自行指定
        rEf = efermi  # 这只是个临时解决方案

    lattice_new = Lattice(structure.lattice.reciprocal_lattice.matrix)
    return BandStructureSymmLine(
        kpoints=kpoints,
        eigenvals=eigenvals,
        lattice=lattice_new,
        efermi=rEf,
        labels_dict=labels_dict,
        structure=structure,
        projections=projections,
    )


def get_phonon_band_data_h5(band: dict):
    number_of_band = band["/BandInfo/NumberOfBand"][0]
    number_of_kpoints = band["/BandInfo/NumberOfQPoints"][0]
    number_of_spin = 1
    symmmetry_kpoints = band["/BandInfo/SymmetryQPoints"]
    symmetry_kPoints_index = band["/BandInfo/SymmetryQPointsIndex"]
    eigenvals = {}
    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down
        if "/BandInfo/" + spin_key + "/BandEnergies" in band:
            data = band["/BandInfo/" + spin_key + "/BandEnergies"]
        elif "/BandInfo/" + spin_key + "/Band" in band:
            data = band["/BandInfo/" + spin_key + "/Band"]
        else:
            print("Band key error")
            return
        frequencies = np.array(data).reshape((number_of_kpoints, number_of_band)).T
        eigenvals[spin] = frequencies
    kpoints = np.asarray(band["/BandInfo/CoordinatesOfQPoints"]).reshape(
        number_of_kpoints, 3
    )
    if "/SupercellAtomInfo/CoordinateType" in band.keys():
        structure = get_structure(band, "/SupercellAtomInfo")
    else:
        structure = get_structure(band, "/AtomInfo")
    return symmmetry_kpoints, symmetry_kPoints_index, kpoints, structure, frequencies


def get_phonon_band_data_json(band: dict):
    number_of_band = band["BandInfo"]["NumberOfBand"]
    number_of_kpoints = band["BandInfo"]["NumberOfQPoints"]
    number_of_spin = 1
    symmmetry_kpoints = band["BandInfo"]["SymmetryQPoints"]
    symmetry_kPoints_index = band["BandInfo"]["SymmetryQPointsIndex"]

    eigenvals = {}
    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down
        if "BandEnergies" in band["BandInfo"][spin_key]:
            data = band["BandInfo"][spin_key]["BandEnergies"]
        elif "Band" in band["BandInfo"][spin_key]:
            data = band["BandInfo"][spin_key]["Band"]
        else:
            print("Band key error")
            return
        frequencies = np.array(data).reshape((number_of_kpoints, number_of_band)).T
        eigenvals[spin] = frequencies

    kpoints = np.asarray(band["BandInfo"]["CoordinatesOfQPoints"]).reshape(
        number_of_kpoints, 3
    )

    if "SupercellAtomInfo" in band.keys():
        structure = get_structure_json(band["SupercellAtomInfo"])
    else:
        structure = get_structure_json(band["AtomInfo"])

    return symmmetry_kpoints, symmetry_kPoints_index, kpoints, structure, frequencies


def get_phonon_band_data(phonon_band_dir: str) -> PhononBandStructureSymmLine:
    if phonon_band_dir.endswith(".h5"):
        band = load_h5(phonon_band_dir)
        (
            symmmetry_kpoints,
            symmetry_kPoints_index,
            kpoints,
            structure,
            frequencies,
        ) = get_phonon_band_data_h5(band)
    elif phonon_band_dir.endswith(".json"):
        with open(phonon_band_dir, "r") as fin:
            band = json.load(fin)
        (
            symmmetry_kpoints,
            symmetry_kPoints_index,
            kpoints,
            structure,
            frequencies,
        ) = get_phonon_band_data_json(band)
    else:
        print("file - " + phonon_band_dir + " :  Unsupported format!")
        return

    labels_dict = {}
    for i, s in enumerate(symmmetry_kpoints):
        labels_dict[s] = kpoints[symmetry_kPoints_index[i] - 1]
    lattice_new = Lattice(structure.lattice.reciprocal_lattice.matrix)

    return PhononBandStructureSymmLine(
        qpoints=kpoints,
        frequencies=frequencies,
        lattice=lattice_new,
        has_nac=False,
        labels_dict=labels_dict,
        structure=structure,
    )


def get_phonon_dos_data(phonon_dos_dir: str) -> PhononDos:
    if phonon_dos_dir.endswith(".h5"):
        dos = load_h5(phonon_dos_dir)
        frequencies = np.asarray(dos["/DosInfo/DosEnergy"])
        densities = dos["/DosInfo/Spin1/Dos"]
    elif phonon_dos_dir.endswith(".json"):
        with open(phonon_dos_dir, "r") as fin:
            dos = json.load(fin)
        frequencies = np.asarray(dos["DosInfo"]["DosEnergy"])
        densities = dos["DosInfo"]["Spin1"]["Dos"]
    else:
        print("file - " + phonon_dos_dir + " :  Unsupported format!")
        return

    return PhononDos(frequencies, densities)
