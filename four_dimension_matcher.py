
# -*- coding: utf-8 -*-
"""
四维度人岗匹配模块
根据比赛要求，从以下四个维度进行分析：
1. 基础要求（学历、经验、地点）
2. 职业技能（专业技能、证书）
3. 职业素养（沟通能力、学习能力、抗压能力、创新能力）- 整合MBTI性格分析
4. 发展潜力（实习经历、项目经验、学习意愿）
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.mbti_analyzer import calculate_mbti_bonus_score, analyze_mbti_career
except ImportError:
    calculate_mbti_bonus_score = None
    analyze_mbti_career = None


def load_job_profiles():
    """加载岗位画像数据"""
    profile_path = os.path.join(BASE_DIR, "data", "job_profiles.json")
    if os.path.exists(profile_path):
        with open(profile_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"岗位画像": [], "换岗路径图谱": []}


JOB_PROFILES = load_job_profiles()


def calculate_basic_requirements_score(user_profile, job_profile):
    """
    维度1：基础要求匹配度
    包含：学历、经验、地点
    """
    score = 0
    details = []

    user_education = user_profile.get("学历", "本科")
    user_experience = user_profile.get("经验", "应届生")
    user_city = user_profile.get("城市", "")

    EDUCATION_WEIGHT = 0.4
    EXPERIENCE_WEIGHT = 0.4
    CITY_WEIGHT = 0.2

    education_levels = {"中专": 1, "高中": 2, "大专": 3, "本科": 4, "硕士": 5, "博士": 6}
    user_edu_level = education_levels.get(user_education, 4)

    if user_edu_level >= 4:
        edu_score = 100
        details.append("学历达标")
    elif user_edu_level == 3:
        edu_score = 70
        details.append("学历基本达标")
    else:
        edu_score = 40
        details.append("学历有差距")

    experience_map = {"应届生": 0, "1年": 1, "1-3年": 2, "3-5年": 3, "5-10年": 5, "10年以上": 10}
    user_exp_level = experience_map.get(user_experience, 0)

    # 应届生要求：经验值为0得满分
    if user_experience == "应届生":
        exp_score = 100
        details.append("经验符合应届生要求")
    elif user_exp_level > 0:
        exp_score = 80
        details.append("经验略有不足")
    else:
        exp_score = 60
        details.append("经验不足")

    city_score = 100 if not user_city else 80

    final_score = edu_score * EDUCATION_WEIGHT + exp_score * EXPERIENCE_WEIGHT + city_score * CITY_WEIGHT

    return {
        "score": min(final_score, 100),
        "details": details,
        "breakdown": {
            "学历": edu_score,
            "经验": exp_score,
            "城市": city_score
        }
    }


def calculate_professional_skills_score(user_skills, job_profile):
    """
    维度2：职业技能匹配度
    包含：专业技能、证书
    """
    job_skills = job_profile.get("专业技能", [])
    job_certificates = job_profile.get("证书要求", [])

    user_skills_lower = [s.lower() for s in user_skills]

    matched_skills = []
    missing_skills = []

    for skill in job_skills:
        skill_lower = skill.lower()
        if any(us in skill_lower or skill_lower in us for us in user_skills_lower):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    skill_coverage = len(matched_skills) / max(len(job_skills), 1)
    skill_score = skill_coverage * 100

    certificate_score = 80

    return {
        "score": min(skill_score * 0.8 + certificate_score * 0.2, 100),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills[:8],
        "skill_coverage": skill_coverage
    }


def calculate_professional_quality_score(user_profile, job_profile):
    """
    维度3：职业素养匹配度
    包含：沟通能力、学习能力、抗压能力、创新能力
    整合MBTI性格分析，根据性格特点调整评分
    """
    qualities = ["沟通能力", "学习能力", "抗压能力", "创新能力"]
    quality_scores = {}

    experience = user_profile.get("经验", "")
    experience_lower = experience.lower()
    mbti_type = user_profile.get("MBTI", "")
    job_title = job_profile.get("岗位名称", "")

    for quality in qualities:
        score = 70

        if quality == "沟通能力":
            if "团队" in experience_lower or "协作" in experience_lower or "沟通" in experience_lower:
                score = 90
        elif quality == "学习能力":
            if "学习" in experience_lower or "自学" in experience_lower or "新技能" in experience_lower:
                score = 90
        elif quality == "抗压能力":
            if "压力" in experience_lower or "紧急" in experience_lower or " deadline" in experience_lower:
                score = 90
        elif quality == "创新能力":
            if "创新" in experience_lower or "优化" in experience_lower or "改进" in experience_lower:
                score = 90

        quality_scores[quality] = score

    avg_score = sum(quality_scores.values()) / len(quality_scores)

    mbti_bonus = 0
    mbti_info = {}
    if mbti_type and calculate_mbti_bonus_score:
        mbti_bonus = calculate_mbti_bonus_score(mbti_type, job_title)
        avg_score = avg_score * 0.7 + mbti_bonus * 10 * 0.3
        if analyze_mbti_career:
            mbti_info = analyze_mbti_career(mbti_type)

    return {
        "score": min(avg_score, 100),
        "breakdown": quality_scores,
        "mbti_bonus": mbti_bonus,
        "mbti_info": mbti_info
    }


def calculate_development_potential_score(user_profile, job_profile):
    """
    维度4：发展潜力匹配度
    包含：实习经历、项目经验、学习意愿
    """
    potential_score = 70
    details = []

    experience = user_profile.get("经验", "")
    skills = user_profile.get("技能", [])

    if experience and len(experience) > 20:
        potential_score += 15
        details.append("有实习/项目经验")

    if len(skills) >= 5:
        potential_score += 10
        details.append("技能储备丰富")

    return {
        "score": min(potential_score, 100),
        "details": details
    }


def four_dimension_match(user_profile, user_skills, job_title=None):
    """
    四维度人岗匹配主函数

    Args:
        user_profile: 用户画像字典
        user_skills: 用户技能列表
        job_title: 指定岗位名称（可选）

    Returns:
        匹配结果，包含四个维度的详细评分
    """
    results = []

    for job_profile in JOB_PROFILES.get("岗位画像", []):
        if job_title and job_profile.get("岗位名称") != job_title:
            continue

        dim1 = calculate_basic_requirements_score(user_profile, job_profile)
        dim2 = calculate_professional_skills_score(user_skills, job_profile)
        dim3 = calculate_professional_quality_score(user_profile, job_profile)
        dim4 = calculate_development_potential_score(user_profile, job_profile)

        WEIGHTS = {
            "基础要求": 0.20,
            "职业技能": 0.40,
            "职业素养": 0.20,
            "发展潜力": 0.20
        }

        total_score = (
            dim1["score"] * WEIGHTS["基础要求"] +
            dim2["score"] * WEIGHTS["职业技能"] +
            dim3["score"] * WEIGHTS["职业素养"] +
            dim4["score"] * WEIGHTS["发展潜力"]
        )

        results.append({
            "岗位名称": job_profile.get("岗位名称"),
            "综合评分": min(total_score, 100),
            "维度评分": {
                "基础要求": dim1,
                "职业技能": dim2,
                "职业素养": dim3,
                "发展潜力": dim4
            },
            "岗位画像": job_profile
        })

    results.sort(key=lambda x: x["综合评分"], reverse=True)
    return results


def get_match_summary(match_result):
    """获取匹配摘要"""
    job_name = match_result.get("岗位名称")
    total_score = match_result.get("综合评分")
    dims = match_result.get("维度评分", {})

    strengths = []
    weaknesses = []

    if dims.get("职业技能", {}).get("score", 0) >= 80:
        strengths.append("职业技能匹配度高")
    else:
        weaknesses.append("职业技能有待提升")

    if dims.get("基础要求", {}).get("score", 0) >= 80:
        strengths.append("基础条件良好")

    return {
        "岗位": job_name,
        "总分": total_score,
        "优势": strengths,
        "不足": weaknesses
    }
