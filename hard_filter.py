# -*- coding: utf-8 -*-
"""
硬匹配过滤器
基于论文中的规则过滤：学历、经验、地点
"""

EDUCATION_LEVELS = {
    "中专": 1,
    "高中": 2,
    "大专": 3,
    "本科": 4,
    "硕士": 5,
    "博士": 6
}

EXPERIENCE_MAP = {
    "应届生": 0,
    "1年": 1,
    "1-3年": 2,
    "3-5年": 3,
    "5-10年": 5,
    "10年以上": 10
}

def parse_education_requirement(text):
    """从岗位描述中解析学历要求"""
    if not text:
        return 0
    
    text = text.lower()
    
    if "博士" in text:
        return 6
    elif "硕士" in text:
        return 5
    elif "本科" in text:
        return 4
    elif "大专" in text:
        return 3
    elif "高中" in text or "中专" in text:
        return 2
    
    return 0

def parse_experience_requirement(text):
    """从岗位描述中解析经验要求"""
    if not text:
        return 0
    
    import re
    
    patterns = [
        r"(\d+)\+?\s*年",
        r"经验\s*(\d+)\s*年",
        r"(\d+)-(\d+)\s*年"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            if len(match.groups()) == 1:
                return int(match.group(1))
            else:
                return int(match.group(1))
    
    if "应届" in text or "毕业生" in text:
        return 0
    elif "不限" in text or "经验" not in text:
        return 0
    
    return 0

def filter_by_education(user_education, job):
    """学历过滤"""
    if not user_education:
        return True
    
    user_level = EDUCATION_LEVELS.get(user_education, 4)
    
    job_desc = job.get("description", "") + job.get("title", "")
    job_level = parse_education_requirement(job_desc)
    
    if job_level == 0:
        return True
    
    return user_level >= job_level

def filter_by_experience(user_experience, job):
    """经验过滤"""
    if not user_experience:
        return True
    
    user_exp = EXPERIENCE_MAP.get(user_experience, 0)
    
    job_desc = job.get("description", "") + job.get("title", "")
    job_exp = parse_experience_requirement(job_desc)
    
    if job_exp == 0:
        return True
    
    return user_exp >= job_exp

def filter_by_city(user_city, job):
    """地点过滤"""
    if not user_city:
        return True
    
    job_city = job.get("city", "")
    
    if not job_city:
        return True
    
    return user_city in job_city or job_city in user_city

def hard_filter(jobs, user_education=None, user_experience=None, user_city=None):
    """
    硬匹配过滤
    
    Args:
        jobs: 岗位列表
        user_education: 用户学历 (本科/硕士/大专等)
        user_experience: 用户经验 (应届生/1年/3-5年等)
        user_city: 用户期望城市
    
    Returns:
        过滤后的岗位列表
    """
    if not jobs:
        return []
    
    filtered = []
    
    for job in jobs:
        if not filter_by_education(user_education, job):
            continue
        if not filter_by_experience(user_experience, job):
            continue
        if not filter_by_city(user_city, job):
            continue
        
        filtered.append(job)
    
    return filtered


def get_filter_stats(jobs_before, jobs_after, user_education=None, user_experience=None, user_city=None):
    """获取过滤统计信息"""
    stats = {
        "total_before": len(jobs_before),
        "total_after": len(jobs_after),
        "filtered_count": len(jobs_before) - len(jobs_after),
        "education_filtered": 0,
        "experience_filtered": 0,
        "city_filtered": 0
    }
    
    if user_education:
        stats["education_filtered"] = sum(1 for j in jobs_before if not filter_by_education(user_education, j))
    
    if user_experience:
        stats["experience_filtered"] = sum(1 for j in jobs_before if not filter_by_experience(user_experience, j))
    
    if user_city:
        stats["city_filtered"] = sum(1 for j in jobs_before if not filter_by_city(user_city, j))
    
    return stats
