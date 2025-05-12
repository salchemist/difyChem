import json
import re # 导入正则表达式库

def main(input_json: str) -> list:
    """
    从输入的JSON字符串中解析嵌套的JSON结构,
    并提取'google_scholar_keywords'列表。

    Args:
        input_json: 包含嵌套JSON的字符串

    Returns:
        包含google_scholar_keywords的列表,如果找不到则返回空列表。

    Raises:
        json.JSONDecodeError: 如果JSON解析失败。
        KeyError: 如果预期的键'google_scholar_keywords'不存在。
        Exception: 处理其他潜在错误。
    """
    try:
        # 检查输入是否为JSON字符串格式
        if not input_json:
            print("错误：输入的JSON字符串为空。")
            return []

        # 清理字符串：移除代码块标记 ```json ... ```
        # 使用正则表达式匹配并提取json内容
        match = re.search(r"```json\s*([\s\S]*?)\s*```", input_json)
        if not match:
            # 如果没有 ```json 标记，尝试直接解析
            cleaned_json_str = input_json
        else:
            cleaned_json_str = match.group(1).strip()

        # 解析JSON字符串
        data = json.loads(cleaned_json_str)

        # 提取 google_scholar_keywords
        keywords = data.get("google_scholar_keywords")
        if keywords is None:
            print("错误：在JSON中未找到'google_scholar_keywords'键。")
            return []

        return keywords

    except json.JSONDecodeError as e:
        print(f"错误：解析JSON时出错 - {e}")
        # 尝试打印可能出错的字符串以帮助调试
        if 'cleaned_json_str' in locals():
            print("可能出错的JSON字符串:", cleaned_json_str)
        elif 'input_json' in locals():
            print("原始input_json字符串:", input_json)
        raise
    except KeyError as e:
        print(f"错误: 缺少预期的键 - {e}")
        raise
    except Exception as e:
        print(f"发生意外错误: {e}")
        raise

# --- 主程序 ---
if __name__ == "__main__":
    # 测试用例
    test_json = '''```json
{
  "google_scholar_keywords": [
    "\"fatigue threshold\" AND \"ionic gel\"",
    "\"ionic gel\" AND \"mechanical properties\" AND \"fatigue\"",
    "\"ionic gel\" AND \"deformation\" AND \"fatigue threshold\""
  ]
}```'''
    
    try:
        extracted_keywords = main(test_json)
        print("提取的Google Scholar关键词:")
        for keyword in extracted_keywords:
            print(f"- {keyword}")
    except Exception:
        print("无法完成关键词提取。")