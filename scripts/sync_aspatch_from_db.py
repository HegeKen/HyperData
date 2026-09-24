import OScommon
import json
import os
import sys

def sync_aspatch_from_db(only_devices=None):
    """
    按照 OScommon.order 的顺序遍历本地 JSON 数据，
    从数据库获取 aspatch 并添加到对应的 ROM 数据中。
    数据库中 aspatch 为 NULL 时写入空字符串。
    """
    # 1. 获取 order 列表中的设备
    devices_order = OScommon.order
    if only_devices:
        devices_order = [d for d in devices_order if d in only_devices]
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

                    # 如果 aspatch 已存在则原地更新，否则在 release 之后插入
                    if 'aspatch' in rom_data:
                        rom_data['aspatch'] = aspatch_value
                    else:
                        new_rom_data = {}
                        for key, value in rom_data.items():
                            new_rom_data[key] = value
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

def check_aspatch_key(only_devices=None):
    """
    检查所有设备 JSON 分支是否设置了 aspatch 键。
    缺失时提示并自动修复：在 table 的 release 之后插入 aspatch，
    并为每个 ROM 条目补充 aspatch 空值。
    """
    fixed_count = 0
    checked_count = 0

    print("开始检查 aspatch 键...")
    print("-" * 80)

    devices_order = OScommon.order
    if only_devices:
        devices_order = [d for d in devices_order if d in only_devices]

    for device in devices_order:
        device_file = OScommon.get_platform_path(f"public/data/devices/{device}.json")

        if not os.path.exists(device_file):
            continue

        with open(device_file, 'r', encoding='utf-8') as f:
            devdata = json.load(f)

        branches = devdata.get('branches', [])
        device_fixed = False

        for branch in branches:
            table_fields = branch.get('table', [])
            checked_count += 1

            if 'aspatch' in table_fields:
                continue

            # 缺失 aspatch，提示
            code = branch.get('branchCode', '')
            tag = branch.get('tag', '')
            idtag = branch.get('idtag', '')
            print(f"⚠ [{device}] 分支缺 aspatch 键: tag={tag} idtag={idtag} code={code}")

            # 自动修复：在 table 的 release 之后插入 aspatch
            if 'release' in table_fields:
                idx = table_fields.index('release')
                table_fields.insert(idx + 1, 'aspatch')
            else:
                table_fields.append('aspatch')
            branch['table'] = table_fields

            # 为每个 ROM 条目补充 aspatch 空值
            roms = branch.get('roms', {})
            for version, rom_data in roms.items():
                if 'aspatch' not in rom_data:
                    new_rom_data = {}
                    for key, value in rom_data.items():
                        new_rom_data[key] = value
                        if key == 'release':
                            new_rom_data['aspatch'] = ""
                    if 'aspatch' not in new_rom_data:
                        new_rom_data['aspatch'] = ""
                    roms[version] = new_rom_data

            device_fixed = True
            fixed_count += 1
            print(f"  → 已自动修复: 补充 aspatch 键到 table 和 ROM 条目")

        if device_fixed:
            with open(device_file, 'w', encoding='utf-8') as f:
                json.dump(devdata, f, ensure_ascii=False, indent='\t')
            print(f"  [{device}] 已保存修复")

    print("-" * 80)
    print(f"检查分支: {checked_count}")
    print(f"修复分支: {fixed_count}")


if __name__ == "__main__":
    args = sys.argv[1:]
    only = [a for a in args if not a.startswith('--')]
    check_aspatch_key(only_devices=only or None)
    sync_aspatch_from_db(only_devices=only or None)
    