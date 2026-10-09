"""S0 · Day1 练习：Python 基础（列表 / 字典 / 函数 / 类）

用法：
    uv run python examples/s0/01_basics.py

规则：
    把下面 5 个函数的 TODO 补完，让最后的断言全部通过。
    先自己想 20 分钟；实在卡住，再看文件最末尾的「提示」（别直接抄）。

目标输出：
    ✅ Day1 全部通过
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ---------- 练习 1：列表运算 ----------
def ex1_list_ops(numbers: list[int]) -> tuple[int, int, float]:
    """返回 (最大值, 总和, 平均值)。要求用内置函数，不要手写循环求和。"""
    # TODO: 用 max() / sum() / len() 实现
    return max(numbers),sum(numbers),sum(numbers)/len(numbers)
    raise NotImplementedError("请补完 ex1_list_ops")


# ---------- 练习 2：字典过滤 ----------
POSTS = [
    {"title": "朝阳区羽毛球馆评测", "tags": ["羽毛球", "球馆"]},
    {"title": "考研英语冲刺经验", "tags": ["考研", "英语"]},
    {"title": "周末约球帖", "tags": ["羽毛球", "约球"]},
]


def ex2_dict_ops(posts: list[dict], tag: str) -> list[str]:
    """过滤出 tags 里包含 tag 的帖子，返回它们的 title 列表（保持原顺序）。"""
    # TODO: 用列表推导式或 for 循环实现
    return [p["title"] for p in posts if tag in p["tags"]]
    raise NotImplementedError("请补完 ex2_dict_ops")


# ---------- 练习 3：字符串清洗 ----------
def ex3_string_clean(text: str) -> str:
    """去掉首尾空白，并把中间连续的空格压缩成一个空格。
    例："  你好   世界  " -> "你好 世界"
    """
    # TODO: 提示：str.strip() 和 str.split()
    return " ".join(text.strip().split())
    raise NotImplementedError("请补完 ex3_string_clean")


# ---------- 练习 4：类 ----------
@dataclass
class User:
    name: str
    tags: list[str] = field(default_factory=list)

    def has_tag(self, tag: str) -> bool:
        """判断用户是否带有某个标签。"""
        # TODO: 一行即可
        if tag in self.tags:
            print("xiao ling ai "+tag)
            return True
        else:return False
        raise NotImplementedError("请补完 User.has_tag")


def ex4_class() -> bool:
    """创建 User('小林', ['考研', '跑步'])，返回 has_tag('跑步') 的结果。"""
    # TODO
    user = User("小林", ["考研", "跑步"]); return user.has_tag("跑步")
    raise NotImplementedError("请补完 ex4_class")


# ---------- 练习 5：循环与条件 ----------
def ex5_fizzbuzz(n: int) -> list[str]:
    """返回 1..n 的 FizzBuzz 序列（字符串列表）：
    能被 3 整除 -> "Fizz"；能被 5 整除 -> "Buzz"；同时 -> "FizzBuzz"；否则 -> 数字字符串。
    例：n=5 -> ['1', '2', 'Fizz', '4', 'Buzz']
    """
    # TODO
    out=[]
    for i in range(1,n+1):
        if i%15==0:out.append("FizzBuzz")
        elif i%3==0:out.append("Fizz")
        elif i%5==0:out.append("Buzz")
        else:out.append(str(i))
    return out
    raise NotImplementedError("请补完 ex5_fizzbuzz")


# ================= 自测（不要修改这一段）=================
def run_tests() -> None:
    # 每题包成 lambda，这样即使抛异常（比如还没写完的 NotImplementedError）
    # 也只是"这一题没过"，不会让整个脚本崩掉。
    checks: list[tuple[str, object, object]] = [
        ("ex1 列表运算", lambda: ex1_list_ops([3, 1, 4, 1, 5]), (5, 14, 2.8)),
        ("ex2 字典过滤", lambda: ex2_dict_ops(POSTS, "羽毛球"), ["朝阳区羽毛球馆评测", "周末约球帖"]),
        ("ex3 字符串清洗", lambda: ex3_string_clean("  你好   世界  "), "你好 世界"),
        ("ex4 类", lambda: ex4_class(), True),
        ("ex5 FizzBuzz", lambda: ex5_fizzbuzz(5), ["1", "2", "Fizz", "4", "Buzz"]),
        ("ex5 FizzBuzz(15) 末位", lambda: ex5_fizzbuzz(15)[-1], "FizzBuzz"),
    ]
    failed = 0
    for name, fn, want in checks:
        try:
            got = fn()  # type: ignore[operator]
        except NotImplementedError:
            print(f"✗ {name}: 还没写（TODO 待补）")
            failed += 1
            continue
        except Exception as e:  # noqa: BLE001
            print(f"✗ {name}: 运行出错 -> {type(e).__name__}: {e}")
            failed += 1
            continue
        ok = got == want
        print(f"{'✓' if ok else '✗'} {name}: got={got!r} want={want!r}")
        if not ok:
            failed += 1
    print()
    if failed == 0:
        print("✅ Day1 全部通过")
    else:
        print(f"❌ 还有 {failed} 题没过，继续加油（别急着看提示）")


if __name__ == "__main__":
    run_tests()


# ================= 提示（先别看！）=================
# ex1: return max(numbers), sum(numbers), sum(numbers) / len(numbers)
# ex2: return [p["title"] for p in posts if tag in p["tags"]]
# ex3: return " ".join(text.strip().split())
#      （split() 不带参数时会自动按任意空白切分并干掉空串）
# ex4: user = User("小林", ["考研", "跑步"]); return user.has_tag("跑步")
# ex5:
#   out = []
#   for i in range(1, n + 1):
#       if i % 15 == 0: out.append("FizzBuzz")
#       elif i % 3 == 0: out.append("Fizz")
#       elif i % 5 == 0: out.append("Buzz")
#       else: out.append(str(i))
#   return out
