"""读取 CSV 文件并返回统计摘要"""
import csv
import os


def main(params):
    filepath = params.get('filepath', '')
    encoding = params.get('encoding', 'utf-8')

    if not filepath:
        return {'status': 'error', 'message': '请提供 filepath 参数'}
    if not os.path.isfile(filepath):
        return {'status': 'error', 'message': f'文件不存在: {filepath}'}

    try:
        with open(filepath, 'r', encoding=encoding, newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            columns = reader.fieldnames or []
    except Exception as e:
        return {'status': 'error', 'message': f'读取失败: {e}'}

    summary = {
        'total_rows': len(rows),
        'columns': columns,
        'column_count': len(columns),
    }

    for col in columns:
        values = [r[col] for r in rows if r.get(col)]
        summary[f'col_{col}_non_empty'] = len(values)
        nums = []
        for v in values:
            try:
                nums.append(float(v))
            except (ValueError, TypeError):
                pass
        if nums:
            summary[f'col_{col}_min'] = min(nums)
            summary[f'col_{col}_max'] = max(nums)
            summary[f'col_{col}_avg'] = round(sum(nums) / len(nums), 2)

    return {
        'status': 'success',
        'message': f'CSV 摘要：{len(rows)} 行 × {len(columns)} 列',
        'filepath': os.path.abspath(filepath),
        'summary': summary,
        'preview': rows[:5] if rows else [],
    }
