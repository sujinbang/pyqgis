import processing
from qgis.core import QgsProject
from qgis.utils import iface

buffer_layer_name = 'LANE_NO_1_Buffer_5m'
field_to_filter = 'path'  # 필터링할 필드 이름
extract_path = r'C:\sjbang\정밀도로지도\extract'
result_path = r'C:\sjbang\정밀도로지도\result'
output_path = r'C:\sjbang\정밀도로지도\output'

user_input = ['제2경인선(인천안양)_시흥지사',
'중부내륙선의 지선_고령지사',
'중부내륙선의 지선_군위지사',
'중부내륙선의 지선_창녕지사',
'중앙선의 지선_양산지사',
'호남선의 지선_논산지사',
'호남선의 지선_대전지사']


# 버퍼 위치 중첩된 부분 추출
def extract_buffer_by_location(buffer_layer_name, point_layer_name):

    extract_buffer = point_layer_name + '_step1'
    extract_layer = QgsProject.instance().mapLayersByName(buffer_layer_name)[0]
    boundary_layer = QgsProject.instance().mapLayersByName(point_layer_name)[0]

    # --- 2. 파라미터 설정 ---
    params = {
        'INPUT': extract_layer,
        'PREDICATE': [0],  # 공간 관계 조건: [0] Intersects, [1] Contains, [2] Disjoint, 등
        'INTERSECT': boundary_layer,
        'OUTPUT': extract_path + '\\' + extract_buffer + '.shp' # 결과물이 저장될 경로
    }

    # --- 3. 알고리즘 실행 ---
    result = processing.run("native:extractbylocation", params)

    # --- 4. 결과 레이어 QGIS에 추가 ---
    output_layer_path = result['OUTPUT']
    iface.addVectorLayer(output_layer_path, extract_buffer, 'ogr')
    
    print("'Step1' 작업이 완료되었습니다.")
    
    return extract_buffer

def get_filtered_paths(extract_buffer, field_to_filter):
    layers = QgsProject.instance().mapLayersByName(extract_buffer)
    if not layers:
        print(f"Error: Layer '{extract_buffer}' not found.")
        return []

    input_layer = layers[0]
    
    # --- path 칼럼 내 고유 값 추출 ---
    unique_values = {feature[field_to_filter] for feature in input_layer.getFeatures()}

    # 결과를 리스트로 변환 (필요시 정렬)
    unique_list = sorted(list(unique_values))
    filtered_paths = []  # 필터링된 경로를 저장할 리스트
    print(f"'{field_to_filter}' 필드의 고유한 값 ({len(unique_list)}개):")

    for val in unique_list:
        if (extract_buffer == '상주영덕선_청송지사_step1'):
            pass
        else:
            if (extract_buffer.split('_')[0] in val) and ('2019모델' in val):
                filtered_paths.append(val)
            elif (extract_buffer.split('_')[0] in val) and ('2020모델' in val) and ('-' not in val):
                filtered_paths.append(val)

    if not filtered_paths:
        print(f"Warning: No valid paths found in '{field_to_filter}' field.")
        # 노선별 예외처리
        if extract_buffer == '광주외곽순환선_광주지사_step1':
            filtered_paths.append(unique_list[0])  # 기본값으로 첫 번째 값을 사용
        elif extract_buffer == '남해제1지선_창원지사_step1':
            for val in unique_list:
                if ('남해1지선' in val) and ('2019모델' in val):
                    filtered_paths.append(val)
                elif ('남해1지선' in val) and ('2020모델' in val) and ('-' not in val):
                    filtered_paths.append(val)
        elif extract_buffer == '남해제2지선_창원지사_step1':
            for val in unique_list:
                if ('남해2지선' in val) and ('2019모델' in val):
                    filtered_paths.append(val)
                elif ('남해2지선' in val) and ('2020모델' in val) and ('-' not in val):
                    filtered_paths.append(val)
        elif extract_buffer in ('당진대전선_공주지사_step1', 
                                '당진대전선_당진지사_step1',
                                '청주상주선_보은지사_step1'):
            for val in unique_list:
                if ('당진영덕선' in val) and ('2019모델' in val):
                    filtered_paths.append(val)
                elif ('당진영덕선' in val) and ('2020모델' in val) and ('-' not in val):
                    filtered_paths.append(val)
        elif extract_buffer == '대구포항선_영천지사_step1':
            for val in unique_list:
                if ('새만금포항선' in val) and ('2019모델' in val):
                    filtered_paths.append(val)
                elif ('새만금포항선' in val) and ('2020모델' in val) and ('-' not in val):
                    filtered_paths.append(val)
        elif extract_buffer == '밀양울산선_서울산지사_step1':
            for val in unique_list:
                if ('함양울산선' in val) and ('2019모델' in val):
                    filtered_paths.append(val)
                elif ('함양울산선' in val) and ('2020모델' in val) and ('-' not in val):
                    filtered_paths.append(val)
        elif extract_buffer in ('부산포항선_울산지사_step1'):
            for val in unique_list:
                if ('동해선' in val) and ('2019모델' in val):
                    filtered_paths.append(val)
                elif ('동해선' in val) and ('2020모델' in val) and ('-' not in val):
                    filtered_paths.append(val)
        elif extract_buffer in ('수도권제1순환선(판교일산)_동서울지사_step1', 
                                '수도권제1순환선(판교퇴계원)_동서울지사_step1',
                                '수도권제1순환선_시흥지사_step1',
                                '수도권제1순환선_인천지사_step1'):
            for val in unique_list:
                if ('서울외곽순환선' in val) and ('2019모델' in val):
                    filtered_paths.append(val)
                elif ('서울외곽순환선' in val) and ('2020모델' in val) and ('-' not in val):
                    filtered_paths.append(val)
        elif extract_buffer in ('완주장수선_논산지사_step1',
                                '완주장수선_무주지사_step1',
                                '완주장수선_진안지사_step1'):
            for val in unique_list:
                if ('새만금포항선' in val) and ('2019모델' in val):
                    filtered_paths.append(val)
                elif ('새만금포항선' in val) and ('2020모델' in val) and ('-' not in val):
                    filtered_paths.append(val)
        elif extract_buffer in ('통영대전선,중부선_경기광주지사_step1',
                                '통영대전선,중부선_고성지사_step1',
                                '통영대전선,중부선_무주지사_step1',
                                '통영대전선,중부선_산청지사_step1',
                                '통영대전선,중부선_영동지사_step1',
                                '통영대전선,중부선_진천지사_step1'):
            for val in unique_list:
                if ('중부선' in val) and ('2019모델' in val):
                    filtered_paths.append(val)
                elif ('중부선' in val) and ('2020모델' in val) and ('-' not in val):
                    filtered_paths.append(val)
        elif extract_buffer == '부산포항선_경주지사_step1':
            for val in unique_list:
                if ('동해선' in val) and ('2019모델' in val):
                    filtered_paths.append(val)
                elif ('동해선' in val) and ('2020모델' in val) and ('-' not in val):
                    filtered_paths.append(val)
        elif extract_buffer == '상주영덕선_청송지사_step1':
            for val in unique_list:
                if ('당진영덕선' in val) and ('2019모델' in val):
                    filtered_paths.append(val)
                elif ('당진영덕선' in val) and ('2020모델' in val) and ('-' not in val):
                    filtered_paths.append(val)
        elif extract_buffer in ('남해선(순천부산)_순천지사_step1',
                                '남해선(순천부산)_양산지사_step1',
                                '남해선(순천부산)_진주지사_step1',
                                '남해선(순천부산)_창원지사_step1',
                                '남해선(영암순천)_보성지사_step1'):
            for val in unique_list:
                if ('남해선' in val) and ('2019모델' in val):
                    filtered_paths.append(val)
                elif ('남해선' in val) and ('2020모델' in val) and ('-' not in val):
                    filtered_paths.append(val)
        elif extract_buffer == '제2경인선(인천안양)_시흥지사_step1':
            for val in unique_list:
                if ('제2경인선' in val) and ('2019모델' in val):
                    filtered_paths.append(val)
                elif ('제2경인선' in val) and ('2020모델' in val) and ('-' not in val):
                    filtered_paths.append(val)
        elif extract_buffer in ('중부내륙선의 지선_고령지사_step1',
                                '중부내륙선의 지선_군위지사_step1',
                                '중부내륙선의 지선_창녕지사_step1',
                                '중앙선의 지선_양산지사_step1',
                                '호남선의 지선_논산지사_step1',
                                '호남선의 지선_대전지사_step1'):
            for val in unique_list:
                if (extract_buffer[:3] in val) and ('2019모델' in val):
                    filtered_paths.append(val)
                elif (extract_buffer[:3] in val) and ('2020모델' in val) and ('-' not in val):
                    filtered_paths.append(val)
                         

    return filtered_paths

# 속성값을 필터링하여 버퍼 추출
def extract_features_by_attribute(extract_buffer, field_to_filter, filter_value, index):
    
    extract_attr_buffer = f"{point_layer_name}_step2_{index}"

    layers = QgsProject.instance().mapLayersByName(extract_buffer)
    if not layers:
        print(f"Error: Layer '{extract_buffer}' not found.")
        return

    input_layer = layers[0]
           
    # Define the parameters for the 'Extract by Attribute' algorithm
    params = {
        'INPUT': input_layer,
        'FIELD': field_to_filter,  # 'path' 필드 사용
        'OPERATOR': 0,  # 0 corresponds to the '=' operator
        'VALUE': filter_value,  # 필터링된 경로가 있으면 첫 번째 값 사용, 없으면 기본값 사용
        'OUTPUT': extract_path + '\\' + extract_attr_buffer + '.shp' # 결과물이 저장될 경로
    }
    
    try:
        result = processing.run("native:extractbyattribute", params)
        output_layer_path = result['OUTPUT']
        
        # Add the resulting layer to the QGIS project
        iface.addVectorLayer(output_layer_path, extract_attr_buffer, "ogr")
        
        print("'Step2' 작업이 완료되었습니다.")

    except Exception as e:
        print(f"An error occurred during extraction: {e}")

    return extract_attr_buffer

# 위치에 따라 포인트 추출
def extract_point_by_location(point_layer_name, extract_attr_buffer, index):
    # 레이어명에 인덱스 추가
    extract_point = f"{point_layer_name}_result_{index}"

    extract_layer = QgsProject.instance().mapLayersByName(point_layer_name)[0]
    boundary_layer = QgsProject.instance().mapLayersByName(extract_attr_buffer)[0]

    # --- 2. 파라미터 설정 ---
    params = {
        'INPUT': extract_layer,
        'PREDICATE': [1],  # 공간 관계 조건: [0] Intersects, [1] Contains, [2] Disjoint, 등
        'INTERSECT': boundary_layer,
        'OUTPUT': result_path + '\\' + extract_point + '.shp' # 결과물이 저장될 경로
    }

    # --- 3. 알고리즘 실행 ---
    result = processing.run("native:extractbylocation", params)

    # --- 4. 결과 레이어 QGIS에 추가 ---
    output_layer_path = result['OUTPUT']
    iface.addVectorLayer(output_layer_path, extract_point, 'ogr')
    
    print("'Step3' 작업이 완료되었습니다.")
    
    return extract_point

# 추출된 포인트 데이터에 path 필드 추가
def pointAddField(extract_point, filter_value, field_to_filter):

    input_layers = QgsProject.instance().mapLayersByName(extract_point)
    
    if len(input_layers) > 0:
        input_layer = input_layers[0] # 첫 번째 일치하는 레이어 사용
        
        # name, length 필드 추가 (파이썬 API)
        input_layer.startEditing()
        field_path = QgsField(field_to_filter, QVariant.String, len=254)  # shapefile 문자열 필드 최대 길이

        provider = input_layer.dataProvider()
        provider.addAttributes([field_path])
        input_layer.commitChanges()
        input_layer.updateFields()
        
        # add features with attributes
        # Set attribute values
        layer = iface.activeLayer()
        layer.startEditing()
        for feature in layer.getFeatures():
            feature['path'] = filter_value
            # Add the feature to the layer
            layer.updateFeature(feature)
        # Update layer extent
        layer.commitChanges()
        print("'Step4' 작업이 완료되었습니다.")
    
# 레이어 삭제
def deleteLayer(target_list):
    project = QgsProject.instance()
    # 삭제하려는 레이어의 이름 (정확하게 입력)
    target_layer_list = target_list
    #'output_addfield'
    # 해당 이름의 레이어를 프로젝트에서 찾습니다.
    # mapLayersByName은 리스트를 반환하므로, 첫 번째 요소를 사용하거나 반복문을 사용합니다.
    for i in range(0,len(target_layer_list)):
        layers_to_remove = project.mapLayersByName(target_layer_list[i])
        if layers_to_remove:
            for layer in layers_to_remove:
                project.removeMapLayer(layer.id()) # 레이어 객체의 ID를 사용하여 제거

# 레이어 병합                
def merge_layers(input_layers, output_path):
    """
    여러 레이어를 하나로 병합하는 함수
    
    Parameters:
        input_layers (list): 병합할 레이어 목록
        output_path (str): 결과물 저장 경로 (.shp 포함)
    """
    # 레이어들을 병합하기 위한 파라미터 설정
    params = {
        'LAYERS': input_layers,  # 병합할 레이어들의 리스트
        'CRS': None,  # 좌표계 (None으로 설정하면 첫 번째 레이어의 CRS 사용)
        'FIELD_NAME_SUFFIX': '',  # 필드명 접미사 없음
        'INPUT_FIELD_LENGTH': 255,  # 필드 길이를 255로 설정
        'OUTPUT': output_path + '\\' + point_layer_name + '.shp'  # 결과물 저장 경로
    }
    
    # 병합 알고리즘 실행
    result = processing.run("native:mergevectorlayers", params)
    
    # 결과 레이어를 QGIS에 추가
    output_layer_path = result['OUTPUT']
    iface.addVectorLayer(output_layer_path, point_layer_name, 'ogr')
    
    print("레이어 병합이 완료되었습니다.")
    return result['OUTPUT']

# 함수 실행
for idx in range(0, len(user_input)):
    point_layer_name = user_input[idx]

    extract_buffer = extract_buffer_by_location(buffer_layer_name, point_layer_name)
    filtered_paths = get_filtered_paths(extract_buffer, field_to_filter)
    for i in range(0, len(filtered_paths)):
        filter_value = filtered_paths[i]
        print(f"\n작업 진행중: {i+1}/{len(filtered_paths)}")
        # 속성값을 필터링하여 버퍼 추출
        extract_attr_buffer = extract_features_by_attribute(extract_buffer, field_to_filter, filter_value, i)
        extract_point = extract_point_by_location(point_layer_name, extract_attr_buffer, i)
        pointAddField(extract_point, filter_value, field_to_filter)
        deleteLayer([extract_attr_buffer])
    deleteLayer([extract_buffer])
    # 레이어 병합
    layers = []
    for layer in QgsProject.instance().mapLayers().values():
        if layer.name().startswith(point_layer_name + '_result_'):  # 예: '경부선_' 으로 시작하는 레이어들
            layers.append(layer)

    merge_layers(layers, output_path)



