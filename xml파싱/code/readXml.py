import xml.etree.ElementTree as ET

file_input = input('파일을 입력하세요 : ') # ex) C:\sjbang\공간정보산업진흥원\code\layer.xml
file_output = input('저장 경로 : ') # ex) C:\sjbang\공간정보산업진흥원\code\output.xml

tree = ET.parse(file_input)
root = tree.getroot()

print(root.tag)
print(root.attrib)

# 태그 구분자 unique
def tagGbn():
    list = []
    for child in root:
        child.tag.split('_')[0]
        list.append(child.tag.split('_')[0])

    list = set(list)
    print(list)

# XML element에 div 속성 추가
def add_element_div():
    my_keywords1 = ['A1', 'A2', 'B1', 'B2' ,'C1', 'C2']
    my_keywords2 = ['AE', 'BE', 'DE']
    my_keywords3 = ['EC01', 'ER16']

    for element in root.iter():
        if 'div' in element.attrib:
            print(f"  (스킵) '{element.tag}' 엘리먼트는 이미 'div' 속성이 있습니다.")
            continue # 다음 엘리먼트로 바로 이동

        for keyword in my_keywords1:
            if keyword in element.tag: 
                element.set('div', 'ngii') # 'div' 속성을 'ngii' 값으로 추가 또는 업데이트
                # print(f"'{element.tag}' 태그에 div='ngii' 속성을 추가했습니다.")

        # 'div' 속성이 이미 설정되었다면, 다음 리스트(my_keywords2, my_keywords3) 검사를 건너뜀
        if 'div' in element.attrib:
            continue

        for keyword in my_keywords2:
            if keyword in element.tag: 
                element.set('div', 'ex') # 'div' 속성을 'ex' 값으로 추가 또는 업데이트
                # print(f"'{element.tag}' 태그에 div='ex' 속성을 추가했습니다.")
        
        if 'div' in element.attrib:
            continue
        
        for keyword in my_keywords3:
            if keyword in element.tag: 
                element.set('div', 'road') # 'div' 속성을 'road' 값으로 추가 또는 업데이트
                # print(f"'{element.tag}' 태그에 div='road' 속성을 추가했습니다.")

    print("\n--- 속성 추가 후 XML 엘리먼트 ---")

    for element in root.iter():
        print(f"태그: {element.tag}, 속성: {element.attrib}")

    # 4. 변경된 XML 내용을 새 파일로 저장
    # 'output.xml'이라는 새 파일에 변경된 내용을 저장합니다.
    # encoding='UTF-8'은 한글이 깨지지 않도록 하며, xml_declaration=True는 XML 선언을 추가합니다.
    tree.write(file_output, encoding='UTF-8', xml_declaration=True)
    print("\n변경된 XML 내용이 'output.xml' 파일로 저장되었습니다.")

# XML element에 year 속성 추가
def add_element_year():

    year_2025 = ['A1_NODE_001',
                'A2_LINK_002',
                'A3_DRIVEWAYSECTION_008',
                'A4_SUBSIDIARYSECTION_009',
                'A4_SUBSIDIARYSECTION_013',
                'A5_PARKINGLOT_015',
                'B2_SURFACELINEMARK_018',
                'B3_SURFACEMARK_019',
                'C2_KILOPOST_023',
                'C5_HEIGHTBARRIER_028',
                'CE_LCS_029',
                'DE_CCTV_037',
                'DE_VDS_040',
                'DE_ROAD_042',
                'DE_ROADPAVEMENT_043',
                'DE_DSRC_044',
                'DE_SOS_045']

    for element in root.iter():
        # 1. 이미 'year' 속성이 있다면 스킵
        if 'year' in element.attrib:
            print(f"  (스킵) '{element.tag}' 엘리먼트는 이미 'year' 속성이 있습니다. (현재: {element.get('year')})")
            continue

        # 2. 'year_2025' 리스트의 키워드에 해당하는지 확인
        found_2025_keyword = False # 2025년 키워드를 찾았는지 여부를 나타내는 플래그
        for keyword in year_2025:
            if keyword in element.tag:
                element.set('year', '2025')
                print(f"  '{element.tag}' 태그에 '{keyword}' 포함 -> year='2025' 추가")
                found_2025_keyword = True
                break # 해당 엘리먼트에 2025년을 부여했으니, 더 이상 이 루프를 돌 필요 없음

        # 3. 2025년 키워드를 찾지 못했다면 '2024'로 설정
        if not found_2025_keyword:
            element.set('year', '2024')
            print(f"  '{element.tag}' 태그에 2025년 키워드 없음 -> year='2024' 추가")


    print("\n--- 속성 추가 후 XML 엘리먼트 ---")

    for element in root.iter():
        print(f"태그: {element.tag}, 속성: {element.attrib}")

    # 4. 변경된 XML 내용을 새 파일로 저장
    # 'output.xml'이라는 새 파일에 변경된 내용을 저장합니다.
    # encoding='UTF-8'은 한글이 깨지지 않도록 하며, xml_declaration=True는 XML 선언을 추가합니다.
    tree.write(file_output, encoding='UTF-8', xml_declaration=True)
    print("\n변경된 XML 내용이 'output.xml' 파일로 저장되었습니다.")

# 결과 추출(text로)
def main_func():
    add_element_div() # div 추가
    add_element_year() # year 추가

    # element 추가된 파일 불러오기
    tree = ET.parse(file_output)
    root = tree.getroot()

    for child in root:
        # print(child.tag, child.attrib)
        print(child.tag + ' / ' + child.attrib.get('name') + ' / ' + str(child.attrib.get('div')) + ' / ' + child.attrib.get('year'))

# 실행
main_func()