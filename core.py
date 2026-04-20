# -*- coding: utf-8 -*-
"""
智途AI - 核心算法模块
整合 RAG检索 + MBTI分析 + 人岗匹配算法
"""

import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_FILE = os.path.join(BASE_DIR, "data", "jobs_with_skills.json")

KNOWLEDGE_FILE = os.path.join(BASE_DIR, "data", "jobs_with_skills.json")

# ============== MBTI 分析模块 ==============

MBTI_ANALYSIS = {
    "INTJ": {"name": "建筑师", "description": "独立思考者，善于分析和规划，具有战略眼光",
             "strengths": ["分析能力强", "独立工作", "战略思维", "追求完美"],
             "suitable_jobs": ["算法工程师", "数据分析师", "架构师", "技术总监"]},
    "INTP": {"name": "逻辑学家", "description": "喜欢探索理论和原理，善于解决复杂问题",
             "strengths": ["逻辑思维", "创新能力", "分析能力", "理论探索"],
             "suitable_jobs": ["算法工程师", "数据科学家", "研究员", "安全工程师"]},
    "ENTJ": {"name": "指挥官", "description": "天生领导者，善于决策和激励团队",
             "strengths": ["领导能力", "决策能力", "战略规划", "执行力"],
             "suitable_jobs": ["技术总监", "CTO", "产品经理", "项目经理"]},
    "ENTP": {"name": "辩论家", "description": "喜欢挑战和创新，善于发现新机会",
             "strengths": ["创新能力", "适应能力", "沟通能力", "机会发现"],
             "suitable_jobs": ["产品经理", "前端开发", "技术专家", "创业者"]},
    "INFJ": {"name": "提倡者", "description": "有理想有追求，注重意义和价值",
             "strengths": ["洞察力", "创造力", "同理心", "理想主义"],
             "suitable_jobs": ["产品经理", "UI设计师", "运营", "心理咨询师"]},
    "INFP": {"name": "调停者", "description": "理想主义，善于创作和调解",
             "strengths": ["创造力", "同理心", "适应能力", "语言能力"],
             "suitable_jobs": ["前端开发", "UI设计师", "内容运营", "教师"]},
    "ENFJ": {"name": "主人公", "description": "天生领导者，善于激励他人",
             "strengths": ["领导能力", "沟通能力", "同理心", "感染力"],
             "suitable_jobs": ["产品经理", "运营经理", "团队负责人", "培训师"]},
    "ENFP": {"name": "竞选者", "description": "热情创意，善于沟通和激励",
             "strengths": ["热情", "创造力", "沟通能力", "适应能力"],
             "suitable_jobs": ["产品运营", "前端开发", "市场营销", "创业者"]},
    "ISTJ": {"name": "物流师", "description": "可靠务实，注重细节和责任",
             "strengths": ["责任感", "可靠性", "细节导向", "执行力"],
             "suitable_jobs": ["后端开发", "测试工程师", "运维工程师", "数据工程师"]},
    "ISFJ": {"name": "守卫者", "description": "细心负责，善于照顾他人",
             "strengths": ["责任感", "细心", "奉献精神", "务实"],
             "suitable_jobs": ["测试工程师", "运维工程师", "技术支持", "运维开发"]},
    "ESTJ": {"name": "总经理", "description": "组织能力强，善于管理",
             "strengths": ["组织能力", "管理能力", "执行力", "责任感"],
             "suitable_jobs": ["技术经理", "测试主管", "运维主管", "项目经理"]},
    "ESFJ": {"name": "执政官", "description": "关注他人，善于协作",
             "strengths": ["协作能力", "责任感", "细心", "社交能力"],
             "suitable_jobs": ["产品运营", "客户运营", "团队协调", "项目经理"]},
    "ISTP": {"name": "鉴赏家", "description": "务实灵活，善于动手操作",
             "strengths": ["动手能力", "分析能力", "适应能力", "实际问题解决"],
             "suitable_jobs": ["后端开发", "嵌入式开发", "游戏开发", "运维工程师"]},
    "ISFP": {"name": "探险家", "description": "艺术气质，善于发现美",
             "strengths": ["艺术感", "创造力", "观察力", "适应能力"],
             "suitable_jobs": ["UI设计师", "前端开发", "视觉设计师", "游戏美术"]},
    "ESTP": {"name": "企业家", "description": "灵活务实，善于把握机会",
             "strengths": ["适应能力", "执行力", "机会把握", "人际交往"],
             "suitable_jobs": ["前端开发", "产品经理", "技术销售", "创业者"]},
    "ESFP": {"name": "表演者", "description": "热情开朗，善于表现",
             "strengths": ["表现力", "社交能力", "热情", "感染力"],
             "suitable_jobs": ["前端开发", "UI设计", "产品运营", "市场营销"]}
}

MBTI_CAREER_MATCH = {
    "INTJ": {"适合度": 0.9, "匹配理由": "独立思考、追求完美，适合技术专精"},
    "INTP": {"适合度": 0.95, "匹配理由": "逻辑思维、理论探索，适合算法研究"},
    "ENTJ": {"适合度": 0.7, "匹配理由": "领导力强，适合管理岗位"},
    "ENTP": {"适合度": 0.75, "匹配理由": "创新精神，适合产品创新"},
    "INFJ": {"适合度": 0.7, "匹配理由": "理想主义，适合产品规划"},
    "INFP": {"适合度": 0.8, "匹配理由": "创造力强，适合创意设计"},
    "ENFJ": {"适合度": 0.65, "匹配理由": "领导力强，适合团队管理"},
    "ENFP": {"适合度": 0.7, "匹配理由": "热情创意，适合运营创新"},
    "ISTJ": {"适合度": 0.9, "匹配理由": "务实可靠，适合后端开发"},
    "ISFJ": {"适合度": 0.85, "匹配理由": "细心负责，适合测试运维"},
    "ESTJ": {"适合度": 0.6, "匹配理由": "组织管理，适合技术管理"},
    "ESFJ": {"适合度": 0.65, "匹配理由": "协作能力强，适合运营协调"},
    "ISTP": {"适合度": 0.85, "匹配理由": "动手能力强，适合嵌入式开发"},
    "ISFP": {"适合度": 0.8, "匹配理由": "艺术美感，适合UI设计"},
    "ESTP": {"适合度": 0.7, "匹配理由": "灵活务实，适合前端开发"},
    "ESFP": {"适合度": 0.75, "匹配理由": "表现力强，适合前端展示"}
}


def analyze_mbti_career(mbti_type):
    """分析MBTI性格类型与职业的匹配度"""
    if not mbti_type:
        return {"type": "未知", "name": "未测试", "description": "未提供MBTI性格类型",
                "strengths": [], "suitable_jobs": ["数据分析师", "后端开发", "前端开发", "产品经理"],
                "career_advice": "完成MBTI测试可获得更精准的岗位推荐", "mbti_match_score": 0.5}

    mbti_upper = mbti_type.upper()
    if mbti_upper not in MBTI_ANALYSIS:
        return {"type": "未知", "name": "无法识别", "description": f"无法识别MBTI类型: {mbti_type}",
                "strengths": [], "suitable_jobs": [], "career_advice": "请输入有效的MBTI类型", "mbti_match_score": 0}

    analysis = MBTI_ANALYSIS[mbti_upper].copy()
    analysis["type"] = f"{mbti_upper} - {analysis['name']}"
    analysis["mbti_match_score"] = MBTI_CAREER_MATCH.get(mbti_upper, {}).get("适合度", 0.7)
    return analysis


def get_mbti_recommendation_for_job(mbti_type, job_title):
    """根据MBTI类型推荐适合的岗位"""
    analysis = analyze_mbti_career(mbti_type)
    return {"recommended_jobs": analysis.get("suitable_jobs", []),
            "match_score": analysis.get("mbti_match_score", 0.7),
            "advice": analysis.get("career_advice", "")}


# ============== 语义RAG模块 ==============

EMBEDDING_MODEL = None
RERANKER_MODEL = None


def get_embedding_model():
    """获取Embedding模型"""
    global EMBEDDING_MODEL
    if EMBEDDING_MODEL is not None:
        return EMBEDDING_MODEL

    try:
        from sentence_transformers import SentenceTransformer
        model_path = os.path.join(BASE_DIR, "models", "bge-small-zh")
        if os.path.exists(model_path):
            EMBEDDING_MODEL = SentenceTransformer(model_path)
            print(f"Embedding模型已加载: {model_path}")
        else:
            print("本地模型不存在，请先下载模型")
            return None
        return EMBEDDING_MODEL
    except Exception as e:
        print(f"Embedding模型加载失败: {e}")
        return None


def get_reranker_model():
    """获取Reranker模型"""
    global RERANKER_MODEL
    if RERANKER_MODEL is not None:
        return RERANKER_MODEL

    try:
        from sentence_transformers import CrossEncoder
        reranker_path = os.path.join(BASE_DIR, "models", "bge-reranker")
        if os.path.exists(reranker_path):
            RERANKER_MODEL = CrossEncoder(reranker_path)
            print("Reranker模型已加载: 本地模型")
        else:
            print("Reranker模型本地不存在，跳过Rerank步骤")
            return None
        return RERANKER_MODEL
    except Exception as e:
        print(f"Reranker模型加载失败: {e}")
        return None


class SemanticRAG:
    def __init__(self):
        self.jobs = []
        self.embedding_model = None
        self.job_embeddings = None
        self.reranker_model = None
        self.load_knowledge_base()
        self.load_models()

    def load_knowledge_base(self):
        """加载岗位知识库"""
        if os.path.exists(KNOWLEDGE_FILE):
            with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                self.jobs = json.load(f)
            print(f"知识库已加载: {len(self.jobs)} 条岗位数据")

    def load_models(self):
        """加载模型"""
        self.embedding_model = get_embedding_model()
        self.reranker_model = get_reranker_model()
        if self.embedding_model and self.jobs:
            self.build_index()

    def build_index(self):
        """构建向量索引"""
        if not self.jobs or not self.embedding_model:
            return

        def job_to_text(job):
            parts = []
            if job.get("title"):
                parts.append(job["title"])
            if job.get("skills"):
                parts.extend(job["skills"])
            if job.get("description"):
                parts.append(job["description"][:500])
            if job.get("industry"):
                parts.append(job["industry"])
            return " ".join(parts)

        job_texts = [job_to_text(j) for j in self.jobs]
        print("正在构建Embedding向量...")
        self.job_embeddings = self.embedding_model.encode(job_texts, batch_size=32, show_progress_bar=True)
        print(f"向量索引已构建: {self.job_embeddings.shape}")

    def retrieve(self, query, top_k=10, rerank=True):
        """语义检索"""
        if not self.jobs or not self.embedding_model:
            return []

        query_embedding = self.embedding_model.encode([query])
        similarities = np.dot(self.job_embeddings, query_embedding.T).flatten()
        top_indices = np.argsort(similarities)[-top_k * 3:][::-1]

        candidates = []
        for idx in top_indices:
            job = self.jobs[idx]
            candidates.append({
                "job_id": job.get("job_id"),
                "title": job.get("title"),
                "city": job.get("city"),
                "company": job.get("company"),
                "salary": job.get("salary", ""),
                "skills": job.get("skills", [])[:10],
                "description": job.get("description", "")[:300],
                "similarity": float(similarities[idx])
            })

        if rerank and self.reranker_model and candidates:
            candidates = self.rerank(query, candidates, top_k)

        return candidates[:top_k]

    def rerank(self, query, candidates, top_k=10):
        """使用Reranker重排序"""
        if not self.reranker_model or not candidates:
            return candidates

        pairs = [(query, f"{c['title']} {' '.join(c['skills'])}") for c in candidates]
        scores = self.reranker_model.predict(pairs)

        for i, c in enumerate(candidates):
            c["rerank_score"] = float(scores[i])
            c["final_score"] = c["rerank_score"]

        candidates.sort(key=lambda x: x["rerank_score"], reverse=True)
        return candidates[:top_k]


# ============== RAG Service (TF-IDF fallback) ==============

class RAGService:
    def __init__(self):
        self.jobs = []
        self.vectorizer = None
        self.job_vectors = None
        self.load_knowledge_base()

    def load_knowledge_base(self):
        """加载岗位知识库"""
        if os.path.exists(KNOWLEDGE_FILE):
            with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                self.jobs = json.load(f)
            print(f"知识库已加载: {len(self.jobs)} 条岗位数据")
        self.build_index()

    def build_index(self):
        """构建向量索引"""
        if not self.jobs:
            return

        def job_to_text(job):
            parts = []
            if job.get("title"):
                parts.append(job["title"])
            if job.get("skills"):
                parts.extend(job["skills"])
            if job.get("description"):
                parts.append(job["description"][:500])
            if job.get("industry"):
                parts.append(job["industry"])
            return " ".join(parts)

        job_texts = [job_to_text(j) for j in self.jobs]
        self.vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2), sublinear_tf=True)
        self.job_vectors = self.vectorizer.fit_transform(job_texts)
        print("TF-IDF向量索引已构建")

    def retrieve(self, query, top_k=10):
        """检索相关岗位"""
        if not self.jobs:
            return []

        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.job_vectors)[0]
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            job = self.jobs[idx]
            results.append({
                "job_id": job.get("job_id"),
                "title": job.get("title"),
                "city": job.get("city"),
                "company": job.get("company"),
                "salary": f"{job.get('salary_min', '')}-{job.get('salary_max', '')}",
                "skills": job.get("skills", [])[:10],
                "description": job.get("description", "")[:300],
                "similarity": float(similarities[idx])
            })
        return results


# ============== 智能匹配器 ==============

class RAGMatcher:
    def __init__(self):
        self.semantic_rag = None
        self.rag = None
        self._init_services()

    def _init_services(self):
        """初始化服务"""
        print("=== 智能匹配服务初始化 ===")
        try:
            self.semantic_rag = SemanticRAG()
            print("✓ 语义RAG检索: 可用 (Embedding + Reranker)")
        except Exception as e:
            print(f"✗ 语义RAG检索: 不可用 ({e})")
            try:
                self.rag = RAGService()
                print("✓ RAG检索: 可用 (TF-IDF)")
            except Exception as e2:
                print(f"✗ RAG检索: 不可用 ({e2})")
        print("===========================")

    def search(self, user_skills, top_k=10):
        """搜索匹配的岗位"""
        if not user_skills:
            return []

        query = " ".join(user_skills) if isinstance(user_skills, list) else str(user_skills)

        if self.semantic_rag and self.semantic_rag.embedding_model:
            results = self.semantic_rag.retrieve(query, top_k=top_k, rerank=True)
        elif self.rag:
            results = self.rag.retrieve(query, top_k=top_k * 3)
        else:
            return []

        for r in results:
            r["final_score"] = r.get("similarity", 0) * 100

        return results[:top_k]

    def smart_match(self, user_skills, city_filter=None, salary_filter=None, use_llm=True, top_k=10,
                    user_education=None, user_experience=None):
        """
        智能匹配

        Returns:
            匹配结果，每条包含：
            - title: 岗位名称
            - company: 公司
            - city: 城市
            - salary: 薪资
            - skills: 技能列表
            - rag_score: RAG评分(0-100)
            - match_score: 匹配度(0-100)
        """
        results = self.search(user_skills, top_k=top_k * 3)

        if city_filter:
            results = [r for r in results if r.get("city") == city_filter]

        normalized_results = []
        for r in results[:top_k]:
            final_score = r.get("final_score", 0)
            rag_score = min(final_score, 100)
            normalized_results.append({
                "title": r.get("title", ""),
                "company": r.get("company", ""),
                "city": r.get("city", ""),
                "salary": r.get("salary", ""),
                "skills": r.get("skills", [])[:10],
                "description": r.get("description", "")[:200] if r.get("description") else "",
                "rag_score": rag_score,
                "match_score": rag_score,
            })

        return normalized_results

    def generate_career_report(self, user_skills):
        """生成职业规划报告"""
        if not user_skills:
            return "请输入您的技能信息"

        results = self.search(user_skills, top_k=5)

        if not results:
            return "未能找到匹配的岗位"

        report = "# 🎯 职业规划建议\n\n"
        report += f"根据您掌握的技能: {', '.join(user_skills) if isinstance(user_skills, list) else user_skills}\n\n"
        report += "## 推荐岗位\n\n"

        for i, job in enumerate(results, 1):
            score = job.get("final_score", 0)
            report += f"### {i}. {job.get('title', '-')}\n"
            report += f"- 公司: {job.get('company', '-')}\n"
            report += f"- 城市: {job.get('city', '-')}\n"
            report += f"- 薪资: {job.get('salary', '-')}\n"
            report += f"- 匹配度: {score:.0f}%\n"
            report += f"- 技能要求: {', '.join(job.get('skills', [])[:5])}\n\n"

        return report


# ============== 四维度匹配 ==============

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


def calculate_skill_scores(skills_text, major=""):
    """计算技能得分"""
    skills_list = [s.strip() for s in skills_text.split(",") if s.strip()] if isinstance(skills_text, str) else skills_text

    skill_scores = {}
    for category, category_skills in SKILL_MAPPING.items():
        matched = sum(1 for s in skills_list if any(cs.lower() in s.lower() or s.lower() in cs.lower() for cs in category_skills))
        skill_scores[category] = min(matched * 25, 100)

    if not skill_scores or max(skill_scores.values()) == 0:
        for category in SKILL_MAPPING.keys():
            skill_scores[category] = 50

    return skill_scores


def generate_ability_profile(education, major, skills, experience, personality_type="", llm_analysis=None):
    """生成能力画像"""
    skill_scores = calculate_skill_scores(skills, major)

    personality_result = analyze_mbti_career(personality_type)

    top_category = max(skill_scores, key=skill_scores.get) if skill_scores else "编程开发"
    combined_jobs = personality_result.get("suitable_jobs", ["后端开发", "前端开发", "数据分析师"])[:5]

    profile = {
        "学历": education,
        "专业": major,
        "技能": skills,
        "技能得分": skill_scores,
        "综合评分": sum(skill_scores.values()) / len(skill_scores) if skill_scores else 0,
        "完整度": min(len([s for s in skill_scores.values() if s > 0]) / len(SKILL_MAPPING) * 100, 100),
        "竞争力": "强" if sum(skill_scores.values()) / len(skill_scores) > 70 else "中" if sum(skill_scores.values()) / len(skill_scores) > 50 else "弱",
        "擅长方向": top_category,
        "适合岗位": combined_jobs,
        "性格分析": personality_result
    }

    return profile


# ============== 工具函数 ==============

def get_personality_result(personality_type):
    """获取性格分析结果"""
    return analyze_mbti_career(personality_type)


def match_jobs_smart(user_skills, top_k=10, city_filter=None, user_education=None, user_experience=None):
    """智能匹配岗位"""
    try:
        matcher = RAGMatcher()
        return matcher.smart_match(user_skills, city_filter=city_filter, top_k=top_k,
                                  user_education=user_education, user_experience=user_experience)
    except Exception as e:
        print(f"匹配失败: {e}")
        return []


def hybrid_match(profile, skills_str, city_filter=None, top_k=10):
    """混合匹配（Demo模式）"""
    demo_jobs = [
        {"title": "Python开发工程师", "company": "字节跳动", "city": "北京", "salary": "25K-40K",
         "skills": ["Python", "Django", "Flask", "MySQL", "Redis"], "description": "负责后端服务开发",
         "rag_score": 85, "match_score": 88},
        {"title": "Java开发工程师", "company": "阿里巴巴", "city": "杭州", "salary": "20K-35K",
         "skills": ["Java", "Spring", "MySQL", "分布式", "微服务"], "description": "企业级应用开发",
         "rag_score": 80, "match_score": 82},
        {"title": "前端开发工程师", "company": "腾讯", "city": "深圳", "salary": "20K-35K",
         "skills": ["Vue", "React", "JavaScript", "CSS", "Node.js"], "description": "移动端Web开发",
         "rag_score": 78, "match_score": 75},
        {"title": "算法工程师", "company": "百度", "city": "北京", "salary": "30K-50K",
         "skills": ["Python", "TensorFlow", "PyTorch", "深度学习", "NLP"], "description": "AI算法研发",
         "rag_score": 82, "match_score": 80},
        {"title": "数据分析师", "company": "美团", "city": "北京", "salary": "18K-30K",
         "skills": ["Python", "SQL", "Pandas", "Tableau", "Excel"], "description": "数据分析与挖掘",
         "rag_score": 76, "match_score": 78},
        {"title": "测试开发工程师", "company": "京东", "city": "北京", "salary": "15K-25K",
         "skills": ["Python", "Selenium", "JMeter", "自动化测试", "CI/CD"], "description": "质量保障",
         "rag_score": 72, "match_score": 70},
    ]

    if city_filter and city_filter != "全部":
        demo_jobs = [j for j in demo_jobs if j.get("city") == city_filter]

    return demo_jobs[:top_k]
