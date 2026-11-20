import OScommon
from datetime import datetime
import subprocess
import sys
from sys import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# 只在真实终端里清屏：输出被重定向到日志时 clear 会把 ANSI 转义序列写进文件
if sys.stdout.isatty():
	subprocess.run(["cls"] if platform == "win32" else ["clear"])

increment = ["1", "100", "200"]
one_devices = ['warm']
base_url = "https://update.intl.miui.com/updates/miota-fullrom.php?d="
MAX_WORKERS = 16

# devices = list(dict.fromkeys(OScommon.unreleased + OScommon.currentStable))
devices = list(dict.fromkeys(OScommon.currentStable + OScommon.unreleased))

_print_lock = threading.Lock()


def log(msg):
	"""线程安全打印：避免多线程输出交错/撕裂。"""
	with _print_lock:
		print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg, flush=True)


def build_tasks():
	"""展开原嵌套循环，生成与串行版本完全一致的请求任务列表。"""
	tasks = []
	for device in devices:
		devdata = OScommon.localData(device)
		device = devdata['device']
		code = devdata['code']
		andvs = devdata['android']
		oss = devdata['supports']
		for branch in OScommon.branches:
			devcode = device + branch['code']
			for os in oss:
				for andv in andvs:
					# 线刷包探测：每个 (branch, os, android, carrier) 一次
					for carrier in branch['carrier']:
						if device in one_devices:
							url = base_url + devcode + "&b=F&r=&n=" + carrier
						else:
							url = base_url + devcode + "&b=F&r=" + branch['region'] + "&n=" + carrier
						tasks.append(('fb', url))
					# OTA 版本探测：每个 (branch, os, android, increment) 一次
					for i in increment:
						if code == "":
							break
						version = os + "." + i + ".0." + OScommon.android(andv) + code + branch['tag']
						if version in devdata:
							continue
						if device in one_devices:
							enc = OScommon.miui_encrypt(
								OScommon.OTAFormer(device, devcode, '', 'F', branch['zone'], andv, version))
						else:
							enc = OScommon.miui_encrypt(
								OScommon.OTAFormer(device, devcode, branch['region'], 'F', branch['zone'], andv, version))
						tasks.append(('ota', enc, device, devcode, version))
	return tasks


def run_task(task, session):
	kind = task[0]
	if kind == 'fb':
		url = task[1]
		log("fastboot " + url)
		OScommon.getFastboot(url, session=session)
	else:
		_, enc, device, devcode, version = task
		log("检测 " + device + " " + devcode + " " + version)
		OScommon.getFromApi(enc, session=session)


def main():
	tasks = build_tasks()
	total = len(tasks)
	log(f"共 {total} 个任务，{MAX_WORKERS} 线程并发，共享 Session 复用连接")
	session = OScommon.get_shared_session()

	done = 0
	with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
		futures = [executor.submit(run_task, t, session) for t in tasks]
		try:
			for f in as_completed(futures):
				done += 1
				try:
					f.result()
				except Exception as e:
					log(f"任务异常: {e}")
				if done % 50 == 0 or done == total:
					log(f"进度 {done}/{total}")
		except KeyboardInterrupt:
			log("收到中断，取消未开始的任务...")
			for f in futures:
				f.cancel()
			raise


if __name__ == '__main__':
	main()
