from qgis.core import QgsWkbTypes, QgsProject
from qgis.utils import iface

fieldList = []

def editSymbol(user_input):
    layer_name = user_input
    input_layers = QgsProject.instance().mapLayersByName(layer_name)
    layer = input_layers[0]

    # layer = iface.activeLayer()

    if layer is None:
        print("활성화된 레이어가 없습니다. 변경할 레이어를 선택해주세요.")
    else:
        # 2. 심볼 라인 너비 설정
        target_line_width = 2.0 # <--- 여기에 원하는 라인 너비를 입력하세요.

        renderer = layer.renderer()
        geom_type = layer.wkbType() # 레이어의 기하학적 타입 가져오기

        # 레이어가 라인 또는 폴리곤 타입인지 확인 (QgsWkbTypes 상수를 직접 비교)
        if (geom_type == QgsWkbTypes.LineString or
            geom_type == QgsWkbTypes.MultiLineString or
            geom_type == QgsWkbTypes.Polygon or
            geom_type == QgsWkbTypes.MultiPolygon):

            if renderer is not None and renderer.symbol() is not None:
                symbol = renderer.symbol()
                line_symbols_found = 0
                
                # 심볼의 각 레이어를 순회하며 라인 심볼을 찾아서 너비 변경
                for sym_layer in symbol.symbolLayers():
                    # 라인 심볼 레이어인지 확인 (width 속성을 가지며 마커 심볼이 아님)
                    if hasattr(sym_layer, 'width') and sym_layer.type() != 'SimpleMarker':
                        sym_layer.setWidth(target_line_width)
                        line_symbols_found += 1
                        
                if line_symbols_found > 0:
                    layer.triggerRepaint() # 레이어 다시 그리기 (변경사항 적용)
                    print(f"'{layer.name()}' 레이어 심볼의 라인 너비를 {target_line_width}으로 설정했습니다. (총 {line_symbols_found}개 라인 심볼 레이어 변경)")
                else:
                    print(f"'{layer.name()}' 레이어 심볼에서 설정 가능한 라인 심볼 레이어를 찾을 수 없습니다. (포인트 심볼 제외)")
            else:
                print(f"'{layer.name()}' 레이어에 렌더러나 심볼이 설정되어 있지 않습니다.")
        else:
            print(f"'{layer.name()}'은(는) 선 또는 폴리곤 레이어가 아닙니다. 라인 심볼 너비를 변경할 수 없습니다.")

for num in range(0, len(fieldList)):
    user_input = fieldList[num]
    editSymbol(user_input)