from qgis.core import QgsTextFormat, QgsTextBufferSettings, QgsPalLayerSettings, QgsVectorLayerSimpleLabeling, QgsProject
from PyQt5.QtGui import QColor, QFont

def get_layer_field_names(layer):

    field_names = []
    # 레이어의 필드 객체들을 가져옵니다.
    fields = layer.fields()
    for field in fields:
        # 각 필드의 이름을 리스트에 추가합니다.
        field_names.append(field.name())
        
    return field_names

def set_layer_labeling(layer_name, label_field_name):

    input_layers = QgsProject.instance().mapLayersByName(layer_name)
    layer = input_layers[0]

    text_format = QgsTextFormat()
    text_format.setFont(QFont("Arial"))
    text_format.setSize(12)
    text_format.setColor(QColor("white"))
    buffer_settings = QgsTextBufferSettings()
    buffer_settings.setEnabled(True)
    buffer_settings.setSize(1)
    buffer_settings.setColor(QColor("gray"))
    text_format.setBuffer(buffer_settings)
    layer_settings = QgsPalLayerSettings()
    layer_settings.setFormat(text_format)
    layer_settings.fieldName = label_field_name
    layer_settings.placement = QgsPalLayerSettings.Line
    label_settings = QgsVectorLayerSimpleLabeling(layer_settings)
    layer.setLabelsEnabled(True)
    layer.setLabeling(label_settings)
    layer.triggerRepaint()

    print(f"'{layer_name}' 레이어의 라벨이 '{label_field_name}' 필드로 설정되었습니다.")
    print("라벨링이 성공적으로 적용되었습니다!")


# QGIS 파이썬 콘솔에서 아래 함수 실행
# set_layer_labeling('points_layer', 'SYSTEM_ID')
