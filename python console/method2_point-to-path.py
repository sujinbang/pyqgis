import processing
from PyQt5.QtCore import QVariant

fieldList = []

user_file_path = r'C:\Users\sjbang\Desktop\블로그\정밀도로지도\pyqgis\ETC_도로중심선_1년_1년_2024\point-to-path' + '/'

# # 1. refactor Field
# # 현재 활성화된 레이어를 입력으로 사용
def refactorField(user_input):
    layer_name = user_input
    input_layers = QgsProject.instance().mapLayersByName(layer_name)
    input_layer = input_layers[0]

    # 'name' 필드의 타입을 Double로 변경하는 매핑 설정
    fields_mapping = [
        {
            'name': 'name',                  # 필드 이름은 그대로 'name'
            'type': QVariant.Double,         # 타입을 Double로 변경
            'length': 10,                    # Double 타입에 적절한 길이 (필요시 조정)
            'precision': 3,                  # Double 타입에 적절한 정밀도 (소수점 이하 자릿수, 필요시 조정)
            'expression': 'to_real("name")', # 기존 'name' 필드 값을 Double로 변환하여 사용
            'old_name': 'name',              # 기존 필드 이름
            'old_type': QVariant.String      # 기존 필드 타입 (String)
        }
    ]

    # Refactor Fields 알고리즘 실행
    result = processing.run(
        "native:refactorfields",
        {
            'INPUT': input_layer,
            'FIELDS_MAPPING': fields_mapping,
            'OUTPUT': r'C:\Users\sjbang\Desktop\블로그\정밀도로지도\pyqgis\ETC_도로중심선_1년_1년_2024\test\Refactored Layer.shp'
        }
    )

    # 결과를 QGIS에 추가
    iface.addVectorLayer(result['OUTPUT'], "Refactored Layer", "ogr")
    
# 2. point to path
def pointTopath(user_input):
    layer_name = 'Refactored Layer'
    input_layers = QgsProject.instance().mapLayersByName(layer_name)
    file_name = user_input + '_line.shp'
    
    if len(input_layers) > 0:
        input_layer = input_layers[0] # 첫 번째 일치하는 레이어 사용

        # pointstopath
        params = {
            'INPUT': input_layer,  # 레이어 객체를 직접 전달
            'ORDER_FIELD': 'name',
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

# 3. line-add-field
def lineAddField(user_input):
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
    target_layer_list = ["Refactored Layer"]
    #'output_addfield'
    # 해당 이름의 레이어를 프로젝트에서 찾습니다.
    # mapLayersByName은 리스트를 반환하므로, 첫 번째 요소를 사용하거나 반복문을 사용합니다.
    for i in range(0,len(target_layer_list)):
        layers_to_remove = project.mapLayersByName(target_layer_list[i])
        if layers_to_remove:
            for layer in layers_to_remove:
                project.removeMapLayer(layer.id()) # 레이어 객체의 ID를 사용하여 제거
                

# 메인함수 실행
def main_func():
    for num in range(0, len(fieldList)):
        user_input = fieldList[num]
        refactorField(user_input)
        pointTopath(user_input)
        lineAddField(user_input)
        deleteLayer()
        
main_func()