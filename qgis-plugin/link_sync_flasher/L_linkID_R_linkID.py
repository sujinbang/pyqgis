from qgis.utils import iface
from PyQt5.QtGui import QColor
from qgis.core import QgsProject, NULL

# 설정
SRC_LAYER_NAME = 'NT2_LINK'
SRC_KEY_FIELD = 'ID'
TARGET_CONFIG = {
    'RS1_ROADBORDER': {'L_linkID': '#FF0000'},
    'RM1_LANELINE': {'L_linkID': '#FF0000', 'R_linkID': '#0000FF'},
    'SF1_BARRIER': {'L_linkID': '#FF0000'}
}

def clean_val(v):
    """데이터 타입을 무시하고 비교 가능한 깨끗한 문자열로 변환"""
    if v is None or v == NULL: return None
    try:
        # 소수점 제거 (100.0 -> 100) 후 문자열 변환
        return str(int(float(v))).strip()
    except:
        return str(v).strip()

def sync_and_flash_rs1_fix():
    try:
        src_layer = QgsProject.instance().mapLayersByName(SRC_LAYER_NAME)[0]
        selected_keys = {clean_val(f[SRC_KEY_FIELD]) for f in src_layer.selectedFeatures() if f[SRC_KEY_FIELD] is not None}
        
        if not selected_keys: return

        for target_name, field_settings in TARGET_CONFIG.items():
            t_layers = QgsProject.instance().mapLayersByName(target_name)
            if not t_layers: continue
            tgt_layer = t_layers[0]
            
            # 레이어 가시성 확인 (꺼져있으면 Flash 안 보임)
            if not QgsProject.instance().layerTreeRoot().findLayer(tgt_layer.id()).isVisible():
                print(f"알림: {target_name} 레이어가 꺼져 있어 Flash가 보이지 않을 수 있습니다.")

            color_groups = {}
            for f in tgt_layer.getFeatures():
                for field_name, color_hex in field_settings.items():
                    # 필드 존재 여부 확인 (대소문자 무시 검색)
                    idx = f.fields().lookupField(field_name)
                    if idx < 0: continue
                    
                    val = clean_val(f[idx])
                    if val in selected_keys:
                        if color_hex not in color_groups: color_groups[color_hex] = []
                        color_groups[color_hex].append(f.id())
                        break

            for color_hex, ids in color_groups.items():
                if ids:
                    color = QColor(color_hex)
                    end_color = QColor(color.red(), color.green(), color.blue(), 0)
                    iface.mapCanvas().flashFeatureIds(tgt_layer, ids, color, end_color, 3, 300)
                    
    except Exception as e:
        print(f"Error: {e}")

# 연결 초기화 및 재연결
try:
    src_obj = QgsProject.instance().mapLayersByName(SRC_LAYER_NAME)[0]
    src_obj.selectionChanged.disconnect()
except: pass

QgsProject.instance().mapLayersByName(SRC_LAYER_NAME)[0].selectionChanged.connect(sync_and_flash_rs1_fix)
print("코드 실행 중...")