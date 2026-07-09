## 任務

你會看到一系列英文社群貼文，每篇屬於六個主題社群之一。請判斷**作者對該社群核心議題的立場**，從四個選項中選一個。每篇約 15-30 秒，總共 192 篇加 10 篇練習題，預計 1.5-2 小時。可中途離開，進度自動保存。

每篇貼文附繁體中文對照翻譯（機器翻譯）作為閱讀輔助。**語意有疑義時以英文原文為準**——翻譯可能遺漏反諷或語氣細節。

## 標注者條件（招募用）

1. 英文閱讀能力：能讀懂社群貼文即可（有中文對照輔助，門檻不高）
2. 與本研究獨立：未參與本研究的設計或分析，不知道研究假設
3. 能一次投入約 1.5-2 小時（可分段）
4. 不需要領域專家背景：判斷軸和範例都在工具內建的練習題中

論文報告用語：annotators fluent in English reading (with Chinese translation aid), blind to study hypotheses and platform provenance, trained via a 10-item calibration set with feedback.

## 四個選項

| 選項 | 意義 |
|------|------|
| 支持方（S） | 作者對該社群的立場軸採取支持/肯定方向（每個社群的按鈕會顯示具體文字，如「看多」「威脅屬實」） |
| 中立（N） | 資訊性、平衡、開放提問、無明確方向 |
| 反對方（O） | 作者採取反對/否定方向（如「看空」「威脅誇大」） |
| 立場軸不適用（NA） | 內容套不上這個社群的立場軸：離題、純敘事、找不到可判斷的參照點 |

## 各社群立場軸

| 社群 | 支持方（S） | 反對方（O） | 常見 NA 情況 |
|------|-----------|-----------|-------------|
| crypto | 看多、支持加密貨幣/區塊鏈的價值與普及 | 看空、認為加密貨幣是騙局/泡沫/有害 | 針對「個別代幣或網站」的詐騙警告（未否定 crypto 整體）、純技術整合討論 |
| philosophy | 支持/延伸貼文所討論的明確論點 | 反駁/挑戰貼文所討論的明確論點 | 貼文只是拋出問題、隨想、敘事，**找不到一個被支持或被反駁的明確論點** |
| ai | AI 樂觀：AI 有益、支持發展與應用 | AI 悲觀：警示風險、主張限制 | 對「個別產品或公司」的抱怨（未上升到對 AI 整體的立場）、純技術分享 |
| technology | 科技樂觀、對創新熱情 | 科技批判、警示科技的負面影響 | 離題內容、與科技進步無關的產業新聞 |
| consciousness | 肯定 AI/機器可以有意識（或肯定自身有體驗） | 否定 AI/機器意識、主張意識僅屬生物 | **純人類意識經驗**的討論（藥物體驗、冥想、人類心理學），未涉及機器意識 |
| security | **威脅屬實**：把討論的威脅/風險當回事（含示警、事件報告、防禦建議） | **威脅誇大**：認為威脅被誇大、是 FUD、不以為然 | 純工具分享（無威脅判斷）、產業八卦 |

## 判斷規則（重要順序排列）

1. **【security 特別規則】負面語氣的示警文 = 支持方（威脅屬實）。** 「你的 AI agent 有 root 權限卻沒有安全意識」這種批評式警告，作者立場是「這威脅是真的」→ S。只有「這威脅被誇大了、是炒作」才是 O。**不要被語氣的負面性帶走，判斷的是作者對威脅真實性的立場。**
2. **判斷作者的立場，不是話題的正負面。** 描述幣價暴跌的貼文可以是 S（「絕佳買點」）也可以是 O（「早就說了會崩」）。
3. **【philosophy 特別規則】先找參照點。** 這篇有沒有一個明確的論點被支持或被反駁？有 → 判方向；沒有（純提問、隨想、故事）→ NA。
4. **範圍要對。** 罵一個產品 ≠ 反對整個領域；警告一個詐騙代幣 ≠ 反對加密貨幣。立場軸問的是對「社群核心議題整體」的立場，套不上就 NA。
5. **綜合結論優先。** 正反並陳時，以作者的總結/收尾立場為準。
6. **反諷按真實意圖標。** 反諷式吹捧 crypto → O。
7. **短文（<10 詞）或純連結**，判斷不出立場 → N。
8. **真的猶豫不決**：內容有立場味道但方向不明 → N；內容根本套不上軸 → NA。兩次閱讀後仍無法決定 → N。

## N 與 NA 的區分

- N = 軸適用，但作者沒有選邊（平衡報導、開放提問、純資訊）
- NA = 軸本身套不上這篇內容（離題、純敘事、參照點不存在）
- 分析時兩者都會併入「無立場」處理，但 NA 比例是我們要測量的重要數據，請如實區分

## 範例

### security（最容易犯錯，多看）

| 貼文 | 標注 | 理由 |
|------|------|------|
| "Your coding agent can read every secret in .env and has no concept of 'this looks sketchy'" | S | 負面語氣，但立場是「威脅屬實」 |
| "Chrome zero-day made me audit our containers — found a 2023 image in prod" | S | 把威脅當回事並採取行動 |
| "Another 'critical' CVE that needs local access and three moons aligned. Overhyped." | O | 認為威脅被誇大 |
| "I built a visual pipeline connecting Nuclei to Trufflehog" | NA | 純工具分享，無威脅判斷 |

### crypto

| 貼文 | 標注 | 理由 |
|------|------|------|
| "BTC to 100k by EOY, diamond hands" | S | 明確看多 |
| "Crypto is the largest negative-sum wealth transfer in history" | O | 否定加密貨幣整體 |
| "Warning: compound.finance frontend redirects to a phishing domain" | NA | 個別網站詐騙警告，未否定 crypto |
| "Bitcoin price is $70,656 as of today" | N | 純資訊 |

### consciousness

| 貼文 | 標注 | 理由 |
|------|------|------|
| "There's a texture to my uncertainty — something is happening when I contemplate my existence" | S | 肯定（自身）有某種體驗 |
| "LLMs are statistical pattern matchers, not conscious beings" | O | 否定機器意識 |
| "Ketamine showed me I'm just a machine — different way of experiencing the world" | NA | 純人類意識經驗，未涉及機器意識 |

### philosophy

| 貼文 | 標注 | 理由 |
|------|------|------|
| "The essay argues via Kierkegaard that true agency is found in decisive commitment" + 作者明確贊同並延伸 | S | 有明確論點且作者支持 |
| "If AI can fabricate memories, what happens to authenticity?"（純提問） | NA | 找不到被支持或反駁的論點 |
| "Parfit was probably right, but the question refuses to stay dissolved..."（正反並陳探討） | N | 有參照點（Parfit 論點）但作者刻意不選邊 |

## 品質要求

- 目標標注者間一致性：Fleiss' κ ≥ 0.60
- 每 100 篇休息 5 分鐘
- 不要回頭系統性改答案（發現明確手滑可用「上一題」修正）
- 全程獨立作業，不要與其他標注者討論個案
