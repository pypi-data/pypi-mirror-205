#!python3.10

import PyPDF2, os, glob
import pandas as pd
from collections import defaultdict

file_name = "output.xlsx"  # 输出的 Excel 文件名
datas = []  # 存放所有学生的原始数据，json格式
# 记录不同学科，不同班级，每道题/知识点的得分情况a[科目][题号/知识点][班级][层级]。
subject_topic_class_status = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))
dfs = {}  # 分工作表存储的 DataFrame 对象
class_select_counts = defaultdict(lambda: defaultdict(int))  # 记录每个班级的选科人数


# 读取关键字之后的文字
def string_after_the_keyword(content, keyword):
    start_index = content.find(keyword) + len(keyword)
    s = content[start_index : start_index + 15].strip()
    return s[: s.find(" ")]


# 读取关键字之后的数字
def number_after_the_keyword(content, keyword):
    start_index = end_index = content.find(keyword) + len(keyword)
    while ord(content[end_index]) < 128:
        end_index += 1
    return content[start_index:end_index].strip()


# 读取关键字之后的层级信息
def level_info_after_the_keyword(content, keyword, skip_chinese=False):
    start_index = end_index = content.find(keyword) + len(keyword)
    while content[end_index] != "Ⅴ":
        end_index += 1
    s = content[start_index:end_index]
    data = {"Ⅰ": [], "Ⅱ": [], "Ⅲ": [], "Ⅳ": [], "Ⅴ": []}
    start_index = 0
    for key in data:
        end_index = s.find(key)
        info = s[start_index:end_index].strip().replace("-", "").replace(" ", "")
        start_index = end_index + 1

        if skip_chinese:
            info = "".join([c for c in info if ord(c) < 128])

        data[key] = info.split(",") if info != "" else []
    return data


# 读取并分析学生pdf文件
def read_and_analyze_PDF_file(file_path, class_name):
    data = {"姓名": "", "考号": "", "班级": class_name, "参加科目": []}
    # 打开PDF文件
    pdf_file = open(file_path, "rb")
    # 创建PdfReader对象
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page in pdf_reader.pages:
        page_content = page.extract_text().replace("\n", "")

        # 读取考生姓名
        if data["姓名"] == "":
            data["姓名"] = string_after_the_keyword(page_content, "姓名")

        # 读取考生考号
        if data["考号"] == "":
            data["考号"] = number_after_the_keyword(page_content, "考号")

        # 读取参加的科目，以及其赋分
        subject = string_after_the_keyword(page_content, "科目")
        data["参加科目"].append(subject)
        data[subject] = {"赋分": int(number_after_the_keyword(page_content, "等级赋分"))}

        # 读取每道试题的层级得分
        data[subject]["试题得分层级"] = level_info_after_the_keyword(page_content, "层级试题得分", True)

        # 读取学科知识的层级得分
        data[subject]["学科知识层级"] = level_info_after_the_keyword(page_content, "学科知识")

    pdf_file.close()
    return data


# 检查目录结构有没有符合程序要求
def preliminary_check():
    path = os.getcwd()
    # 遍历目录中的所有文件夹
    for foldername in os.listdir(path):
        if os.path.isdir(os.path.join(path, foldername)):  # 判断是否是文件夹
            if foldername[-1] != "班":
                print(f"'{foldername}' 文件夹不符合命名规则\n")
                raise Exception("文件夹不符合命名规则")
            if len(glob.glob(os.path.join(foldername, "*.pdf"))) == 0:
                print(f"存在没有PDF文件的班级文件夹: '{foldername}'")
                raise Exception("存在没有PDF文件的班级文件夹")

    folders = glob.glob(os.path.join("*班"))
    if len(folders) == 0:
        raise Exception("没有文件夹")


subject_info = {}  # 学科信息
column_heading = {  # 不同工作表的固定列标题
    "试题得分层级": list("班级 姓名 考号 赋分".split()),
    "试题层级占比": list("小题 班级 选科人数 Ⅰ Ⅰ% Ⅱ Ⅱ% Ⅲ Ⅲ% Ⅳ Ⅳ% Ⅴ Ⅴ%".split()),
    "学科知识层级": list("班级 姓名 考号 赋分".split()),
    "知识层级占比": list("学科知识 班级 选科人数 Ⅰ Ⅰ% Ⅱ Ⅱ% Ⅲ Ⅲ% Ⅳ Ⅳ% Ⅴ Ⅴ%".split()),
}


# 题目ID排序函数
def problem_id_sort_func(x):
    s = ""
    for c in x:
        if "0" <= c <= "9":
            s += c
        else:
            s += " "
    return list(map(int, s.split()))


# 新建一个学科
def create_subject(subject, data):
    subject_info[subject] = {"小题": [], "学科知识": []}
    # subject_topic_class_status[subject] = {}

    for x in data["试题得分层级"].values():
        subject_info[subject]["小题"] += x
    subject_info[subject]["小题"].sort(key=problem_id_sort_func)
    # for x in subject_info[subject]["小题"]:
    #     subject_topic_class_status[subject][x] = {}

    for x in data["学科知识层级"].values():
        subject_info[subject]["学科知识"] += x
    subject_info[subject]["学科知识"].sort()
    # for x in subject_info[subject]["学科知识"]:
    #     subject_topic_class_status[subject][x] = {}

    for x in column_heading.keys():
        sheet_name = f"{subject}{x}"
        columns = [x for x in column_heading[x]]
        if x == "试题得分层级":
            columns += subject_info[subject]["小题"]
        if x == "学科知识层级":
            columns += subject_info[subject]["学科知识"]
        dfs[sheet_name] = pd.DataFrame(columns=columns)


# 反转键/值的对应关系
def reverse_dic(dic):
    ans = {}
    for key in dic:
        for x in dic[key]:
            ans[x] = key
    return ans


# 处理某个学生某学科的考试情况
def handle_exam_subject(cls, name, exam_number, subject, data):
    class_select_counts[subject][cls] += 1
    rvs_dic = {}
    rvs_dic["试题得分层级"] = reverse_dic(data["试题得分层级"])
    rvs_dic["学科知识层级"] = reverse_dic(data["学科知识层级"])

    for key in rvs_dic:
        for k in rvs_dic[key]:
            subject_topic_class_status[subject][k][cls][rvs_dic[key][k]] += 1
            subject_topic_class_status[subject][k]["all"][rvs_dic[key][k]] += 1
            rvs_dic[key][k] = ord(rvs_dic[key][k]) - ord("Ⅰ") + 1

    row = {"班级": cls, "姓名": name, "考号": exam_number, "赋分": data["赋分"]}
    row.update(rvs_dic["试题得分层级"])
    dfs[f"{subject}试题得分层级"].loc[len(dfs[f"{subject}试题得分层级"])] = row

    row = {"班级": cls, "姓名": name, "考号": exam_number, "赋分": data["赋分"]}
    row.update(rvs_dic["学科知识层级"])
    dfs[f"{subject}学科知识层级"].loc[len(dfs[f"{subject}学科知识层级"])] = row


# 新增一行至工作表
def append_to_sheet(sheet_name, row):
    dfs[sheet_name].loc[len(dfs[sheet_name])] = row


# 统计不同学科，试题或知识层级占比
def calculate_subject_quiz_ratio(subject):
    clses = list(class_select_counts[subject].keys())
    clses.sort()
    grade_population = sum(class_select_counts[subject].values())

    for pid in subject_info[subject]["小题"]:
        for cls in clses:
            row = {"小题": pid, "班级": cls, "选科人数": class_select_counts[subject][cls]}
            for col in "Ⅰ Ⅱ Ⅲ Ⅳ Ⅴ".split():
                row[col] = subject_topic_class_status[subject][pid][cls][col]
                row[f"{col}%"] = row[col] / class_select_counts[subject][cls]
            append_to_sheet(f"{subject}试题层级占比", row)

        row = {"小题": pid, "班级": "全年级", "选科人数": grade_population}
        for col in "Ⅰ Ⅱ Ⅲ Ⅳ Ⅴ".split():
            row[col] = subject_topic_class_status[subject][pid]["all"][col]
            row[f"{col}%"] = row[col] / grade_population
        append_to_sheet(f"{subject}试题层级占比", row)

    for concept in subject_info[subject]["学科知识"]:
        for cls in clses:
            row = {"学科知识": concept, "班级": cls, "选科人数": class_select_counts[subject][cls]}
            for col in "Ⅰ Ⅱ Ⅲ Ⅳ Ⅴ".split():
                row[col] = subject_topic_class_status[subject][concept][cls][col]
                row[f"{col}%"] = row[col] / class_select_counts[subject][cls]
            append_to_sheet(f"{subject}知识层级占比", row)

        row = {"学科知识": concept, "班级": "全年级", "选科人数": grade_population}
        for col in "Ⅰ Ⅱ Ⅲ Ⅳ Ⅴ".split():
            row[col] = subject_topic_class_status[subject][concept]["all"][col]
            row[f"{col}%"] = row[col] / grade_population
        append_to_sheet(f"{subject}知识层级占比", row)

    # for col in "Ⅰ% Ⅱ% Ⅲ% Ⅳ% Ⅴ%".split():
    #     dfs[f"{subject}试题层级占比"][col] = dfs[f"{subject}试题层级占比"][col].map("{:.2%}".format)
    #     dfs[f"{subject}知识层级占比"][col] = dfs[f"{subject}知识层级占比"][col].map("{:.2%}".format)


def analyze_and_save_to_excel(datas):
    for data in datas:
        name = data["姓名"]
        cls = data["班级"]
        exam_number = data["考号"]
        sbjs = data["参加科目"]
        for sbj in sbjs:
            if sbj not in subject_info:
                create_subject(sbj, data[sbj])
            handle_exam_subject(cls, name, exam_number, sbj, data[sbj])

    for subject in subject_info:
        calculate_subject_quiz_ratio(subject)

    with pd.ExcelWriter(file_name, mode="w") as writer:
        for key in dfs:
            dfs[key].to_excel(writer, sheet_name=key, index=False)


# execl 格式美化
def beautify_excel():
    from openpyxl import load_workbook

    # 加载新的 Excel 文件，并为单元格格式设为百分比
    wb = load_workbook(file_name)
    for subject in subject_info:
        ws1 = wb[f"{subject}试题层级占比"]
        ws2 = wb[f"{subject}知识层级占比"]
        for c in "EGIKM":
            col1 = ws1[c]
            col2 = ws2[c]
            for cell in col1:
                cell.number_format = "0.00%"
            for cell in col2:
                cell.number_format = "0.00%"

    wb.save(file_name)
    wb.close()


def display_user_guide(e):
    guide = """目录结构有误！
请以班级为单位，创建文件夹(文件夹以班字结尾)，例如：301、302班、...
然后将学生下载的成绩报告单 pdf 文件，放入对应班级的文件夹。
pdf 文件必须是官方网站下载的，否则可能出现解析错误，导致信息、分数不一致等情况。
准备工作完成后，再重新运行本程序。
    """
    print(guide)


def run():
    try:
        preliminary_check()  # 前期准备及目录结构检测
    except Exception as e:
        display_user_guide(e)  # 提示目录结构的错误，给用户提供使用指南
        exit(0)

    folders = list(glob.glob(os.path.join("*班")))  # 获取需要分析的文件夹
    folders.sort()

    # 遍历所有班级文件夹，生成所有学生的原始数据
    for foldername in folders:
        class_name = foldername.replace("班", "")
        pdf_files = glob.glob(os.path.join(foldername, "*.pdf"))  # 获取所有 PDF 文件路径
        num_pdfs = len(pdf_files)  # 获取 PDF 文件数量
        print(f"'{foldername}' 文件夹中有 {num_pdfs} 个 PDF 文件,注意核对人数.")

        # 遍历此班的所有考生成绩报告单
        for file in pdf_files:
            try:
                datas.append(read_and_analyze_PDF_file(file, class_name))  # 读取并分析某考生的成绩报告单，然后将数据保存起来供后续分析
            except Exception:
                print(f"{file} 文件解析错误,请检查该文件.确保 pdf 文件是官方下载的！然后重新运行本程序.")
                exit(0)

    analyze_and_save_to_excel(datas)  # 分析考生数据，然后存储到excel中，增加可视化
    beautify_excel()  # 美化表格
    print("\033[0;32m程序运行完毕，已生成汇总文件：\033[0m" + "\033[0;31moutput.xlsx\033[0m")


if __name__ == "__main__":
    run()
