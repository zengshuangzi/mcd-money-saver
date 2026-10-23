#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麦麦省钱助手 - 核心省钱推荐算法（演示版）

本脚本演示「麦麦省钱助手」的核心省钱逻辑：
在给定预算约束下，从候选餐品/套餐中，结合可用优惠券，
找出"省钱比例最高"的组合。

说明：
- 这是算法演示与单元测试性质的源代码，不直接调用 MCP（调用见 SKILL.md）。
- 真实场景中，candidates 和 coupons 的数据来自麦当劳 MCP 的
  query-meals / query-meal-detail / query-my-coupons 等工具返回结果。

运行：
    python money_saver.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Coupon:
    """优惠券"""
    name: str
    # 满减券
    threshold: float = 0.0        # 满 X 元可用
    discount: float = 0.0         # 减 Y 元
    # 折扣券（二选一）
    rate: Optional[float] = None  # 如 0.8 表示打 8 折
    max_cut: float = float("inf")  # 折扣券封顶减免


@dataclass
class Meal:
    """候选餐品/套餐"""
    name: str
    price: float
    calories: float = 0.0


@dataclass
class Plan:
    """推荐方案"""
    meals: List[Meal] = field(default_factory=list)
    coupon: Optional[Coupon] = None
    original_price: float = 0.0
    final_price: float = 0.0
    saved: float = 0.0

    @property
    def calories(self) -> float:
        return sum(m.calories for m in self.meals)


def apply_coupon(total: float, coupon: Coupon) -> float:
    """计算使用某张券后的实付金额"""
    if total < coupon.threshold:
        return total  # 不满足门槛，券不可用
    if coupon.rate is not None:
        cut = total * (1 - coupon.rate)
        cut = min(cut, coupon.max_cut)
        return round(total - cut, 2)
    return round(total - coupon.discount, 2)


def best_plan(
    meals: List[Meal],
    coupons: List[Coupon],
    budget: float = float("inf"),
    max_calories: float = float("inf"),
) -> Optional[Plan]:
    """在预算与热量约束下，找出省钱比例最高的点单方案（单次最多选一样主食）。"""
    best: Optional[Plan] = None
    best_ratio = -1.0

    for meal in meals:
        if meal.calories > max_calories:
            continue
        original = meal.price

        # 无券
        if original <= budget:
            p = Plan(meals=[meal], original_price=original,
                     final_price=original, saved=0.0)
            if p.saved / max(original, 0.01) > best_ratio or best is None:
                best, best_ratio = p, p.saved / max(original, 0.01)

        # 逐张券尝试
        for c in coupons:
            final = apply_coupon(original, c)
            if final >= original:  # 券未生效
                continue
            if final > budget:
                continue
            saved = round(original - final, 2)
            ratio = saved / max(original, 0.01)
            if ratio > best_ratio:
                best_ratio = ratio
                best = Plan(meals=[meal], coupon=c,
                            original_price=original,
                            final_price=final, saved=saved)
    return best


def demo():
    meals = [
        Meal("麦辣鸡腿堡套餐", 35.0, 720),
        Meal("双层吉士堡套餐", 32.0, 620),
        Meal("板烧鸡腿堡套餐", 34.0, 650),
        Meal("麦香鱼套餐", 30.0, 540),
        Meal("6块麦乐鸡", 18.0, 380),
    ]
    coupons = [
        Coupon(name="满30减5", threshold=30, discount=5),
        Coupon(name="满25减3", threshold=25, discount=3),
        Coupon(name="8折券(封顶10元)", threshold=20, rate=0.8, max_cut=10),
    ]

    print("=" * 50)
    print("麦麦省钱助手 · 算法演示")
    print("=" * 50)

    # 场景1：预算30
    p = best_plan(meals, coupons, budget=30)
    print(f"\n[场景1] 预算 ¥30：")
    if p:
        print(f"  推荐 {p.meals[0].name} | 原价 ¥{p.original_price} "
              f"→ 用券「{p.coupon.name if p.coupon else '无'}」后 ¥{p.final_price}，省 ¥{p.saved}")
    else:
        print("  无满足条件的方案")

    # 场景2：热量500以内
    p = best_plan(meals, coupons, max_calories=500)
    print(f"\n[场景2] 热量 ≤ 500 大卡：")
    if p:
        print(f"  推荐 {p.meals[0].name}（{p.meals[0].calories}大卡）| "
              f"原价 ¥{p.original_price} → ¥{p.final_price}，省 ¥{p.saved}")
    else:
        print("  无满足条件的方案")

    # 场景3：不限预算，找省钱比例最高
    p = best_plan(meals, coupons)
    print(f"\n[场景3] 不限预算，省钱比例最高：")
    if p:
        print(f"  推荐 {p.meals[0].name} | 原价 ¥{p.original_price} "
              f"→ ¥{p.final_price}，省 ¥{p.saved}")

    print("\n注：真实数据来自麦当劳 MCP 工具，本脚本仅演示算法逻辑。")


if __name__ == "__main__":
    demo()