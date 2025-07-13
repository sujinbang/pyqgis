import os
from qgis.core import QgsVectorFileWriter, QgsProject, QgsFeatureRequest

user_input = 'ETC_S0_07_04_709280'
expression = u'"도로명" = \'경부선\''
output_filename = 'test.shp'

def export_selected_features(user_input, expression, output_filename):
    layer_name = user_input
    input_layers = QgsProject.instance().mapLayersByName(layer_name)
    layer = input_layers[0]

    layer.selectByExpression(expression)

    output_dir = r'C:\Users\sjbang\Desktop\블로그\정밀도로지도\ETC_도로중심선_1년_1년_2024' # 내보낼 폴더 경로 (예: 'C:/Users/사용자명/Documents/QGIS_Output')
    #output_filename = 'test_export_data.shp' # 내보낼 파일 이름 (확장자 포함)
    output_format = "ESRI Shapefile" # "ESRI Shapefile", "GPKG", "GeoJSON" 등 원하는 형식
    output_filepath = os.path.join(output_dir, output_filename)
    os.makedirs(output_dir, exist_ok=True) # 출력 디렉토리 생성

    # QgsVectorFileWriter를 사용하여 선택된 피처만 파일로 내보내기
    # 'onlySelected=True'가 핵심입니다!
    QgsVectorFileWriter.writeAsVectorFormat(
        layer,
        output_filepath,
        'korean',
        driverName='ESRI Shapefile',
        onlySelected=True
    )

    print(f"쿼리로 선택된 피처가 '{output_filepath}' (으)로 성공적으로 내보내졌습니다.")

    # 내보낸 레이어를 QGIS에 추가 (선택 사항)
    iface.addVectorLayer(output_filepath, os.path.basename(output_filepath), 'ogr')

export_selected_features(user_input, expression, output_filename)