# -*- coding: utf-8 -*-
"""
智能匹配服务 - 多级兜底方案
方案1: RAG + 大模型 (主方案)
方案2: TF-IDF + LightGBM排序模型 (兜底1)
方案3: TF-IDF向量检索 (兜底2)
"""

import json
import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_FILE = os.path.join(BASE_DIR, "data", "jobs_with_skills.json")
CACHE_FILE = os.path.join(BASE_DIR, "data", "tfidf_cache.pkl")
RANKER_FILE = os.path.join(BASE_DIR, "data", "ranker_model.pkl")

SKILL_WEIGHTS = {
    "Java": 3.0, "Python": 3.0, "Go": 3.0, "C++": 2.5,
    "SpringBoot": 2.5, "Spring": 2.0, "Django": 2.5, "Flask": 2.5,
    "Vue": 2.0, "React": 2.0, "Angular": 2.0, "JavaScript": 1.8,
    "MySQL": 2.0, "Redis": 2.0, "MongoDB": 2.0,
    "机器学习": 3.5, "深度学习": 3.5, "TensorFlow": 3.5, "PyTorch": 3.5,
    "NLP": 3.0, "推荐算法": 3.0, "计算机视觉": 3.0,
    "Linux": 2.0, "Docker": 2.5, "K8s": 2.5, "Kubernetes": 2.5,
    "Hadoop": 3.0, "Spark": 3.0, "Flink": 3.0, "Hive": 2.5,
    "测试": 1.5, "Selenium": 2.0, "JMeter": 2.0,
    "MyBatis": 2.0, "Hibernate": 1.5,
}

class SmartMatcher:
    def __init__(self):
        self.jobs = []
        self.vectorizer = None
        self.job_vectors = None
        self.ranker = None
        self.ranker_features = []
        
        self.load_knowledge_base()
        self.load_tfidf_index()
        self.load_ranker()
    
    def load_knowledge_base(self):
        """加载岗位知识库"""
        if os.path.exists(KNOWLEDGE_FILE):
            with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                self.jobs = json.load(f)
            print(f"知识库已加载: {len(self.jobs)} 条岗位数据")
    
    def load_tfidf_index(self):
        """加载TF-IDF索引"""
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "rb") as f:
                data = pickle.load(f)
                self.vectorizer = data["vectorizer"]
                self.job_vectors = data["vectors"]
            print("TF-IDF索引已加载")
        else:
            self.build_tfidf_index()
    
    def load_ranker(self):
        """加载排序模型"""
        if os.path.exists(RANKER_FILE):
            with open(RANKER_FILE, "rb") as f:
                data = pickle.load(f)
                self.ranker = data["model"]
                self.ranker_features = data["feature_names"]
            print("排序模型已加载")
    
    def build_tfidf_index(self):
        """构建TF-IDF索引"""
        if not self.jobs:
            return
        
        def job_to_text(job):
            parts = []
            if job.get("title"):
                parts.append(" ".join([job["title"]] * 6))
            if job.get("skills"):
                for skill in job["skills"]:
                    weight = SKILL_WEIGHTS.get(skill, 1.0)
                    parts.extend([skill] * int(weight * 3))
            if job.get("description"):
                parts.append(job["description"][:500])
            return " ".join(parts)
        
        job_texts = [job_to_text(j) for j in self.jobs]
        
        self.vectorizer = TfidfVectorizer(
            max_features=12000,
            ngram_range=(1, 3),
            min_df=1,
            sublinear_tf=True
        )
        self.job_vectors = self.vectorizer.fit_transform(job_texts)
        
        with open(CACHE_FILE, "wb") as f:
            pickle.dump({
                "vectorizer": self.vectorizer,
                "vectors": self.job_vectors
            }, f)
        
        print("TF-IDF索引已构建")
    
    def extract_features(self, user_skills, job_skills):
        """提取排序特征"""
        if not user_skills:
            user_skills = []
        if not job_skills:
            job_skills = []
        
        user_set = set([s.strip().lower() for s in user_skills])
        job_set = set([s.strip().lower() for s in job_skills])
        matched = user_set & job_set
        
        user_weight = sum(SKILL_WEIGHTS.get(s, 1.0) for s in user_skills)
        job_weight = sum(SKILL_WEIGHTS.get(s, 1.0) for s in job_skills)
        matched_weight = sum(SKILL_WEIGHTS.get(s, 1.0) for s in matched)
        
        features = {
            "user_skill_count": len(user_skills),
            "job_skill_count": len(job_skills),
            "matched_count": len(matched),
            "unmatched_user_count": len(user_set - job_set),
            "unmatched_job_count": len(job_set - user_set),
            "jaccard_similarity": len(matched) / max(len(user_set | job_set), 1),
            "match_ratio": len(matched) / max(len(job_set), 1),
            "user_weight": user_weight,
            "job_weight": job_weight,
            "matched_weight": matched_weight,
            "weight_ratio": matched_weight / max(job_weight, 1),
            "skill_overlap_rate": len(matched) / max(len(user_set), 1),
            "title_keyword_match": 0,
            "desc_keyword_match": 0
        }
        return features
    
    def search(self, user_skills, top_k=10, city_filter=None, salary_min=None):
        """智能搜索 - 自动选择最佳方案"""
        if not user_skills:
            return []
        
        query = " ".join(user_skills)
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.job_vectors)[0]
        
        results = []
        candidate_count = min(200, len(self.jobs))
        top_indices = np.argsort(similarities)[-candidate_count:][::-1]
        
        for idx in top_indices:
            job = self.jobs[idx]
            
            if city_filter and job.get("city") != city_filter:
                continue
            
            if salary_min and (not job.get("salary_min") or job.get("salary_min") < salary_min):
                continue
            
            sim = similarities[idx]
            
            if self.ranker:
                features = self.extract_features(user_skills, job.get("skills", []))
                feature_array = np.array([[features.get(f, 0) for f in self.ranker_features]])
                ranker_score = self.ranker.predict(feature_array)[0] * 100
            else:
                ranker_score = 50.0
            
            final_score = (sim * 40) + (ranker_score * 0.50) + (10 if sim > 0.1 else 0)
            final_score = min(final_score, 100)
            
            results.append({
                "job_id": job.get("job_id"),
                "title": job.get("title"),
                "city": job.get("city"),
                "company": job.get("company"),
                "salary": f"{job.get('salary_min', '')}-{job.get('salary_max', '')}",
                "skills": job.get("skills", [])[:10],
                "description": job.get("description", "")[:200],
                "similarity": float(sim),
                "ranker_score": float(ranker_score),
                "match_score": final_score
            })
        
        results.sort(key=lambda x: x["match_score"], reverse=True)
        return results[:top_k]


matcher = SmartMatcher()

def recommend_jobs(user_skills, top_k=10, city_filter=None, salary_min=None):
    return matcher.search(user_skills, top_k, city_filter, salary_min)
