# WorkBuddy 开发对话上下文

> 本文件记录使用腾讯 WorkBuddy 开发「麦麦省钱助手」的完整过程，用于核验 WorkBuddy 专项奖励的联动活动资格。

## 开发概述

- **开发工具**：腾讯 WorkBuddy（AI 智能体）
- **项目名称**：麦麦省钱助手（McD Money Saver）
- **项目类型**：基于麦当劳 MCP 能力开发的创意 Skill
- **开发时间**：2026-10-20 ~ 2026-10-22

## 需求提出（用户）

用户提出希望参加「麦当劳程序员创意开发大赛」，询问参赛条件与操作方式。WorkBuddy 通过联网检索，梳理了大赛的参赛条件、时间节点、报名方式与奖励规则，并向用户完整说明。

## 需求对齐（用户 × WorkBuddy）

WorkBuddy 通过结构化提问，与用户对齐了三个关键决策：

1. **创意方向**：麦麦省钱助手（根据预算/优惠券自动推荐最划算的麦当劳套餐）
2. **GitHub 准备**：用户已有 GitHub 账号，可直接发布公开仓库
3. **交付范围**：全套 —— 创意 + 开发 + 参赛必需文件

## 开发过程（WorkBuddy）

### 第一步：调研麦当劳 MCP 能力

WorkBuddy 通过访问官方仓库，获取了以下关键信息：

- 麦当劳 MCP Server 接入地址：`https://mcp.mcd.cn`（Streamable HTTP）
- 完整工具清单（30 个 Tool），其中与本项目强相关的工具包括：
  - `query-my-coupons` / `available-coupons` / `auto-bind-coupons` / `query-store-coupons`（优惠券相关）
  - `query-meals` / `query-meal-detail`（菜单查询）
  - `calculate-price`（价格计算，核心）
  - `list-nutrition-foods`（营养信息）
  - `query-nearby-stores` / `query-my-account`（辅助）

### 第二步：设计省钱逻辑

WorkBuddy 将省钱流程设计为五步编排：

```
查券 → 领券 → 查菜单 → 比价(calculate-price) → 输出最优方案
```

并设计了三种典型玩法：预算内最省钱、薅羊毛模式、热量可控又省钱。

### 第三步：生成项目文件

WorkBuddy 依次生成：

1. `SKILL.md` —— Skill 定义与省钱逻辑提示词（核心）
2. `READM.md` → `README.md` —— 项目介绍、安装、示例、目标用户
3. `CONTEST_DECLARATION.md` —— 采用官方模板（不可修改）
4. `MCP_INTEGRATION.md` —— MCP 接入与工具调用说明
5. `mcp-config.example.json` —— 脱敏配置示例（环境变量占位符）
6. `workbuddy.md` —— 本文件

### 第四步：发布与报名指导

WorkBuddy 向用户提供了 GitHub 公开仓库发布、Issue 报名模板及注意事项（标题正文间不加换行、链接不用 Markdown 格式等）。

## 总结

整个项目从需求提出到文件交付，均在 WorkBuddy 的辅助下完成，完整对话过程保留于 WorkBuddy 会话记录中。本项目真实使用腾讯 WorkBuddy 智能体进行创意构思、逻辑设计与文档编写。