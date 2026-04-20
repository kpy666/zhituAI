# -*- coding: utf-8 -*-
"""
技能匹配优化模块
- 技能同义词扩展
- 技能相似度计算
- 智能纠错
"""

SKILL_ALIASES = {
    "java": ["java", "javase", "java开发", "java工程师"],
    "python": ["python", "python开发", "py", "python3"],
    "c++": ["c++", "cpp", "c语言", "c/c++"],
    "golang": ["go", "golang", "go语言", "go开发"],
    "javascript": ["js", "javascript", "前端js"],
    "typescript": ["ts", "typescript", "ts开发"],
    "vue": ["vue", "vue.js", "vuejs", "vue2", "vue3"],
    "react": ["react", "react.js", "reactjs"],
    "angular": ["angular", "angularjs"],
    "spring": ["spring", "springboot", "spring framework"],
    "django": ["django", "django框架"],
    "flask": ["flask", "flask框架"],
    "mysql": ["mysql", "mysql数据库", "mysqlsql"],
    "redis": ["redis", "redis缓存", "redis数据库"],
    "mongodb": ["mongodb", "mongo", "nosql"],
    "sql": ["sql", "mysql", "oracle", "sqlserver", "数据库"],
    "linux": ["linux", "linux运维", "linux系统"],
    "docker": ["docker", "容器", "dockerfile"],
    "k8s": ["k8s", "kubernetes", "K8S"],
    "机器学习": ["机器学习", "ml", "machine learning"],
    "深度学习": ["深度学习", "dl", "deep learning"],
    "tensorflow": ["tensorflow", "tf", "tf2"],
    "pytorch": ["pytorch", "pyTorch"],
    "nlp": ["nlp", "自然语言处理", "文本处理"],
    "cv": ["cv", "计算机视觉", "图像处理", "视觉"],
    "spark": ["spark", "大数据spark"],
    "hadoop": ["hadoop", "hdfs", "mapreduce"],
    "flink": ["flink", "实时计算"],
    "hive": ["hive", "hql"],
    "elasticsearch": ["es", "elasticsearch", "搜索引擎"],
    "rabbitmq": ["rabbitmq", "mq", "消息队列"],
    "kafka": ["kafka", "消息队列kafka"],
    "数据结构": ["数据结构", "算法", "algorithm"],
    "设计模式": ["设计模式", "design pattern"],
}

SKILL_CATEGORIES = {
    "后端开发": ["java", "python", "golang", "c++", "spring", "django", "flask", "springboot", "node.js", "go", "php", "ruby"],
    "前端开发": ["vue", "react", "angular", "javascript", "typescript", "html", "css", "jquery", "webpack", "小程序", "react native", "flutter"],
    "移动端": ["android", "ios", "swift", "kotlin", "flutter", "react native", "uni-app"],
    "算法工程师": ["机器学习", "深度学习", "tensorflow", "pytorch", "nlp", "cv", "推荐算法", "搜索算法", "算法"],
    "数据开发": ["spark", "hadoop", "flink", "hive", "hdfs", "mapreduce", "etl", "大数据"],
    "数据分析": ["sql", "python", "r", "excel", "tableau", "power bi", "spss", "数据分析"],
    "测试开发": ["selenium", "jmeter", "appium", "自动化测试", "测试", "qa"],
    "运维": ["linux", "docker", "k8s", "ansible", "jenkins", "shell", "运维", "devops"],
    "数据库": ["mysql", "redis", "mongodb", "oracle", "postgresql", "sqlserver"],
    "架构师": ["分布式", "微服务", "高并发", "系统设计", "架构"],
}

def normalize_skill(skill):
    """技能名称标准化"""
    skill = skill.lower().strip()
    skill = skill.replace(" ", "").replace("-", "").replace("_", "")
    return skill

def get_canonical_skill(skill):
    """获取技能的标准名称"""
    normalized = normalize_skill(skill)
    
    for canonical, aliases in SKILL_ALIASES.items():
        if normalized in aliases or skill.lower() in aliases:
            return canonical
    
    return normalized

def expand_skills(skills):
    """扩展技能列表"""
    expanded = set()
    for skill in skills:
        canonical = get_canonical_skill(skill)
        expanded.add(canonical)
        expanded.add(skill.lower())
        
        for key, aliases in SKILL_ALIASES.items():
            if skill.lower() in aliases:
                expanded.add(key)
                expanded.update(aliases)
    
    return list(expanded)

def calculate_skill_similarity(user_skills, job_skills):
    """计算技能相似度"""
    if not user_skills or not job_skills:
        return 0.0
    
    user_skills = expand_skills(user_skills)
    job_skills = expand_skills(job_skills)
    
    user_set = set([normalize_skill(s) for s in user_skills])
    job_set = set([normalize_skill(s) for s in job_skills])
    
    intersection = user_set & job_set
    union = user_set | job_set
    
    jaccard = len(intersection) / max(len(union), 1)
    
    match_ratio = len(intersection) / max(len(job_set), 1)
    
    return (jaccard * 0.4 + match_ratio * 0.6)

def infer_job_category(user_skills):
    """根据用户技能推断岗位类别"""
    user_skills_lower = [s.lower() for s in user_skills]
    
    category_scores = {}
    for category, required_skills in SKILL_CATEGORIES.items():
        score = sum(1 for s in user_skills_lower if any(rs in s or s in rs for rs in required_skills))
        category_scores[category] = score
    
    if not category_scores or max(category_scores.values()) == 0:
        return None
    
    return max(category_scores, key=category_scores.get)

def filter_by_category(jobs, category):
    """按类别筛选岗位"""
    if not category:
        return jobs
    
    category_keywords = SKILL_CATEGORIES.get(category, [])
    
    filtered = []
    for job in jobs:
        job_text = (job.get("title", "") + " " + " ".join(job.get("skills", []))).lower()
        
        if any(kw in job_text for kw in category_keywords):
            filtered.append(job)
    
    return filtered if filtered else jobs
