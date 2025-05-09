import gradio as gr
import argparse
from evaluate_benchmark import EvalAgent
from evaluator import QwenAgent
from prompt import evaluate_system
from evaluate_benchmark import load_query_criteria

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process lines from an input file.")
    parser.add_argument("--ak", type=str,required=True, help="qwen ak.")

    args = parser.parse_args()

    # 加载类型配置
    query_criteria_map, subtype_choices = load_query_criteria("criteria.jsonl")
    agent = EvalAgent(QwenAgent(system_prompt=evaluate_system,api_key=args.ak), query_criteria_map)

    print("剧本类型配置：", subtype_choices)

    # 创建 label -> value 的映射
    label_value_map = {item["label"]: item["value"] for item in subtype_choices}

    with gr.Blocks() as demo:
        gr.Markdown("### AI评分")

        # 下拉菜单显示 label，但实际存储 value
        label = gr.Dropdown(
            choices=[item["label"] for item in subtype_choices],  # 显示 label
            label="选择剧本类型",
            value=subtype_choices[0]["label"] if subtype_choices else None  # 默认选中第一个
        )

        drama_content = gr.Textbox(lines=10, label="请输入剧本内容")
        # output = gr.Textbox(label="评分结果", lines=4)
        output = gr.HTML()
        submit_btn = gr.Button("提交评分")
        
        def label_to_value(label, content):
            """将用户选择的 label 转换为 value 再提交"""
            value = label_value_map.get(label)
            return agent.evaluate_script(value, content)
        
        submit_btn.click(
            fn=label_to_value,
            inputs=[label, drama_content],
            outputs=output
        )

    demo.launch()