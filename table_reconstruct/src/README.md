题目描述
============
### 输入要求
---
### 输出要求
1. **int errNo:**//错误码
	- 0: 成功
	- 1: 指定打横索引错误
	- 2: 元数据行错误(元数据行烈属不匹配、元数据行类型不匹配等)
3. **int totalLines:**//处理的数据总行数(不包括元数据行)
4. **int ignoredLines:**//因为存在单元格取值为null且该列无缺省值定义而被跳过的行数量
5. **int illegalLines:**//因为存在单元格取值与元数据行指定类型不匹配、列数量不匹配等错误
    而被跳过的数据行数量
6. **List<Column>:**//经过排序的数据表结构(详见项目工程)
7. 新增列的列名固定未“Flag_${源列名}_${枚举值}”的格式(如Flag_Gender_Male);
    新增列集要求在所有源列之后进行输出，且已按要求完成排序;
    *注意新增列集单元格的取值范围未(True|False)*
8. 已被计入ignoredLines、illegalLines的数据整行不做输出
8. 当errCode取值为非0时，可以不用设置其他变量值
9. 当totoleLines == ignoreLines + illegalLines时，不用设置List<Column>变量


