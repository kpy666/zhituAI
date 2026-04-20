# -*- coding: utf-8 -*-
"""
MBTI性格分析模块
将MBTI性格类型整合到职业规划系统中
"""

MBTI_ANALYSIS = {
    "INTJ": {
        "name": "建筑师",
        "description": "独立思考者，善于分析和规划，具有战略眼光",
        "strengths": ["分析能力强", "独立工作", "战略思维", "追求完美"],
        "suitable_jobs": ["算法工程师", "数据分析师", "架构师", "技术总监"],
        "career_advice": "适合需要深度思考和技术专精的岗位，适合成为技术专家或架构师",
        "work_style": "独立完成、深度研究、长周期项目",
        "team_role": "智囊团、技术专家",
        "communication_style": "直接、理性、重逻辑",
        "potential_weaknesses": "可能过于挑剔、缺乏社交、难以理解他人情感",
        "ideal_work_env": "独立工作空间、强调效率和能力的环境"
    },
    "INTP": {
        "name": "逻辑学家",
        "description": "喜欢探索理论和原理，善于解决复杂问题",
        "strengths": ["逻辑思维", "创新能力", "分析能力", "理论探索"],
        "suitable_jobs": ["算法工程师", "数据科学家", "研究员", "安全工程师"],
        "career_advice": "适合研究性、技术性工作，适合深入某个技术领域成为专家",
        "work_style": "探索性研究、解决复杂问题、创新解决方案",
        "team_role": "技术顾问、架构设计",
        "communication_style": "内向、专注、技术深度",
        "potential_weaknesses": "可能过于理想化、不切实际、忽视沟通",
        "ideal_work_env": "研究型环境、允许独立探索的空间"
    },
    "ENTJ": {
        "name": "指挥官",
        "description": "天生领导者，善于决策和激励团队",
        "strengths": ["领导能力", "决策能力", "战略规划", "执行力"],
        "suitable_jobs": ["技术总监", "CTO", "产品经理", "项目经理"],
        "career_advice": "适合管理和领导岗位，适合带领团队实现目标",
        "work_style": "目标导向、团队领导、战略执行",
        "team_role": "领导者、决策者",
        "communication_style": "强势、直接、说服力强",
        "potential_weaknesses": "可能过于强势、缺乏耐心、忽视他人感受",
        "ideal_work_env": "快速决策的环境、有明确目标和竞争氛围"
    },
    "ENTP": {
        "name": "辩论家",
        "description": "喜欢挑战和创新，善于发现新机会",
        "strengths": ["创新能力", "适应能力", "沟通能力", "机会发现"],
        "suitable_jobs": ["产品经理", "前端开发", "技术专家", "创业者"],
        "career_advice": "适合需要创新和灵活性的岗位，适合新产品开发",
        "work_style": "多任务并行、创新项目、解决新问题",
        "team_role": "创新推动者、问题解决者",
        "communication_style": "外向、创意、说服力",
        "potential_weaknesses": "可能缺乏专注、难以坚持、过于好辩",
        "ideal_work_env": "创新实验室、创业环境、多样化项目"
    },
    "INFJ": {
        "name": "提倡者",
        "description": "有理想有追求，注重意义和价值",
        "strengths": ["洞察力", "创造力", "同理心", "理想主义"],
        "suitable_jobs": ["产品经理", "UI设计师", "运营", "心理咨询师"],
        "career_advice": "适合能实现个人价值的岗位，喜欢帮助他人成长",
        "work_style": "意义导向、深度合作、长线项目",
        "team_role": "引导者、理想主义者",
        "communication_style": "温和、有洞察力、共情能力强",
        "potential_weaknesses": "可能过于理想化、难以接受批评、忽视现实",
        "ideal_work_env": "有意义的目标、人文关怀、创造性的空间"
    },
    "INFP": {
        "name": "调停者",
        "description": "理想主义，善于创作和调解",
        "strengths": ["创造力", "同理心", "适应能力", "语言能力"],
        "suitable_jobs": ["前端开发", "UI设计师", "内容运营", "教师"],
        "career_advice": "适合创作性和帮助他人的工作，能在艺术和技术结合的岗位发挥",
        "work_style": "创意工作、独立完成、灵活协作",
        "team_role": "创意输出者、调解者",
        "communication_style": "温和、创意、有同理心",
        "potential_weaknesses": "可能过于敏感、现实感差、难以做决定",
        "ideal_work_env": "创造性自由、支持个人价值观、安静的工作环境"
    },
    "ENFJ": {
        "name": "主人公",
        "description": "天生领导者，善于激励他人",
        "strengths": ["领导能力", "沟通能力", "同理心", "感染力"],
        "suitable_jobs": ["产品经理", "运营经理", "团队负责人", "培训师"],
        "career_advice": "适合需要带领团队和影响他人的岗位，能成为优秀的领导者",
        "work_style": "团队协作、影响他人、培养人才",
        "team_role": "领导者、导师、激励者",
        "communication_style": "热情、有感染力、鼓励他人",
        "potential_weaknesses": "可能过于理想化、忽视自己需求、容易被操控",
        "ideal_work_env": "团队合作、支持性环境，培养他人的机会"
    },
    "ENFP": {
        "name": "竞选者",
        "description": "热情创意，善于沟通和激励",
        "strengths": ["热情", "创造力", "沟通能力", "适应能力"],
        "suitable_jobs": ["产品运营", "前端开发", "市场营销", "创业者"],
        "career_advice": "适合需要创意和沟通的工作，能在快速变化的环境中发挥",
        "work_style": "多任务、创意工作、灵活协作",
        "team_role": "创新者、激励者",
        "communication_style": "热情、创意、有感染力",
        "potential_weaknesses": "可能缺乏专注、难以坚持、容易分心",
        "ideal_work_env": "自由创意空间、多样化社交环境、变化丰富"
    },
    "ISTJ": {
        "name": "物流师",
        "description": "可靠务实，注重细节和责任",
        "strengths": ["责任感", "可靠性", "细节导向", "执行力"],
        "suitable_jobs": ["后端开发", "测试工程师", "运维工程师", "数据工程师"],
        "career_advice": "适合需要稳定性和可靠性的岗位，能成为团队的中坚力量",
        "work_style": "稳定工作、细节执行、持续改进",
        "team_role": "执行者、稳定器",
        "communication_style": "直接、务实、可靠",
        "potential_weaknesses": "可能过于保守、不灵活、难以接受新事物",
        "ideal_work_env": "结构化环境、明确流程、稳定的团队"
    },
    "ISFJ": {
        "name": "守卫者",
        "description": "细心负责，善于照顾他人",
        "strengths": ["责任感", "细心", "奉献精神", "务实"],
        "suitable_jobs": ["测试工程师", "运维工程师", "技术支持", "运维开发"],
        "career_advice": "适合需要耐心和细心的岗位，能为团队提供稳定的支持",
        "work_style": "稳定支持、细节关注、持续维护",
        "team_role": "支持者、守护者",
        "communication_style": "温和、细心、可靠",
        "potential_weaknesses": "可能过于谦虚、难以拒绝他人、忽视自己需求",
        "ideal_work_env": "稳定的团队、明确职责、支持性的氛围"
    },
    "ESTJ": {
        "name": "总经理",
        "description": "组织能力强，善于管理",
        "strengths": ["组织能力", "管理能力", "执行力", "责任感"],
        "suitable_jobs": ["技术经理", "测试主管", "运维主管", "项目经理"],
        "career_advice": "适合管理和执行岗位，能有效组织团队完成任务",
        "work_style": "目标导向、团队管理、质量控制",
        "team_role": "管理者、执行者",
        "communication_style": "强势、有条理、决策力强",
        "potential_weaknesses": "可能过于专制、缺乏弹性、不善倾听",
        "ideal_work_env": "目标驱动、高效率、明确的组织结构"
    },
    "ESFJ": {
        "name": "执政官",
        "description": "关注他人，善于协作",
        "strengths": ["协作能力", "责任感", "细心", "社交能力"],
        "suitable_jobs": ["产品运营", "客户运营", "团队协调", "项目经理"],
        "career_advice": "适合需要大量协调和沟通的岗位，能成为团队的粘合剂",
        "work_style": "团队协作、客户沟通、项目协调",
        "team_role": "协调者、沟通者",
        "communication_style": "热情、友好、善于协调",
        "potential_weaknesses": "可能过于在意他人看法、难以处理冲突、忽视自己感受",
        "ideal_work_env": "人际导向、协作氛围、被认可和欣赏"
    },
    "ISTP": {
        "name": "鉴赏家",
        "description": "务实灵活，善于动手操作",
        "strengths": ["动手能力", "分析能力", "适应能力", "实际问题解决"],
        "suitable_jobs": ["后端开发", "嵌入式开发", "游戏开发", "运维工程师"],
        "career_advice": "适合需要实际动手能力的技术岗位，能解决复杂的实际问题",
        "work_style": "动手实践、问题解决、技术深度",
        "team_role": "技术专家、问题解决者",
        "communication_style": "内向、务实、技术导向",
        "potential_weaknesses": "可能缺乏耐心、难以坚持、社交能力不足",
        "ideal_work_env": "动手操作的环境、独立工作空间、技术挑战"
    },
    "ISFP": {
        "name": "探险家",
        "description": "艺术气质，善于发现美",
        "strengths": ["艺术感", "创造力", "观察力", "适应能力"],
        "suitable_jobs": ["UI设计师", "前端开发", "视觉设计师", "游戏美术"],
        "career_advice": "适合需要美学感知的设计和技术结合岗位，能创造美好的用户体验",
        "work_style": "创意设计、独立完成、美学导向",
        "team_role": "设计师、创意输出",
        "communication_style": "温和、艺术感、观察力强",
        "potential_weaknesses": "可能过于自由散漫、难以遵守规则、缺乏计划性",
        "ideal_work_env": "艺术氛围、创意空间、灵活自由的工作方式"
    },
    "ESTP": {
        "name": "企业家",
        "description": "灵活务实，善于把握机会",
        "strengths": ["适应能力", "执行力", "机会把握", "人际交往"],
        "suitable_jobs": ["前端开发", "产品经理", "技术销售", "创业者"],
        "career_advice": "适合需要快速反应和实际执行的环境，能在压力下表现出色",
        "work_style": "快速行动、问题解决、多任务处理",
        "team_role": "执行者、机会捕捉者",
        "communication_style": "直接、务实、有说服力",
        "potential_weaknesses": "可能缺乏长远规划、冒险冲动、忽视细节",
        "ideal_work_env": "快节奏、挑战性、奖励机制明确"
    },
    "ESFP": {
        "name": "表演者",
        "description": "热情开朗，善于表现",
        "strengths": ["表现力", "社交能力", "热情", "感染力"],
        "suitable_jobs": ["前端开发", "UI设计", "产品运营", "市场营销"],
        "career_advice": "适合需要展示和表达的岗位，能为团队带来活力",
        "work_style": "展示演示、团队互动、灵活应变",
        "team_role": "展示者、氛围制造者",
        "communication_style": "热情、外向、有感染力",
        "potential_weaknesses": "可能过于追求关注、难以专注、冲动决策",
        "ideal_work_env": "社交环境、展示舞台、充满活力的氛围"
    }
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
    """
    分析MBTI性格类型与职业的匹配度

    Args:
        mbti_type: MBTI性格类型（如INTJ）

    Returns:
        dict: 包含性格分析、职业推荐、匹配建议等
    """
    if not mbti_type:
        return {
            "type": "未知",
            "name": "未测试",
            "description": "未提供MBTI性格类型",
            "strengths": [],
            "suitable_jobs": ["数据分析师", "后端开发", "前端开发", "产品经理"],
            "career_advice": "完成MBTI测试可获得更精准的岗位推荐",
            "mbti_match_score": 0.5
        }

    mbti_upper = mbti_type.upper()

    if mbti_upper not in MBTI_ANALYSIS:
        return {
            "type": "未知",
            "name": "无法识别",
            "description": f"无法识别MBTI类型: {mbti_type}",
            "strengths": [],
            "suitable_jobs": ["数据分析师", "后端开发", "前端开发", "产品经理"],
            "career_advice": "请输入有效的MBTI类型",
            "mbti_match_score": 0.5
        }

    analysis = MBTI_ANALYSIS[mbti_upper].copy()
    career_match = MBTI_CAREER_MATCH.get(mbti_upper, {"适合度": 0.5, "匹配理由": "性格适配"})

    analysis["mbti_match_score"] = career_match["适合度"]
    analysis["mbti_match_reason"] = career_match["匹配理由"]

    return analysis


def get_mbti_recommendation_for_job(mbti_type, job_title):
    """
    根据MBTI类型和目标岗位，给出个性化建议

    Args:
        mbti_type: MBTI性格类型
        job_title: 目标岗位

    Returns:
        dict: 包含匹配度、建议、注意事项等
    """
    analysis = analyze_mbti_career(mbti_type)

    job_mbti_suitability = {
        "Java开发工程师": {"INTJ": 0.9, "INTP": 0.85, "ISTJ": 0.9, "ISTP": 0.85},
        "前端开发工程师": {"ENTP": 0.85, "ENFP": 0.8, "ISFP": 0.85, "ESFP": 0.8},
        "算法工程师": {"INTJ": 0.95, "INTP": 0.95, "INFJ": 0.8, "ISTP": 0.8},
        "数据分析师": {"INTJ": 0.85, "INTP": 0.9, "ISTJ": 0.8, "INFJ": 0.75},
        "产品经理": {"ENTJ": 0.9, "ENFJ": 0.9, "ENTP": 0.85, "INFJ": 0.8},
        "UI设计师": {"INFP": 0.9, "ISFP": 0.95, "ENFP": 0.85, "INFJ": 0.85},
        "测试工程师": {"ISFJ": 0.9, "ISTJ": 0.9, "INTP": 0.75, "ESFJ": 0.7},
        "运维工程师": {"ISTJ": 0.9, "ISFJ": 0.85, "ISTP": 0.8, "ESTJ": 0.75},
    }

    job_score = job_mbti_suitability.get(job_title, {}).get(mbti_type.upper(), 0.7)

    recommendations = {
        "job_title": job_title,
        "mbti_type": mbti_type.upper() if mbti_type else "未知",
        "personality_name": analysis.get("name", ""),
        "job_suitability": job_score,
        "strengths_for_job": analysis.get("strengths", []),
        "work_style": analysis.get("work_style", ""),
        "team_role": analysis.get("team_role", ""),
        "personalized_advice": _generate_advice(mbti_type, job_title, job_score),
        "career_path": _generate_career_path(mbti_type, job_title)
    }

    return recommendations


def _generate_advice(mbti_type, job_title, job_score):
    """生成个性化建议"""
    if job_score >= 0.9:
        return f"{mbti_type}类型非常适合{job_title}岗位。你的性格特点与该岗位高度匹配，建议重点发展相关技术栈。"
    elif job_score >= 0.8:
        return f"{mbti_type}类型比较适合{job_title}岗位。建议发挥性格优势，同时补充岗位所需的专业技能。"
    elif job_score >= 0.7:
        return f"{mbti_type}类型适合{job_title}岗位。需要适当调整工作方式以适应岗位特点，建议多参与团队协作。"
    else:
        return f"{mbti_type}类型与{job_title}岗位匹配度一般。如果特别喜欢该岗位，可以通过后天培养适应；也可以考虑更匹配的岗位方向。"


def _generate_career_path(mbti_type, job_title):
    """生成职业发展路径建议"""
    paths = {
        "Java开发工程师": [
            "初级Java工程师 → 中级Java工程师 → 高级Java工程师 → 架构师/技术专家",
            "Java工程师 → 技术管理 → 技术经理 → 技术总监",
            "Java工程师 → 转向大数据/AI方向 → 高级工程师 → 领域专家"
        ],
        "前端开发工程师": [
            "初级前端 → 中级前端 → 高级前端 → 前端专家/架构师",
            "前端 → 全栈工程师 → 技术专家 → 技术总监",
            "前端 → UI设计 → 交互设计 → 设计总监"
        ],
        "算法工程师": [
            "算法工程师 → 高级算法 → 算法专家 → 首席科学家",
            "算法工程师 → AI产品经理 → AI产品总监 → VP产品",
            "算法工程师 → 技术管理 → AI团队负责人 → 技术VP"
        ],
        "数据分析师": [
            "初级分析师 → 中级分析师 → 高级分析师 → 数据总监",
            "分析师 → 数据产品经理 → 数据产品总监 → VP产品",
            "分析师 → 算法工程师 → 高级算法 → 算法专家"
        ],
        "产品经理": [
            "产品专员 → 产品经理 → 高级产品经理 → 产品总监 → VP产品",
            "产品经理 → 项目经理 → 运营总监 → COO",
            "产品经理 → 创业 → CEO → 投资人"
        ],
        "UI设计师": [
            "UI设计师 → 高级UI → UI专家 → 设计专家/设计总监",
            "UI → 交互设计 → UX设计 → 设计总监",
            "UI → 产品经理 → 高级产品经理 → 产品总监"
        ]
    }
    return paths.get(job_title, ["技术路线：初级 → 中级 → 高级 → 专家"])


def calculate_mbti_bonus_score(mbti_type, job_title):
    """
    计算MBTI对岗位匹配的加成分数

    Args:
        mbti_type: MBTI性格类型
        job_title: 目标岗位

    Returns:
        float: MBTI加成分数（0-10）
    """
    job_mbti_suitability = {
        "Java开发工程师": {"INTJ": 8, "INTP": 7, "ISTJ": 8, "ISTP": 7, "ENTJ": 5, "ENFP": 4, "ISFP": 5, "ESFP": 4, "INFJ": 5, "INFP": 5, "ENFJ": 4, "ESFJ": 4},
        "前端开发工程师": {"ENFP": 8, "ENTP": 8, "ISFP": 8, "ESFP": 8, "INFP": 7, "INFJ": 6, "INTJ": 5, "ISTP": 6, "ENTJ": 5, "ESTJ": 4, "ISFJ": 4, "ESFJ": 4},
        "算法工程师": {"INTJ": 10, "INTP": 10, "INFJ": 7, "ISTP": 7, "ENTJ": 5, "ENFP": 4, "ISFP": 4, "ESFP": 3, "INFP": 5, "ENFJ": 4, "ISTJ": 5, "ESFJ": 3},
        "数据分析师": {"INTJ": 8, "INTP": 9, "ISTJ": 7, "INFJ": 7, "ENTJ": 5, "ENFP": 4, "ISFP": 4, "ESFP": 3, "INFP": 5, "ENFJ": 4, "ISTP": 6, "ESFJ": 3},
        "产品经理": {"ENTJ": 9, "ENFJ": 9, "ENTP": 8, "INFJ": 8, "INTJ": 6, "ENFP": 7, "INFP": 6, "ISFP": 4, "ISTJ": 4, "ISTP": 4, "ESTJ": 5, "ESFJ": 4},
        "UI设计师": {"INFP": 9, "ISFP": 10, "INFJ": 8, "ENFP": 8, "INTJ": 5, "INTP": 5, "ENTP": 6, "ISTP": 4, "ENTJ": 4, "ENFJ": 5, "ISTJ": 3, "ESFJ": 3},
        "测试工程师": {"ISFJ": 9, "ISTJ": 9, "INTP": 7, "INFJ": 6, "ISTP": 7, "INTJ": 5, "ENFJ": 4, "ISFP": 5, "ENTJ": 4, "ENFP": 3, "ESTJ": 5, "ESFJ": 5},
        "运维工程师": {"ISTJ": 9, "ISFJ": 8, "ISTP": 8, "INTJ": 6, "INTP": 6, "ESTJ": 6, "ENTJ": 4, "ENFP": 3, "ISFP": 4, "ESFP": 3, "INFJ": 4, "ENFJ": 3}
    }

    if not mbti_type or not job_title:
        return 5.0

    return job_mbti_suitability.get(job_title, {}).get(mbti_type.upper(), 5.0)
