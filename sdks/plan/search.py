import requests
import json

def main(arg1: str) -> dict:
    """
    使用 SearchAPI.io 的 Google Scholar API 搜索学术文献，
    自动获取所有分页结果并合并返回。
    
    Args:
        arg1: 搜索关键词或查询字符串
        
    Returns:
        包含所有分页搜索结果的字典
    """
    try:
        # SearchAPI.io Google Scholar 搜索的API端点
        url = "https://www.searchapi.io/api/v1/search"
        
        # 存储所有页的结果
        all_results = []
        pagesize = 20
        current_page = 1
        has_next = True
        first_page_data = None  # 存储第一页的完整数据
        
        # 循环获取所有页面的结果
        while has_next:
            # 使用 start 参数控制分页
            start = (current_page - 1) * pagesize
            
            # 设置请求参数
            params = {
                "engine": "google_scholar",  # 使用Google Scholar搜索引擎
                "q": arg1,                   # 搜索关键词
                "api_key": "x8qK16ZFZoopaFwwSoLg7k7Q",  # API密钥
                "num": pagesize                    # 每页结果数量
            }
            
            # 只有非第一页才添加 start 参数
            if start > 0:
                params["start"] = start
            
            print(f"正在获取第 {current_page} 页结果... (start={start})")
            
            # 发送GET请求
            response = requests.get(url, params=params)
            
            # 检查请求是否成功
            if response.status_code == 200:
                # 解析JSON响应
                data = json.loads(response.text)
                
                # 保存第一页的完整数据
                if current_page == 1:
                    first_page_data = data
                
                # 提取搜索结果
                if "organic_results" in data:
                    # 将当前页的结果添加到总结果列表中
                    all_results.extend(data["organic_results"])
                    
                    # 检查是否已达到40条结果的上限
                    if len(all_results) >= 40:
                        print("已达到或超过40条结果上限，将结果截断为最多40条。")
                        all_results = all_results[:40] # 确保最多40条
                        has_next = False
                    # 否则，检查API是否还有下一页 (并且我们还没因为达到40条而停止)
                    elif ("pagination" in data and
                          "next" in data["pagination"] and
                          data["pagination"]["next"]):
                        current_page += 1
                    else:
                        # API没有下一页了，或者 pagination 结构不完整
                        print("API表示沒有更多頁面，搜索結束。")
                        has_next = False
                else:
                    # 没有搜索结果或结果格式不符合预期
                    print("当前页没有搜索结果或结果格式不符合预期。")
                    has_next = False
            else:
                # 请求失败
                print(f"API请求失败，状态码: {response.status_code}")
                return {
                    "result": f"错误：API请求失败，状态码: {response.status_code}，响应: {response.text}"
                }
        
        # 确保有第一页数据
        if not first_page_data:
            return {
                "result": "错误：未能获取第一页数据。"
            }
            
        # 构建最终返回结果，保持与原API一致的结构
        # 但替换 organic_results 为合并后的所有结果
        result = first_page_data.copy()
        result["organic_results"] = all_results
        result["search_information"]["total_results_all_pages"] = len(all_results)
        result["search_information"]["pages_retrieved"] = current_page
        
        # 根据要求移除 related_searches 和 pagination 字段
        if "related_searches" in result:
            del result["related_searches"]
        if "pagination" in result:
            del result["pagination"]
        
        # 返回合并后的结果, 包装在 { "result": ... } 结构中
        return {"result": result}
            
    except requests.exceptions.RequestException as e:
        return {
            "result": f"错误：请求异常 - {str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            "result": f"错误：JSON解析失败 - {str(e)}"
        }
    except Exception as e:
        return {
            "result": f"错误：意外异常 - {str(e)}"
        }


# 如果需要在本地测试
if __name__ == "__main__":
    import time
    
    # 测试用例 - 使用示例关键词
    test_query = "fatigue threshold"
    
    # 获取所有页结果
    start_time = time.time()
    results = main(test_query)
    end_time = time.time()
    
    # 打印结果统计
    if isinstance(results, dict) and "organic_results" in results:
        organic_results = results["organic_results"]
        print(f"共获取 {len(organic_results)} 条记录")
        print(f"总耗时: {end_time - start_time:.2f} 秒")
        
        # 打印前3条结果的标题(如果有)
        for i, result in enumerate(organic_results[:3], 1):
            if "title" in result:
                print(f"{i}. {result['title']}")
    else:
        print(f"搜索失败: {results}")