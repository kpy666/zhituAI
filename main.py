# -*- coding: utf-8 -*-
"""
智途AI - AI职业规划智能体
主程序入口
"""

import streamlit as st
import json
import random
import os
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
    :root { --primary-color: #0066CC; --secondary-color: #00A3FF; --accent-color: #FF6B35; }
    .main-title { font-size: 2.5rem !important; font-weight: 700 !important; color: #0066CC !important; text-align: center; }
    .subtitle { font-size: 1.1rem !important; color: #666 !important; text-align: center; margin-bottom: 2rem !important; }
    .skill-tag { display: inline-block; background: #E6F0FF; color: #0066CC; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; margin: 2px; }
    .skill-tag.matched { background: #D1FAE5; color: #059669; }
    .skill-tag.missing { background: #FEE2E2; color: #DC2626; }
    .match-badge { display: inline-block; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600; font-size: 0.9rem; }
    .match-high { background: #D1FAE5; color: #059669; }
    .match-medium { background: #FEF3C7; color: #D97706; }
    .match-low { background: #FEE2E2; color: #DC2626; }
    .stButton > button { border-radius: 8px; font-weight: 500; }
    .info-card { background: white; border-radius: 12px; padding: 1rem; margin-bottom: 0.5rem; border-left: 4px solid #0066CC; }
    .tip-card { background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid #0284c7; }
    .resume-card { background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid #d97706; }
    .section-divider { margin: 1.5rem 0; border-top: 2px dashed #E5E7EB; }
    .career-path { background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; }
    .career-path h4 { color: #0369a1; margin-bottom: 0.5rem; }
    .download-btn { background: linear-gradient(135deg, #0066CC 0%, #00A3FF 100%); color: white !important; padding: 0.75rem 1.5rem; border-radius: 8px; text-decoration: none; display: inline-block; margin-top: 1rem; }
    .stat-card { background: white; border-radius: 12px; padding: 1.5rem; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
    .stat-card .value { font-size: 2rem; font-weight: 700; color: #0066CC; }
    .stat-card .label { color: #666; margin-top: 0.5rem; }
</style>""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎯 智途AI - AI职业规划智能体</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">基于大模型与RAG检索的智能职业规划平台</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 能力评估与职业规划", "📚 岗位浏览", "💰 薪资预测", "📈 行业趋势", "📊 竞争力分析"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from src.core import (
    SKILL_MAPPING, calculate_skill_scores, generate_ability_profile,
    get_personality_result, match_jobs_smart, hybrid_match, analyze_mbti_career
)

USE_RAG = False
rag_matcher = None
USE_LLM = False
llm_service = None

try:
    from src.core import RAGMatcher
    rag_matcher = RAGMatcher()
    USE_RAG = True
    print("RAG匹配器初始化成功")
except Exception as e:
    print(f"RAG匹配器初始化失败: {e}")

def load_jobs():
    with open(os.path.join(BASE_DIR, "data", "jobs_with_skills.json"), "r", encoding="utf-8") as f:
        return json.load(f)

JOBS_DATA = load_jobs()

def create_download_link(content, filename, text):
    b64 = base64.b64encode(content.encode('utf-8')).decode()
    return f'<a href="data:text/markdown;base64,{b64}" download="{filename}" class="download-btn">{text}</a>'

with tab1:
    st.header("📝 填写你的信息")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("姓名", placeholder="请输入姓名")
        education = st.selectbox("学历", ["大专", "本科", "硕士", "博士"], key="edu")
        major = st.text_input("专业", placeholder="如：计算机科学与技术", key="major")
        personality_type = st.selectbox("MBTI性格", ["", "INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
                                                       "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"], key="mbti")

    with col2:
        experience = st.text_area("经历描述", placeholder="请描述你的实习经历、项目经验等", height=100, key="exp")
        skills_input = st.text_area("技能列表", placeholder="Java, Python, MySQL, Spring (用逗号分隔)", height=100, key="skills")

    if st.button("🔍 开始分析", type="primary", use_container_width=True):
        if not skills_input:
            st.warning("请输入您的技能信息")
        else:
            skills_str = skills_input
            skills_list = [s.strip() for s in skills_str.split(",") if s.strip()]

            profile = generate_ability_profile(education, major, skills_str, experience, personality_type)
            recommended_jobs = match_jobs_smart(skills_str, top_k=6)
            if not recommended_jobs:
                recommended_jobs = hybrid_match(profile, skills_str, city_filter=None)

            st.markdown("---")
            st.markdown("### 📊 能力画像")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("综合评分", f"{profile['综合评分']:.1f}")
            with col2:
                st.metric("技能完整度", f"{profile['完整度']:.1f}%")
            with col3:
                st.metric("竞争力指数", f"{profile['竞争力']}")
            with col4:
                st.metric("擅长方向", profile['擅长方向'])

            skill_data = profile.get("技能得分", {})
            if skill_data:
                col_chart1, col_chart2 = st.columns(2)
                with col_chart1:
                    st.write("**技能雷达图**")
                    import pandas as pd
                    df = pd.DataFrame({"技能类别": list(skill_data.keys()), "得分": list(skill_data.values())})
                    st.bar_chart(df.set_index("技能类别")["得分"])

                with col_chart2:
                    st.write("**技能进度**")
                    for cat, score in sorted(skill_data.items(), key=lambda x: x[1], reverse=True):
                        color = "#667eea" if score >= 80 else "#ffa500" if score >= 60 else "#ff6b6b"
                        st.markdown(f'''<div style="margin-bottom: 8px;"><div style="display: flex; justify-content: space-between; margin-bottom: 2px;"><span style="font-size: 13px; color: #333;">{cat}</span><span style="font-size: 13px; color: {color}; font-weight: bold;">{score:.0f}%</span></div><div style="background: #f0f0f0; border-radius: 5px; height: 8px; overflow: hidden;"><div style="background: {color}; width: {score}%; height: 100%; border-radius: 5px;"></div></div></div>''', unsafe_allow_html=True)

            st.write("**适合岗位**: " + ", ".join(profile['适合岗位'][:3]))

            if recommended_jobs:
                st.markdown("### 🎯 推荐岗位一览")
                display_jobs = recommended_jobs[:6]
                cols = st.columns(3)
                for idx, job in enumerate(display_jobs):
                    with cols[idx % 3]:
                        score = job.get("match_score", job.get("rag_score", 0))
                        badge_class = "match-high" if score >= 80 else "match-medium" if score >= 60 else "match-low"
                        st.markdown(f'''<div class="info-card"><h4>{job.get('title', '未知岗位')}</h4><span class="match-badge {badge_class}">匹配度: {score:.0f}%</span><p><b>公司:</b> {job.get('company', '-')}<br/><b>城市:</b> {job.get('city', '-')}<br/><b>薪资:</b> {job.get('salary', '-')}</p><b>技能要求:</b><br/>{" ".join([f"<span class='skill-tag'>{s}</span>" for s in job.get('skills', [])[:5]])}</div>''', unsafe_allow_html=True)

            personality_result = profile.get("性格分析", {})
            if personality_result:
                st.markdown("### 🧠 性格分析")
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    st.markdown(f"**{personality_result.get('type', '未知')}**")
                    st.write(personality_result.get('description', ''))
                    st.write(f"**优势**: {', '.join(personality_result.get('strengths', [])[:4])}")
                with col_p2:
                    st.write(f"**适合方向**: {', '.join(personality_result.get('suitable_jobs', [])[:4])}")
                    st.write(f"**职业建议**: {personality_result.get('career_advice', '')}")

            st.markdown("---")
            st.markdown("### 📋 职业发展路径规划")

            career_paths = {
                "后端开发": ["初级开发工程师 → 中级开发工程师 → 高级开发工程师 → 技术专家/架构师 → 技术总监"],
                "前端开发": ["初级前端工程师 → 中级前端工程师 → 高级前端工程师 → 前端架构师 → 前端负责人"],
                "算法工程师": ["算法工程师 → 高级算法工程师 → 算法专家 → 算法研究员 → AI总监"],
                "数据分析师": ["数据分析师 → 高级分析师 → 数据挖掘工程师 → 数据架构师 → 数据总监"],
                "产品经理": ["产品助理 → 产品经理 → 高级产品经理 → 产品总监 → CPO"],
            }
            main_direction = profile.get("擅长方向", "后端开发")
            path = career_paths.get(main_direction, career_paths["后端开发"])[0]
            st.info(f"🚀 {path}")

            st.markdown("### 📚 个性化技能提升计划")
            priority_skills = [
                ("Python核心语法", "高", "掌握Python基础语法和高级特性"),
                ("Django/Flask框架", "高", "熟悉Web开发框架"),
                ("MySQL数据库", "中", "理解数据库设计与优化"),
                ("Git版本控制", "中", "团队协作必备技能"),
            ]
            for skill_name, priority, suggestion in priority_skills:
                icon = "🔴" if priority == "高" else "🟡"
                st.markdown(f"{icon} **{skill_name}** (优先级{priority}) - {suggestion}")

            if recommended_jobs:
                st.markdown("### 💼 求职准备建议")
                col_w1, col_w2, col_w3 = st.columns(3)
                with col_w1:
                    st.markdown("**简历优化**")
                    st.write("• 突出Python项目经验")
                    st.write("• 量化工作成果")
                    st.write("• 展示技术深度")
                with col_w2:
                    st.markdown("**面试准备**")
                    st.write("• 夯实算法基础")
                    st.write("• 准备系统设计")
                    st.write("• 模拟行为面试")
                with col_w3:
                    st.markdown("**技能补充**")
                    st.write("• 深入学习框架原理")
                    st.write("• 参与开源项目")
                    st.write("• 积累实战经验")

with tab2:
    st.header("📚 岗位浏览")
    city_select = st.selectbox("选择城市", ["全部", "北京", "上海", "深圳", "广州", "杭州", "成都", "南京"])
    category_select = st.selectbox("选择类别", ["全部", "技术开发", "算法", "数据", "产品", "设计", "运维", "测试"])

    JOB_CATEGORIES = {
        "技术开发": {"Java开发": "后端开发", "Python开发": "后端开发", "前端开发": "前端开发", "Go开发": "后端开发"},
        "算法": {"算法工程师": "算法", "机器学习": "算法", "深度学习": "算法"},
        "数据": {"数据分析师": "数据分析", "大数据开发": "大数据", "数据挖掘": "数据分析"},
        "产品": {"产品经理": "产品", "产品运营": "运营"},
        "设计": {"UI设计": "设计", "前端设计": "设计"},
        "运维": {"运维工程师": "运维", "DBA": "运维"},
        "测试": {"测试工程师": "测试", "测试开发": "测试"}
    }

    def get_category_jobs(category, subcategory):
        return [j for j in JOBS_DATA if subcategory in j.get("title", "")][:20]

    if category_select != "全部" and category_select in JOB_CATEGORIES:
        subcats = JOB_CATEGORIES[category_select]
        cols = st.columns(len(subcats))
        for idx, (sub_name, _) in enumerate(subcats.items()):
            with cols[idx]:
                if st.button(sub_name, key=f"cat_{sub_name}", use_container_width=True):
                    jobs = get_category_jobs(category_select, sub_name)
                    if city_select != "全部":
                        jobs = [j for j in jobs if j.get("city") == city_select]
                    if jobs:
                        st.success(f"找到 {len(jobs)} 个{sub_name}岗位")
                        for job in jobs[:10]:
                            with st.expander(f"{job.get('title', '未知')} - {job.get('company', '-')}", expanded=False):
                                col_j1, col_j2 = st.columns(2)
                                with col_j1:
                                    st.write(f"**城市**: {job.get('city', '-')}")
                                    st.write(f"**薪资**: {job.get('salary_min', '-')}K-{job.get('salary_max', '-')}K")
                                with col_j2:
                                    st.write(f"**行业**: {job.get('industry', '-')}")
                                st.write("**技能要求**:")
                                for s in job.get("skills", [])[:8]:
                                    st.markdown(f'<span class="skill-tag">{s}</span>', unsafe_allow_html=True)
                    else:
                        st.warning(f"暂无{sub_name}岗位数据")
    else:
        st.write("点击上方分类查看岗位")

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
            city_salary_factor = {"北京": 1.3, "上海": 1.25, "深圳": 1.25, "广州": 1.1, "杭州": 1.15, "成都": 0.95, "南京": 1.0, "武汉": 0.9, "西安": 0.9, "其他": 0.85}
            factor = city_salary_factor.get(pred_city, 1.0)
            job_salary_base = {
                "Java开发工程师": {"base": 12000, "per_skill": 800}, "Python开发工程师": {"base": 12000, "per_skill": 900},
                "前端开发工程师": {"base": 11000, "per_skill": 700}, "算法工程师": {"base": 18000, "per_skill": 1200},
                "数据分析师": {"base": 10000, "per_skill": 600}, "运维工程师": {"base": 9000, "per_skill": 500},
                "测试工程师": {"base": 8500, "per_skill": 500}, "产品经理": {"base": 13000, "per_skill": 700}
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
            factors = [("一线城市", 1.2)] if pred_city in ["北京", "上海", "深圳"] else []
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
        "Java开发工程师": {"前景": "★★★★☆", "趋势": "稳定增长", "薪资": "15K-40K", "需求": "企业级应用核心语言，需求持续稳定", "发展": "向微服务、云原生方向演进"},
        "Python开发工程师": {"前景": "★★★★★", "趋势": "高速增长", "薪资": "15K-45K", "需求": "AI/大数据/自动化领域核心语言，需求爆发", "发展": "AI工程化、数据科学、DevOps多领域延伸"},
        "前端开发工程师": {"前景": "★★★★☆", "趋势": "稳定增长", "薪资": "12K-35K", "需求": "移动端、小程序、可视化需求旺盛", "发展": "跨平台框架(Flutter/React Native)、Serverless"},
        "算法工程师": {"前景": "★★★★★", "趋势": "高速增长", "薪资": "20K-60K", "需求": "AI落地推动CV/NLP/推荐算法人才紧缺", "发展": "大模型、AIGC、智能驾驶等前沿领域"},
        "数据分析师": {"前景": "★★★★☆", "趋势": "稳定增长", "薪资": "12K-30K", "需求": "企业数字化转型带动数据分析需求激增", "发展": "BI可视化、数据中台、实时分析"},
        "运维工程师": {"前景": "★★★☆☆", "趋势": "平稳", "薪资": "12K-30K", "需求": "云原生推动DevOps/SRE岗位增长", "发展": "K8s运维、平台工程、智能化运维"},
        "测试工程师": {"前景": "★★★☆☆", "趋势": "平稳", "薪资": "10K-25K", "需求": "自动化测试、质量保障需求稳定", "发展": "测试开发、效能提升、AI辅助测试"},
        "产品经理": {"前景": "★★★★☆", "趋势": "稳定增长", "薪资": "15K-40K", "需求": "互联网产品策划与运营人才需求稳定", "发展": "AI产品经理、B端产品、数据产品"}
    }

    if st.button("🔍 分析行业趋势", type="primary", use_container_width=True):
        trend_data = industry_trends.get(trend_job, industry_trends["Python开发工程师"])
        st.success("✅ 行业趋势分析完成")

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown(f"### 📊 {trend_job} 行业分析\n\n**行业前景**: {trend_data['前景']} {trend_data['趋势']}\n\n**薪资范围**: {trend_data['薪资']}\n\n**市场需求**: {trend_data['需求']}")
        with col_t2:
            st.markdown(f"### 🚀 发展趋势\n\n{trend_data['发展']}\n\n### 💡 职业建议\n\n1. 持续学习新技术，保持竞争力\n2. 深耕专业领域，形成差异化优势\n3. 关注行业动态，把握转型机会\n4. 积累项目经验，提升实战能力")
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
        | 数据分析师 | 12K-30K | 15-38W |
        | 运维工程师 | 12K-30K | 15-38W |
        | 测试工程师 | 10K-25K | 12-30W |
        | 产品经理 | 15K-40K | 18-50W |
        """)

with tab5:
    st.header("📊 竞争力分析")
    st.markdown("评估你在目标岗位的竞争力")

    competitor_job = st.selectbox("选择目标岗位", ["Java开发工程师", "Python开发工程师", "前端开发工程师", "算法工程师", "数据分析师", "运维工程师", "测试工程师", "产品经理"], key="comp_job")
    user_skills_comp = st.text_area("你的技能", placeholder="Java, Python, MySQL, Spring, Redis (用逗号分隔)", height=80, key="comp_skills")

    if st.button("📊 分析竞争力", type="primary", use_container_width=True):
        if user_skills_comp:
            skills = [s.strip() for s in user_skills_comp.split(",") if s.strip()]
            job_requirements = {
                "Java开发工程师": ["Java", "Spring", "MySQL", "Redis", "微服务", "Docker"],
                "Python开发工程师": ["Python", "Django", "Flask", "MySQL", "Redis", "API"],
                "前端开发工程师": ["HTML", "CSS", "JavaScript", "Vue", "React", "Webpack"],
                "算法工程师": ["Python", "TensorFlow", "PyTorch", "机器学习", "深度学习", "NLP"],
                "数据分析师": ["Python", "SQL", "Pandas", "Tableau", "Excel", "统计学"],
                "运维工程师": ["Linux", "Docker", "K8s", "Jenkins", "Shell", "监控"],
                "测试工程师": ["Selenium", "JUnit", "Python", "自动化测试", "CI/CD", "测试框架"],
                "产品经理": ["需求分析", "产品设计", "Axure", "PRD", "数据分析", "项目管理"]
            }
            required = job_requirements.get(competitor_job, [])
            matched = [s for s in skills if any(r.lower() in s.lower() or s.lower() in r.lower() for r in required)]
            missing = [r for r in required if not any(r.lower() in s.lower() or s.lower() in r.lower() for s in skills)]

            score = len(matched) / len(required) * 100 if required else 0

            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                st.metric("匹配度", f"{score:.0f}%", delta=f"已匹配{len(matched)}项")
            with col_c2:
                st.metric("已掌握", f"{len(matched)}项", delta="技能")
            with col_c3:
                st.metric("需补充", f"{len(missing)}项", delta="差距")

            st.markdown("### ✅ 已匹配技能")
            for s in matched:
                st.markdown(f'<span class="skill-tag matched">✓ {s}</span>', unsafe_allow_html=True)

            st.markdown("### ❌ 需补充技能")
            for s in missing:
                st.markdown(f'<span class="skill-tag missing">✗ {s}</span>', unsafe_allow_html=True)

            st.markdown("### 💡 提升建议")
            st.write(f"针对 {competitor_job} 岗位，建议优先学习以下技能：")
            for i, s in enumerate(missing[:3], 1):
                st.write(f"{i}. **{s}** - 深入学习并积累项目经验")
        else:
            st.warning("请输入你的技能")

    st.markdown("---")
    st.markdown("### 📈 技术方向趋势")

    col_tr1, col_tr2 = st.columns(2)
    with col_tr1:
        st.markdown("""
        **🔥 热门技术方向**
        - **AI/ML工程师**: 大模型、AIGC、Agent开发
        - **云原生**: K8s、DevOps、平台工程
        - **前端创新**: React Server Components、跨端框架
        """)
    with col_tr2:
        st.markdown("""
        **💎 稳定发展技术**
        - **企业级Java**: 微服务架构、云原生转型
        - **数据工程**: 数据中台、实时分析、湖仓一体
        - **安全测试**: 应用安全、安全运营
        """)
