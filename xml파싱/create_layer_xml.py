
import pandas as pd
import re
from lxml import etree

# --- readExcel.ipynb의 핵심 로직 시작 ---

# 엑셀 파일 경로
file_path = r'2024_도로공사_고속도로 정밀도로지도 데이터명세서_250530_1018.xlsx'

# 엑셀 파일의 모든 시트 이름 확인
xl = pd.ExcelFile(file_path)
sheet_names = xl.sheet_names
sheet_names.remove('총괄')

def get_number_range(sheet_name):
    """시트명에서 숫자 범위를 추출하는 함수"""
    if '~' in sheet_name:
        numbers = sheet_name.split('_')[0]
        start, end = numbers.split('~')
        start_num = int(start.lstrip('0'))
        end_num = int(end.lstrip('0'))
        return list(range(start_num, end_num + 1))
    else:
        return [int(sheet_name.split('_')[0].lstrip('0'))]

# 각 시트 처리하여 데이터프레임 생성
for sheet_name in sheet_names:
    layer_name_df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        usecols='J',
        nrows=2,
        header=None
    )
    layer_name = layer_name_df.iloc[1, 0]

    temp_df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        header=4,
        usecols='A:L'
    )

    first_empty_row = None
    for idx, row in temp_df.iterrows():
        if row.isna().all():
            first_empty_row = idx
            break

    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        header=4,
        nrows=first_empty_row if first_empty_row else None,
        usecols='A:L'
    )

    df.dropna(axis=1, how='all', inplace=True)
    df['레이어명'] = layer_name

    number_range = get_number_range(sheet_name)
    for num in number_range:
        globals()[f'df_{num}'] = df.copy()

# --- readExcel.ipynb의 핵심 로직 끝 ---


# --- XML 생성 로직 시작 ---

def get_name_from_sheet(sheet_name):
    """시트 이름에서 'name' 속성 값을 추출하는 함수"""
    # 예: '003~009_A3' -> '차도구간(교량)'
    # 이 부분은 실제 엑셀 파일의 구조에 맞게 수정해야 할 수 있습니다.
    # 현재는 임시로 레이어명을 그대로 사용합니다.
    # 실제로는 엑셀 시트의 특정 셀에서 가져와야 할 수도 있습니다.
    try:
        name_df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            usecols='C',  # '구분' 또는 '레이어명'이 있는 열
            nrows=1,
            header=None
        )
        return name_df.iloc[0, 0]
    except Exception:
        # 시트에서 이름을 찾지 못한 경우 기본값 반환
        return "이름 없음"


root = etree.Element("root")

all_numbers = []
for sheet_name in sheet_names:
    all_numbers.extend(get_number_range(sheet_name))
all_numbers = sorted(set(all_numbers))

for num in all_numbers:
    df_name = f'df_{num}'
    if df_name in globals():
        df = globals()[df_name]
        layer_name = df['레이어명'].iloc[0]

        # layer.xml과 유사한 태그 이름 생성 (예: A1_NODE_001)
        tag_name = f"{layer_name}_{num:03d}"

        # 'name' 속성값 가져오기
        # 이 부분은 엑셀 파일의 어느 부분에서 'name'을 가져올지에 대한 정의가 필요합니다.
        # 현재는 임시로 'name' 속성을 비워둡니다.
        # 올바른 'name' 값을 위해 get_name_from_sheet 함수를 구현해야 합니다.
        original_sheet_name = ""
        for sn in sheet_names:
            if num in get_number_range(sn):
                original_sheet_name = sn
                break
        
        # 'name' 속성값을 C열 1행에서 가져오도록 수정
        name_df = pd.read_excel(
            file_path,
            sheet_name=original_sheet_name,
            usecols='C',
            nrows=1,
            header=None
        )
        name_attr = str(name_df.iloc[0, 0])


        # div와 year 속성은 현재 데이터프레임에 정보가 없으므로 임의로 설정하거나,
        # 엑셀 파일의 특정 위치에서 읽어와야 합니다.
        layer_element = etree.SubElement(root, tag_name, name=name_attr, div="ngii", year="2025")

        for index, row in df.iterrows():
            # 속성 정보를 담을 딕셔너리
            attribs = {}

            # 데이터 타입 처리
            data_type = str(row.get('데이터타입', ''))
            type_val = 'String' # 기본값
            length_val = ''
            if 'VARCHAR2' in data_type:
                type_val = 'String'
                length_val = re.search(r'\((\d+)\)', data_type).group(1) if re.search(r'\((\d+)\)', data_type) else ''
            elif 'FLOAT' in data_type:
                type_val = 'Float'
                length_val = re.search(r'\((.*)\)', data_type).group(1) if re.search(r'\((.*)\)', data_type) else ''
            elif 'NUMBER' in data_type:
                type_val = 'Number'
                length_val = re.search(r'\((\d+)\)', data_type).group(1) if re.search(r'\((\d+)\)', data_type) else ''


            attribs['type'] = type_val
            if length_val:
                attribs['length'] = length_val

            # 제약조건 처리
            constraint = str(row.get('제약조건', ''))
            if 'NOT NULL' in constraint:
                attribs['constraint'] = 'Y'
            else:
                attribs['constraint'] = 'N'

            # PK/FK 처리
            key = str(row.get('KEY', ''))
            if 'PK' in key:
                attribs['pk'] = 'Y'
            if 'FK' in key:
                attribs['fk'] = 'Y'
            
            # 'name' 속성 (한글 속성명)
            attribs['name'] = str(row.get('속성', ''))


            # XML 요소 생성
            field_element = etree.SubElement(layer_element, str(row['속성명']), attribs)


# 생성된 XML을 파일에 저장
tree = etree.ElementTree(root)
tree.write("new_layer.xml", pretty_print=True, xml_declaration=True, encoding="utf-8")

print("new_layer.xml 파일이 생성되었습니다.")
