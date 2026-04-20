# -*- coding: utf-8 -*-
"""
RAG 智能匹配服务
整合向量检索 + 大模型推理 + 技能匹配优化
自动选择最佳方案，无API时自动降级
"""

try:
    from src.rag_service import rag_service, retrieve_jobs, get_context
    RAG_AVAILABLE = True
except:
    RAG_AVAILABLE = False

try:
    from src.semantic_rag import semantic_rag as semantic_rag_service
    SEMANTIC_RAG_AVAILABLE = True
except:
    SEMANTIC_RAG_AVAILABLE = False

try:
    from src.llm_service import llm_service
    LLM_AVAILABLE = True
except:
    LLM_AVAILABLE = False

try:
    from src.smart_matcher import matcher as tfidf_matcher
    TFIDF_AVAILABLE = True
except:
    TFIDF_AVAILABLE = False

try:
    from src.skill_matcher import calculate_skill_similarity, expand_skills, infer_job_category, filter_by_category
    SKILL_MATCH_AVAILABLE = True
except:
    SKILL_MATCH_AVAILABLE = False

try:
    from src.hard_filter import hard_filter, get_filter_stats
    HARD_FILTER_AVAILABLE = True
except:
    HARD_FILTER_AVAILABLE = False


class RAGMatcher:
    def __init__(self):
        self.rag = rag_service if RAG_AVAILABLE else None
        self.semantic_rag = semantic_rag_service if SEMANTIC_RAG_AVAILABLE else None
        self.llm = llm_service if LLM_AVAILABLE else None
        self.tfidf = tfidf_matcher if TFIDF_AVAILABLE else None
        self.use_llm = False
        self.use_semantic = False
        self.use_hard_filter = HARD_FILTER_AVAILABLE
        
        self._check_available()
    
    def _check_available(self):
        """检查可用方案"""
        print("=== 智能匹配服务初始化 ===")
        
        if self.llm:
            print("✓ 大模型服务: 可用 (Few-shot + CoT)")
            self.use_llm = True
        else:
            print("✗ 大模型服务: 不可用 (需要API Key)")
        
        if self.semantic_rag:
            print("✓ 语义RAG检索: 可用 (Embedding + Reranker)")
            self.use_semantic = True
        elif self.rag:
            print("✓ RAG检索: 可用 (TF-IDF)")
        else:
            print("✗ RAG检索: 不可用")
        
        if self.tfidf:
            print("✓ TF-IDF兜底: 可用")
        else:
            print("✗ TF-IDF兜底: 不可用")
        
        if SKILL_MATCH_AVAILABLE:
            print("✓ 技能匹配优化: 可用")
        
        if self.use_hard_filter:
            print("✓ 硬匹配过滤: 可用 (学历/经验/地点)")
        
        print("===========================")
    
    def search(self, user_skills, top_k=10, use_llm=False):
        """
        搜索匹配的岗位
        
        Args:
            user_skills: 用户技能列表
            top_k: 返回结果数量
            use_llm: 是否使用大模型增强匹配
        
        Returns:
            匹配的岗位列表
        """
        if not user_skills:
            return []
        
        query = " ".join(user_skills)
        
        if self.semantic_rag:
            results = self.semantic_rag.retrieve(query, top_k=top_k, rerank=True)
        elif self.rag:
            results = self.rag.retrieve(query, top_k=top_k*3)
        elif self.tfidf:
            results = self.tfidf.search(user_skills, top_k=top_k*3)
            for r in results:
                r["similarity"] = r.get("match_score", 0) / 100
        else:
            return []
        
        if self.use_semantic:
            pass
        elif SKILL_MATCH_AVAILABLE and user_skills:
            expanded_skills = expand_skills(user_skills)
            for r in results:
                job_skills = r.get("skills", [])
                skill_sim = calculate_skill_similarity(user_skills, job_skills)
                r["skill_similarity"] = skill_sim
                r["final_score"] = r.get("similarity", 0) * 0.4 + skill_sim * 0.6
            results.sort(key=lambda x: x.get("final_score", 0), reverse=True)
        else:
            for r in results:
                r["final_score"] = r.get("similarity", 0)
        
        results = results[:top_k]
        
        if use_llm and self.llm and results:
            try:
                llm_analysis = self.llm.match_jobs(user_skills, results)
                for r in results:
                    r["llm_analysis"] = llm_analysis
            except:
                pass
        
        return results
    
    def generate_career_report(self, user_skills):
        """
        生成职业规划报告
        
        Args:
            user_skills: 用户技能列表
        
        Returns:
            职业规划报告内容
        """
        if not user_skills:
            return "请输入您的技能信息"
        
        if self.llm:
            query = " ".join(user_skills)
            if self.rag:
                retrieved_jobs = self.rag.retrieve(query, top_k=10)
            elif self.tfidf:
                retrieved_jobs = self.tfidf.search(user_skills, top_k=10)
            else:
                return "服务暂不可用"
            
            if not retrieved_jobs:
                return "未能找到匹配的岗位信息"
            
            try:
                report = self.llm.generate_career_report(user_skills, retrieved_jobs)
                return report
            except:
                pass
        
        if self.tfidf:
            return self._generate_simple_report(user_skills)
        
        return "服务暂不可用，请稍后再试"
    
    def _generate_simple_report(self, user_skills):
        """生成简单报告(无LLM时)"""
        results = self.search(user_skills, top_k=5)
        
        if not results:
            return "未能找到匹配的岗位"
        
        category = infer_job_category(user_skills) if SKILL_MATCH_AVAILABLE else None
        
        report = "# 🎯 职业规划建议\n\n"
        report += f"根据您掌握的技能: {', '.join(user_skills)}\n\n"
        
        if category:
            report += f"**推断岗位类别**: {category}\n\n"
        
        report += "## 推荐岗位\n\n"
        
        for i, job in enumerate(results, 1):
            score = job.get("final_score", job.get("match_score", 0))
            report += f"### {i}. {job.get('title', '-')}\n"
            report += f"- 公司: {job.get('company', '-')}\n"
            report += f"- 城市: {job.get('city', '-')}\n"
            report += f"- 薪资: {job.get('salary', '-')}\n"
            report += f"- 匹配度: {score:.0f}%\n"
            report += f"- 技能要求: {', '.join(job.get('skills', [])[:5])}\n\n"
        
        return report
    
    def smart_match(self, user_skills, city_filter=None, salary_filter=None, use_llm=True, top_k=10,
                    user_education=None, user_experience=None):
        """
        智能匹配
        
        Args:
            user_skills: 用户技能
            city_filter: 城市筛选
            salary_filter: 薪资筛选
            use_llm: 是否使用大模型
            user_education: 用户学历（用于硬匹配过滤）
            user_experience: 用户经验（用于硬匹配过滤）
        
        Returns:
            匹配结果，每条包含：
            - title: 岗位名称
            - company: 公司
            - city: 城市
            - salary: 薪资
            - skills: 技能列表
            - rag_score: RAG评分(0-100)，标准化后的分数
            - match_score: 匹配度(0-100)
        """
        salary_min = self._parse_salary(salary_filter)
        
        results = self.search(user_skills, top_k=top_k*3, use_llm=use_llm and self.use_llm)
        
        if self.use_hard_filter and (user_education or user_experience):
            results = hard_filter(
                results, 
                user_education=user_education,
                user_experience=user_experience,
                user_city=city_filter
            )
        else:
            if city_filter:
                results = [r for r in results if r.get("city") == city_filter]
        
        if salary_min:
            results = [r for r in results if self._check_salary(r, salary_min)]
        
        normalized_results = []
        for r in results[:top_k]:
            final_score = r.get("final_score", 0)
            rag_score = final_score * 100
            normalized_results.append({
                "title": r.get("title", ""),
                "company": r.get("company", ""),
                "city": r.get("city", ""),
                "salary": r.get("salary", ""),
                "skills": r.get("skills", [])[:10],
                "description": r.get("description", "")[:200] if r.get("description") else "",
                "rag_score": min(rag_score, 100),
                "match_score": min(rag_score, 100),
                "skill_match_details": r.get("skill_match_details", {}),
            })
        
        return normalized_results
    
    def _parse_salary(self, salary_filter):
        """解析薪资筛选"""
        if not salary_filter or salary_filter == "不限":
            return None
        
        salary_map = {
            "5K以下": 0,
            "5K-10K": 5000,
            "10K-15K": 10000,
            "15K-20K": 15000,
            "20K以上": 20000
        }
        return salary_map.get(salary_filter)
    
    def _check_salary(self, job, salary_min):
        """检查薪资是否符合要求"""
        salary_str = job.get("salary", "")
        if not salary_str:
            return True
        
        try:
            salary_parts = salary_str.replace("K", "000").replace("k", "000").split("-")
            if len(salary_parts) >= 2:
                min_salary = int(salary_parts[0])
                return min_salary >= salary_min
        except:
            pass
        return True


try:
    matcher = RAGMatcher()
except:
    matcher = None


def search(user_skills, top_k=10):
    """便捷搜索函数"""
    if matcher:
        return matcher.search(user_skills, top_k)
    return []


def generate_report(user_skills):
    """生成职业报告"""
    if matcher:
        return matcher.generate_career_report(user_skills)
    return "服务暂不可用"


def smart_match(user_skills, city_filter=None, salary_filter=None):
    """智能匹配"""
    if matcher:
        return matcher.smart_match(user_skills, city_filter, salary_filter)
    return []
