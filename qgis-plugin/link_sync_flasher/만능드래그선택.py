from qgis.utils import iface
from qgis.gui import QgsMapToolIdentify, QgsRubberBand
from qgis.core import QgsProject, QgsVectorLayer, QgsRectangle, QgsWkbTypes, QgsApplication
from PyQt5.QtWidgets import QAction, QShortcut
from PyQt5.QtGui import QIcon, QColor, QKeySequence
from PyQt5.QtCore import Qt, QObject

# --- 1. 만능 드래그 & 클릭 선택 툴 클래스 ---
# class MagicDragSelectTool(QgsMapToolIdentify):
#     def __init__(self, canvas):
#         super().__init__(canvas)
#         self.canvas = canvas
#         self.dragging = False
#         self.rubber_band = QgsRubberBand(self.canvas, QgsWkbTypes.PolygonGeometry)
#         self.rubber_band.setColor(QColor(0, 120, 215, 60)) 
#         self.rubber_band.setWidth(1)
#         self.setCursor(Qt.PointingHandCursor)

#     def canvasPressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.dragging = True
#             self.start_pos = event.pos()
#             self.rubber_band.reset(QgsWkbTypes.PolygonGeometry)

#     def canvasMoveEvent(self, event):
#         if self.dragging:
#             rect = QgsRectangle(self.toMapCoordinates(self.start_pos), self.toMapCoordinates(event.pos()))
#             self.rubber_band.setToCanvasRectangle(self.canvas.mapSettings().mapToPixel().transform(rect).toRect())
#             self.rubber_band.show()

#     def canvasReleaseEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.dragging = False
#             self.rubber_band.hide()
#             end_pos = event.pos()
            
#             if (self.start_pos - end_pos).manhattanLength() < 5:
#                 results = self.identify(event.x(), event.y(), self.TopDownAll)
#             else:
#                 rect = QgsRectangle(self.toMapCoordinates(self.start_pos), self.toMapCoordinates(end_pos))
#                 results = self.identify(rect, self.TopDownAll)

#             if not results: return

#             target_res = results[0]
#             layer = target_res.mLayer
#             if isinstance(layer, QgsVectorLayer):
#                 if iface.activeLayer() != layer:
#                     iface.layerTreeView().setCurrentLayer(layer)
                
#                 layer.removeSelection()
#                 if (self.start_pos - end_pos).manhattanLength() < 5:
#                     layer.select(target_res.mFeature.id())
#                 else:
#                     ids = [res.mFeature.id() for res in results if res.mLayer == layer]
#                     layer.selectByIds(ids)
                
#                 self.canvas.refresh()
#                 iface.statusBarIface().showMessage(f"✨ {layer.name()} 선택됨", 1000)

# --- 2. 공식 단축키 등록 및 액션 설정 ---
def setup_final_magic_tool():
    # 중복 제거 (기존 액션 및 단축키 청소)
    if hasattr(iface, 'magic_action'):
        iface.removeToolBarIcon(iface.magic_action)
    
    # 새로운 액션 생성
    icon = QIcon(QgsApplication.iconPath("mActionStar.svg"))
    action = QAction(icon, "만능 드래그 선택 (End)", iface.mainWindow())
    action.setCheckable(True)
    action.setObjectName("MagicSelectAction") # 시스템 내부 이름 설정
    
    def toggle_tool():
        canvas = iface.mapCanvas()
        if action.isChecked():
            iface.magic_tool = MagicDragSelectTool(canvas)
            canvas.setMapTool(iface.magic_tool)
            iface.statusBarIface().showMessage("🌟 만능 선택 모드 활성화", 2000)
        else:
            canvas.unsetMapTool(getattr(iface, 'magic_tool', None))
            iface.statusBarIface().showMessage("만능 선택 모드 해제", 1000)

    action.triggered.connect(toggle_tool)
    
    # 툴 변경 시 버튼 상태 동기화
    iface.mapCanvas().mapToolSet.connect(lambda tool: action.setChecked(tool == getattr(iface, 'magic_tool', None)))

    # 툴바에 추가
    iface.addToolBarIcon(action)
    iface.magic_action = action

    # --- 3. [핵심] End 키 단축키 강제 연결 ---
    # QAction에 단축키 직접 할당 (가장 우선순위가 높음)
    action.setShortcut(QKeySequence(Qt.Key_End))
    
    # QGIS 단축키 매니저에 등록 (설정 -> 키보드 단축키에 나타나게 함)
    iface.registerMainWindowAction(action, "End")

    print("✅ [최종 완료] 이제 'End' 키로 기능을 켜고 끌 수 있습니다.")
    print("💡 만약 작동하지 않으면 QGIS 상단의 별표 아이콘을 직접 확인해보세요.")

setup_final_magic_tool()