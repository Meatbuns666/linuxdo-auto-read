from playwright.sync_api import sync_playwright
import time

username = 'your-username'
password = 'your-password'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # 启动浏览器
    page = browser.new_page()
    
    page.goto("https://linux.do/")
    print("[+] 开始加载页面")
    
    # 登录流程
    page.click('xpath=//*[@id="ember3"]/div[2]/header/div/div/div[3]/span/span/button')
    page.fill('xpath=//*[@id="login-account-name"]', username)
    page.fill('xpath=//*[@id="login-account-password"]', password)
    page.click('xpath=//*[@id="login-button"]')
    print("[+] 登录流程执行完毕")
    
    page.wait_for_timeout(3000)

    # 检查登录状态
    cookies = page.context.cookies()
    logged_in = any(cookie['name'] == '_t' for cookie in cookies)
    
    if logged_in:
        print("[+] 恭喜！登录成功了哦>_<")
        page.goto("https://connect.linux.do/")
        
        # 获取用户欢迎信息
        text = page.text_content('xpath=/html/body/h1')
        if text:
            start = text.find('，') + 1
            end = text.find('用户')
            middle_text = text[start:end].strip() if start != -1 and end != -1 else ''
            print(f"[+] 你好啊！{middle_text}")
            page.goto("https://linux.do/")
            
            # 循环提取话题 ID
            def extract_topic_ids():
                for i in range(56, 85):  # 从 id56 到 id84
                    element_xpath = f'//*[@id="ember{i}"]'
                    try:
                        # 获取 data-topic-id 属性
                        data_topic_id = page.get_attribute(element_xpath, 'data-topic-id')
                        if data_topic_id:
                            print(f"[+] 元素 {i} 的 data-topic-id: {data_topic_id}")
                            # 打开话题页面
                            page.goto("https://linux.do/t/topic/" + data_topic_id)
                            
                            # 获取话题标题
                            topic_title_text = page.text_content('xpath=//*[@id="topic-title"]/div/h1/a[1]/span')
                            print(f"[+] 已打开话题: {topic_title_text}")

                            # 滑动60秒
                            print("[+] 开始滑动页面...")
                            for _ in range(60):
                                page.mouse.wheel(0, 100)  # 向下滚动
                                time.sleep(1)  # 每秒滚动一次

                            # 返回主页
                            page.goto("https://linux.do/")
                            print("[+] 返回主页，准备下一个话题...")
                        else:
                            print(f"[-] 元素 {i} 没有 data-topic-id 属性")
                    except Exception as e:
                        print(f"[-] 无法找到元素 {i}: {e}")

            # 开始提取话题 ID
            while True:
                extract_topic_ids()
                # 刷新当前页面，准备下一个循环
                page.reload()
                page.wait_for_load_state('networkidle')
        else:
            print("[-] 未找到用户详细信息")
    else:
        print("[-] 哦不！登录失败了@_@")

    # 关闭浏览器
    browser.close()
