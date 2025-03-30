import bpy
import os
import json
from typing import List, Tuple

# 缓存目录列表
_cached_directories = None
_cached_items = None

def get_config_path():
    """获取配置文件路径"""
    return os.path.join(bpy.utils.user_resource('CONFIG'), 'cctools_export_dirs.json')

def load_directories() -> List[str]:
    """加载保存的导出目录列表"""
    global _cached_directories
    
    if _cached_directories is not None:
        return _cached_directories.copy()
        
    config_path = get_config_path()
    directories = []
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                directories = json.load(f)
                # 验证目录是否存在
                directories = [d for d in directories if os.path.exists(d)]
        except Exception as e:
            print(f"加载目录历史出错: {str(e)}")
    
    _cached_directories = directories
    return directories.copy()

def save_directories(directories: List[str], max_count: int = 10) -> None:
    """保存导出目录列表
    
    Args:
        directories: 目录列表
        max_count: 最大保存数量，默认10个
    """
    global _cached_directories, _cached_items
    
    try:
        # 移除重复项并保持顺序
        unique_dirs = []
        seen = set()
        for d in reversed(directories):
            if d not in seen and os.path.exists(d):
                seen.add(d)
                unique_dirs.append(d)
        
        # 保留最新的N个目录
        unique_dirs = unique_dirs[:max_count]
        unique_dirs.reverse()  # 恢复原始顺序
        
        # 更新缓存
        _cached_directories = unique_dirs
        _cached_items = None  # 清除枚举项缓存
        
        # 保存到文件
        config_path = get_config_path()
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(unique_dirs, f, ensure_ascii=False, indent=2)
        
    except Exception as e:
        print(f"保存目录历史出错: {str(e)}")

def format_path(path: str) -> Tuple[str, str]:
    """格式化路径显示
    
    Args:
        path: 完整路径
    Returns:
        显示名称, 提示信息
    """
    try:
        if not path:
            return "无历史记录", ""
            
        # 标准化路径分隔符
        path = os.path.normpath(path)
        
        # 获取驱动器和路径部分
        drive, tail = os.path.splitdrive(path)
        
        # 分割路径
        parts = tail.split(os.sep)
        parts = [p for p in parts if p]  # 移除空字符串
        
        if not parts:
            return path, path
            
        # 如果路径很短，直接返回
        if len(parts) <= 2:
            return path, path
            
        # 生成显示名称
        if len(parts) > 2:
            # 显示格式：驱动器:\第一级目录\最后一级目录
            if drive:
                display_name = f"{drive}{os.sep}{parts[0]}{os.sep}...{os.sep}{parts[-1]}"
            else:
                display_name = f"{parts[0]}{os.sep}...{os.sep}{parts[-1]}"
        else:
            display_name = path
            
        return display_name, path
        
    except Exception as e:
        print(f"格式化路径出错: {str(e)}")
        return path, path

def get_directory_items(self, context) -> List[Tuple[str, str, str]]:
    """获取目录列表项
    
    Returns:
        List of tuples (identifier, name, description)
    """
    global _cached_items
    
    try:
        # 如果有缓存的枚举项，直接返回
        if _cached_items is not None:
            return _cached_items
            
        directories = load_directories()
        items = []
        
        # 按最后修改时间排序
        dir_with_time = [(d, os.path.getmtime(d)) for d in directories if os.path.exists(d)]
        dir_with_time.sort(key=lambda x: x[1], reverse=True)
        
        # 转换为枚举项
        for d, _ in dir_with_time:
            display_name, tooltip = format_path(d)
            items.append((d, display_name, tooltip))
        
        # 如果列表为空，添加一个提示项
        if not items:
            items.append(("", "无历史记录", ""))
            
        # 缓存结果
        _cached_items = items
        return items
        
    except Exception as e:
        print(f"获取目录列表出错: {str(e)}")
        return [("", "加载出错", "")]

def update_directory(self, context) -> None:
    """更新当前目录"""
    try:
        if hasattr(self, 'text_file_enum') and self.text_file_enum:
            if os.path.exists(self.text_file_enum):
                context.scene.manual_directory = self.text_file_enum
            else:
                print(f"选择的目录不存在: {self.text_file_enum}")
                # 从列表中移除不存在的目录
                directories = load_directories()
                if self.text_file_enum in directories:
                    directories.remove(self.text_file_enum)
                    save_directories(directories)
    except Exception as e:
        print(f"更新目录出错: {str(e)}")

def refresh_directory_list():
    """强制刷新目录列表"""
    global _cached_directories, _cached_items
    
    try:
        # 清除缓存
        _cached_directories = None
        _cached_items = None
        
        # 强制重绘UI
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                area.tag_redraw()
    except Exception as e:
        print(f"刷新目录列表出错: {str(e)}") 