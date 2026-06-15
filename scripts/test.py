import OScommon
import json

def fill_security_patches():
  """
  遍历数据库 roms 表中 recovery 不为 NULL 的记录，
  通过 CDN 下载链接获取安全补丁级别，并写入 aspatch 字段（date 类型）。
  """
  import time

  # 1. 获取所有需要处理的记录
  sql = "SELECT id, device, code, version, recovery FROM roms WHERE recovery IS NOT NULL AND recovery != '' AND aspatch IS NULL ORDER BY id DESC"
  rows = OScommon.db_job(sql)
  if not rows:
    print("没有需要处理的记录")
    return

  total = len(rows)
  success = 0
  failed = 0

  print(f"共找到 {total} 条记录需要处理")

  for idx, row in enumerate(rows, 1):
    rom_id, device, code, version, recovery = row
    url = OScommon.form_url(recovery, version)

    # 终端超链接格式 (OSC 8): ESC ] 8 ; ; URI BEL text ESC ] 8 ; ; BEL
    link_text = f"\x1b]8;;{url}\x07{version}\x1b]8;;\x07"
    print(f"\r[{idx}/{total}] ID={rom_id} {device} {link_text} ...  ", end="", flush=True)

    try:
      asp = OScommon.get_security_patch_from_ota_url(url, 'recovery', timeout=30)
      if asp:
        # asp 格式为 "2026-03-01"，可直接写入 datetime 类型字段
        OScommon.db_job(f"UPDATE roms SET aspatch = '{asp}' WHERE id = {rom_id}")
        print(f"\r[{idx}/{total}] ✓ {device} {version} → {asp}  ", end="", flush=True)
        success += 1
      else:
        print(f"\r[{idx}/{total}] ✗ {device} {version} → 无补丁信息  ", end="", flush=True)
        failed += 1
    except Exception as e:
      print(f"\r[{idx}/{total}] ✗ {device} {version} → {e}  ", end="", flush=True)
      failed += 1

    # 每 50 条短暂休眠，避免请求过于密集
    if idx % 50 == 0:
      time.sleep(1)

  print(f"\n处理完成：成功 {success}，失败 {failed}，共 {total}")

def test_single():
  """
  测试单条记录的安全补丁获取，用于排查问题。
  """
  import traceback

  sql = "SELECT id, device, code, version, recovery FROM roms WHERE id = 52763"
  rows = OScommon.db_job(sql)
  if not rows:
    print("没有需要处理的记录")
    return

  rom_id, device, code, version, recovery = rows[0]
  url = OScommon.form_url(recovery, version)

  print(f"测试记录: ID={rom_id}, device={device}, version={version}")
  print(f"recovery: {recovery}")
  print(f"URL: {url}")
  print()

  # 一步一步调试
  print("=== 1. 获取文件大小 ===")
  file_length = OScommon.get_file_length(url, timeout=30)
  print(f"文件大小: {file_length}")
  if not file_length:
    print("✗ 获取文件大小失败")
    return

  print("\n=== 2. 直接调用 extract_ota_metadata ===")
  metadata = OScommon.extract_ota_metadata(url, 'recovery', timeout=30)
  print(f"metadata: {metadata}")
  if metadata:
    if metadata.get('post'):
      asp = metadata['post'].get('security_patch_level')
      print(f"安全补丁级别: {asp}")
    else:
      print("metadata 中无 post 字段")
  else:
    print("✗ metadata 为 None")

  print("\n=== 3. 调用 get_security_patch_from_ota_url ===")
  try:
    asp2 = OScommon.get_security_patch_from_ota_url(url, 'recovery', timeout=30)
    print(f"结果: {asp2}")
    if asp2:
      # 写入数据库验证
      OScommon.db_job(f"UPDATE roms SET aspatch = '{asp2}' WHERE id = {rom_id}")
      print(f"✓ 已写入数据库: UPDATE roms SET aspatch = '{asp2}' WHERE id = {rom_id}")
  except Exception as e:
    print(f"异常: {e}")
    traceback.print_exc()

if __name__ == "__main__":
  fill_security_patches()