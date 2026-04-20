# -*- coding: utf-8 -*-
"""
RAG 检索服务
使用向量存储 + 大模型进行智能匹配
"""

import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_FILE = os.path.join(BASE_DIR, "data", "jobs_with_skills.json")

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
        
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        self.job_vectors = self.vectorizer.fit_transform(job_texts)
        print("向量索引已构建")
    
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
    
    def build_context(self, retrieved_jobs):
        """构建RAG上下文"""
        context = "以下是候选岗位信息：\n\n"
        for i, job in enumerate(retrieved_jobs, 1):
            context += f"【岗位{i}】\n"
            context += f"职位：{job['title']}\n"
            context += f"城市：{job['city']}\n"
            context += f"公司：{job['company']}\n"
            context += f"薪资：{job['salary']}\n"
            context += f"技能要求：{', '.join(job['skills'])}\n"
            context += f"职位描述：{job['description']}\n"
            context += "\n"
        return context


rag_service = RAGService()

def retrieve_jobs(query, top_k=10):
    """检索岗位的便捷函数"""
    return rag_service.retrieve(query, top_k)

def get_context(jobs):
    """获取RAG上下文的便捷函数"""
    return rag_service.build_context(jobs)
