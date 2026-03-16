#!/usr/bin/env python3
"""
Browser Form Filler Skill for OpenClaw
自動填寫網頁表單（API 模式）
"""

import sys
import json
import subprocess

def install_dependencies():
    """安裝必要的依賴"""
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "-q"])

def fill_form(url, fields):
    """填寫表單（透過分析表單結構）"""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        # 取得表單頁面
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到表單
        form = soup.find('form')
        if not form:
            return "❌ 找不到表單"
        
        # 取得表單資訊
        form_info = {
            "action": form.get('action', ''),
            "method": form.get('method', 'get').upper(),
            "inputs": [],
            "selects": [],
            "textareas": []
        }
        
        # 解析 input
        for inp in form.find_all('input'):
            form_info["inputs"].append({
                "name": inp.get('name', ''),
                "type": inp.get('type', 'text'),
                "placeholder": inp.get('placeholder', '')
            })
        
        # 解析 select
        for sel in form.find_all('select'):
            options = [opt.get('value', '') for opt in sel.find_all('option')]
            form_info["selects"].append({
                "name": sel.get('name', ''),
                "options": options
            })
        
        # 解析 textarea
        for ta in form.find_all('textarea'):
            form_info["textareas"].append({
                "name": ta.get('name', ''),
                "placeholder": ta.get('placeholder', '')
            })
        
        # 嘗試填寫並提交（如果提供了欄位）
        if fields:
            data = {}
            for f in fields:
                if '=' in f:
                    key, value = f.split('=', 1)
                    data[key] = value
            
            if data:
                # 取得完整 URL
                action = form_info["action"]
                if not action.startswith('http'):
                    from urllib.parse import urljoin
                    action = urljoin(url, action)
                
                # 提交表單
                if form_info["method"] == "POST":
                    result = requests.post(action, data=data, timeout=10)
                else:
                    result = requests.get(action, params=data, timeout=10)
                
                return f"""✅ 表單提交成功！

**提交網址**: {action}
**方法**: {form_info["method"]}
**狀態碼**: {result.status_code}
**回應長度**: {len(result.text)} 字元
"""
        
        # 輸出表單結構
        result = f"""📋 **表單結構分析**

**Action**: {form_info['action']}
**Method**: {form_info['method']}

**輸入欄位**:
"""
        for inp in form_info["inputs"]:
            result += f"- `{inp['name']}` ({inp['type']})"
            if inp['placeholder']:
                result += f" - 範例: {inp['placeholder']}"
            result += "\n"
        
        if form_info["selects"]:
            result += "\n**下拉選單**:\n"
            for sel in form_info["selects"]:
                result += f"- `{sel['name']}`: {', '.join(sel['options'][:5])}"
                if len(sel['options']) > 5:
                    result += f" ... 共 {len(sel['options'])} 個選項"
                result += "\n"
        
        if form_info["textareas"]:
            result += "\n**文字區域**:\n"
            for ta in form_info["textareas"]:
                result += f"- `{ta['name']}`\n"
        
        if not fields:
            result += "\n💡 **使用方式**:\n"
            result += f"```\nfill_form {url} field1=value1 field2=value2\n```"
        
        return result
        
    except ImportError:
        install_dependencies()
        return fill_form(url, fields)
    except Exception as e:
        return f"❌ 錯誤: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("使用方法: fill_form <URL> [欄位1=值1] [欄位2=值2]")
        print("例如: fill_form https://example.com name=John email=john@example.com")
        sys.exit(1)
    
    url = sys.argv[1]
    fields = sys.argv[2:] if len(sys.argv) > 2 else []
    
    result = fill_form(url, fields)
    print(result)

if __name__ == "__main__":
    main()
