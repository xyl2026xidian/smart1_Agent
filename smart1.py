# ============================================================
# 文件名: module1_intro.py
# 说明: 智能制造工程导论 - 模块一 智能学习交互页面
# 功能: 3D知识图谱 + 深度交互 + 趣味匹配 + 成就系统
# 运行: streamlit run module1_intro.py
# ============================================================

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import time

st.set_page_config(
    page_title="模块一 · 智能制造导论",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================= 自定义CSS =======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .main-header { font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #1a3a5c, #4a90d9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 5px; }
    .sub-header { font-size: 1.1rem; color: #6c757d; text-align: center; margin-bottom: 20px; }
    .glow-card { background: linear-gradient(135deg, #ffffff, #f8f9fa); border-radius: 16px; padding: 20px; box-shadow: 0 8px 30px rgba(0,0,0,0.08); border: 1px solid rgba(255,255,255,0.5); transition: transform 0.3s ease; }
    .glow-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(26,58,92,0.15); }
    .badge { display: inline-block; background: linear-gradient(135deg, #ffd700, #ffb300); color: #1a3a5c; padding: 4px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }
    .knowledge-detail { background: linear-gradient(135deg, #f0f4f8, #e8f0fe); border-radius: 12px; padding: 20px; border-left: 4px solid #2c5f8a; margin: 10px 0; }
    .knowledge-detail h4 { color: #1a3a5c; margin-top: 0; }
    .knowledge-detail .tag { display: inline-block; background: #2c5f8a; color: white; padding: 2px 12px; border-radius: 12px; font-size: 0.7rem; margin-right: 6px; }
    .match-card { background: white; border-radius: 12px; padding: 15px; border: 2px solid #e9ecef; text-align: center; cursor: pointer; transition: all 0.3s; }
    .match-card:hover { border-color: #2c5f8a; transform: scale(1.02); }
    .match-card.selected { border-color: #2c5f8a; background: #e8f4fd; }
    .match-card.matched { border-color: #28a745; background: #e6f7e6; }
    .achievement { background: linear-gradient(135deg, #fff8e1, #fff3cd); border-radius: 12px; padding: 12px; border: 1px solid #ffd700; text-align: center; }
    .stButton>button { background: linear-gradient(135deg, #1a3a5c, #2c5f8a); color: white; border: none; border-radius: 10px; padding: 10px 24px; font-weight: 600; transition: all 0.3s; }
    .stButton>button:hover { transform: scale(1.03); box-shadow: 0 6px 20px rgba(26,58,92,0.3); }
</style>
""", unsafe_allow_html=True)

# ======================= 会话状态初始化 =======================
if 'module1_progress' not in st.session_state:
    st.session_state.module1_progress = 0
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'matched_pairs' not in st.session_state:
    st.session_state.matched_pairs = []
if 'selected_card' not in st.session_state:
    st.session_state.selected_card = None
if 'interest_score' not in st.session_state:
    st.session_state.interest_score = 0
if 'explored_nodes' not in st.session_state:
    st.session_state.explored_nodes = set()
if 'selected_knowledge' not in st.session_state:
    st.session_state.selected_knowledge = None

# ======================= 详细知识库 =======================
KNOWLEDGE_DETAILS = {
    "HCPS": {
        "label": "HCPS 人-信息-物理系统",
        "emoji": "🧠",
        "desc": "智能制造的核心理论框架，强调人、信息系统、物理系统的深度融合与协同。",
        "key_points": [
            "人 (Human)：包含操作者、管理者、设计者等，是系统的决策核心",
            "信息 (Cyber)：包含数据、知识、算法、模型，是系统的智慧大脑",
            "物理 (Physical)：包含设备、工件、产线等，是系统的执行身躯"
        ],
        "application": "智能工厂设计、人机协作优化、制造系统架构规划",
        "analogy": "就像人体：大脑（信息）指挥手脚（物理）行动，人（Human）作为整体协调。",
        "related": ["数字孪生", "工业互联网", "边缘计算"],
        "color": "#FF6B6B"
    },
    "数字化": {
        "label": "📊 数字化技术",
        "emoji": "💻",
        "desc": "将物理世界转化为数字信息，让制造过程变得可计算、可存储、可传输。",
        "key_points": [
            "数字建模：CAD/CAE/CAM 将产品数字化",
            "数据采集：传感器将物理量转为数字信号",
            "数字主线：打通设计-制造-运维全流程数据"
        ],
        "application": "产品设计仿真、工艺规划、BOM管理、数字孪生底座",
        "analogy": "就像把一本书从纸质版变成电子版，可以复制、搜索、传输、分析。",
        "related": ["数字孪生", "数字主线", "BOM"],
        "color": "#4ECDC4"
    },
    "网络化": {
        "label": "🌐 网络化技术",
        "emoji": "📡",
        "desc": "将设备、系统、人员通过工业网络互联，让制造资源可协同、可调度。",
        "key_points": [
            "设备联网：PLC、传感器、机器人通过工业以太网互联",
            "数据互通：OPC UA、MQTT 等协议实现跨系统数据交换",
            "协同制造：实现跨车间、跨工厂的资源调度"
        ],
        "application": "MES/ERP集成、远程监控、AGV调度、供应链协同",
        "analogy": "就像城市的交通网络，车辆（设备）通过道路（网络）互联互通。",
        "related": ["工业互联网", "MES", "边缘计算"],
        "color": "#45B7D1"
    },
    "智能化": {
        "label": "🧠 智能化技术",
        "emoji": "🤖",
        "desc": "利用人工智能技术让制造系统具备感知、学习、决策、优化的能力。",
        "key_points": [
            "感知：机器视觉、传感器融合",
            "决策：AI模型分析数据并给出决策",
            "优化：持续学习使系统性能不断提升"
        ],
        "application": "智能质检、预测性维护、工艺参数优化、智能排产",
        "analogy": "就像让工厂有了一个会思考的大脑，能自己发现问题、解决问题。",
        "related": ["机器学习", "大模型", "机器视觉"],
        "color": "#96CEB4"
    },
    "机器人": {
        "label": "🤖 智能装备",
        "emoji": "🦾",
        "desc": "工业机器人、数控机床、AGV 等智能装备是智能制造的物理执行层。",
        "key_points": [
            "工业机器人：焊接、装配、搬运、喷涂",
            "数控机床：精密加工、五轴联动",
            "AGV/AMR：自主移动、柔性物流"
        ],
        "application": "汽车焊装线、3C装配、零部件加工、智能仓储物流",
        "analogy": "就像人的双手和双脚，执行大脑（信息系统）下达的指令。",
        "related": ["PLC", "SCADA", "边缘计算"],
        "color": "#FFEAA7"
    },
    "数字孪生": {
        "label": "🔄 数字孪生",
        "emoji": "🔄",
        "desc": "在虚拟空间中创建物理实体的高保真数字化镜像，实现双向映射与实时交互。",
        "key_points": [
            "高保真建模：精确还原物理实体的几何、物理、行为属性",
            "实时映射：传感器数据驱动虚拟模型同步更新",
            "闭环优化：虚拟分析结果反馈到物理实体进行优化"
        ],
        "application": "产线虚拟调试、设备预测性维护、加工过程仿真、虚拟培训",
        "analogy": "就像有一个和现实世界完全一样的'平行宇宙'，可以在里面先试错。",
        "related": ["数字主线", "工业互联网", "仿真"],
        "color": "#DDA0DD"
    },
    "工业互联网": {
        "label": "🌐 工业互联网",
        "emoji": "🌐",
        "desc": "将工业设备、系统、人员通过物联网和互联网连接，实现数据采集、分析、优化的基础设施。",
        "key_points": [
            "平台架构：边缘层 → IaaS → PaaS → SaaS",
            "标识解析：赋予每个工业设备一个唯一身份",
            "数据中台：汇聚、治理、分析海量工业数据"
        ],
        "application": "设备状态监控、预测性维护、产业链协同、能耗管理",
        "analogy": "就像工业的'神经系统'，感知每个节点的状态并做出协调。",
        "related": ["边缘计算", "5G", "MES"],
        "color": "#87CEEB"
    },
    "人工智能": {
        "label": "🧠 人工智能",
        "emoji": "🧠",
        "desc": "利用深度学习、大模型等技术，赋予制造系统理解、推理、生成和自主决策能力。",
        "key_points": [
            "大模型：工业知识问答、智能排产、代码生成",
            "智能体：自主感知环境、规划任务、调用工具",
            "机器视觉：缺陷检测、尺寸测量、机器人引导"
        ],
        "application": "AI质检、智能调度、知识管理、设备预测性维护",
        "analogy": "就像给工厂装了一个'智慧大脑'，能理解复杂情况并做出正确决策。",
        "related": ["大模型", "智能体", "机器视觉"],
        "color": "#F0A0A0"
    }
}

# ======================= 匹配游戏数据 =======================
MATCH_PAIRS = [
    ("HCPS", "人-信息-物理系统"),
    ("数字孪生", "物理-虚拟双向映射"),
    ("工业互联网", "设备联网协同制造"),
    ("数字化", "物理→数字可计算"),
    ("智能化", "数据驱动智能决策"),
]

# ======================= 主界面 =======================
st.markdown('<div class="main-header">🚀 智能制造 · 探索之旅</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">模块一：从机械制造到智能制造的范式跃迁</div>', unsafe_allow_html=True)

# ===== 顶部状态栏 =====
col_status1, col_status2, col_status3, col_status4 = st.columns(4)
with col_status1:
    progress_pct = min(100, int(st.session_state.module1_progress / len(KNOWLEDGE_DETAILS) * 100))
    st.markdown(f"📊 **探索进度**  \n{progress_pct}%")
    st.progress(progress_pct/100)
with col_status2:
    st.markdown(f"🏆 **成就**  \n{len(st.session_state.achievements)} 个")
with col_status3:
    st.markdown(f"⭐ **兴趣分**  \n{st.session_state.interest_score}")
with col_status4:
    st.markdown(f"💡 **已探索**  \n{len(st.session_state.explored_nodes)}/{len(KNOWLEDGE_DETAILS)}")

st.markdown("---")

# ===== 知识详情展示区（点击节点后弹出） =====
if st.session_state.selected_knowledge:
    node_id = st.session_state.selected_knowledge
    info = KNOWLEDGE_DETAILS[node_id]
    
    st.markdown(f"""
    <div class="knowledge-detail" style="border-left-color:{info['color']};">
        <h4>{info['emoji']} {info['label']}</h4>
        <p style="font-size:1.05rem;color:#1a3a5c;font-weight:500;">{info['desc']}</p>
        <div style="margin:10px 0;">
            <span class="tag">核心要点</span>
        </div>
        <ul style="margin:8px 0 12px 20px;">
            {''.join([f'<li>{p}</li>' for p in info['key_points']])}
        </ul>
        <div style="background:white;border-radius:8px;padding:12px;margin:8px 0;">
            <strong>🏭 应用场景：</strong> {info['application']}
        </div>
        <div style="background:#f0f4f8;border-radius:8px;padding:12px;margin:8px 0;">
            <strong>💡 趣味类比：</strong> {info['analogy']}
        </div>
        <div style="margin-top:8px;">
            <strong>🔗 关联术语：</strong>
            {''.join([f'<span style="display:inline-block;background:#e9ecef;padding:2px 12px;border-radius:12px;margin:2px 4px;font-size:0.8rem;">{t}</span>' for t in info['related']])}
        </div>
        <div style="margin-top:12px;">
            <span class="badge">已探索 ✓</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("✕ 关闭详情", use_container_width=True):
        st.session_state.selected_knowledge = None
        st.rerun()
    
    st.markdown("---")

# ===== 主布局：3D知识星球 =====
st.markdown("### 🌍 点击下方节点，探索智能制造的核心概念")
st.markdown("*每个节点包含详细定义、核心要点、应用场景和趣味类比*")

# 3D 知识星球
fig = go.Figure()

node_ids = list(KNOWLEDGE_DETAILS.keys())
x_vals = [-2, 2, -1.5, 1.5, 0, -1.2, 1.2, 0]
y_vals = [2, 1, 1, 0, 0, -1, -1.2, -0.8]
z_vals = [0, 0.5, -0.3, 1.2, -1, 0.8, -0.5, -1.2]
labels = [KNOWLEDGE_DETAILS[n]["label"] for n in node_ids]
colors = [KNOWLEDGE_DETAILS[n]["color"] for n in node_ids]
emojis = [KNOWLEDGE_DETAILS[n]["emoji"] for n in node_ids]

# 连线
for i in range(len(node_ids)):
    for j in range(i+1, len(node_ids)):
        if np.random.random() > 0.5:
            fig.add_trace(go.Scatter3d(
                x=[x_vals[i], x_vals[j]],
                y=[y_vals[i], y_vals[j]],
                z=[z_vals[i], z_vals[j]],
                mode='lines',
                line=dict(color='rgba(200,200,200,0.3)', width=1),
                showlegend=False,
                hoverinfo='none'
            ))

# 节点
fig.add_trace(go.Scatter3d(
    x=x_vals,
    y=y_vals,
    z=z_vals,
    mode='markers+text',
    marker=dict(
        size=30,
        color=colors,
        symbol='circle',
        line=dict(color='white', width=2),
        opacity=0.9
    ),
    text=[f"{e} {l}" for e, l in zip(emojis, labels)],
    textposition='top center',
    textfont=dict(size=9, color='#1a3a5c', family='Inter'),
    hoverinfo='text',
    hovertext=[KNOWLEDGE_DETAILS[n]["desc"] for n in node_ids],
    customdata=node_ids,
    name='知识节点'
))

fig.update_layout(
    scene=dict(
        xaxis=dict(showbackground=False, showgrid=False, showticklabels=False, title=''),
        yaxis=dict(showbackground=False, showgrid=False, showticklabels=False, title=''),
        zaxis=dict(showbackground=False, showgrid=False, showticklabels=False, title=''),
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
    ),
    height=400,
    margin=dict(l=0, r=0, t=0, b=0),
    showlegend=False,
    hovermode='closest'
)

st.plotly_chart(fig, use_container_width=True, key='knowledge_graph')

# ===== 节点按钮网格 =====
st.markdown("**📌 点击下方卡片深入了解每个概念**")
cols = st.columns(4)
for i, node_id in enumerate(node_ids[:8]):
    with cols[i % 4]:
        info = KNOWLEDGE_DETAILS[node_id]
        is_explored = node_id in st.session_state.explored_nodes
        btn_label = f"{info['emoji']} {info['label'][:12]}"
        if st.button(btn_label, key=f"detail_{node_id}", use_container_width=True):
            st.session_state.selected_knowledge = node_id
            if not is_explored:
                st.session_state.explored_nodes.add(node_id)
                st.session_state.module1_progress = len(st.session_state.explored_nodes)
                st.session_state.interest_score += 5
                if len(st.session_state.explored_nodes) >= 3 and "探索者" not in st.session_state.achievements:
                    st.session_state.achievements.append("探索者")
                if len(st.session_state.explored_nodes) >= 6 and "知识猎人" not in st.session_state.achievements:
                    st.session_state.achievements.append("知识猎人")
            st.rerun()

st.caption("💡 点击任意卡片展开详细知识卡片 | 每探索一个新概念 +5 兴趣分")

# ===== 右侧：成就面板 =====
st.markdown("---")
col_achievement, col_match = st.columns([1, 2])

with col_achievement:
    st.markdown("### 🏅 成就徽章")
    if st.session_state.achievements:
        for a in st.session_state.achievements:
            st.markdown(f"""
            <div class="achievement">
                🎖️ <strong>{a}</strong>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center;color:#adb5bd;padding:20px;">
            <div style="font-size:3rem;">🔒</div>
            <p>探索3个节点解锁「探索者」</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔥 学习热度")
    heat = min(100, st.session_state.interest_score * 2)
    st.metric("", f"{min(100, heat)}%")
    st.caption("探索新概念 +5 分 | 匹配成功 +10 分")

# ===== 匹配挑战 =====
with col_match:
    st.markdown("### 🧩 知识匹配挑战")
    st.markdown("*将左侧术语与右侧定义配对*")
    
    col_match_left, col_match_right = st.columns(2)
    
    with col_match_left:
        st.markdown("**📌 术语**")
        terms = [p[0] for p in MATCH_PAIRS if p not in st.session_state.matched_pairs]
        for term in terms:
            if st.button(f"选择 {term}", key=f"sel_{term}", use_container_width=True):
                if term not in [p[0] for p in st.session_state.matched_pairs]:
                    st.session_state.selected_card = term
                    st.rerun()
    
    with col_match_right:
        st.markdown("**📖 定义**")
        for term, defin in MATCH_PAIRS:
            if [term, defin] not in st.session_state.matched_pairs:
                if st.button(f"配对: {defin}", key=f"match_{term}", use_container_width=True):
                    if st.session_state.selected_card == term:
                        st.session_state.matched_pairs.append([term, defin])
                        st.session_state.interest_score += 10
                        st.session_state.selected_card = None
                        if len(st.session_state.matched_pairs) >= 3 and "匹配新星" not in st.session_state.achievements:
                            st.session_state.achievements.append("匹配新星")
                        if len(st.session_state.matched_pairs) == len(MATCH_PAIRS):
                            st.session_state.achievements.append("匹配大师")
                        st.rerun()
                    else:
                        st.warning("请先选择对应的术语！")
    
    if st.session_state.matched_pairs:
        st.markdown("**✅ 已匹配：**")
        matched_text = ", ".join([f"{p[0]} ↔ {p[1]}" for p in st.session_state.matched_pairs])
        st.markdown(f"<div style='background:#e6f7e6;padding:10px;border-radius:8px;'>{matched_text}</div>", unsafe_allow_html=True)
        if len(st.session_state.matched_pairs) == len(MATCH_PAIRS):
            st.success("🎉 全部匹配成功！")

# ===== 学习总结 =====
st.markdown("---")
with st.expander("📝 学习总结与思考", expanded=False):
    st.markdown("""
    ### 🎯 核心概念回顾
    - **智能制造** = 数字化 + 网络化 + 智能化 与制造技术的深度融合
    - **HCPS** = 人-信息-物理系统，是智能制造的核心理论框架
    - **三大赋能技术**：数字化（可计算）、网络化（可连接）、智能化（可思考）
    
    ### 🏭 智能装备与系统
    - **智能装备**：工业机器人、数控机床、AGV/AMR
    - **数字孪生**：物理-虚拟双向映射，实时交互与优化
    - **工业互联网**：设备联网、数据中台、协同制造
    """)
    feedback = st.text_area("💬 你的学习感悟", placeholder="今天学到了什么？有什么疑问？")
    if feedback:
        st.success("📝 已记录！继续加油！🚀")