"""合并多个 JSON 文件为一个（支持 dry_run）"""
import json
import os


def main(params):
    input_dir = params.get('input_dir', '.')
    output_file = params.get('output_file', 'merged.json')
    dry_run = params.get('dry_run', False)

    if not os.path.isdir(input_dir):
        return {'status': 'error', 'message': f'目录不存在: {input_dir}'}

    json_files = sorted(f for f in os.listdir(input_dir) if f.endswith('.json'))
    if not json_files:
        return {'status': 'error', 'message': f'目录下无 .json 文件: {input_dir}'}

    merged = []
    errors = []
    for fname in json_files:
        try:
            with open(os.path.join(input_dir, fname), 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                merged.extend(data)
            else:
                merged.append(data)
        except Exception as e:
            errors.append({'file': fname, 'error': str(e)})

    if dry_run:
        return {
            'status': 'success',
            'message': f'[试运行] 将合并 {len(json_files)} 个文件，共 {len(merged)} 条记录，输出到 {output_file}',
            'dry_run': True,
            'files_count': len(json_files),
            'records_count': len(merged),
            'errors': errors,
            'sample': merged[:3] if merged else [],
        }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    return {
        'status': 'success',
        'message': f'已合并 {len(json_files)} 个文件（{len(merged)} 条记录）→ {output_file}',
        'output_file': os.path.abspath(output_file),
        'files_count': len(json_files),
        'records_count': len(merged),
        'errors': errors,
    }
