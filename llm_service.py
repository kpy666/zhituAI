# -*- coding: utf-8 -*-
"""
大模型服务
支持 GLM-4 / GLM-5 / 通义千问 / 文心一言
"""

import json
import requests
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

try:
    from src.config import API_KEY, LLM_PROVIDER
except:
    API_KEY = os.environ.get("API_KEY", "")
    LLM_PROVIDER = "glm"

class LLMService:
    def __init__(self, provider="glm"):
        self.provider = provider
        self.api_key = API_KEY
        self.base_url = ""
        self.set_provider(provider)
    
    def set_provider(self, provider):
        """设置模型提供商"""
        self.provider = provider
        
        if provider == "glm":
            self.base_url = "https://open.bigmodel.cn/api/paas/v4"
            self.model = "glm-4"
        elif provider == "glm-5":
            self.base_url = "https://open.bigmodel.cn/api/paas/v4"
            self.model = "glm-4-flash"
        elif provider == "qwen":
            self.base_url = "https://dashscope.aliyuncs.com/api/v1"
            self.model = "qwen-turbo"
        elif provider == "ernie":
            self.base_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1"
            self.model = "ernie-bot"
        else:
            self.base_url = "https://open.bigmodel.cn/api/paas/v4"
            self.model = "glm-4"
    
    def chat(self, system_prompt, user_prompt, temperature=0.7):
        """调用大模型"""
        if self.provider == "glm" or self.provider == "glm-5":
            return self._call_glm(system_prompt, user_prompt, temperature)
        elif self.provider == "qwen":
            return self._call_qwen(system_prompt, user_prompt, temperature)
        elif self.provider == "ernie":
            return self._call_ernie(system_prompt, user_prompt, temperature)
        else:
            return self._call_glm(system_prompt, user_prompt, temperature)
    
    def _call_glm(self, system_prompt, user_prompt, temperature):
        """调用智谱GLM-4"""
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            return f"API调用失败: {str(e)}"
    
    def _call_qwen(self, system_prompt, user_prompt, temperature):
        """调用通义千问"""
        url = f"{self.base_url}/services/aigc/text-generation/generation"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "input": {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            },
            "parameters": {"temperature": temperature}
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            result = response.json()
            return result.get("output", {}).get("text", "")
        except Exception as e:
            return f"API调用失败: {str(e)}"
    
    def _call_ernie(self, system_prompt, user_prompt, temperature):
        """调用文心一言"""
        # 获取access_token
        auth_url = "https://aip.baidubce.com/oauth/2.0/token"
        auth_params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key.split(":")[0] if ":" in self.api_key else self.api_key,
            "client_secret": self.api_key.split(":")[1] if ":" in self.api_key else ""
        }
        
        try:
            auth_response = requests.post(auth_url, params=auth_params, timeout=10)
            access_token = auth_response.json().get("access_token", "")
            
            url = f"{self.base_url}/text_gen/ernie-bot?access_token={access_token}"
            headers = {"Content-Type": "application/json"}
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": temperature
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=60)
            result = response.json()
            return result.get("result", "")
        except Exception as e:
            return f"API调用失败: {str(e)}"
    
    def generate_career_report(self, user_skills, retrieved_jobs):
        """生成职业报告"""
        context = "\n".join([
            f"职位: {job['title']}, 城市: {job['city']}, 技能: {', '.join(job['skills'][:5])}"
            for job in retrieved_jobs[:5]
        ])
        
        system_prompt = """你是一位专业的职业规划顾问，擅长分析用户的技能匹配度和职业发展路径。
请基于提供的岗位信息，为用户生成专业的职业规划报告。"""
        
        user_prompt = f"""用户技能: {', '.join(user_skills)}

匹配岗位信息:
{context}

请根据以上信息，为用户生成职业规划报告，包括：
1. 技能匹配分析
2. 推荐岗位及理由
3. 技能提升建议
4. 职业发展路径

请用简洁专业的语言回答。"""
        
        return self.chat(system_prompt, user_prompt)
    
    def match_jobs(self, user_skills, retrieved_jobs):
        """使用大模型进行智能匹配"""
        context = "\n".join([
            f"岗位{i}: {job['title']} | 城市: {job['city']} | 技能: {', '.join(job['skills'][:8])}"
            for i, job in enumerate(retrieved_jobs, 1)
        ])
        
        system_prompt = """你是一位专业的HR顾问，擅长人岗匹配。请根据用户技能和岗位要求进行匹配分析。"""
        
        user_prompt = f"""用户技能: {', '.join(user_skills)}

候选岗位:
{context}

请从候选岗位中选出最匹配的3个岗位，并说明匹配理由。按以下格式输出：
【推荐岗位1】
岗位名称: xxx
匹配度: xx%
匹配理由: xxx

【推荐岗位2】
...

【推荐岗位3】
..."""
        
        return self.chat(system_prompt, user_prompt)

    def recommend_jobs_direct(self, user_profile):
        """
        直接使用大模型推荐岗位
        使用 Few-shot + CoT + 结构化输出

        输出包含：
        - 分析过程：技能分类、方向匹配、综合考量
        - 推荐岗位：包含匹配度、理由、薪资范围、技能差距（带优先级）
        - 技能提升计划：按优先级排序的技能学习计划
        - 职业风险评估：就业风险评估和应对建议
        """
        education = user_profile.get("学历", "")
        major = user_profile.get("专业", "")
        skills = user_profile.get("技能", [])
        experience = user_profile.get("经验", "")
        city = user_profile.get("城市", "")

        system_prompt = """你是一位专业的职业规划顾问，擅长根据用户情况推荐合适的岗位。

## 重要约束
1. 必须严格按照JSON格式输出，禁止输出其他内容
2. 分析过程请参考Few-shot示例中的推理步骤
3. 推荐要结合用户的具体技能组合
4. 技能差距必须包含"重要性"和"学习优先级"字段
5. 必须包含职业风险评估

## 输出格式
请严格按照以下JSON格式输出：
{
  "分析过程": {
    "技能分类": "根据用户技能判断属于哪个方向",
    "方向匹配": "该方向与哪些岗位匹配",
    "综合考量": "结合学历、经验等因素的考量"
  },
  "推荐岗位": [
    {
      "名称": "岗位名称",
      "匹配度": 85,
      "理由": "推荐理由",
      "薪资范围": "X-K",
      "技能差距": [
        {"技能": "微服务", "重要性": "高", "学习优先级": 1, "建议": "先学这个，它是核心技能"},
        {"技能": "Redis", "重要性": "中", "学习优先级": 2, "建议": "缓存是必备"}
      ]
    }
  ],
  "技能提升计划": [
    {"技能": "微服务", "当前掌握": "不足", "目标": "理解分布式架构", "学习顺序": 1, "建议资源": "SpringCloud官方文档"},
    {"技能": "Redis", "当前掌握": "了解", "目标": "熟练使用", "学习顺序": 2, "建议资源": "Redis实战教程"}
  ],
  "职业风险评估": {
    "就业风险": "中",
    "风险原因": "Java岗位竞争激烈，但有SpringBoot经验有差异化优势",
    "应对建议": "突出项目经验，同时关注Go语言岗位拓宽选择"
  }
}"""

        user_prompt = f"""## 用户信息
- 学历：{education}
- 专业：{major}
- 城市：{city}
- 经验：{experience}
- 技能：{', '.join(skills) if skills else '暂无'}

## Few-shot 示例

【示例1】
用户技能: Java, SpringBoot, MySQL, Redis
推理过程:
  1. 技能分类：Java+SpringBoot属于后端开发方向
  2. 方向匹配：后端开发 → Java开发工程师、Go开发工程师
  3. 综合考量：掌握Redis和MySQL，适合互联网后端开发
输出:
{{
  "分析过程": {{
    "技能分类": "后端开发",
    "方向匹配": "Java开发工程师、Go开发工程师",
    "综合考量": "技术栈完整，适合互联网公司后端开发"
  }},
  "推荐岗位": [
    {{
      "名称": "Java开发工程师",
      "匹配度": 92,
      "理由": "技术栈完全匹配，有SpringBoot经验",
      "薪资范围": "15-25K",
      "技能差距": [
        {{"技能": "微服务架构", "重要性": "高", "学习优先级": 1, "建议": "分布式系统是高级工程师必备"}},
        {{"技能": "Docker容器化", "重要性": "中", "学习优先级": 2, "建议": "DevOps技能加分"}},
        {{"技能": "消息队列", "重要性": "中", "学习优先级": 3, "建议": "Kafka/RocketMQ"}}
      ]
    }},
    {{
      "名称": "后端开发工程师",
      "匹配度": 85,
      "理由": "后端技能扎实，可转型其他语言",
      "薪资范围": "12-22K",
      "技能差距": [
        {{"技能": "Go语言", "重要性": "中", "学习优先级": 1, "建议": "云原生时代Go更流行"}}
      ]
    }}
  ],
  "技能提升计划": [
    {{"技能": "微服务架构", "当前掌握": "不足", "目标": "理解分布式系统设计", "学习顺序": 1, "建议资源": "SpringCloud微服务实战"}},
    {{"技能": "Docker容器化", "当前掌握": "不足", "目标": "熟练使用Docker部署", "学习顺序": 2, "建议资源": "Docker官方教程"}},
    {{"技能": "消息队列", "当前掌握": "了解", "目标": "掌握异步通信原理", "学习顺序": 3, "建议资源": "Kafka权威指南"}}
  ],
  "职业风险评估": {{
    "就业风险": "中",
    "风险原因": "Java岗位竞争激烈，每年有大量毕业生投递，但有SpringBoot项目经验可以形成差异化",
    "应对建议": "1)在简历中突出SpringBoot项目经验 2)同时学习Go语言，拓宽岗位选择 3)准备好多线程、高并发等面试重点"
  }}
}}

【示例2】
用户技能: Python, SQL, Excel, Tableau
推理过程:
  1. 技能分类：Python+SQL+可视化工具属于数据分析方向
  2. 方向匹配：数据分析 → 数据分析师、BI工程师
  3. 综合考量：擅长工具使用，适合业务数据分析
输出:
{{
  "分析过程": {{
    "技能分类": "数据分析",
    "方向匹配": "数据分析师、BI工程师",
    "综合考量": "工具熟练，适合业务分析岗位"
  }},
  "推荐岗位": [
    {{
      "名称": "数据分析师",
      "匹配度": 90,
      "理由": "Python和SQL技能扎实",
      "薪资范围": "10-18K",
      "技能差距": [
        {{"技能": "机器学习基础", "重要性": "高", "学习优先级": 1, "建议": "向算法方向发展的基础"}},
        {{"技能": "Python数据分析库", "重要性": "高", "学习优先级": 2, "建议": "Pandas、NumPy必须熟练"}},
        {{"技能": "业务理解能力", "重要性": "中", "学习优先级": 3, "建议": "结合行业知识"}}
      ]
    }},
    {{
      "名称": "BI工程师",
      "匹配度": 82,
      "理由": "Tableau技能突出",
      "薪资范围": "12-20K",
      "技能差距": [
        {{"技能": "ETL流程", "重要性": "中", "学习优先级": 1, "建议": "数据仓库知识"}}
      ]
    }}
  ],
  "技能提升计划": [
    {{"技能": "机器学习基础", "当前掌握": "不足", "目标": "掌握常用算法原理", "学习顺序": 1, "建议资源": "吴恩达机器学习课程"}},
    {{"技能": "Python数据分析库", "当前掌握": "了解", "目标": "熟练使用Pandas", "学习顺序": 2, "建议资源": "Python数据分析实战"}}
  ],
  "职业风险评估": {{
    "就业风险": "低",
    "风险原因": "数据分析岗位需求稳定增长，Python+SQL+可视化技能组合具有竞争力",
    "应对建议": "1)积累业务分析项目经验 2)学习机器学习提升差异化 3)关注行业特定业务知识"
  }}
}}

## 请推理并输出
用户技能: {', '.join(skills) if skills else '暂无'}
(其他信息: 学历={education}, 专业={major}, 城市={city})

请按照示例格式输出JSON:"""

        return self.chat(system_prompt, user_prompt)


llm_service = LLMService(LLM_PROVIDER)

def chat(prompt, system_prompt="你是一位专业的职业规划助手"):
    """便捷的聊天函数"""
    return llm_service.chat(system_prompt, prompt)

def generate_report(user_skills, jobs):
    """生成职业报告"""
    return llm_service.generate_career_report(user_skills, jobs)

def match_jobs(user_skills, jobs):
    """智能匹配岗位"""
    return llm_service.match_jobs(user_skills, jobs)
