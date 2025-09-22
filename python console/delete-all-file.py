import os

# line 데이터 제외 모두 삭제
target_folder = r"C:\sjbang\test"

# 파일 삭제
def delete_all_files_in_folder(folder_path):
    deleted_count = 0
    # os.listdir()는 폴더 내의 모든 파일과 폴더 이름을 리스트로 반환합니다.
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename) # 파일의 전체 경로 생성
        
        # 파일인지 확인 (폴더는 삭제하지 않음)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path) # 파일 삭제
                deleted_count += 1
            except OSError as e:
                print(f"  오류: '{filename}' 삭제 실패 - {e}")
        else:
            print(f"  건너뜀 (폴더): {filename}")

    print(f"'{folder_path}' 폴더에서 총 {deleted_count}개의 파일이 삭제되었습니다.")
    
delete_all_files_in_folder(target_folder)