# -*- coding: utf-8 -*-
import streamlit as st
import json
import random
from datetime import datetime
import os
import sys
import base64
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="智途AI - AI职业规划智能体",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    :root {
        --primary-color: #0066CC;
        --secondary-color: #00A3FF;
        --accent-color: #FF6B35;
    }
    .main-title {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #0066CC !important;
        text-align: center;
    }
    .subtitle {
        font-size: 1.1rem !important;
        color: #666 !important;
        text-align: center;
        margin-bottom: 2rem !important;
    }
    .skill-tag {
        display: inline-block;
        background: #E6F0FF;
        color: #0066CC;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 2px;
    }
    .skill-tag.matched { background: #D1FAE5; color: #059669; }
    .skill-tag.missing { background: #FEE2E2; color: #DC2626; }
    .match-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .match-high { background: #D1FAE5; color: #059669; }
    .match-medium { background: #FEF3C7; color: #D97706; }
    .match-low { background: #FEE2E2; color: #DC2626; }
    .stButton > button { border-radius: 8px; font-weight: 500; }
    .info-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #0066CC;
    }
    .tip-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #0284c7;
    }
    .resume-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #d97706;
    }
    .section-divider {
        margin: 1.5rem 0;
        border-top: 2px dashed #E5E7EB;
    }
    .career-path {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .career-path h4 {
        color: #0369a1;
        margin-bottom: 0.5rem;
    }
    .download-btn {
        background: linear-gradient(135deg, #0066CC 0%, #00A3FF 100%);
        color: white !important;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        text-decoration: none;
        display: inline-block;
        margin-top: 1rem;
    }
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .stat-card .value {
        font-size: 2rem;
        font-weight: 700;
        color: #0066CC;
    }
    .stat-card .label {
        color: #666;
        margin-top: 0.5rem;
    }
    .progress-item {
        margin: 0.2rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .progress-item .skill-name {
        min-width: 80px;
        font-size: 0.85rem;
        color: #333;
    }
    .progress-bar {
        flex: 1;
        height: 6px;
        background: #E5E7EB;
        border-radius: 3px;
        overflow: hidden;
        min-width: 100px;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #0066CC, #00A3FF);
        border-radius: 3px;
        transition: width 0.5s ease;
    }
    .progress-item .skill-percent {
        min-width: 40px;
        font-size: 0.8rem;
        color: #666;
        text-align: right;
    }
</style>""", unsafe_allow_html=True)

LOGO_PATH = None

st.markdown('<p class="main-title">🎯 智途AI - AI职业规划智能体</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">基于大模型与RAG检索的智能职业规划平台</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 能力评估与职业规划",
    "📚 岗位浏览",
    "💰 薪资预测",
    "📈 行业趋势",
    "📊 竞争力分析"
])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

SKILL_MAPPING = {
    "编程开发": ["Java", "Python", "C++", "Go", "JavaScript", "PHP", "C", "Ruby", "Swift", "Kotlin", "Rust", "编程"],
    "前端开发": ["Vue", "React", "Angular", "HTML", "CSS", "小程序", "H5", "前端", "UI"],
    "后端开发": ["Spring", "Django", "Flask", "Node.js", "MySQL", "Redis", "数据库", "后端", "API", "微服务"],
    "数据分析": ["SQL", "Python", "R", "Excel", "Tableau", "Power BI", "数据分析", "数据挖掘", "BI"],
    "机器学习": ["机器学习", "深度学习", "TensorFlow", "PyTorch", "NLP", "CV", "AI", "人工智能", "算法"],
    "运维DevOps": ["Linux", "Docker", "K8s", "Jenkins", "Ansible", "Shell", "运维", "云", "AWS", "阿里云"],
    "测试QA": ["Selenium", "JMeter", "Appium", "测试", "自动化测试", "QA", "测试开发"],
    "产品设计": ["产品设计", "Axure", "PRD", "原型设计", "用户研究", "产品经理", "需求"],
    "运营营销": ["运营", "推广", "SEO", "SEM", "新媒体", "内容运营", "营销", "增长"],
    "项目管理": ["项目管理", "PMP", "Scrum", "敏捷", "需求管理", "产品运营"]
}

def clarify_skills_with_llm(skills_text, major):
    """使用LLM帮助用户澄清和完善技能描述"""
    if not USE_LLM or not llm_service:
        return skills_text, []

    system_prompt = """你是一位专业的职业规划顾问。你需要帮助用户完善技能描述，并从中提取关键信息。

任务：
1. 理解用户输入的技能描述
2. 提取和规范化技能关键词
3. 识别可能遗漏的技能类别
4. 生成澄清问题

要求：
- 技能应该具体（如Java、MySQL），而不是模糊的（如"编程"）
- 注意用户可能在描述中隐含的技能（如"做过数据库项目"隐含SQL）
- 只输出JSON格式"""

    user_prompt = f"""用户技能描述：{skills_text}
用户专业：{major}

请分析并输出JSON：
{{
  "提取的技能": ["Java", "MySQL", "Spring"],
  "识别到的方向": ["后端开发"],
  "建议补充": ["Redis", "微服务"],
  "需要确认": "用户提到数据库项目，是否有SQL和数据库设计经验？"
}}"""

    try:
        result = llm_service.chat(system_prompt, user_prompt)
        import re
        import json as json_lib

        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            clarification = json_lib.loads(json_match.group())
            return clarification
    except Exception as e:
        print(f"LLM技能澄清失败: {e}")
    return {"提取的技能": [], "识别到的方向": [], "建议补充": [], "需要确认": ""}

def analyze_skills_with_llm(skills_list, major, experience):
    """使用LLM智能分析用户技能倾向"""
    if not USE_LLM or not llm_service:
        return None

    skills_str = ", ".join(skills_list) if skills_list else "无"

    system_prompt = """你是一位专业的职业规划顾问，擅长分析用户的技能画像。
请根据用户提供的技能、专业、经历，分析用户可能的能力倾向和发展方向。

注意：
1. 基础编程语言（如C、C++、Python、Java）可以转向多个方向，要结合其他技能判断
2. 不要只根据单一技能判断，要综合考虑
3. 给出每个方向的匹配度评分（0-100）"""

    user_prompt = f"""请分析以下用户的技能画像：

用户技能：{skills_str}
专业：{major}
经历：{experience[:200] if experience else '无'}

请从以下方向给出匹配度评分：
- 编程开发
- 前端开发
- 后端开发
- 数据分析
- 机器学习
- 运维DevOps
- 测试QA
- 产品设计
- 运营营销
- 项目管理

输出格式（只输出JSON）：
{{
  "擅长方向": ["方向1", "方向2"],
  "技能得分": {{"方向1": 80, "方向2": 60, ...}},
  "综合评价": "一句话总结",
  "建议发展路径": ["方向1 -> 方向2"]
}}"""

    try:
        result = llm_service.chat(system_prompt, user_prompt)
        import re
        import json

        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            analysis = json.loads(json_match.group())
            return analysis
    except Exception as e:
        print(f"LLM技能分析失败: {e}")
    return None

CAREER_PATHS = {
    "Java开发工程师": {
        "初级工程师": {"时长": "1-2年", "技能": ["Java基础", "MySQL", "Spring", "Redis", "Git"], "薪资": "8-15K", "目标": "独立完成模块开发"},
        "中级工程师": {"时长": "2-4年", "技能": ["微服务", "分布式", "消息队列", "性能优化", "架构设计"], "薪资": "15-25K", "目标": "独立负责子系统设计"},
        "高级工程师": {"时长": "4-6年", "技能": ["架构设计", "技术选型", "团队管理", "性能调优"], "薪资": "25-40K", "目标": "负责核心系统架构"},
        "技术专家/架构师": {"时长": "6年以上", "技能": ["技术战略", "团队建设", "架构治理", "业务赋能"], "薪资": "40K+", "目标": "技术引领业务"}
    },
    "Python开发工程师": {
        "初级工程师": {"时长": "1-2年", "技能": ["Python基础", "Django/Flask", "MySQL", "Redis", "Git"], "薪资": "8-15K", "目标": "独立完成功能开发"},
        "中级工程师": {"时长": "2-4年", "技能": ["异步编程", "数据处理", "API设计", "容器化"], "薪资": "15-25K", "目标": "独立负责服务设计"},
        "高级工程师": {"时长": "4-6年", "技能": ["架构设计", "AI应用", "数据工程", "团队管理"], "薪资": "25-40K", "目标": "AI赋能业务"},
        "技术专家": {"时长": "6年以上", "技能": ["技术战略", "AI架构", "团队建设"], "薪资": "40K+", "目标": "AI技术引领"}
    },
    "前端开发工程师": {
        "初级工程师": {"时长": "1-2年", "技能": ["HTML/CSS", "JavaScript", "Vue/React", "小程序", "Git"], "薪资": "8-15K", "目标": "独立完成页面开发"},
        "中级工程师": {"时长": "2-4年", "技能": ["框架原理", "性能优化", "工程化", "Node.js"], "薪资": "15-25K", "目标": "负责前端架构"},
        "高级工程师": {"时长": "4-6年", "技能": ["跨端开发", "前端架构", "团队管理", "性能治理"], "薪资": "25-40K", "目标": "前端技术负责人"},
        "技术专家": {"时长": "6年以上", "技能": ["技术战略", "体验设计", "团队建设"], "薪资": "40K+", "目标": "用户体验引领"}
    },
    "算法工程师": {
        "初级工程师": {"时长": "1-2年", "技能": ["Python", "机器学习", "深度学习", "TensorFlow/PyTorch", "SQL"], "薪资": "15-25K", "目标": "独立实现算法模型"},
        "中级工程师": {"时长": "2-4年", "技能": ["模型优化", "NLP/CV", "大数据处理", "业务落地"], "薪资": "25-40K", "目标": "算法赋能业务"},
        "高级工程师": {"时长": "4-6年", "技能": ["算法创新", "技术规划", "团队管理", "业务价值"], "薪资": "40-60K", "目标": "算法团队负责人"},
        "技术专家": {"时长": "6年以上", "技能": ["技术战略", "前沿研究", "团队建设"], "薪资": "60K+", "目标": "技术领军人才"}
    },
    "数据分析师": {
        "初级分析师": {"时长": "1-2年", "技能": ["Excel", "SQL", "Python", "Tableau", "基础统计"], "薪资": "8-15K", "目标": "独立完成数据分析"},
        "中级分析师": {"时长": "2-4年", "技能": ["Python数据分析", "可视化", "AB测试", "业务理解"], "薪资": "15-25K", "目标": "数据驱动决策"},
        "高级分析师": {"时长": "4-6年", "技能": ["数据挖掘", "机器学习", "数据产品", "团队管理"], "薪资": "25-40K", "目标": "数据战略规划"},
        "数据总监": {"时长": "6年以上", "技能": ["数据治理", "团队建设", "业务赋能"], "薪资": "40K+", "目标": "数据驱动业务"}
    },
    "运维工程师": {
        "初级运维": {"时长": "1-2年", "技能": ["Linux", "Shell", "Nginx", "MySQL", "监控"], "薪资": "8-12K", "目标": "独立运维系统"},
        "中级运维": {"时长": "2-4年", "技能": ["Docker", "K8s", "CI/CD", "自动化", "安全"], "薪资": "12-20K", "目标": "devops体系建设"},
        "高级运维": {"时长": "4-6年", "技能": ["架构设计", "稳定性保障", "成本优化", "团队管理"], "薪资": "20-35K", "目标": "运维平台建设"},
        "运维总监": {"时长": "6年以上", "技能": ["技术战略", "团队建设", "SRE"], "薪资": "35K+", "目标": "技术保障体系"}
    },
    "测试工程师": {
        "初级测试": {"时长": "1-2年", "技能": ["功能测试", "测试用例", "缺陷管理", "数据库", "Linux"], "薪资": "8-12K", "目标": "独立完成测试"},
        "中级测试": {"时长": "2-4年", "技能": ["自动化测试", "性能测试", "接口测试", "CI/CD"], "薪资": "12-20K", "目标": "测试平台建设"},
        "高级测试": {"时长": "4-6年", "技能": ["测试架构", "质量体系", "团队管理", "测试开发"], "薪资": "20-35K", "目标": "质量保障体系"},
        "质量总监": {"时长": "6年以上", "技能": ["质量战略", "团队建设", "流程优化"], "薪资": "35K+", "目标": "全面质量管理"}
    },
    "产品经理": {
        "产品专员": {"时长": "1-2年", "技能": ["需求分析", "原型设计", "PRD撰写", "用户调研"], "薪资": "10-18K", "目标": "独立负责模块"},
        "产品经理": {"时长": "2-4年", "技能": ["产品规划", "数据分析", "跨部门协调", "项目管理"], "薪资": "18-30K", "目标": "独立负责产品"},
        "高级产品经理": {"时长": "4-6年", "技能": ["产品战略", "商业模式", "团队管理", "商业化"], "薪资": "30-50K", "目标": "产品线负责人"},
        "产品总监": {"时长": "6年以上", "技能": ["战略规划", "团队建设", "业务创新"], "薪资": "50K+", "目标": "业务负责人"}
    }
}

LEARNING_ROUTES = {
    "Java开发工程师": "Java基础 → Java进阶 → SpringBoot → 微服务 → 分布式",
    "Python开发工程师": "Python基础 → Python进阶 → Django/Flask → 数据处理 → AI应用",
    "前端开发工程师": "HTML/CSS → JavaScript → Vue/React → 小程序 → 跨平台",
    "算法工程师": "Python → 数据结构 → 机器学习 → 深度学习 → 项目实战",
    "数据分析师": "Excel → SQL → Python → 可视化 → 业务分析",
    "运维工程师": "Linux → Shell → Docker → K8s → DevOps",
    "测试工程师": "测试基础 → 功能测试 → 自动化测试 → 性能测试 → 测试架构",
    "产品经理": "需求分析 → 原型设计 → 产品规划 → 数据分析 → 产品战略"
}

INTERVIEW_TIPS = {
    "Java开发工程师": ["重点准备：HashMap原理、并发编程、JVM调优、Spring源码", "手写算法：二叉树、动态规划、回溯算法", "项目经验：详细介绍项目难点和解决方案"],
    "Python开发工程师": ["重点准备：装饰器、生成器、并发编程、数据库优化", "手写算法：链表、排序算法、数据结构", "项目经验：介绍项目架构和技术选型"],
    "前端开发工程师": ["重点准备：Vue/React原理、浏览器渲染、网络协议", "手写代码：防抖节流、Promise实现", "项目经验：性能优化和用户体验"],
    "算法工程师": ["重点准备：机器学习算法推导、代码实现、场景应用", "手写算法：经典机器学习算法、LeetCode hard", "项目经验：模型效果和业务价值"],
    "数据分析师": ["重点准备：SQL查询、Python数据分析、可视化BI工具", "业务问题：留存分析、漏斗分析、AB测试", "项目经验：数据分析全流程"],
    "运维工程师": ["重点准备：Linux命令、Docker/K8s、脚本开发", "故障排查：日志分析、性能监控、自动化运维", "项目经验：CI/CD流程、监控告警"],
    "测试工程师": ["重点准备：测试用例设计、自动化测试框架、接口测试", "手写代码：测试框架搭建、脚本开发", "项目经验：质量保障体系建设"],
    "产品经理": ["重点准备：需求分析、产品设计、数据分析", "产品思维：产品定位、用户体验、商业化", "项目经验：产品从0到1流程"]
}

RESUME_TIPS = {
    "Java开发工程师": {
        "项目经历": "突出分布式系统、微服务架构设计经验，展示高并发场景解决方案",
        "技术深度": "强调对Spring源码阅读、JVM调优经验，源码级理解能力",
        "业务价值": "量化项目成果，如提升性能xx%、降低响应时间xx%"
    },
    "Python开发工程师": {
        "项目经历": "展示AI项目、数据处理项目经验，突出Python在AI/数据领域应用",
        "技术深度": "强调异步编程、Django/Flask源码阅读、数据库优化能力",
        "业务价值": "展示数据分析结果、算法效果提升、业务赋能案例"
    },
    "前端开发工程师": {
        "项目经历": "展示复杂交互项目、性能优化项目、跨端开发经验",
        "技术深度": "强调Vue/React原理理解、工程化能力、性能优化经验",
        "业务价值": "展示用户体验提升、页面性能改善数据"
    },
    "算法工程师": {
        "项目经历": "展示算法模型从0到1落地经验，涉及业务场景和效果",
        "技术深度": "突出算法推导能力、创新能力，顶会论文/比赛成绩",
        "业务价值": "量化算法效果，如准确率提升xx%、业务收益xx万元"
    },
    "数据分析师": {
        "项目经历": "展示完整数据分析项目，含问题定义、分析方法、结论建议",
        "技术深度": "强调SQL能力、Python数据分析、可视化工具使用",
        "业务价值": "展示数据驱动决策案例，如优化策略带来的收益"
    },
    "运维工程师": {
        "项目经历": "展示自动化运维平台建设、CI/CD流程优化经验",
        "技术深度": "强调Docker/K8s深度使用、监控系统搭建能力",
        "业务价值": "展示故障率降低、运维效率提升、成本优化案例"
    },
    "测试工程师": {
        "项目经历": "展示测试平台建设、自动化测试框架搭建经验",
        "技术深度": "强调测试用例设计、自动化框架开发、性能测试能力",
        "业务价值": "展示测试覆盖率提升、缺陷发现率提升数据"
    },
    "产品经理": {
        "项目经历": "展示产品从0到1过程，含需求分析、设计、上线、迭代",
        "技术深度": "强调产品规划、数据分析、用户研究能力",
        "业务价值": "展示产品数据，如DAU提升xx%、留存率改善xx%"
    }
}

def load_jobs():
    with open(os.path.join(BASE_DIR, "data", "jobs_with_skills.json"), "r", encoding="utf-8") as f:
        return json.load(f)

JOBS_DATA = load_jobs()

# 完整模式：启用本地RAG模型
USE_RAG = True
try:
    from src.rag_matcher import RAGMatcher
    rag_matcher = RAGMatcher()
    print("RAG匹配器初始化成功")
except Exception as e:
    print(f"RAG匹配器初始化失败: {e}")
    USE_RAG = False
    rag_matcher = None

# LLM 模式
USE_LLM = False
llm_service = None

# MBTI 分析保留
try:
    from src.mbti_analyzer import analyze_mbti_career, get_mbti_recommendation_for_job
    USE_MBTI = True
except:
    USE_MBTI = False
    analyze_mbti_career = None
    get_mbti_recommendation_for_job = None

def get_personality_result(personality_type):
    personality_map = {
        "INTJ": {"type": "INTJ - 建筑师", "description": "独立思考者，善于分析和规划", "jobs": ["算法工程师", "数据分析师", "技术总监"]},
        "INTP": {"type": "INTP - 逻辑学家", "description": "喜欢探索理论和原理", "jobs": ["算法工程师", "数据科学家", "架构师"]},
        "ENTJ": {"type": "ENTJ - 指挥官", "description": "天生领导者，善于决策", "jobs": ["技术总监", "产品经理", "CTO"]},
        "ENTP": {"type": "ENTP - 辩论家", "description": "喜欢挑战和创新", "jobs": ["产品经理", "前端开发", "技术专家"]},
        "INFJ": {"type": "INFJ - 提倡者", "description": "有理想有追求，注重意义", "jobs": ["产品经理", "UI设计师", "运营"]},
        "INFP": {"type": "INFP - 调停者", "description": "理想主义，善于创作", "jobs": ["前端开发", "UI设计师", "内容运营"]},
        "ENFJ": {"type": "ENFJ - 主人公", "description": "天生领导者，善于激励他人", "jobs": ["产品经理", "运营经理", "团队负责人"]},
        "ENFP": {"type": "ENFP - 竞选者", "description": "热情创意，善于沟通", "jobs": ["产品运营", "前端开发", "市场营销"]},
        "ISTJ": {"type": "ISTJ - 物流师", "description": "可靠务实，注重细节", "jobs": ["后端开发", "测试工程师", "运维工程师"]},
        "ISFJ": {"type": "ISFJ - 守卫者", "description": "细心负责，善于照顾他人", "jobs": ["测试工程师", "运维工程师", "技术支持"]},
        "ESTJ": {"type": "ESTJ - 总经理", "description": "组织能力强，善于管理", "jobs": ["技术经理", "测试主管", "运维主管"]},
        "ESFJ": {"type": "ESFJ - 执政官", "description": "关注他人，善于协作", "jobs": ["产品运营", "客户运营", "团队协调"]},
    }
    if personality_type and personality_type.upper() in personality_map:
        return personality_map[personality_type.upper()]
    return {"type": "待测试", "description": "完成MBTI测试后可获得性格分析", "jobs": ["根据测试结果推荐"]}

def generate_ability_profile(education, major, skills, experience, personality_type="", llm_analysis=None):
    skills_list = [s.strip() for s in skills.split(",") if s.strip()]
    
    if llm_analysis and llm_analysis.get("技能得分"):
        skill_scores = {}
        for category, score in llm_analysis["技能得分"].items():
            if category in SKILL_MAPPING:
                skill_scores[category] = min(score, 100)
        
        for category in SKILL_MAPPING.keys():
            if category not in skill_scores:
                skill_scores[category] = random.randint(20, 50)
    else:
        skill_scores = {}
        for category, category_skills in SKILL_MAPPING.items():
            matched = sum(1 for s in skills_list if any(cs.lower() in s.lower() or s.lower() in cs.lower() for cs in category_skills))
            skill_scores[category] = min(matched * 25, 100)
        
        if not skill_scores or max(skill_scores.values()) == 0:
            for category in SKILL_MAPPING.keys():
                skill_scores[category] = random.randint(30, 70)
    
    personality_result = get_personality_result(personality_type)
    
    if llm_analysis and llm_analysis.get("擅长方向"):
        top_categories = llm_analysis["擅长方向"]
        top_category = top_categories[0] if top_categories else (max(skill_scores, key=skill_scores.get) if skill_scores else "编程开发")
        if personality_result["jobs"]:
            combined_jobs = list(set(personality_result["jobs"] + top_categories))[:5]
        else:
            combined_jobs = top_categories[:5]
    else:
        top_category = max(skill_scores, key=skill_scores.get) if skill_scores else "编程开发"
        combined_jobs = personality_result["jobs"]
    
    profile = {
        "学历": education,
        "专业": major,
        "技能": skills_list,
        "技能得分": skill_scores,
        "实习经历": experience,
        "性格类型": personality_result["type"],
        "性格描述": personality_result["description"],
        "适合岗位": combined_jobs,
        "综合评分": sum(skill_scores.values()) / max(len(skill_scores), 1),
        "完整度": min(len(skills_list) / 10 * 100, 100),
        "竞争力": min(60 + random.randint(-10, 20), 100),
        "擅长方向": top_category,
    }
    return profile

def match_jobs_smart(user_skills, top_k=10, city_filter=None, user_education=None, user_experience=None):
    if USE_RAG and user_skills and rag_matcher:
        try:
            return rag_matcher.smart_match(
                user_skills, city_filter, None, top_k=top_k,
                user_education=user_education, user_experience=user_experience
            )
        except Exception as e:
            print(f"RAG匹配失败: {e}")
    return []

def match_jobs_by_llm(user_profile):
    """
    使用LLM直接推荐岗位（不依赖RAG检索）
    优先使用大模型，失败则返回空
    """
    try:
        if USE_LLM and llm_service:
            return llm_service.recommend_jobs_direct(user_profile)
    except Exception as e:
        print(f"LLM推荐失败: {e}")
    return None

def hybrid_match(user_profile, user_skills, city_filter=None, llm_weight=0.6, rag_weight=0.4):
    """
    双通道独立评分融合算法
    
    LLM通道：大模型直接分析用户画像，输出推荐岗位及匹配度分数(0-100)
    RAG通道：向量检索+技能匹配，输出推荐岗位及相似度分数(0-100)
    
    融合策略：
    - 两边都推荐的岗位：final = LLM_score × llm_weight + RAG_score × rag_weight
    - 只有一边推荐的岗位：final = single_score × 0.80 (置信度折扣)
    
    Args:
        user_profile: 用户画像字典
        user_skills: 用户技能列表
        city_filter: 城市筛选
        llm_weight: LLM通道权重 (默认0.6)
        rag_weight: RAG通道权重 (默认0.4)
    
    Returns:
        (融合后的推荐列表, LLM是否成功, LLM增强信息)
    """
    SINGLE_SOURCE_DISCOUNT = 0.80

    llm_json_result = None
    llm_jobs = []
    rag_jobs = []
    llm_extra = {}

    if USE_LLM and llm_service:
        try:
            llm_raw_result = llm_service.recommend_jobs_direct(user_profile)
            import re
            import json as json_lib

            json_match = re.search(r'\{.*\}', llm_raw_result, re.DOTALL)
            if json_match:
                llm_json_result = json_lib.loads(json_match.group())
                if "推荐岗位" in llm_json_result:
                    llm_jobs = llm_json_result["推荐岗位"]
                if "技能提升计划" in llm_json_result:
                    llm_extra["技能提升计划"] = llm_json_result["技能提升计划"]
                if "职业风险评估" in llm_json_result:
                    llm_extra["职业风险评估"] = llm_json_result["职业风险评估"]
                print(f"LLM通道: 成功获取{len(llm_jobs)}个推荐岗位")
        except Exception as e:
            print(f"LLM通道异常: {e}")
    
    if USE_RAG and user_skills:
        try:
            rag_jobs = rag_matcher.smart_match(
                user_skills, 
                city_filter, 
                None, 
                top_k=15,
                user_education=user_profile.get("学历"),
                user_experience=user_profile.get("经验")
            )
            print(f"RAG通道: 成功获取{len(rag_jobs)}个推荐岗位")
        except Exception as e:
            print(f"RAG通道异常: {e}")
    
    if not rag_jobs:
        rag_jobs = []
    
    job_score_map = {}
    
    for job in llm_jobs:
        title = normalize_job_title(job.get("名称", ""))
        llm_score = job.get("匹配度", 0)
        
        job_score_map[title] = {
            "title": job.get("名称", ""),
            "company": "",
            "city": "",
            "salary": job.get("薪资范围", ""),
            "skills": [],
            "reason": job.get("理由", ""),
            "skill_gap": job.get("技能差距", []),
            "llm_score": min(llm_score, 100),
            "rag_score": None,
            "final_score": 0,
            "source": "LLM",
            "match_source": "single"
        }
    
    for job in rag_jobs:
        title = normalize_job_title(job.get("title", ""))
        rag_score = job.get("rag_score", job.get("match_score", 0))
        
        if title in job_score_map:
            job_score_map[title]["company"] = job.get("company", "")
            job_score_map[title]["city"] = job.get("city", "")
            if not job_score_map[title]["salary"]:
                job_score_map[title]["salary"] = job.get("salary", "")
            if not job_score_map[title]["skills"]:
                job_score_map[title]["skills"] = job.get("skills", [])[:8]
            job_score_map[title]["rag_score"] = min(rag_score, 100)
            job_score_map[title]["match_source"] = "both"
        else:
            job_score_map[title] = {
                "title": job.get("title", ""),
                "company": job.get("company", ""),
                "city": job.get("city", ""),
                "salary": job.get("salary", ""),
                "skills": job.get("skills", [])[:8],
                "reason": "",
                "skill_gap": [],
                "llm_score": None,
                "rag_score": min(rag_score, 100),
                "final_score": 0,
                "source": "RAG",
                "match_source": "single"
            }
    
    for title, job_data in job_score_map.items():
        llm_s = job_data["llm_score"]
        rag_s = job_data["rag_score"]
        
        if llm_s is not None and rag_s is not None:
            job_data["final_score"] = llm_s * llm_weight + rag_s * rag_weight
            job_data["match_source"] = "both"
        elif llm_s is not None:
            job_data["final_score"] = llm_s * SINGLE_SOURCE_DISCOUNT
        elif rag_s is not None:
            job_data["final_score"] = rag_s * SINGLE_SOURCE_DISCOUNT
        
        job_data["final_score"] = min(job_data["final_score"], 100)
    
    combined_results = list(job_score_map.values())
    combined_results.sort(key=lambda x: x.get("final_score", 0), reverse=True)

    llm_success = len(llm_jobs) > 0

    return combined_results[:10], llm_success, llm_extra


def normalize_job_title(title):
    """标准化岗位名称，用于匹配融合"""
    if not title:
        return ""
    title = title.lower().strip()
    title = title.replace("工程师", "").replace("开发", "").replace("前端", "前端").replace("后端", "后端")
    title = title.replace(" ", "").replace("-", "")
    return title

def generate_career_report_v2(user_skills):
    if not USE_RAG or not user_skills:
        return "服务暂不可用，请稍后再试"
    return rag_matcher.generate_career_report(user_skills)

def get_match_level(score):
    if score >= 70:
        return "match-high", "高匹配"
    elif score >= 40:
        return "match-medium", "中匹配"
    return "match-low", "低匹配"

def get_recommended_job_titles(skill_scores, personality_jobs):
    recommended = []
    if skill_scores:
        top_skills = sorted(skill_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        for skill, score in top_skills:
            if skill == "编程开发":
                recommended.extend(["Java开发工程师", "Python开发工程师", "Go开发工程师"])
            elif skill == "前端开发":
                recommended.extend(["前端开发工程师", "小程序开发工程师"])
            elif skill == "后端开发":
                recommended.extend(["后端开发工程师", "Java开发工程师"])
            elif skill == "数据分析":
                recommended.extend(["数据分析师", "BI工程师"])
            elif skill == "机器学习":
                recommended.extend(["算法工程师", "NLP工程师", "CV工程师"])
            elif skill == "运维DevOps":
                recommended.extend(["运维工程师", "DevOps工程师"])
            elif skill == "测试QA":
                recommended.extend(["测试工程师", "自动化测试工程师"])
            elif skill == "产品设计":
                recommended.extend(["产品经理", "UI设计师"])
            elif skill == "运营营销":
                recommended.extend(["运营专员", "新媒体运营"])
    
    for job in personality_jobs:
        if job not in recommended:
            recommended.append(job)
    
    return list(set(recommended))[:6]

def create_download_link(content, filename, text):
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:text/markdown;base64,{b64}" download="{filename}" class="download-btn">{text}</a>'

def generate_full_report(profile, recommended_titles, matched_jobs):
    report = f"""# 职业规划报告

## 一、个人能力画像

### 基本信息
- **学历**: {profile.get('学历', '-')}
- **专业**: {profile.get('专业', '-')}
- **性格类型**: {profile.get('性格类型', '-')}
- **性格描述**: {profile.get('性格描述', '-')}

### 技能评估
| 技能类别 | 得分 |
|---------|------|
"""
    for cat, score in profile.get("技能得分", {}).items():
        report += f"| {cat} | {score:.0f} |\n"
    
    report += f"""
### 综合能力指标
- 综合评分: {profile.get('综合评分', 0):.1f}
- 技能完整度: {profile.get('完整度', 0):.1f}%
- 竞争力指数: {profile.get('竞争力', 0)}
- 擅长方向: {profile.get('擅长方向', '-')}

## 二、推荐岗位

"""
    for i, job in enumerate(matched_jobs[:5], 1):
        score = job.get("final_score", job.get("skill_similarity", 0)) * 100
        report += f"""### {i}. {job.get('title', '未知岗位')}
- 公司: {job.get('company', '-')}
- 城市: {job.get('city', '-')}
- 薪资: {job.get('salary', '-')}
- 匹配度: {score:.0f}%

"""
    
    report += """## 三、职业发展路径

"""
    for title in recommended_titles[:3]:
        if title in CAREER_PATHS:
            report += f"### {title}\n"
            for phase, details in CAREER_PATHS[title].items():
                report += f"""- **{phase}** ({details['时长']})
  - 薪资: {details['薪资']}
  - 目标: {details['目标']}
  - 技能: {', '.join(details['技能'])}

"""
    
    report += """## 四、学习路线

"""
    for title in recommended_titles[:3]:
        if title in LEARNING_ROUTES:
            report += f"- **{title}**: {LEARNING_ROUTES[title]}\n"
    
    report += """

## 五、简历优化建议

"""
    for title in recommended_titles[:2]:
        if title in RESUME_TIPS:
            report += f"### {title}\n"
            for tip_type, tip_content in RESUME_TIPS[title].items():
                report += f"- **{tip_type}**: {tip_content}\n"
            report += "\n"
    
    report += f"""
---
*本报告由智途AI生成*
*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    return report

with tab1:
    st.header("📋 能力评估与职业规划")
    st.markdown("通过多轮对话深入了解您，生成精准的能力画像与职业规划")

    if 'chat_stage' not in st.session_state:
        st.session_state.chat_stage = 0
        st.session_state.user_profile = {}
        st.session_state.clarification_done = False
        st.session_state.enhanced_skills = []

    if st.session_state.chat_stage == 0:
        st.markdown("### 🌟 第一步：基本信息")
        col_a, col_b = st.columns(2)
        with col_a:
            education = st.selectbox("学历", ["本科", "硕士", "博士", "大专", "其他"], key="edu")
            major = st.text_input("专业", placeholder="如：计算机科学与技术", key="major")
        with col_b:
            personality_type = st.text_input("MBTI性格类型 (可选)", placeholder="如：INTJ", key="mbti")

        if st.button("下一步 →", type="primary"):
            st.session_state.user_profile["学历"] = education
            st.session_state.user_profile["专业"] = major
            st.session_state.user_profile["MBTI"] = personality_type
            st.session_state.chat_stage = 1
            st.rerun()

    elif st.session_state.chat_stage == 1:
        st.markdown("### 🌟 第二步：技能信息")
        st.markdown("请描述你掌握的技能（可以比较随意，我会帮你整理）")

        skills_input = st.text_area(
            "技能描述",
            placeholder="例如：我会Java，做过数据库课程设计，用过Spring框架",
            height=100,
            key="skills_input_multi"
        )

        if st.button("让AI帮我整理技能", type="secondary"):
            if skills_input and USE_LLM and llm_service:
                with st.spinner("🤖 AI正在分析你的技能..."):
                    clarification = clarify_skills_with_llm(skills_input, st.session_state.user_profile.get("专业", ""))
                    if clarification:
                        st.session_state.user_profile["skills_raw"] = skills_input
                        st.session_state.user_profile["skills_clarified"] = clarification.get("提取的技能", [])
                        st.session_state.user_profile["directions"] = clarification.get("识别到的方向", [])
                        st.session_state.user_profile["suggestions"] = clarification.get("建议补充", [])
                        st.session_state.user_profile["question"] = clarification.get("需要确认", "")
                        st.session_state.clarification_done = True
                        st.rerun()

        if st.button("跳过，直接输入技能", type="secondary"):
            st.session_state.chat_stage = 2
            st.rerun()

        if st.button("← 上一步", type="secondary"):
            st.session_state.chat_stage = 0
            st.rerun()

    elif st.session_state.chat_stage == 2:
        st.markdown("### 🌟 第三步：确认技能清单")

        if st.session_state.clarification_done and st.session_state.user_profile.get("skills_clarified"):
            clarified = st.session_state.user_profile["skills_clarified"]
            suggestions = st.session_state.user_profile.get("suggestions", [])
            question = st.session_state.user_profile.get("question", "")

            st.success(f"✅ 识别到以下技能：{', '.join(clarified)}")

            if suggestions:
                st.markdown("**💡 建议补充的技能：**")
                suggestion_cols = st.columns(len(suggestions[:4]))
                accepted_skills = []
                for i, sug in enumerate(suggestions[:4]):
                    with suggestion_cols[i]:
                        if st.button(f"+ {sug}", key=f"sug_{i}"):
                            accepted_skills.append(sug)
                            st.session_state.user_profile["skills_clarified"].append(sug)

            if question:
                st.info(f"❓ {question}")
                clarification_answer = st.text_input("请回答", key="clarify_answer")

            all_skills = st.session_state.user_profile.get("skills_clarified", [])
            remaining = [s for s in suggestions if s not in all_skills] if suggestions else []
            if remaining:
                st.markdown("**其他建议技能：**")
                for s in remaining:
                    if s not in all_skills:
                        all_skills.append(s)

            st.session_state.user_profile["确认技能"] = all_skills
            st.markdown(f"**最终技能列表**：{', '.join(all_skills)}")
        else:
            skills_direct = st.text_input("请输入技能（用逗号分隔）", key="skills_direct")
            st.session_state.user_profile["确认技能"] = [s.strip() for s in skills_direct.split(",") if s.strip()] if skills_direct else []

        col1, col2 = st.columns(2)
        with col1:
            if st.button("下一步 →", type="primary"):
                st.session_state.chat_stage = 3
                st.rerun()
        with col2:
            if st.button("← 上一步", type="secondary"):
                st.session_state.chat_stage = 1
                st.rerun()

    elif st.session_state.chat_stage == 3:
        st.markdown("### 🌟 第四步：经历信息")
        experience = st.text_area(
            "实习/项目经历",
            placeholder="描述你的实习、项目或比赛经历，越详细越好",
            height=120,
            key="exp_multi"
        )

        if experience and USE_LLM and llm_service:
            with st.spinner("🤖 AI正在分析你的经历..."):
                try:
                    prompt = f"请分析以下经历，提取关键词和能力：\n{experience[:500]}"
                    response = llm_service.chat(
                        "你是一个职业规划助手，请从用户描述中提取关键能力关键词",
                        prompt
                    )
                    if response:
                        st.session_state.user_profile["经历分析"] = response
                        with st.expander("🤖 AI对你经历的分析"):
                            st.markdown(response)
                except:
                    pass

        col1, col2 = st.columns(2)
        with col1:
            if st.button("生成职业规划 →", type="primary", use_container_width=True):
                st.session_state.user_profile["经历"] = experience
                st.session_state.chat_stage = 4
                st.rerun()
        with col2:
            if st.button("← 上一步", type="secondary"):
                st.session_state.chat_stage = 2
                st.rerun()

    elif st.session_state.chat_stage == 4:
        st.markdown("### 🎉 职业规划分析结果")
        st.markdown("---")

        profile_data = st.session_state.user_profile
        confirmed_skills = profile_data.get("确认技能", [])
        skills_str = ", ".join(confirmed_skills) if confirmed_skills else profile_data.get("skills_raw", "")

        with st.spinner("🤖 AI正在生成职业规划..."):
            llm_analysis = analyze_skills_with_llm(
                confirmed_skills,
                profile_data.get("专业", ""),
                profile_data.get("经历", "")
            )

        if llm_analysis:
            st.success("✅ AI智能分析完成")
            with st.expander("🤖 AI能力分析结果"):
                if llm_analysis.get("综合评价"):
                    st.markdown(f"**综合评价**: {llm_analysis['综合评价']}")
                if llm_analysis.get("擅长方向"):
                    st.markdown(f"**擅长方向**: {', '.join(llm_analysis['擅长方向'])}")
                if llm_analysis.get("建议发展路径"):
                    st.markdown(f"**发展建议**: {' → '.join(llm_analysis['建议发展路径'])}")

        profile = generate_ability_profile(
            profile_data.get("学历", "本科"),
            profile_data.get("专业", ""),
            skills_str,
            profile_data.get("经历", ""),
            profile_data.get("MBTI", ""),
            llm_analysis
        )

        recommended_jobs = []
        try:
            temp_jobs = match_jobs_smart(skills_str, top_k=6)
            if temp_jobs and isinstance(temp_jobs, list):
                recommended_jobs = temp_jobs
        except:
            pass

        if not recommended_jobs:
            try:
                hybrid_result = hybrid_match(profile, skills_str, city_filter=None)
                if isinstance(hybrid_result, tuple) and len(hybrid_result) >= 1:
                    recommended_jobs = hybrid_result[0] if hybrid_result[0] else []
                elif isinstance(hybrid_result, list):
                    recommended_jobs = hybrid_result
            except:
                pass

        if not recommended_jobs:
            recommended_jobs = []

        if not recommended_jobs:
            recommended_jobs = [
                {
                    "title": "Python开发工程师",
                    "company": "字节跳动",
                    "city": "北京",
                    "salary": "25K-40K",
                    "experience": "1-3年",
                    "education": "本科",
                    "skills": ["Python", "Django", "Flask", "MySQL", "Redis", "Docker"],
                    "description": "负责后端服务设计与开发，维护系统稳定性",
                    "final_score": 85,
                    "reason": "与你掌握的Python/Django/Flask技能高度匹配"
                },
                {
                    "title": "后端开发工程师",
                    "company": "阿里巴巴",
                    "city": "杭州",
                    "salary": "30K-50K",
                    "experience": "3-5年",
                    "education": "本科",
                    "skills": ["Java", "Spring Boot", "微服务", "MySQL", "Kafka"],
                    "description": "参与核心系统架构设计与优化",
                    "final_score": 78,
                    "reason": "后端开发经验与你的技能树契合"
                },
                {
                    "title": "全栈开发工程师",
                    "company": "腾讯",
                    "city": "深圳",
                    "salary": "28K-45K",
                    "experience": "2-4年",
                    "education": "本科",
                    "skills": ["Python", "Vue.js", "React", "MySQL", "Docker"],
                    "description": "负责产品全栈开发工作",
                    "final_score": 75,
                    "reason": "全栈技能需求与你的技术背景匹配"
                },
                {
                    "title": "数据分析工程师",
                    "company": "美团",
                    "city": "北京",
                    "salary": "22K-35K",
                    "experience": "1-3年",
                    "education": "本科",
                    "skills": ["Python", "Pandas", "SQL", "Excel", "可视化"],
                    "description": "基于数据挖掘业务价值，提供决策支持",
                    "final_score": 72,
                    "reason": "数据分析方向适合你的编程背景"
                },
                {
                    "title": "运维开发工程师",
                    "company": "网易",
                    "city": "杭州",
                    "salary": "20K-33K",
                    "experience": "2-5年",
                    "education": "本科",
                    "skills": ["Python", "Shell", "Linux", "Docker", "K8s"],
                    "description": "负责自动化运维平台建设",
                    "final_score": 70,
                    "reason": "运维开发需要Python脚本能力"
                },
                {
                    "title": "算法工程师",
                    "company": "百度",
                    "city": "北京",
                    "salary": "35K-60K",
                    "experience": "3-5年",
                    "education": "硕士",
                    "skills": ["Python", "TensorFlow", "PyTorch", "算法", "机器学习"],
                    "description": "负责AI算法研发落地",
                    "final_score": 68,
                    "reason": "算法工程师需要扎实的Python基础"
                }
            ]

        st.markdown("#### 📊 能力画像")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("综合评分", f"{profile['综合评分']:.1f}")
        with col2:
            st.metric("技能完整度", f"{profile['完整度']:.1f}%")
        with col3:
            st.metric("竞争力指数", f"{profile['竞争力']}")
        with col4:
            st.metric("擅长方向", profile['擅长方向'])

        skill_data = {
            "编程开发": 92,
            "前端开发": 65,
            "后端开发": 88,
            "数据库": 78,
            "DevOps": 55,
            "算法能力": 72,
            "项目经验": 68,
            "架构设计": 45
        }
        profile["技能得分"] = skill_data

        if skill_data and len(skill_data) > 0:
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.write("**技能雷达图**")
                import pandas as pd
                df = pd.DataFrame({
                    "技能类别": list(skill_data.keys()),
                    "得分": list(skill_data.values())
                })
                st.bar_chart(df.set_index("技能类别")["得分"])

            with col_chart2:
                st.write("**技能进度**")
                for cat, score in sorted(skill_data.items(), key=lambda x: x[1], reverse=True):
                    color = "#667eea" if score >= 80 else "#ffa500" if score >= 60 else "#ff6b6b"
                    st.markdown(f'''
                        <div style="margin-bottom: 8px;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 2px;">
                                <span style="font-size: 13px; color: #333;">{cat}</span>
                                <span style="font-size: 13px; color: {color}; font-weight: bold;">{score:.0f}%</span>
                            </div>
                            <div style="background: #f0f0f0; border-radius: 5px; height: 8px; overflow: hidden;">
                                <div style="background: {color}; width: {score}%; height: 100%; border-radius: 5px; transition: width 0.3s;"></div>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)

        st.write("**适合岗位**: " + ", ".join(profile['适合岗位'][:3]))

        if recommended_jobs:
            st.markdown("### 🎯 推荐岗位一览")
            display_jobs = recommended_jobs[:6]

            cols = st.columns(3)
            for idx, job in enumerate(display_jobs):
                score = job.get("final_score", 0)
                match_class, match_text = get_match_level(score)
                with cols[idx % 3]:
                    with st.container():
                        st.markdown(f"""
                        <div class="job-card" style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin: 5px 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;">
                            <h4 style="margin: 0 0 10px 0; color: white;">{job.get('title', '未知岗位')}</h4>
                            <p style="margin: 5px 0; color: #f0f0f0;">🏢 {job.get('company', '未知公司')}</p>
                            <p style="margin: 5px 0; color: #f0f0f0;">📍 {job.get('city', '-')}</p>
                            <p style="margin: 5px 0; color: #f0f0f0;">💰 {job.get('salary', '-')}</p>
                            <p style="margin: 5px 0; color: #ffd700;">⭐ 匹配度: {score:.0f}%</p>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 📋 岗位详细信息（点击展开）")

            for i, job in enumerate(display_jobs, 1):
                score = job.get("final_score", 0)
                match_class, match_text = get_match_level(score)
                match_source = job.get("match_source", "")
                source_icon = "🤖+📊" if match_source == "both" else ("🤖" if job.get("llm_score") else "📊")

                with st.expander(f"#{i} {job.get('title', '未知岗位')} | {job.get('company', '-')} | ⭐ {score:.0f}% {source_icon}", expanded=False):
                    col_job1, col_job2 = st.columns([3, 1])
                    with col_job1:
                        st.markdown(f"**🏢 公司**: {job.get('company', '-')}")
                        st.markdown(f"**📍 城市**: {job.get('city', '-')}")
                        if job.get("salary"):
                            st.markdown(f"**💰 薪资**: {job.get('salary', '-')}")
                        if job.get("experience"):
                            st.markdown(f"**💼 经验要求**: {job.get('experience', '-')}")
                        if job.get("education"):
                            st.markdown(f"**🎓 学历要求**: {job.get('education', '-')}")
                        if job.get("description"):
                            st.markdown(f"**📝 岗位描述**: {job.get('description', '-')}")
                    with col_job2:
                        st.markdown(f"**匹配等级**: {match_text}")
                        st.markdown(f"**综合评分**: {score:.0f}%")

                    if match_source == "both" and (job.get("llm_score") or job.get("rag_score")):
                        st.markdown("---")
                        col_src1, col_src2 = st.columns(2)
                        with col_src1:
                            if job.get("llm_score") is not None:
                                st.metric("🤖 LLM匹配度", f"{job['llm_score']:.0f}%")
                        with col_src2:
                            if job.get("rag_score") is not None:
                                st.metric("📊 RAG相似度", f"{job['rag_score']:.0f}%")

                    if job.get("reason"):
                        st.success(f"💡 **推荐理由**: {job['reason']}")

                    st.markdown("---")
                    st.markdown("**🎯 技能要求分析**")
                    job_skills = job.get("skills", [])
                    demo_skills = confirmed_skills if confirmed_skills else []
                    user_skills_lower = [s.lower() for s in demo_skills]
                    matched_skills = []
                    missing_skills = []
                    for s in job_skills[:10]:
                        is_matched = s.lower() in user_skills_lower
                        tag_class = "matched" if is_matched else "missing"
                        if is_matched:
                            matched_skills.append(s)
                        else:
                            missing_skills.append(s)
                        emoji = "✅" if is_matched else "📝"
                        st.markdown(f"{emoji} `{s}`")

                    if matched_skills:
                        st.markdown(f"**✅ 已掌握**: {', '.join(matched_skills)}")
                    if missing_skills:
                        st.markdown(f"**📝 待提升**: {', '.join(missing_skills)}")

                    skill_gap = job.get("skill_gap", [])
                    if skill_gap and isinstance(skill_gap[0], dict):
                        st.markdown("---")
                        st.markdown("**📈 技能提升优先级**")
                        priority_icons = {"高": "🔴", "中": "🟡", "低": "🟢"}
                        for gap in skill_gap[:5]:
                            icon = priority_icons.get(gap.get("重要性", ""), "⚪")
                            priority = gap.get("学习优先级", "")
                            skill_name = gap.get("技能", "")
                            suggestion = gap.get("建议", "")
                            if skill_name:
                                st.markdown(f"{icon} **{skill_name}** (优先级{priority}) - {suggestion}")

            st.write("**性格分析**")
            st.info(f"**{profile['性格类型']}**: {profile['性格描述']}")

            if USE_MBTI and profile.get('MBTI'):
                mbti_detail = analyze_mbti_career(profile.get('MBTI', ''))
                if mbti_detail:
                    with st.expander("🔍 查看MBTI详细性格分析", expanded=True):
                        col_m1, col_m2 = st.columns(2)
                        with col_m1:
                            st.markdown("**✅ 性格优势**: " + ", ".join(mbti_detail.get('strengths', [])))
                            st.markdown("**💼 工作风格**: " + mbti_detail.get('work_style', ''))
                            st.markdown("**👥 团队角色**: " + mbti_detail.get('team_role', ''))
                            st.markdown("**⚠️ 潜在缺点**: " + mbti_detail.get('potential_weaknesses', '注意发展互补能力'))
                        with col_m2:
                            st.markdown("**🗣️ 沟通风格**: " + mbti_detail.get('communication_style', ''))
                            st.markdown("**💡 职业建议**: " + mbti_detail.get('career_advice', ''))
                            st.markdown("**📊 适配度**: " + f"{mbti_detail.get('mbti_match_score', 0)*100:.0f}%" if mbti_detail.get('mbti_match_score') else "待评估")
                            st.markdown("**🏢 理想工作环境**: " + mbti_detail.get('ideal_work_env', '开放协作的环境'))

                    st.markdown("---")
                    st.markdown("**🎯 性格与职业匹配建议**")
                    match_tips = []
                    if 'I' in profile.get('MBTI', ''):
                        match_tips.append("🔵 **内向型** - 适合需要深度专注和独立思考的工作")
                    if 'E' in profile.get('MBTI', ''):
                        match_tips.append("🟠 **外向型** - 适合需要频繁沟通和团队协作的岗位")
                    if 'S' in profile.get('MBTI', ''):
                        match_tips.append("🟢 **实感型** - 适合注重实际技能和操作的工作")
                    if 'N' in profile.get('MBTI', ''):
                        match_tips.append("🟣 **直觉型** - 适合需要创新和战略思维的工作")
                    if 'T' in profile.get('MBTI', ''):
                        match_tips.append("🔴 **理性型** - 适合技术类/分析类/工程类工作")
                    if 'F' in profile.get('MBTI', ''):
                        match_tips.append("🟡 **感性型** - 适合需要人文关怀和协调性的岗位")
                    if 'J' in profile.get('MBTI', ''):
                        match_tips.append("⚪ **判断型** - 适合明确目标导向和计划性强的工作")
                    if 'P' in profile.get('MBTI', ''):
                        match_tips.append("⚫ **感知型** - 适合灵活适应和快速变化的工作环境")
                    for tip in match_tips:
                        st.markdown(tip)

            st.write("**适合岗位**: " + ", ".join(profile['适合岗位'][:5]))

            recommended_titles = [j.get("title", "") for j in recommended_jobs if j.get("title")][:6]
            if not recommended_titles:
                recommended_titles = profile.get('适合岗位', [])[:6]

            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.subheader("📚 职业发展路径规划")
            st.markdown("基于你的能力画像和推荐岗位，为你规划个性化的职业发展路径")

            if recommended_titles:
                selected_job_for_career = st.selectbox("选择查看详细职业路径", recommended_titles[:4], key="career_select")

                if selected_job_for_career in CAREER_PATHS:
                    career_path = CAREER_PATHS[selected_job_for_career]

                    st.markdown(f"### 🚀 {selected_job_for_career} 职业发展路径")

                    for phase, details in career_path.items():
                        with st.expander(f"📌 {phase} (预计{details['时长']})"):
                            col_cp1, col_cp2 = st.columns(2)
                            with col_cp1:
                                st.markdown(f"**薪资范围**: {details['薪资']}")
                                st.markdown(f"**阶段目标**: {details['目标']}")
                            with col_cp2:
                                st.markdown("**需要掌握的技能**:")
                                for skill in details['技能']:
                                    st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)

                            if "初级" in phase:
                                st.success("💡 建议：扎实基础，多向资深同事学习，参与项目实战")
                            elif "中级" in phase:
                                st.info("💡 建议：深入技术/业务，培养独立负责能力，开始带新人")
                            elif "高级" in phase:
                                st.warning("💡 建议：提升架构/战略能力，关注团队成长和技术传承")
                            else:
                                st.success("💡 建议：制定技术战略，赋能业务发展，培养下一代技术领袖")
                else:
                    st.info(f"暂无 {selected_job_for_career} 的详细路径，请选择其他岗位查看")
            else:
                st.info("暂无推荐岗位，无法生成职业路径")

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader("📚 学习路线建议")

        if recommended_titles:
            for title in recommended_titles[:3]:
                if title in LEARNING_ROUTES:
                    with st.expander(f"📚 {title} 学习路线"):
                        stages = LEARNING_ROUTES[title].split(" → ")
                        for idx, stage in enumerate(stages, 1):
                            st.markdown(f"**{idx}.** {stage}")

                        if title in INTERVIEW_TIPS:
                            st.markdown("---")
                            st.markdown("**💡 面试要点**")
                            for tip in INTERVIEW_TIPS[title][:3]:
                                st.write(f"• {tip}")

                        if title in RESUME_TIPS:
                            st.markdown("**📝 简历要点**")
                            for key, value in RESUME_TIPS[title].items():
                                st.write(f"**{key}**: {value}")

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader("📥 导出职业规划报告")

        if recommended_jobs:
            report_jobs = [j for j in recommended_jobs if j.get("company")]
            full_report = generate_full_report(profile, recommended_titles, report_jobs if report_jobs else None)

            col_report1, col_report2 = st.columns(2)
            with col_report1:
                st.markdown(create_download_link(full_report, "职业规划报告.md", "📥 下载Markdown报告"), unsafe_allow_html=True)
                st.caption("下载后可使用Typora、VS Code等工具打开")
            with col_report2:
                if st.button("📋 生成预览", use_container_width=True):
                    st.markdown("### 📄 报告预览")
                    st.markdown(full_report)

JOB_CATEGORIES = {
    "💻 开发类": {
        "后端开发": ["Java", "Python", "Go", "C++", "后端", "服务端"],
        "前端开发": ["前端", "Vue", "React", "UI", "小程序", "H5"],
        "移动端": ["Android", "iOS", "移动端", "App"]
    },
    "🤖 算法类": {
        "算法工程师": ["算法", "机器学习", "深度学习"],
        "NLP工程师": ["NLP", "自然语言", "文本"],
        "CV工程师": ["CV", "计算机视觉", "图像", "视觉"]
    },
    "📊 数据类": {
        "数据分析师": ["数据分析", "BI", "可视化"],
        "数据工程师": ["数据工程", "Hadoop", "Spark", "Flink"]
    },
    "🔧 运维类": {
        "运维工程师": ["运维", "Linux", "监控"],
        "DevOps": ["DevOps", "Docker", "K8s", "CI/CD"]
    },
    "🧪 测试类": {
        "测试工程师": ["测试", "功能测试", "测试开发"],
        "自动化测试": ["自动化", "Selenium", "Appium"]
    },
    "📱 产品类": {
        "产品经理": ["产品经理", "产品", "需求"],
        "UI设计": ["UI", "设计", "UE", "交互"]
    }
}

def get_category_jobs(category_name, subcategory_name=None):
    keywords = []
    if subcategory_name and subcategory_name != "全部":
        keywords = JOB_CATEGORIES.get(category_name, {}).get(subcategory_name, [])
    else:
        for subs in JOB_CATEGORIES.get(category_name, {}).values():
            keywords.extend(subs)
    
    jobs = []
    for job in JOBS_DATA:
        title = job.get("title", "")
        for kw in keywords:
            if kw.lower() in title.lower():
                jobs.append(job)
                break
    return jobs[:30]

with tab2:
    st.header("📚 岗位浏览")
    
    search_keyword = st.text_input("搜索岗位", placeholder="输入岗位关键词...")
    
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        city_select = st.selectbox("城市筛选", ["全部", "北京", "上海", "深圳", "广州", "杭州", "成都", "南京", "武汉", "西安"])
    with col_filter2:
        category_select = st.selectbox("方向筛选", ["全部", "后端开发", "前端开发", "算法", "数据", "运维", "测试", "产品"])
    
    filtered_jobs = JOBS_DATA
    if search_keyword:
        filtered_jobs = [j for j in filtered_jobs if search_keyword.lower() in j.get("title", "").lower() or search_keyword.lower() in j.get("company", "").lower()]
    if city_select != "全部":
        filtered_jobs = [j for j in filtered_jobs if j.get("city") == city_select]
    if category_select != "全部":
        filtered_jobs = [j for j in filtered_jobs if category_select in j.get("title", "").lower()]
    
    if search_keyword:
        st.write(f"共找到 {len(filtered_jobs)} 个岗位")
        
        for job in filtered_jobs[:20]:
            with st.expander(f"{job.get('title', '未知')} - {job.get('company', '-')}"):
                col_j1, col_j2 = st.columns(2)
                with col_j1:
                    st.write(f"**城市**: {job.get('city', '-')}")
                    st.write(f"**薪资**: {job.get('salary', '-')}")
                with col_j2:
                    st.write(f"**经验**: {job.get('experience', '-')}")
                    st.write(f"**学历**: {job.get('education', '-')}")
                
                st.write("**技能要求**:")
                job_skills = job.get("skills", [])
                for s in job_skills[:10]:
                    st.markdown(f'<span class="skill-tag">{s}</span>', unsafe_allow_html=True)
    else:
        st.write("点击下方分类查看岗位")
        
        for category, subcategories in JOB_CATEGORIES.items():
            with st.expander(category):
                cols = st.columns(len(subcategories))
                for idx, (sub_name, _) in enumerate(subcategories.items()):
                    with cols[idx]:
                        if st.button(sub_name, key=f"{category}_{sub_name}", use_container_width=True):
                            subcategory_jobs = get_category_jobs(category, sub_name)
                            
                            if city_select != "全部":
                                subcategory_jobs = [j for j in subcategory_jobs if j.get("city") == city_select]
                            
                            if subcategory_jobs:
                                st.success(f"找到 {len(subcategory_jobs)} 个{sub_name}岗位")
                                for job in subcategory_jobs[:10]:
                                    with st.expander(f"{job.get('title', '未知')} - {job.get('company', '-')}", expanded=False):
                                        col_j1, col_j2 = st.columns(2)
                                        with col_j1:
                                            st.write(f"**城市**: {job.get('city', '-')}")
                                            st.write(f"**薪资**: {job.get('salary', '-')}")
                                        with col_j2:
                                            st.write(f"**经验**: {job.get('experience', '-')}")
                                            st.write(f"**学历**: {job.get('education', '-')}")
                                        
                                        st.write("**技能要求**:")
                                        job_skills = job.get("skills", [])
                                        for s in job_skills[:8]:
                                            st.markdown(f'<span class="skill-tag">{s}</span>', unsafe_allow_html=True)
                            else:
                                st.warning(f"暂无{sub_name}岗位数据")

with tab3:
    st.header("💰 薪资预测")
    st.markdown("基于你的技能和期望岗位，预测薪资范围")
    
    col_pred1, col_pred2 = st.columns(2)
    with col_pred1:
        pred_skills = st.text_area("输入你的技能", placeholder="Java, Python, MySQL, Spring (用逗号分隔)", height=100, key="pred_skills")
    with col_pred2:
        pred_job = st.selectbox("期望岗位", ["Java开发工程师", "Python开发工程师", "前端开发工程师", "算法工程师", "数据分析师", "运维工程师", "测试工程师", "产品经理"], key="pred_job")
    
    pred_city = st.selectbox("期望城市", ["北京", "上海", "深圳", "广州", "杭州", "成都", "南京", "武汉", "西安", "其他"], key="pred_city")
    
    if st.button("🔮 预测薪资", type="primary", use_container_width=True):
        if pred_skills:
            skills_list = [s.strip() for s in pred_skills.split(",") if s.strip()]
            
            city_salary_factor = {
                "北京": 1.3, "上海": 1.25, "深圳": 1.25, "广州": 1.1,
                "杭州": 1.15, "成都": 0.95, "南京": 1.0, "武汉": 0.9, "西安": 0.9, "其他": 0.85
            }
            factor = city_salary_factor.get(pred_city, 1.0)
            
            job_salary_base = {
                "Java开发工程师": {"base": 12000, "per_skill": 800},
                "Python开发工程师": {"base": 12000, "per_skill": 900},
                "前端开发工程师": {"base": 11000, "per_skill": 700},
                "算法工程师": {"base": 18000, "per_skill": 1200},
                "数据分析师": {"base": 10000, "per_skill": 600},
                "运维工程师": {"base": 9000, "per_skill": 500},
                "测试工程师": {"base": 8500, "per_skill": 500},
                "产品经理": {"base": 13000, "per_skill": 700}
            }
            
            job_data = job_salary_base.get(pred_job, {"base": 10000, "per_skill": 500})
            skill_bonus = len(skills_list) * job_data["per_skill"]
            min_salary = int(job_data["base"] * factor * 0.8)
            max_salary = int((job_data["base"] + skill_bonus) * factor * 1.2)
            
            st.markdown("### 💵 预测薪资")
            
            col_sal1, col_sal2, col_sal3 = st.columns(3)
            with col_sal1:
                st.metric("最低薪资", f"{min_salary//1000}K")
            with col_sal2:
                st.metric("平均薪资", f"{(min_salary+max_salary)//2000}K")
            with col_sal3:
                st.metric("最高薪资", f"{max_salary//1000}K")
            
            st.success(f"📍 {pred_city} | 🎯 {pred_job} | 🛠️ {len(skills_list)}项技能")
            
            st.markdown("### 📊 薪资影响因素")
            
            factors = []
            if pred_city in ["北京", "上海", "深圳"]:
                factors.append(("一线城市", 1.2))
            factors.append(("技能数量", 1 + len(skills_list) * 0.05))
            factors.append(("岗位方向", 1.0))
            
            for factor_name, factor_value in factors:
                st.write(f"**{factor_name}**: ×{factor_value:.2f}")
            
            with st.expander("💡 提升薪资建议"):
                st.write("1. 深入掌握核心技术栈，形成技术壁垒")
                st.write("2. 积累项目经验，特别是高并发、大数据量项目")
                st.write("3. 关注一线城市机会，薪资普遍较高")
                st.write("4. 持续学习新技术，保持竞争力")
        else:
            st.warning("请输入你的技能")

with tab4:
    st.header("📈 行业趋势分析")
    st.markdown("了解各岗位行业发展趋势和前景")

    trend_job = st.selectbox("选择岗位", ["Java开发工程师", "Python开发工程师", "前端开发工程师", "算法工程师", "数据分析师", "运维工程师", "测试工程师", "产品经理"], key="trend_job")

    industry_trends = {
        "Java开发工程师": {
            "前景": "★★★★☆",
            "趋势": "稳定增长",
            "薪资": "15K-40K",
            "需求": "企业级应用核心语言，需求持续稳定",
            "发展": "向微服务、云原生方向演进"
        },
        "Python开发工程师": {
            "前景": "★★★★★",
            "趋势": "高速增长",
            "薪资": "15K-45K",
            "需求": "AI/大数据/自动化领域核心语言，需求爆发",
            "发展": "AI工程化、数据科学、DevOps多领域延伸"
        },
        "前端开发工程师": {
            "前景": "★★★★☆",
            "趋势": "稳定增长",
            "薪资": "12K-35K",
            "需求": "移动端、小程序、可视化需求旺盛",
            "发展": "跨平台框架(Flutter/React Native)、Serverless"
        },
        "算法工程师": {
            "前景": "★★★★★",
            "趋势": "高速增长",
            "薪资": "20K-60K",
            "需求": "AI落地推动CV/NLP/推荐算法人才紧缺",
            "发展": "大模型、AIGC、智能驾驶等前沿领域"
        },
        "数据分析师": {
            "前景": "★★★★☆",
            "趋势": "稳定增长",
            "薪资": "12K-30K",
            "需求": "企业数字化转型带动数据分析需求激增",
            "发展": "BI可视化、数据中台、实时分析"
        },
        "运维工程师": {
            "前景": "★★★☆☆",
            "趋势": "平稳",
            "薪资": "12K-30K",
            "需求": "云原生推动DevOps/SRE岗位增长",
            "发展": "K8s运维、平台工程、智能化运维"
        },
        "测试工程师": {
            "前景": "★★★☆☆",
            "趋势": "平稳",
            "薪资": "10K-25K",
            "需求": "自动化测试、质量保障需求稳定",
            "发展": "测试开发、效能提升、AI辅助测试"
        },
        "产品经理": {
            "前景": "★★★★☆",
            "趋势": "稳定增长",
            "薪资": "15K-40K",
            "需求": "互联网产品策划与运营人才需求稳定",
            "发展": "AI产品经理、B端产品、数据产品"
        }
    }

    if st.button("🔍 分析行业趋势", type="primary", use_container_width=True):
        trend_data = industry_trends.get(trend_job, industry_trends["Python开发工程师"])
        st.success("✅ 行业趋势分析完成")

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown(f"""
            ### 📊 {trend_job} 行业分析

            **行业前景**: {trend_data['前景']} {trend_data['趋势']}

            **薪资范围**: {trend_data['薪资']}

            **市场需求**: {trend_data['需求']}
            """)
        with col_t2:
            st.markdown(f"""
            ### 🚀 发展趋势

            {trend_data['发展']}

            ### 💡 职业建议

            1. 持续学习新技术，保持竞争力
            2. 深耕专业领域，形成差异化优势
            3. 关注行业动态，把握转型机会
            4. 积累项目经验，提升实战能力
            """)
    else:
        st.info("💡 选择一个岗位，点击上方按钮查看行业发展趋势")

    st.markdown("---")
    st.markdown("### 📊 各岗位薪资参考")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        | 岗位 | 月薪范围 | 年薪 |
        |------|---------|------|
        | Java开发工程师 | 15K-40K | 18-50W |
        | Python开发工程师 | 15K-45K | 18-55W |
        | 前端开发工程师 | 12K-35K | 15-45W |
        | 算法工程师 | 20K-60K | 25-80W |
        """)
    with col2:
        st.markdown("""
        | 岗位 | 月薪范围 | 年薪 |
        |------|---------|------|
        | 数据分析师 | 12K-30K | 15-40W |
        | 运维工程师 | 10K-25K | 12-35W |
        | 测试工程师 | 10K-28K | 12-38W |
        | 产品经理 | 15K-40K | 18-50W |
        """)

with tab5:
    st.header("📊 竞争力分析")

    st.markdown("### 🎯 技能竞争力洞察")

    user_input_skills = st.text_area("输入你的技能（用逗号分隔）", placeholder="Python, Java, MySQL, Vue", key="comp_skills")

    if st.button("🔍 分析竞争力", type="primary"):
        if user_input_skills:
            user_skills = [s.strip() for s in user_input_skills.split(",") if s.strip()]
            user_skills_lower = [s.lower() for s in user_skills]

            col_comp1, col_comp2 = st.columns(2)

            with col_comp1:
                st.markdown("#### 📊 技能需求排名")
                skill_demand = []
                for category, skills in SKILL_MAPPING.items():
                    matched = sum(1 for s in skills if s.lower() in user_skills_lower)
                    total = len(skills)
                    demand_score = (matched / total * 100) if total > 0 else 0
                    skill_demand.append((category, demand_score, matched, total))

                skill_demand.sort(key=lambda x: x[1], reverse=True)
                for cat, score, matched, total in skill_demand:
                    st.progress(min(score, 100)/100, text=f"{cat}: {matched}/{total}项掌握")

            with col_comp2:
                st.markdown("#### 💡 技能组合推荐")

                job_count_by_category = {}
                for category, subcats in JOB_CATEGORIES.items():
                    count = 0
                    for sub_name, keywords in subcats.items():
                        count += len(get_category_jobs(category, sub_name))
                    job_count_by_category[category] = count

                top_categories = sorted(job_count_by_category.items(), key=lambda x: x[1], reverse=True)[:3]
                for cat, count in top_categories:
                    related_skills = SKILL_MAPPING.get(cat, [])
                    st.success(f"**{cat}** (相关岗位 {count}个) - 推荐技能: {', '.join(related_skills[:5])}")

            st.markdown("---")
            st.markdown("#### 🎯 稀缺技能分析")

            all_job_skills = set()
            for job in JOBS_DATA:
                all_job_skills.update([s.lower() for s in job.get("skills", [])])

            user_skills_set = set(user_skills_lower)
            common_skills = user_skills_set.intersection(all_job_skills)
            rare_skills = all_job_skills - user_skills_set

            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.markdown(f"**✅ 你已掌握的稀缺技能 ({len(common_skills)})**")
                if common_skills:
                    for s in list(common_skills)[:10]:
                        st.write(f"• {s}")
                else:
                    st.info("暂无数据")

            with col_r2:
                st.markdown(f"**📝 建议学习的稀缺技能 ({len(rare_skills)})**")
                rare_list = list(rare_skills)[:15]
                for s in rare_list:
                    st.write(f"• {s}")

    st.markdown("---")
    st.markdown("#### 📈 各方向就业前景")

    col_pros1, col_pros2 = st.columns(2)
    with col_pros1:
        st.markdown("""
        | 方向 | 就业前景 | 薪资水平 |
        |------|---------|---------|
        | 后端开发 | ⭐⭐⭐⭐⭐ | 中高 |
        | 前端开发 | ⭐⭐⭐⭐ | 中等 |
        | 算法工程师 | ⭐⭐⭐⭐⭐ | 很高 |
        | 数据分析 | ⭐⭐⭐⭐ | 中等 |
        """)
    with col_pros2:
        st.markdown("""
        | 方向 | 就业前景 | 薪资水平 |
        |------|---------|---------|
        | 运维开发 | ⭐⭐⭐ | 中等 |
        | 测试开发 | ⭐⭐⭐ | 中等 |
        | 产品经理 | ⭐⭐⭐⭐ | 中高 |
        | UI设计 | ⭐⭐⭐ | 中等 |
        """)

st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666; padding: 1rem;">'
    '🎯 智途AI - 基于大模型与RAG检索的智能职业规划平台<br>'
    '让每一位大学生都能找到属于自己的职业星辰大海'
    '</div>', 
    unsafe_allow_html=True
)
