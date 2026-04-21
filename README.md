# 智职规划 - AI职业推荐系统

基于大语言模型(LLM)和检索增强生成(RAG)的智能职业推荐系统，结合MBTI性格分析，为应届生和职场新人提供个性化职业发展建议。

## 项目结构

```
zhituAI/
├── src/                          # 核心源代码
│   ├── app.py                    # Streamlit Web应用入口
│   ├── main.py                   # 主程序逻辑
│   ├── config.py                 # 配置文件
│   ├── core.py                   # 核心算法（MBTI分析、人岗匹配）
│   ├── llm_service.py            # 大模型服务（GLM-4调用）
│   ├── rag_service.py            # RAG检索服务
│   ├── semantic_rag.py           # 语义向量检索（BGE模型）
│   ├── rag_matcher.py            # RAG人岗匹配
│   ├── skill_matcher.py          # 技能匹配算法
│   ├── smart_matcher.py          # 智能匹配（双通道融合）
│   ├── four_dimension_matcher.py  # 四维度匹配算法
│   ├── hard_filter.py            # 硬性条件过滤（学历/经验/地点）
│   └── mbti_analyzer.py          # MBTI性格分析
├── requirements.txt              # Python依赖
├── .gitignore                    # Git忽略配置
└── README.md                     # 项目说明文档
```

## 核心模块说明

### src/app.py
Streamlit Web应用入口，负责构建5个标签页的用户界面：
- **首页** - 用户画像输入
- **岗位推荐** - 基于双通道融合的智能推荐
- **MBTI分析** - 16种性格类型与职业匹配
- **技能对比** - 用户技能与岗位要求对比
- **职业发展** - 个性化发展建议

### src/main.py
主程序逻辑，协调各个模块工作，处理用户请求流程。

### src/config.py
系统配置参数，包括：
- 大模型API配置
- RAG检索参数
- 匹配权重配置

### src/core.py
核心算法集合：
- MBTI_ANALYSIS: 16种性格类型分析
- MBTI_CAREER_MATCH: 性格-职业匹配度
- analyze_mbti_career(): MBTI职业分析

### src/llm_service.py
大模型服务模块：
- 调用智谱GLM-4 API
- Few-shot + CoT提示工程
- JSON格式输出解析

### src/semantic_rag.py
语义向量检索模块：
- BGE-small-zh-v1.5模型
- 7952条岗位数据向量
- 支持同义词语义匹配

### src/rag_matcher.py
RAG人岗匹配，实现四维度评分：
- 基础要求匹配（学历/经验/地点）
- 职业技能匹配（技能覆盖/缺口）
- 职业素养匹配（沟通/学习/抗压/创新）
- 发展潜力匹配（实习/项目/学习意愿）

### src/smart_matcher.py
双通道融合匹配：
- LLM通道（60%权重）：大模型智能分析
- RAG通道（40%权重）：向量检索匹配
- 双通道结果融合与置信度折扣

### src/mbti_analyzer.py
MBTI性格分析模块：
- 16种性格类型详细分析
- 性格特点、工作风格、团队角色
- MBTI与岗位适配度计算

### src/four_dimension_matcher.py
四维度人岗匹配算法实现，整合MBTI性格加成。

### src/hard_filter.py
硬性条件过滤器：
- 学历要求过滤
- 工作经验过滤
- 工作地点过滤

### src/skill_matcher.py
技能匹配算法，计算技能覆盖率与技能缺口。

## 技术栈

- **Web框架**: Streamlit
- **大模型**: 智谱GLM-4 (ChatGLM)
- **向量模型**: BGE-small-zh-v1.5
- **数据处理**: NumPy, Pandas, Scikit-learn
- **Python版本**: 3.8+

## 快速启动

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
python -m streamlit run src/app.py
```

访问 http://localhost:8501 即可使用。

## 系统功能

1. **智能推荐** - 基于LLM+RAG双通道融合的精准岗位推荐
2. **MBTI分析** - 16种性格类型与职业匹配分析
3. **技能对比** - 可视化技能差距分析
4. **发展建议** - 个性化职业发展路径规划

## License

MIT License
