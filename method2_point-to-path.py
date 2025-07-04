import processing
from PyQt5.QtCore import QVariant

fieldList = ['경부선_구미지사',
'경부선_대구지사',
'경부선_대전지사',
'경부선_서울산지사',
'경부선_수원지사',
'경부선_영동지사',
'경부선_천안지사',
'경인선_인천지사',
'고창담양선_담양지사',
'광주대구선_고령지사',
'광주대구선_광주지사',
'광주대구선_남원지사',
'광주외곽순환선_광주지사',
'남해선(순천부산)_순천지사',
'남해선(순천부산)_양산지사',
'남해선(순천부산)_진주지사',
'남해선(순천부산)_창원지사',
'남해선(영암순천)_보성지사',
'남해제1지선_창원지사',
'남해제2지선_창원지사',
'논산천안선_광주지사',
'논산천안선_담양지사',
'논산천안선_순천지사',
'당진대전선_공주지사',
'당진대전선_당진지사',
'당진청주선_천안지사',
'대구외곽순환선_대구지사',
'대구포항선_영천지사',
'대전남부순환선_대전지사',
'대전남부순환선_영동지사',
'동해선_강릉지사',
'동해선_양양지사',
'무안광주선_함평지사',
'밀양울산선_서울산지사',
'부산외곽순환선_양산지사',
'부산외곽순환선_울산지사',
'부산포항선_경주지사',
'부산포항선_울산지사',
'상주영덕선_청송지사',
'서울양양선_양양지사',
'서울양양선_춘천지사',
'서천공주선_부여지사',
'서해안선_당진지사',
'서해안선_보령지사',
'서해안선_부안지사',
'서해안선_시흥지사',
'서해안선_함평지사',
'서해안선_화성지사',
'수도권제1순환선(판교일산)_동서울지사',
'수도권제1순환선(판교퇴계원)_동서울지사',
'수도권제1순환선_시흥지사',
'수도권제1순환선_인천지사',
'수도권제2순환선_군포지사',
'순천완주선_구례지사',
'순천완주선_진안지사',
'영동선_군포지사',
'영동선_대관령지사',
'영동선_원주지사',
'영동선_이천지사',
'영동선_진천지사',
'완주장수선_논산지사',
'완주장수선_무주지사',
'완주장수선_진안지사',
'울산선_경주지사',
'제2경인선(인천안양)_시흥지사',
'제2중부선_경기광주지사',
'중부내륙선_상주지사',
'중부내륙선_성주지사',
'중부내륙선_이천지사',
'중부내륙선_창년지사',
'중부내륙선_충주지사',
'중부내륙선의 지선_고령지사',
'중부내륙선의 지선_군위지사',
'중부내륙선의 지선_창녕지사',
'중앙선_군위지사',
'중앙선_양산지사',
'중앙선_영주지사',
'중앙선_제천지사',
'중앙선_홍천지사',
'중앙선의 지선_양산지사',
'청주상주선_보은지사',
'통영대전선,중부선_경기광주지사',
'통영대전선,중부선_고성지사',
'통영대전선,중부선_대전지사',
'통영대전선,중부선_무주지사',
'통영대전선,중부선_산청지사',
'통영대전선,중부선_영동지사',
'통영대전선,중부선_진천지사',
'평택제천선_엄정지사',
'평택제천선_화성지사',
'호남선_광주지사',
'호남선_논산지사',
'호남선_담양지사',
'호남선_순천지사',
'호남선_전주지사',
'호남선의 지선_논산지사',
'호남선의 지선_대전지사']

user_file_path = 'C:/sjbang/Final/'

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
            'OUTPUT': r'C:\sjbang\test\Refactored Layer.shp'
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