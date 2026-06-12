#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
遍历 OScommon.order 中的设备，使用 db_job 精确查询本地数据库
检查每个 ROM 文件（recovery/fastboot）是否存在于数据库中，如果不存在则写入 NewROMs.txt
"""

import os
import json
import sys

# 添加脚本目录到路径
sys.path.append('/Users/hegeken/Desktop/Codes/HyperOS.fans/public/data/scripts')

# 导入 OScommon 模块
from OScommon import order, db_job, writeData

# 数据目录
DATA_DIR = '/Users/hegeken/Desktop/Codes/HyperOS.fans/public/data/devices'

# 输出文件 - 使用绝对路径确保写入到项目根目录
OUTPUT_FILE = '/Users/hegeken/Desktop/Codes/HyperOS.fans/public/data/scripts/NewROMs.txt'

def rom_exists_in_db(filename, rom_type):
    """在数据库中精确查询指定文件名的 ROM 是否存在"""
    if not filename:
        return False
    
    # 根据 ROM 类型选择对应的数据库字段
    if rom_type == 'recovery':
        field = 'recovery'
    elif rom_type == 'fastboot':
        if "telecom" in filename:
            field = 'ctelecom'
        elif "mobile" in filename:
            field = 'cmobile'
        elif "unicom" in filename:
            field = 'cunicom'
        else:
            field = 'fastboot'
    else:
        field = 'checkpoint'
    
    # 使用精确匹配查询数据库
    sql = f"SELECT * FROM roms WHERE {field} = '{filename}'"
    results = db_job(sql)
    
    if results and len(results) > 0:
        count = results[0][0]
        return count > 0
    
    return False

def main():
    missing_roms = []
    
    print(f"开始遍历 {len(order)} 个设备...")
    
    for codename in order:
        device_file = os.path.join(DATA_DIR, f"{codename}.json")
        
        if not os.path.exists(device_file):
            print(f"跳过不存在的设备文件: {codename}")
            continue
        
        print(f"\n处理设备: {codename}")
        
        try:
            with open(device_file, 'r', encoding='utf-8') as f:
                device_data = json.load(f)
            
            branches = device_data.get('branches', [])
            
            for branch in branches:
                branch_code = branch.get('branchCode', '')
                roms = branch.get('roms', {})
                
                for version, rom_info in roms.items():
                    recovery = rom_info.get('recovery', '').strip()
                    fastboot = rom_info.get('fastboot', '').strip()
                    
                    # 精确查询 recovery 文件是否存在于数据库
                    if recovery:
                        exists = rom_exists_in_db(recovery, 'recovery')
                        
                        if not exists:
                            print(f"  数据库中不存在: {recovery}")
                            writeData(recovery)
                    
                    # 精确查询 fastboot 文件是否存在于数据库
                    if fastboot:
                        exists = rom_exists_in_db(fastboot, 'fastboot')
                        
                        if not exists:
                            print(f"  数据库中不存在: {fastboot}")
                            writeData(fastboot)
        
        except Exception as e:
            print(f"处理设备 {codename} 时出错: {e}")
    
    print(f"\n完成！共发现 {len(missing_roms)} 个数据库中不存在的 ROM 文件")
    print(f"结果已保存到: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()