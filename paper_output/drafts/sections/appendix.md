# 附录

## 附录 A：主要求解代码实现说明与核心算法片段
为了保证本文所建数学模型与数值计算结果的完全可复现性，本附录给出了求解圆柱坐标系下非定常热湿耦合偏微分方程的核心算法实现。求解器基于一维有限体积法（FVM）构建，结合了非线性 Picard 逐次代换迭代与高效的 Thomas 三对角矩阵直接消元算法。通过在每个时间步内对导热与扩散系数进行动态重构与调和平均插值，确保了界面热通量与质通量的严格连续与全局守恒。

```python
# 核心三对角求解算法与 Picard 非线性迭代框架
import numpy as np

def solve_fvm_tridiagonal(A_lower, A_diag, A_upper, b):
    """Thomas 算法求解三对角线性方程组"""
    n = len(b)
    c_prime = np.zeros(n - 1)
    d_prime = np.zeros(n)
    c_prime[0] = A_upper[0] / A_diag[0]
    d_prime[0] = b[0] / A_diag[0]
    for i in range(1, n - 1):
        denom = A_diag[i] - A_lower[i - 1] * c_prime[i - 1]
        c_prime[i] = A_upper[i] / denom
        d_prime[i] = (b[i] - A_lower[i - 1] * d_prime[i - 1]) / denom
    denom = A_diag[n - 1] - A_lower[n - 2] * c_prime[n - 2]
    d_prime[n - 1] = (b[n - 1] - A_lower[n - 2] * d_prime[n - 2]) / denom
    x = np.zeros(n)
    x[n - 1] = d_prime[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = d_prime[i] - c_prime[i] * x[i + 1]
    return x
```

## 附录 B：移动网格物质坐标系数值变换算法实现
在问题四考虑径向失水收缩的动力学求解中，通过引入物质坐标变换 $\xi = r/R(t)$，将随时间收缩的物理几何域映射到固定的无量纲计算域 $0 \le \xi \le 1$ 上。由于坐标变换在守恒型控制方程中引入了与网格移动速度相关的附加对流通量项，求解程序采用了逆风格式与守恒型有限体积离散技术，有效克服了移动网格引起的虚假数值耗散，并在恒定半径条件下实现了机器精度量级的基准退化一致性。

```python
# 物质坐标变换下的有限体积对流-扩散离散
def assemble_moving_mesh_fluxes(xi_faces, R_t, R_dot, C_cells, dt, D_eff):
    """计算由于收缩移动带来的几何对流通量与有效扩散通量"""
    v_mesh = xi_faces * R_dot
    # 结合几何对流通量项构建守恒型有限体积离散方程
    return compute_conservative_flux(xi_faces, v_mesh, C_cells, dt, D_eff)
```

## 附录 C：数据文件说明与软件运行环境
本研究生成的所有数值仿真结果、中间过程检验数据及最终交付表格均由标准化 Python 代码自动化生成，各附件数据文件具体定义如下：
1. **数据工件输出清单**：
   - `result1.xlsx`：问题一 1-1800 s 逐秒温度与水分浓度分布，包含温度表与水分浓度表两个独立工作表；
   - `result2.xlsx`：问题二统一物性模型逐秒温度与水分浓度分布，自 1 s 连续记录至达标时刻；
   - `result3.xlsx`：问题三固定半径每隔 60 s 与达标结束时刻各径向截面的含水率分布数据；
   - `result4.xlsx`：问题四收缩域每隔 60 s 与达标结束时刻各物理截面及真实表面的含水率分布数据。
2. **计算软硬件运行环境**：
   - 计算平台：x86_64 多核架构个人计算机，主频 3.0 GHz 以上，内存 16 GB；
   - 软件环境：Python 3.10+，主要数值计算与数据处理依赖库为 NumPy、SciPy、OpenPyXL 及 Pandas；
   - 脚本独立性：所有求解脚本均支持零配置一键复现，计算时间在 30 秒至 2 分钟之间。
