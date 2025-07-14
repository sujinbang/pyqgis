import os
from qgis.core import QgsVectorFileWriter, QgsProject, QgsFeatureRequest

def export_selected_features(user_input, expression, output_filename):
    layer_name = user_input
    input_layers = QgsProject.instance().mapLayersByName(layer_name)
    layer = input_layers[0]

    layer.selectByExpression(expression)

    output_dir = r'C:\Users\sjbang\Desktop\블로그\정밀도로지도\pyqgis\ETC_도로중심선_1년_1년_2024\export-selected-features' # 내보낼 폴더 경로 (예: 'C:/Users/사용자명/Documents/QGIS_Output')
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

road_list = ['경부선',
'남해선(영암순천)',
'남해선(순천부산)',
'무안광주선',
'광주대구선',
'밀양울산선',
'함양울산선',
'서해안선',
'울산선',
'평택화성선',
'완주장수선',
'새만금포항선(대구~포항)',
'논산천안선/호남선',
'호남선',
'논산천안선',
'순천완주선',
'구리포천선',
'양주지선',
'서산영덕선(상주영덕선)',
'서산영덕선(청주상주선)',
'서산영덕선(당진대전선)',
'당진청주선',
'통영대전선/중부선',
'통영대전선',
'중부선',
'제2중부선',
'평택제천선',
'중부내륙선',
'영동선',
'중앙선',
'서울양양선',
'동해선',
'동해선(삼척속초)',
'부산포항선',
'수도권제1순환선',
'수도권제1순환선(판교퇴계원)',
'수도권제1순환선(퇴계원일산)',
'수도권제1순환선(판교일산)',
'남해제1지선',
'남해제2지선',
'제2경인선(인천안양)',
'경인선',
'인천국제공항선',
'서천공주선',
'오산화성선',
'새만금포항선의 지선',
'호남선의 지선',
'고창담양선',
'대전남부순환선',
'봉담동탄선',
'중부내륙선의 지선',
'광주외곽순환선',
'중앙선의 지선',
'부산외곽순환선',
'대구외곽순환선'
]
def main_func():
    user_input = 'ETC_S0_07_04_709280'

    for i in range(0, len(road_list)):
        road_name = road_list[i]
        expression = f'"도로명" = \'{road_name}\''
        output_filename = road_list[i] + '.shp'
        export_selected_features(user_input, expression, output_filename)

main_func()