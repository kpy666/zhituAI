# -*- coding: utf-8 -*-
"""
语义检索服务 - 使用Embedding + Reranker
基于 BGE 中文语义向量模型
"""

import json
import os
import numpy as np

KNOWLEDGE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "jobs_with_skills.json"
)

EMBEDDING_MODEL = None
RERANKER_MODEL = None

def get_embedding_model():
    """获取Embedding模型"""
    global EMBEDDING_MODEL
    if EMBEDDING_MODEL is not None:
        return EMBEDDING_MODEL
    
    try:
        from sentence_transformers import SentenceTransformer
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "models", "bge-small-zh"
        )
        if os.path.exists(model_path):
            EMBEDDING_MODEL = SentenceTransformer(model_path)
            print(f"Embedding模型已加载: {model_path}")
        else:
            EMBEDDING_MODEL = SentenceTransformer('BAAI/bge-small-zh-v1.5')
            print("Embedding模型已加载: BAAI/bge-small-zh-v1.5")
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
        reranker_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "models", "bge-reranker"
        )
        if os.path.exists(reranker_path):
            RERANKER_MODEL = CrossEncoder(reranker_path)
            print("Reranker模型已加载: 本地模型")
        else:
            print("Reranker模型本地不存在，跳过Rerank步骤")
            return None
        return RERANKER_MODEL
    except Exception as e:
        print(f"Reranker模型加载失败（将跳过Rerank步骤）: {e}")
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
        self.job_embeddings = self.embedding_model.encode(
            job_texts, 
            batch_size=32,
            show_progress_bar=True
        )
        print(f"向量索引已构建: {self.job_embeddings.shape}")
    
    def retrieve(self, query, top_k=10, rerank=True):
        """语义检索"""
        if not self.jobs:
            return []
        
        if not self.embedding_model:
            return []
        
        query_embedding = self.embedding_model.encode([query])
        
        similarities = np.dot(self.job_embeddings, query_embedding.T).flatten()
        top_indices = np.argsort(similarities)[-top_k*3:][::-1]
        
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


semantic_rag = SemanticRAG()

def search(query, top_k=10):
    """便捷搜索函数"""
    if semantic_rag:
        return semantic_rag.retrieve(query, top_k)
    return []
