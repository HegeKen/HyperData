import subprocess
import json
import config

result = None
try:
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", config.deploy_url],
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.returncode == 0 and result.stdout:
        response = json.loads(result.stdout)
        if response.get("success"):
            deploy_id = response.get("result", {}).get("id", "未知")
            print(f"✓ 部署请求成功，ID: {deploy_id}")
        else:
            errors = response.get("errors", [])
            print(f"✗ 部署请求失败: {errors}")
    else:
        print(f"✗ curl 执行失败: {result.stderr}")
except subprocess.TimeoutExpired:
    print("✗ 部署请求超时")
except json.JSONDecodeError:
    if result is not None:
        print(f"✗ 无法解析返回的 JSON: {result.stdout}")
    else:
        print("✗ 无法解析返回的 JSON")
except Exception as e:
    print(f"✗ 部署请求异常: {str(e)}")