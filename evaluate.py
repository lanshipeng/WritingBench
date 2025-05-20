import gradio as gr
import argparse
import os
import PyPDF2
from docx import Document
from evaluate_benchmark import EvalAgent
from evaluator import QwenAgent
from prompt import evaluate_system
from evaluate_benchmark import load_query_criteria

# 模型列表
MODEL_OPTIONS = ["qwen-plus","qwen-plus-latest","deepseek-v3","deepseek-r1","qwen-turbo", "qwen-long","qwen-max-latest","qwen3-235b-a22b","qwen3-32b","qwen2.5-7b-instruct",
                 "qwen2.5-32b-instruct","qwen2.5-72b-instruct","llama3.1-8b-instruct","llama-4-maverick-17b-128e-instruct","llama-4-scout-17b-16e-instruct"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process lines from an input file.")
    parser.add_argument("--ak", type=str, required=True, help="Qwen API Key")
    args = parser.parse_args()

    # 加载评分维度配置
    query_criteria_map, subtype_choices = load_query_criteria("criteria.jsonl")
    drama_map = {item["desc"]: item["index"] for item in subtype_choices}

    with gr.Blocks() as demo:
        gr.Markdown("### 🎬AI剧本评分")

        with gr.Row():
            drama_desc = gr.Dropdown(
                choices=[item["desc"] for item in subtype_choices],
                label="选择剧本类型",
                value=subtype_choices[0]["desc"] if subtype_choices else None
            )
            model_selector = gr.Dropdown(
                choices=MODEL_OPTIONS,
                label="model",
                value=MODEL_OPTIONS[0]
            )

        with gr.Row():
            drama_content = gr.Textbox(lines=10, label="请输入剧本内容", interactive=True)
            file_input = gr.File(label="上传剧本文件（支持 .txt | .docx | .pdf）", file_types=[".txt", ".docx", ".pdf"])

        output = gr.HTML()
        submit_btn = gr.Button("提交评分")

        def load_file(file):
            if file is None:
                return ""
            ext = os.path.splitext(file.name)[-1].lower()
            try:
                if ext == ".txt":
                    with open(file.name, "r", encoding="utf-8") as f:
                        return f.read()
                elif ext == ".docx":
                    doc = Document(file.name)
                    return "\n".join([para.text for para in doc.paragraphs])
                elif ext == ".pdf":
                    reader = PyPDF2.PdfReader(file.name)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
                    return text
            except Exception as e:
                return f"文件解析失败: {e}"
            return "不支持的文件类型"

        def evaluate(drama_desc, content, model_name,progress=gr.Progress()):
            print("model:", model_name)
            
            progress(0.0, desc="准备评估参数...")
            drama_desc = drama_map.get(drama_desc)
            
            progress(0.0, desc="初始化AI模型...")
            agent = EvalAgent(QwenAgent(system_prompt=evaluate_system, api_key=args.ak, model=model_name), query_criteria_map)
            
            def progress_callback(prog, desc):
                progress(prog, desc=desc)
            
            # 执行评估
            progress(0, desc="开始评估...")
            result = agent.evaluate(drama_desc, content, progress_callback)
            
            progress(1.0, desc="评估完成")
            return result

        file_input.change(
            fn=load_file,
            inputs=file_input,
            outputs=drama_content
        )

        submit_btn.click(
            fn=evaluate,
            inputs=[drama_desc, drama_content, model_selector],
            outputs=output
        )

    demo.launch(server_name="0.0.0.0", server_port=7860)
