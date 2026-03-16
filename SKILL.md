# browser-form-filler

瀏覽器表單自動填寫技能

## 功能

- 自動分析網頁表單結構
- 解析表單欄位（input, select, textarea）
- 自動填寫並提交表單
- 支援 GET/POST 方法

## 安裝依賴

```bash
pip3 install requests beautifulsoup4
```

## 使用方式

```bash
# 分析表單結構
python3 fill_form.py https://example.com/form

# 填寫並提交表單
python3 fill_form.py https://example.com/form name=John email=john@example.com
```

## 範例

```bash
# 分析表單
python3 fill_form.py https://httpbin.org/forms/post

# 填寫表單
python3 fill_form.py https://httpbin.org/post custname=Tony custemail=tony@test.com
```

## 輸出說明

- **表單結構**：action URL、method
- **輸入欄位**：name、type、placeholder
- **下拉選單**：name、options
- **提交結果**：狀態碼、回應長度

---

*版本：1.0 | 建立日期：2026-03-16*
