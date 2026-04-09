from qgis.gui import QgsMapToolEmitPoint
from qgis.utils import iface
from qgis.core import QgsProject, QgsRectangle
from PyQt5.QtWidgets import QApplication

# --- [설정값 입력 구역] ---
CONFIG = {
    'A2_5지구': ['path'],
    '5지구_MERGE': ['layer', 'SecName'],
    'NT2_5지구': ['path']
}
# -----------------------

class ClickToCopyTool(QgsMapToolEmitPoint):
    def __init__(self, canvas):
        super(ClickToCopyTool, self).__init__(canvas)
        self.canvas = canvas

    def canvasReleaseEvent(self, e):
        # 1. 클릭한 지점의 좌표 계산
        point = self.toMapCoordinates(e.pos())
        
        # 2. 좌표계 가져오기 (수정된 부분)
        crs = self.canvas.mapSettings().destinationCrs()
        
        # 검색 반경 설정 (현재 화면의 1픽셀 크기 기준으로 클릭 범위 생성)
        pixel_size = self.canvas.mapUnitsPerPixel()
        tolerance = pixel_size * 5 
        search_rect = QgsRectangle(
            point.x() - tolerance, point.y() - tolerance,
            point.x() + tolerance, point.y() + tolerance
        )

        found_any = False

        # 3. 프로젝트 내 레이어 순회
        for layer_name, fields in CONFIG.items():
            layers = QgsProject.instance().mapLayersByName(layer_name)
            if not layers:
                continue
            
            layer = layers[0]
            # 해당 영역에 걸치는 객체들 가져오기
            features = [f for f in layer.getFeatures(search_rect)]
            
            if features:
                # 첫 번째로 발견된 객체 처리
                feat = features[0]
                try:
                    vals = [str(feat[field]) for field in fields if field in feat.attributeMap() or field in [f.name() for f in layer.fields()]]
                    if not vals: continue
                    
                    final_text = " - ".join(vals)
                    
                    # 4. 클립보드 복사
                    QApplication.clipboard().setText(final_text)
                    iface.messageBar().pushMessage("클릭 복사", f"[{layer_name}] {final_text}", level=0, duration=1)
                    found_any = True
                    break 
                except Exception as ex:
                    print(f"데이터 추출 중 오류: {ex}")
                    continue
        
        if not found_any:
            # 설정된 레이어가 아닌 곳을 클릭했을 때 알림 (콘솔 출력)
            print("해당 지점에 설정된 레이어 객체가 없습니다.")

# --- 실행부 ---
canvas = iface.mapCanvas()
# 기존 툴이 있다면 해제하고 새 툴 등록
my_tool = ClickToCopyTool(canvas)
canvas.setMapTool(my_tool)

print("🎯 '다이렉트 클릭 복사' 모드 재시작!")