# A题计算说明

仅使用题给环境、半径和物性。有限体积离散、后向欧拉、Picard收敛和Thomas算法。

在项目根目录依次执行（需要numpy、pandas、numba、openpyxl、matplotlib）：

```text
python -B paper_output/code/data_processing/prepare_a_data.py
python -B paper_output/code/visualization/run_numerical_validation.py
python -B paper_output/code/modeling/run_modeling.py
```

数值验证先选定通过误差目标的网格和步长，四问从已有验证报告读取同一配置。
验证不通过时应检查误差和加密，不修改报告状态。每次模型改动后重新验证和计算。
已有model_validation_checks.json保存长程对照与边界情景；原有结果、图表与附件就地更新。
本轮不新增代码、数据或分章草稿文件。S7按用户要求对已有源稿原位修订，缺失的标准写作状态不伪造。
不加潜热和新材料参数；Ce为有效边界参考值。收缩域材料坐标的守恒仅在所声明干基假设下成立。
