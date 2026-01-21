# 🧪 测试文档

## 测试文件

项目包含两个测试文件：

1. **test_llm_simple.py** - 简化功能测试（推荐）
2. **test_llm_client.py** - 完整单元测试（包含 mock）

## 快速运行测试

### 方式 1: 简化测试（推荐）

```bash
python3 test_llm_simple.py
```

这会测试：
- ✅ 模拟模式
- ✅ 不同 LLM 提供商
- ✅ 系统提示词
- ✅ 错误处理和自动降级
- ✅ 单例模式
- ✅ API 格式验证
- ✅ 当前环境测试

### 方式 2: 完整单元测试

```bash
python3 test_llm_client.py
```

包含更详细的单元测试（使用 mock）。

### 方式 3: 使用 unittest

```bash
python3 -m unittest test_llm_client.py -v
```

## 测试覆盖

### ✅ 已测试的功能

#### 1. 模拟模式
- 测试无需 API Key 的模拟生成
- 验证不同类型的响应（大纲、角色、分镜、镜头）

#### 2. HTTP 请求
- Anthropic API 格式
- OpenAI API 格式（兼容格式）
- 阿里云通义千问 API 格式

#### 3. 错误处理
- API 失败时自动降级到模拟模式
- 网络错误处理
- 无效配置处理

#### 4. 配置管理
- 多提供商配置切换
- URL、Key、Model 配置验证
- 环境变量读取

#### 5. 其他功能
- 单例模式
- 系统提示词支持
- 并发安全

## 测试结果示例

```
============================================================
🧪 LLM 客户端功能测试
============================================================

测试 1: 模拟模式
✓ 生成大纲成功
✓ 生成角色成功
✅ 测试 1 通过

测试 2: 不同提供商配置
✓ ANTHROPIC 提供商测试成功
✓ OPENAI 提供商测试成功
✓ DASHSCOPE 提供商测试成功
✅ 测试 2 通过

测试 3: 系统提示词
✓ 带系统提示词生成成功
✅ 测试 3 通过

测试 4: 错误处理和降级
✗ LLM 调用失败: ... (预期的错误)
✓ 错误降级机制正常
✅ 测试 4 通过

测试 5: 单例模式
✓ 单例模式正常
✅ 测试 5 通过

测试 6: API 请求格式验证
✓ 配置格式正确
✅ 测试 6 通过

测试 7: 当前环境实际测试
✓ 生成成功
✅ 测试 7 通过

============================================================
📊 测试总结
============================================================
总测试数: 7
✅ 通过: 7
❌ 失败: 0

🎉 所有测试通过！
```

## 如何添加新测试

### 添加功能测试

在 `test_llm_simple.py` 中添加新的测试函数：

```python
def test_your_feature():
    """测试你的功能"""
    print("=" * 60)
    print("测试 X: 你的功能")
    print("=" * 60)

    # 设置环境
    os.environ['USE_MOCK_MODE'] = 'true'

    # 导入和测试
    from llm_client import LLMClient
    client = LLMClient()

    # 执行测试
    result = client.your_method()

    # 断言
    assert result is not None, "结果不能为空"

    print("✅ 测试 X 通过\n")
```

然后在 `run_all_tests()` 中添加：

```python
tests = [
    # ... 现有测试
    ("你的功能", test_your_feature),
]
```

### 添加单元测试

在 `test_llm_client.py` 的 `TestLLMClient` 类中添加：

```python
def test_your_feature(self):
    """测试你的功能"""
    # 测试代码
    pass
```

## 测试最佳实践

### 1. 使用模拟模式

测试时始终使用模拟模式，避免调用真实 API：

```python
os.environ['USE_MOCK_MODE'] = 'true'
```

### 2. 测试错误情况

确保测试各种错误情况：

```python
def test_error_case():
    # 设置会触发错误的配置
    os.environ['OPENAI_BASE_URL'] = 'https://invalid-url.com'

    # 测试是否正确处理错误
    client = LLMClient()
    response = client.generate("test")

    # 应该降级到模拟模式
    assert len(response) > 0
```

### 3. 清理环境

每个测试后重新加载模块：

```python
import importlib
import config
importlib.reload(config)
```

### 4. 验证关键属性

确保验证响应的关键属性：

```python
assert len(response) > 0, "响应不能为空"
assert "关键字" in response, "应包含关键字"
```

## 持续集成（CI）

### GitHub Actions 配置示例

创建 `.github/workflows/test.yml`：

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run tests
      run: |
        python3 test_llm_simple.py
```

## 测试真实 API

如果你想测试真实的 API 调用：

### 1. 配置真实 API Key

```bash
# 创建 .env 文件
echo "USE_MOCK_MODE=false" > .env
echo "LLM_PROVIDER=openai" >> .env
echo "OPENAI_API_KEY=your-real-key" >> .env
```

### 2. 运行单个测试

```python
# test_real_api.py
from llm_client import get_llm_client

client = get_llm_client()
response = client.generate("你好，请介绍一下自己")

print("响应:", response)
```

### 3. 注意事项

- ⚠️ 真实 API 会产生费用
- ⚠️ 需要网络连接
- ⚠️ 响应时间较慢
- ⚠️ 不适合自动化 CI/CD

## 调试测试

### 详细日志

设置日志级别：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 打印请求详情

在 `llm_client.py` 中临时添加：

```python
print(f"Request URL: {url}")
print(f"Request Headers: {headers}")
print(f"Request Data: {data}")
```

### 使用 pdb 调试

```python
import pdb; pdb.set_trace()
```

## 常见问题

### Q: 测试失败：ImportError

**A:** 安装依赖：
```bash
pip install -r requirements.txt
```

### Q: 测试超时

**A:** 增加超时时间或使用模拟模式

### Q: mock 测试失败

**A:** 确保使用正确的 mock 路径：
```python
with patch('llm_client.requests.post', ...):
    # 测试代码
```

## 性能测试

### 测试响应时间

```python
import time

start = time.time()
response = client.generate("test")
end = time.time()

print(f"响应时间: {end - start:.2f} 秒")
assert (end - start) < 5, "响应时间应小于5秒"
```

### 并发测试

```python
import concurrent.futures

def test_concurrent():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(client.generate, "test") for _ in range(10)]
        results = [f.result() for f in futures]

    assert len(results) == 10
    assert all(len(r) > 0 for r in results)
```

## 覆盖率报告

安装 coverage：

```bash
pip install coverage
```

运行带覆盖率的测试：

```bash
coverage run -m pytest test_llm_client.py
coverage report
coverage html  # 生成 HTML 报告
```

---

**保持测试更新！** 每次添加新功能时都要添加对应的测试。🧪✨
