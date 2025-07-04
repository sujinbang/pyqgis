from qgis.core import QgsProject, QgsVectorLayer
import processing

user_input = '수도권제1순환선(판교퇴계원)_동서울지사'
user_file_path = 'C:/sjbang/result2/'
# 노선이 세로형이면 Coord_y, 가로형이면 Coord_x
sort_expression = '"Coord_y"'

# 1. addXYfields
def addXYfields():
    # 레이어 이름으로 QGIS 프로젝트에서 레이어 객체 가져오기
    # '경부선_서울산지사_xy_y기준정렬' 레이어가 QGIS 프로젝트에 로드되어 있어야 합니다.
    layer_name = user_input
    input_layers = QgsProject.instance().mapLayersByName(layer_name)
    print(input_layers)
    output_path = r'C:\sjbang\test\output_with_xy.shp'

    # addxyfields
    if len(input_layers) > 0:
        input_layer = input_layers[0] # 첫 번째 일치하는 레이어 사용
        
        # X,Y 필드에  사용할 접두사
        field_prefix = 'Coord_'
        # 좌표계 설정
        target_crs_authid = input_layer.crs().authid()
        
        params = {
            'INPUT': input_layer,           # 입력 레이어 객체
            'PREFIX': field_prefix,         # 새 필드 이름의 접두사
            'CRS': target_crs_authid,       # X/Y 좌표를 추출할 대상 CRS (EPSG 코드)
            'OUTPUT': output_path
        }

        result = processing.run("qgis:addxyfields", params)

    # 결과 확인 및 QGIS 추가
    if result['OUTPUT']:
        # 결과 레이어 로드 (메모리 레이어 또는 파일)
        # output_layer = QgsVectorLayer(result['OUTPUT'], f"{input_layer.name()}_with_XY", "ogr" if output_path else "memory")
        output_layer = QgsVectorLayer(result['OUTPUT'], "output_with_xy", "ogr" if output_path else "memory")

        if output_layer.isValid():
            QgsProject.instance().addMapLayer(output_layer)
            print(f"'{output_layer.name()}' 레이어가 성공적으로 생성되어 QGIS 프로젝트에 추가되었습니다.")
            if output_path:
                print(f"결과가 파일로 저장되었습니다: {output_path}")
        else:
            print("오류: 결과 레이어를 로드하거나 QGIS에 추가하는 데 실패했습니다.")
    else:
        print("오류: 'Add X/Y Fields' 처리 작업이 실패했습니다.")
        

# 2. order by expression
def orderByexpression():
    layer_name = 'output_with_xy'
    input_layers = QgsProject.instance().mapLayersByName(layer_name)
    print(input_layers)
    output_path = r'C:\sjbang\test\output_sort.shp'

    if len(input_layers) > 0:
        input_layer = input_layers[0] # 첫 번째 일치하는 레이어 사용
        
        params_sort = {
            'INPUT': input_layer,
            'EXPRESSION': sort_expression,
            'ASCENDING': True, # True: 오름차순 (작은 Y에서 큰 Y), False: 내림차순
            'OUTPUT': output_path
        }
        
        result_sort = processing.run("qgis:orderbyexpression", params_sort)
        
    if result_sort['OUTPUT']:
        # 결과 레이어 로드 (메모리 레이어 또는 파일)
        output_layer = QgsVectorLayer(result_sort['OUTPUT'], "output_sort", "ogr" if output_path else "memory")

        if output_layer.isValid():
            QgsProject.instance().addMapLayer(output_layer)
            print(f"'{output_layer.name()}' 레이어가 성공적으로 생성되어 QGIS 프로젝트에 추가되었습니다.")
            if output_path:
                print(f"결과가 파일로 저장되었습니다: {output_path}")
        else:
            print("오류: 결과 레이어를 로드하거나 QGIS에 추가하는 데 실패했습니다.")
    else:
        print("오류: 'Order by expression' 처리 작업이 실패했습니다.")

# 3. add field
def addField():
    layer_name = 'output_sort'
    input_layers = QgsProject.instance().mapLayersByName(layer_name)
    print(input_layers)
    output_path = r'C:\sjbang\test\output_addfield.shp'
    field_name = 'test_id'

    if len(input_layers) > 0:
        input_layer = input_layers[0] # 첫 번째 일치하는 레이어 사용
        
        # 필드 추가 (파이썬 API)
        input_layer.startEditing()
        new_field = QgsField(field_name, QVariant.Int)
        input_layer.dataProvider().addAttributes([new_field])
        input_layer.commitChanges()
        input_layer.updateFields()

        # 필드 계산기
        params_calculate_field = {
            'INPUT': input_layer,
            'FIELD_NAME': field_name,
            'FORMULA': '@row_number', 
            'OUTPUT': output_path,
            'RESULT_FIELD_LENGTH': 10,
            'RESULT_FIELD_PRECISION': 0,
            'RTYPE': 0 # Integer 타입
        }
        result_addfield = processing.run("qgis:fieldcalculator", params_calculate_field)
        print(f"필드 '{field_name}'에 순차적 값이 성공적으로 채워졌습니다.")
        
        if result_addfield['OUTPUT']:
            # 결과 레이어 로드 (메모리 레이어 또는 파일)
            output_layer = QgsVectorLayer(result_addfield['OUTPUT'], "output_addfield", "ogr" if output_path else "memory")

            if output_layer.isValid():
                QgsProject.instance().addMapLayer(output_layer)
                print(f"'{output_layer.name()}' 레이어가 성공적으로 생성되어 QGIS 프로젝트에 추가되었습니다.")
                if output_path:
                    print(f"결과가 파일로 저장되었습니다: {output_path}")
            else:
                print("오류: 결과 레이어를 로드하거나 QGIS에 추가하는 데 실패했습니다.")
        else:
            print("오류: 'Add Field' 처리 작업이 실패했습니다.")
            
# 4. point to path
def pointTopath():
    layer_name = 'output_addfield'
    input_layers = QgsProject.instance().mapLayersByName(layer_name)
    file_name = user_input + '_line.shp'
    
    if len(input_layers) > 0:
        input_layer = input_layers[0] # 첫 번째 일치하는 레이어 사용

        # pointstopath
        params = {
            'INPUT': input_layer,  # 레이어 객체를 직접 전달
            'ORDER_FIELD': 'test_id',
            'GROUP_FIELD': '',
            'OUTPUT': user_file_path + file_name
        }
        result = processing.run("qgis:pointstopath", params)

    # 4. 결과 확인 (선택 사항)
    if result['OUTPUT']:
        output_layer = QgsVectorLayer(result['OUTPUT'], user_input + '_line', "ogr")
        if output_layer.isValid():
            QgsProject.instance().addMapLayer(output_layer)
            print(f"'{output_layer.name()}' 라인 레이어가 성공적으로 생성되어 프로젝트에 추가되었습니다.")
        else:
            print("생성된 라인 레이어를 QGIS에 추가하는 데 실패했습니다.")
    else:
        print("라인 레이어 생성에 실패했습니다. 처리 결과를 확인하세요.")

# 5. line-add-field
def lineAddField():
    layer_name = user_input + '_line'
    input_layers = QgsProject.instance().mapLayersByName(layer_name)
    field_name1 = 'name'
    field_name2 = 'length'
    
    if len(input_layers) > 0:
        input_layer = input_layers[0] # 첫 번째 일치하는 레이어 사용
        
        # name, length 필드 추가 (파이썬 API)
        input_layer.startEditing()
        field_name = QgsField(field_name1, QVariant.String)
        field_length = QgsField(field_name2, QVariant.Double)
        provider = input_layer.dataProvider()
        provider.addAttributes([field_name, field_length])
        input_layer.commitChanges()
        input_layer.updateFields()
        
        # add features with attributes
        # Set attribute values
        layer = iface.activeLayer()
        layer.startEditing()
        for feature in layer.getFeatures():
            feature['name'] = user_input
            feature['length'] = feature.geometry().length()
            # Add the feature to the layer
            layer.updateFeature(feature)
        # Update layer extent
        layer.commitChanges()

    


# 레이어 삭제
def deleteLayer():
    project = QgsProject.instance()
    # 삭제하려는 레이어의 이름 (정확하게 입력)
    target_layer_list = ['output_with_xy', 'output_sort']
    #'output_addfield'
    # 해당 이름의 레이어를 프로젝트에서 찾습니다.
    # mapLayersByName은 리스트를 반환하므로, 첫 번째 요소를 사용하거나 반복문을 사용합니다.
    for i in range(0,len(target_layer_list)):
        layers_to_remove = project.mapLayersByName(target_layer_list[i])
        if layers_to_remove:
            for layer in layers_to_remove:
                project.removeMapLayer(layer.id()) # 레이어 객체의 ID를 사용하여 제거

# main 함수 실행
addXYfields()
orderByexpression()
addField()
pointTopath()
lineAddField()

# 레이어 삭제
deleteLayer()
