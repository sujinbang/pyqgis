from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterField,
    QgsFeatureSink,
    QgsFeature,
    QgsField
)

class ExtractPointsByDistance(QgsProcessingAlgorithm):
    def name(self): return 'extract_by_distance_match'
    def displayName(self): return '거리값 매칭 포인트 추출'
    def group(self): return 'sjbang'
    def groupId(self): return 'sjbang'
    def createInstance(self): return ExtractPointsByDistance()

    INPUT_POINTS = 'INPUT_POINTS'
    INPUT_FIELD = 'INPUT_FIELD'
    INPUT_DRIVEWAY = 'INPUT_DRIVEWAY'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ExtractPointsByDistance()

    def name(self):
        return 'extract_by_distance_match'

    def displayName(self):
        return self.tr('거리값 매칭 포인트 추출')

    def group(self):
        return self.tr('sjbang')

    def groupId(self):
        return 'sjbang'

    def initAlgorithm(self, config=None):
        # 영동선_전체_1m 레이어 입력
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_POINTS,
                self.tr('이정_1m (포인트 레이어)'),
                [QgsProcessing.TypeVectorPoint]
            )
        )
        # 003_A3_DRIVEWAYSECTION 레이어 입력
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_DRIVEWAY,
                self.tr('벡터 레이어'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        # 필드 입력
        self.addParameter(
            QgsProcessingParameterField(
                self.INPUT_FIELD,
                self.tr('이정_1m 거리값 필드'),
                parentLayerParameterName=self.INPUT_POINTS
            )
        )
        # 결과 출력
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('추출된 포인트 레이어')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        # 소스 레이어 가져오기
        source_points = self.parameterAsSource(parameters, self.INPUT_POINTS, context)
        source_driveway = self.parameterAsSource(parameters, self.INPUT_DRIVEWAY, context)
        field_name = self.parameterAsString(parameters, self.INPUT_FIELD, context)
        
        feedback.pushInfo(f"선택된 필드명: {field_name}")
        
        # 결과 레이어 전용 필드 구성 (기본 필드 + PNT_SE 구분 필드)
        output_fields = source_points.fields()
        output_fields.append(QgsField('PNT_SE', QVariant.String))

        # 결과 레이어 생성
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            output_fields,
            source_points.wkbType(),
            source_points.sourceCrs()
        )

        # 1. 포인트 레이어를 딕셔너리로 인덱싱 (거리값 -> [피처들])
        point_map = {}
        for feat in source_points.getFeatures():
            if feedback.isCanceled(): break
            try:
                dist_val = float(feat[field_name])
                if dist_val not in point_map:
                    point_map[dist_val] = []
                point_map[dist_val].append(feat)
            except (ValueError, TypeError) as e:
                feedback.pushInfo(f"필드 읽기 오류: {e}")
                continue
        
        feedback.pushInfo(f"포인트 맵 생성 완료: {len(point_map)}개의 고유 거리값")

        # 2. DRIVEWAY 레이어를 돌면서 ST와 ED 각각 매칭하여 추출
        driveway_features = source_driveway.getFeatures()
        total = source_driveway.featureCount()
        
        st_count = 0
        ed_count = 0
        
        for current, d_feat in enumerate(driveway_features):
            if feedback.isCanceled():
                break

            # Start Point 매칭
            st = d_feat['CTLN_STPNT']
            if st is not None:
                st_val = float(st)
                if st_val in point_map:
                    for p_feat in point_map[st_val]:
                        new_feat = QgsFeature(p_feat)
                        # 원본 속성에 'ST' 추가
                        attrs = p_feat.attributes()
                        attrs.append('ST')
                        new_feat.setAttributes(attrs)
                        sink.addFeature(new_feat, QgsFeatureSink.FastInsert)
                        st_count += 1

            # End Point 매칭
            ed = d_feat['CTLN_EDPNT']
            if ed is not None:
                ed_val = float(ed)
                if ed_val in point_map:
                    for p_feat in point_map[ed_val]:
                        new_feat = QgsFeature(p_feat)
                        # 원본 속성에 'ED' 추가
                        attrs = p_feat.attributes()
                        attrs.append('ED')
                        new_feat.setAttributes(attrs)
                        sink.addFeature(new_feat, QgsFeatureSink.FastInsert)
                        ed_count += 1

            # 진행률 표시
            if total > 0:
                feedback.setProgress(int(current / total * 100))
        
        feedback.pushInfo(f"추출 완료 - ST: {st_count}개, ED: {ed_count}개, 총 {st_count + ed_count}개")

        return {self.OUTPUT: dest_id}