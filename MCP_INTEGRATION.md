# MCP 接入说明（MCP_INTEGRATION）

本文档说明「麦麦省钱助手」实际使用的麦当劳 MCP Server、调用的 Tool、完整调用流程与业务价值。

## 1. 使用的 MCP Server

- **名称**：麦当劳中国 MCP Server（`mcd-mcp`）
- **接入地址**：`https://mcp.mcd.cn`
- **传输协议**：Streamable HTTP
- **鉴权方式**：请求头携带 `Authorization: Bearer <MCP_TOKEN>`
- **官方说明**：https://github.com/M-China/mcd-mcp-server

配置示例（脱敏，仅使用环境变量占位符，见 `mcp-config.example.json`）：

```json
{
  "mcpServers": {
    "mcd-mcp": {
      "type": "streamablehttp",
      "url": "https://mcp.mcd.cn",
      "headers": {
        "Authorization": "Bearer ${MCD_MCP_TOKEN}"
      }
    }
  }
}
```

## 2. 实际调用的 Tool 及用途

| Tool | 用途 | 在本项目中的角色 |
|------|------|------------------|
| `query-my-coupons` | 查询账户下所有优惠券 | 摸底：用户手里有哪些券可用 |
| `available-coupons` | 查询可领取的麦麦省券列表 | 挖掘：还有哪些券可以领 |
| `auto-bind-coupons` | 一键领取全部可领优惠券 | 执行：把能领的券先领到手 |
| `query-store-coupons` | 查询指定门店可用优惠券 | 到店：门店专属券 |
| `query-meals` | 查询当前可售卖的餐品菜单 | 选品：拿菜单和分类 |
| `query-meal-detail` | 查询餐品详情与套餐组成 | 选品：看套餐可替换项 |
| `calculate-price` | 计算商品金额、优惠金额、配送费、应付总价 | 核心：算最省方案 |
| `list-nutrition-foods` | 查询餐品营养成分 | 扩展：热量约束下的省钱推荐 |
| `query-nearby-stores` | 查询附近可用门店 | 定位：确定点餐门店 |
| `query-my-account` | 查询积分账户信息 | 扩展：结合积分兑换 |

## 3. 核心调用流程

用户发起"省钱点麦当劳"请求后，Skill 按以下顺序调用 MCP 工具：

```
用户：我只有 30 块，想吃顿麦当劳
        │
        ▼
① query-nearby-stores   ──► 找到附近门店
        │
        ▼
② query-my-coupons      ──► 我有哪些券
   available-coupons    ──► 还能领哪些券
   （必要时 auto-bind-coupons 一键领券）
        │
        ▼
③ query-meals           ──► 拿当前可售菜单
        │
        ▼
④ calculate-price       ──► 遍历候选套餐 × 可用券，
                             找出 "实付 ≤ 预算" 且省钱最多的组合
        │
        ▼
⑤ 输出结论 ──► "原价 ¥39.5 → 用券 ¥29.5，省了 ¥10"
              （附可复制点单清单；用户确认后才 create-order）
```

## 4. 业务价值

- **对用户**：下单前自动完成"查券 → 领券 → 比价 → 算最优组合"，把"怎么点最省钱"这件繁琐比对的事变成一句话。
- **对业务**：提升优惠券领取率与使用率，将散落在多个入口的券能力聚合为一个主动省钱的智能入口，提升用户点餐体验与黏性。
- **对开发者**：示范了 MCP 多工具编排（查询类 + 计算类 + 执行类）如何组合成一个解决真实问题的 Agentic Skill。

## 5. 注意事项

- 单个 Token 限流 600 次/分钟，请合理控制调用频率。
- 价格、券、库存以麦当劳官方实时结果为准。
- 本项目不保存任何真实 Token，配置一律使用环境变量占位符。