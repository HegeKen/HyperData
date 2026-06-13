import OScommon
import json
import os

def sync_aspatch_from_db():
    """
    按照 OScommon.order 的顺序遍历本地 JSON 数据，
    从数据库获取 aspatch 并添加到对应的 ROM 数据中。
    数据库中 aspatch 为 NULL 时写入空字符串。
    """
    # 1. 获取 order 列表中的设备
    devices_order = OScommon.order
    updated_count = 0
    skipped_count = 0
    total_checked = 0

    print(f"开始从数据库同步 aspatch 到 JSON 文件...")
    print(f"共 {len(devices_order)} 个设备需要处理")
    print("-" * 80)

    for device in devices_order:
        device_file = OScommon.get_platform_path(f"public/data/devices/{device}.json")

        if not os.path.exists(device_file):
            print(f"跳过不存在的设备: {device}")
            skipped_count += 1
            continue

        try:
            with open(device_file, 'r', encoding='utf-8') as f:
                devdata = json.load(f)
        except Exception as e:
            print(f"读取 {device}.json 失败: {e}")
            skipped_count += 1
            continue

        device_name = devdata.get('name', {}).get('zh', '') or devdata.get('name', {}).get('en', device)
        branches = devdata.get('branches', [])
        device_updated = 0

        for branch in branches:
            roms = branch.get('roms', {})
            table_fields = branch.get('table', [])

            # 检查是否需要处理 aspatch
            if 'aspatch' not in table_fields:
                continue

            for version, rom_data in roms.items():
                total_checked += 1

                # 从数据库查询 aspatch
                code = branch.get('branchCode', '')
                if not code:
                    continue

                try:
                    # 查询数据库
                    sql = f"SELECT aspatch FROM roms WHERE code = '{code}' AND version = '{version}' LIMIT 1"
                    result = OScommon.db_job_latest(sql)

                    # 获取 aspatch 值，如果为 NULL 则写入空字符串
                    if result and result[0]:
                        # 将 date 对象转换为字符串格式 (YYYY-MM-DD)
                        aspatch_value = str(result[0]) if hasattr(result[0], 'strftime') else result[0]
                    else:
                        aspatch_value = ""

                    # 重建 rom_data，将 aspatch 插入到 release 和 recovery 之间
                    new_rom_data = {}
                    for key, value in rom_data.items():
                        new_rom_data[key] = value
                        # 在 release 之后插入 aspatch
                        if key == 'release':
                            new_rom_data['aspatch'] = aspatch_value
                    roms[version] = new_rom_data

                    device_updated += 1
                    print(f"✓ [{device}] {device_name} - {version} → {aspatch_value if aspatch_value else '(空)'}")
                except Exception as e:
                    print(f"✗ [{device}] 查询失败: {version} - {e}")
                    continue

        # 如果有更新，保存文件
        if device_updated > 0:
            try:
                with open(device_file, 'w', encoding='utf-8') as f:
                    json.dump(devdata, f, ensure_ascii=False, indent='\t')
                updated_count += device_updated
                print(f"[{device}] 已更新 {device_updated} 条 aspatch")
            except Exception as e:
                print(f"✗ [{device}] 保存失败: {e}")

    print("-" * 80)
    print(f"处理完成!")
    print(f"检查 ROM: {total_checked}")
    print(f"更新 aspatch: {updated_count}")
    print(f"跳过设备: {skipped_count}")

if __name__ == "__main__":
    sync_aspatch_from_db()