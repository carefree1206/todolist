import streamlit as st
import requests
import json
import time

# 页面配置
st.set_page_config(
    page_title="AI对话助手",
    page_icon="🤖",
    layout="wide"
)

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 侧边栏配置
with st.sidebar:
    st.title("🤖 AI对话助手")
    st.subheader("配置")

    # API设置
    api_key = st.text_input("API密钥", type="password")
    api_url = st.text_input("API端点", value="https://api.openai.com/v1/chat/completions")

    # 模型参数
    temperature = st.slider("随机性", min_value=0.0, max_value=1.0, value=0.7)
    max_tokens = st.slider("最大生成长度", min_value=100, max_value=2000, value=500)

    # 清空对话历史
    if st.button("清空对话"):
        st.session_state.messages = []
        st.rerun()

# 主界面
st.title("💬 AI对话助手")
st.caption("与AI助手进行对话")

# 显示对话历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("请输入您的问题..."):
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)

    # 显示AI回复
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        # 模拟API调用（实际使用时替换为真实API调用）
        # 这里使用模拟的流式响应
        full_response = ""
        for chunk in simulate_api_call(prompt, st.session_state.messages):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.02)

        message_placeholder.markdown(full_response)

    # 添加AI回复到历史
    st.session_state.messages.append({"role": "assistant", "content": full_response})


# 模拟API调用函数（实际使用时替换为真实API调用）
def simulate_api_call(prompt, messages):
    """
    模拟API调用，实际使用时替换为真实的大模型API调用
    """
    # 模拟思考过程
    responses = [
        "让我思考一下您的问题...",
        f"您的问题是: {prompt}",
        "基于我的理解，我认为...",
        "这是一个很好的问题！",
        "让我为您详细解释一下..."
    ]

    # 根据问题生成长度适中的回复
    import random
    response_length = random.randint(3, 8)

    for i in range(response_length):
        if i < len(responses):
            yield responses[i] + " "
        else:
            yield f"这是回复的第{i + 1}部分。 "

    yield "\n\n如果您需要更多帮助，请告诉我！"


# 实际API调用函数示例（以OpenAI格式为例）
def call_ai_api(api_key, api_url, messages, temperature=0.7, max_tokens=500):
    """
    实际调用AI API的函数
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",  # 根据实际模型调整
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True  # 启用流式响应
    }

    try:
        response = requests.post(api_url, headers=headers, json=data, stream=True)

        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        line = line[6:]  # 移除"data: "前缀
                        if line.strip() != '[DONE]':
                            try:
                                json_response = json.loads(line)
                                if 'choices' in json_response and len(json_response['choices']) > 0:
                                    delta = json_response['choices'][0].get('delta', {})
                                    if 'content' in delta:
                                        yield delta['content']
                            except json.JSONDecodeError:
                                continue
        else:
            yield f"API调用失败，状态码: {response.status_code}"

    except Exception as e:
        yield f"发生错误: {str(e)}"


# 部署说明
st.sidebar.markdown("---")
st.sidebar.subheader("部署说明")
st.sidebar.info("""
1. 安装依赖: `pip install streamlit requests`
2. 运行应用: `streamlit run app.py`
3. 在浏览器中访问显示的URL
""")