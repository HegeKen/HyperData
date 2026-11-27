# HyperData

HyperOS.fans data / HyperOS.fans 数据仓库。

> [!IMPORTANT]
> **Migration / 迁移：** ROM 数据、兼容接口与维护脚本已整合到 [HegeKen/miroms](https://github.com/HegeKen/miroms)。
> 新使用者请查阅 [miroms 数据文档](https://github.com/HegeKen/miroms/blob/master/README.md)；现有 HyperOS.fans 页面可迁移到 V2 兼容接口，新接入推荐使用同时覆盖 MIUI 与 HyperOS 的 V3 全量接口。
>
> ROM data, compatibility endpoints and maintenance scripts are now consolidated in [HegeKen/miroms](https://github.com/HegeKen/miroms). Use V2 for HyperOS.fans compatibility, or V3 for new integrations requiring both MIUI and HyperOS data.

## Migration guide / 迁移指南

新的线上 API 根地址为 **https://api.miuier.com/api** 。旧文件路径不能原样拼接到新域名后：HyperOS.fans 对应的数据位于 `api/v2/`，机型图片则统一放在仓库根的 `images/`。

| HyperData 原路径 | miroms 新路径 |
| --- | --- |
| `devices/<codename>.json` | `api/v2/devices/<codename>.json` |
| `devices.json` | `api/v2/devices.json` |
| `index.json` | `api/v2/index.json` |
| `dev.json` | `api/v2/dev.json` |
| `dev/<week>.json` | `api/v2/dev/<week>.json` |
| `sitelog.json` | `api/v2/sitelog.json` |
| `updates.json` | `api/v2/updates.json` |
| `new-rom.json` | `api/v2/new-rom.json` |
| `assets/images/<file>` | `images/<file>` |
| `scripts/` | [`miroms/scripts/`](https://github.com/HegeKen/miroms/tree/master/scripts) |

例如，设备 `agate` 的 HyperOS 数据可读取：

```bash
# V2：保持 HyperOS.fans 现有数据结构
curl -fsSL https://api.miuier.com/api/v2/devices/agate.json

# V3：MIUI + HyperOS 全量数据，推荐新接入使用
curl -fsSL https://api.miuier.com/api/v3/devices/agate.json

# 机型图片不再从 api/v2/assets/images/ 获取
curl -fsSL -o agate.png https://api.miuier.com/images/agate.png
```

V2 是旧站兼容格式；V3 的字段结构不同，并增加了独立的多语言更新日志、设备索引、版本与发布日期索引等数据。切换前请按 [API 数据说明](https://github.com/HegeKen/miroms/blob/master/README.md#api-数据--api-data) 调整解析逻辑，不要仅替换域名。

The current API base URL is `https://api.miuier.com/api`. Add the `api/v2/` prefix when migrating existing HyperOS.fans paths, use `images/<file>` for device images, and consult the miroms documentation before upgrading to the different V3 schema.

完整的目录结构、附属接口、脚本和字段约定见 [miroms README](https://github.com/HegeKen/miroms/blob/master/README.md)。
