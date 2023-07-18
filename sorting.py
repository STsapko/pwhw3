from concurrent.futures import ThreadPoolExecutor
import shutil
from pathlib import Path

categories = {
    'audio': ('.mp3', '.ogg', '.wav', '.amr'),
    'video': ('.avi', '.mp4', '.mov', '.mkv'),
    'images': ('.jpeg', '.png', '.jpg', '.svg'),
    'documents': ('.doc', '.docs', '.txt', '.pdf', '.xlsx', '.pptx'),
    'archives': ('.zip', '.gz', '.tar')
}

def get_file_category(file_path: Path):
    file_extension = file_path.suffix.lower()
    file_path_category = next((category for category, extensions in categories.items() if file_extension in extensions), 'other')
    return file_path_category

def move_file(file_path, target_dir_path):
    try:
        shutil.move(file_path, target_dir_path)
    except shutil.Error:
        pass
        
def collect_file_paths(folder_path: Path):
    file_paths = []
    items = folder_path.iterdir()
    with ThreadPoolExecutor() as ex:
        for item in items:
            if item.is_file():
                file_paths.append(item)
            if item.is_dir():
                future = ex.submit(collect_file_paths, item)
                file_paths.extend(future.result())
    return file_paths

def sort_dir(folder_path: str):
    folder_path = Path(folder_path)
    file_paths = collect_file_paths(folder_path)
    other_folder = folder_path / "other"
    other_folder.mkdir(exist_ok = True)
    
    for category in categories:
        category_folder_path = folder_path / category
        category_folder_path.mkdir(exist_ok = True)
        
    with ThreadPoolExecutor() as ex:
        for file_path in file_paths:
            target_dir_path = folder_path / get_file_category(file_path)
            if target_dir_path != file_path.parent:
                ex.submit(move_file, file_path, target_dir_path)

def remove_empty_folder(folder_path: str):
    folder_path = Path(folder_path)
    for item in folder_path.iterdir():
        if item.is_dir():
            remove_empty_folder(item)
    if not any(folder_path.iterdir()):
        folder_path.rmdir()
        
def main(folder_path: str):
   sort_dir(folder_path)
   remove_empty_folder(folder_path)

if __name__ == '__main__':
    folder_path = "C:\\Users\\Surface\\Рабочий стол\\test"
    main(folder_path)
            