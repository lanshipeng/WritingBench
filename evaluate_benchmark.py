import json
import os
import argparse
import jsonlines
from tqdm import tqdm
from prompt import evaluate_system, evaluate_prompt
from evaluator import ClaudeAgent, CriticAgent, QwenAgent

EVAL_TIMES = 1

class EvalAgent(object):
    def __init__(self, agent,query_criteria_map):
        self.agent = agent
        self.query_criteria_map = query_criteria_map
    def success_check_fn_score(self, response):
        try:
            result = json.loads(response.strip('json|```'))
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            return False
        
        valid_score_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        if "score" not in result or "reason" not in result:
            print("Missing 'score' or 'reason' in the result")
            return False
        if result["score"] not in valid_score_values:
            return False
        if not isinstance(result["reason"], str):
            return False
        return True


    def generate_score(self, content, query, criteria):
        prompt_data = {
            "query": query,
            "drama": content["drama"],
            "criteria": criteria,
        }
        retry = 0
        success = False
        while not success and retry < 3:
            prompt = evaluate_prompt.format(**prompt_data)
            response, success = self.agent.run(
                prompt=prompt,
                success_check_fn=self.success_check_fn_score
            )
            try:
                response = json.loads(response.strip('json|```'))
            except json.JSONDecodeError as e:
                print("JSON decode error:", e)
                response = eval(response.strip('json|```'))
            retry += 1
        if success:
            return response
        else:
            raise ValueError("Fail to generate score!")
    def evaluate(self, index, drama_content,progress_callback=None):
        content = {"index": index, "drama": drama_content}
                
        if index not in self.query_criteria_map:
            return {"error": "未知剧本类型"}
        
        query = self.query_criteria_map[index]['query']
        criteria = self.query_criteria_map[index]['criteria']

        data = {
            "index": index,
            "scores": {}
        }

        total_score = 0  # 总分累加器
        total_steps = len(criteria)*EVAL_TIMES
        current_step = 0
        # 添加总进度条（评估所有标准）
        with tqdm(total=len(criteria)*EVAL_TIMES, 
                desc=f"评估剧本类型 {index}", 
                unit="次") as pbar:
            
            for c in criteria:
                data["scores"][c["name"]] = []
                
                # 每个标准评估EVAL_TIMES次
                for _ in range(EVAL_TIMES):
                    score = self.generate_score(content, query, c)
                    data["scores"][c["name"]].append(score)
                    total_score += float(score["score"])  # 直接累加每次评分的分数
                    pbar.update(1)  # 更新进度条
                    current_step +=1
                    if progress_callback:
                        progress = current_step / total_steps
                        progress_callback(progress, desc=f"评估标准: {c['name']}")

        # 计算整体平均分（总分数 / 总评分次数）
        if criteria and EVAL_TIMES > 0:
            data["average_score"] = round(total_score / (len(criteria) * EVAL_TIMES), 1)

        return self.format_score_result(data)
    def format_score_result(self, score_data):
        html = f"""
        <div style='font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;'>
            <h2 style='color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 8px; margin-bottom: 20px;'>
                评分结果
            </h2>
            
            <!-- 平均分 -->
            <div style='margin-bottom: 30px;'>
                <h3 style='margin: 0 0 10px 0; font-size: 18px; color: #2c3e50;'>
                    Average Score: 
                    <span style='color: {"#e74c3c" if score_data["average_score"] < 5 else "#f39c12" if score_data["average_score"] < 8 else "#27ae60"};'>
                        {score_data["average_score"]}
                    </span>
                </h3>
                <h3 style='margin: 10px 0; font-size: 18px; color: #2c3e50;'>
                    Scoring Details
                </h3>
            </div>
        """
        
        for category, evaluation in score_data['scores'].items():
            score = evaluation[0]['score']
            reason = evaluation[0]['reason']
            
            color = "#e74c3c" if score < 5 else "#f39c12" if score < 8 else "#27ae60"
            
            html += f"""
            <div style='margin-bottom: 20px;'>
                <h4 style='margin: 0 0 5px 0; font-size: 16px; color: #2c3e50; font-weight: 600;'>{category}</h4>
                <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                    <span style='font-size: 15px; color: #7f8c8d;'>score: </span>
                    <span style='font-size: 18px; font-weight: bold; color: {color}; margin-left: 5px;'>
                        {score}
                    </span>
                </div>
                <div style='background: #f8f9fa; padding: 12px; border-radius: 4px;'>
                    <p style='margin: 0; color: #34495e; line-height: 1.5; font-size: 14px;'>{reason}</p>
                </div>
            </div>
            """
        
        html += "</div>"
        return html
def save_output(output, file_name):
    """
    Saves output data to a specified file in JSONL format.
    """
    with open(file_name, 'a', encoding='utf-8') as f:
        for record in output:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

def load_file(file_name):
    """
    Loads JSONL lines from a file into a list of dictionaries.
    """
    if os.path.isfile(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            records = [json.loads(line) for line in f]
            return records, len(records)
    return [], 0

def load_query_criteria(jsonl_file_path):
    """
    Loads criteria from a JSONL file into a dictionary.
    """
    data_list = {}
    subtype_list = []
    with jsonlines.open(jsonl_file_path) as reader:
        for obj in reader:
            data_list[obj['index']] = {}
            data_list[obj['index']]['query'] = obj['query']
            data_list[obj['index']]['criteria'] = obj['criteria']
            subtype_list.append({"desc": obj['subtype'], "index": obj['index']})
    return data_list,subtype_list

def process(agent, input_file, out_file, id_query_criteria_map):
    """
    Processes input files through the evaluation agent, producing scores and saving results.
    """
    records, existing_count = load_file(out_file)
    cnt = existing_count
    contents, input_cnt = load_file(input_file)
    with tqdm(total=input_cnt, initial=0, desc=f"Processing {input_file.split('/')[-1]}") as pbar:
        for i, content in enumerate(contents):
            if existing_count > 0 and i < existing_count - 1:
                pbar.update()
                continue
            
            data = {
                "index": content["index"],
                "scores": {}
            }

            query = id_query_criteria_map[content["index"]]['query']
            criteria = id_query_criteria_map[content["index"]]['criteria']

            with tqdm(total=len(criteria) * EVAL_TIMES, desc=f"Data ID {content['index']} Progress", leave=False) as internal_pbar:
                for c in criteria:
                    if c["name"] not in criteria:
                        data["scores"][c["name"]] = []
                    while len(data["scores"][c["name"]]) < EVAL_TIMES:
                        score = agent.generate_score(content, query, c)
                        data["scores"][c["name"]].append(score)
                        internal_pbar.update(1)

            save_output([data], out_file)
            cnt += 1
            pbar.update()

        print(f"CNT: {cnt}")

    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process lines from an input file.")
    parser.add_argument("--evaluator", choices=['claude', 'critic','qwen'], required=True, help="Choose the scoring model to use: 'claude' or 'critic'.")
    parser.add_argument("--query_criteria_file", type=str, help="Path to the query and criteria file.")
    parser.add_argument("--input_file", type=str, help="Path to the input file.")
    parser.add_argument("--output_file", type=str, help="Path to the output file.")

    args = parser.parse_args()

    # Evaluator initialization based on chosen model
    if args.evaluator == 'claude':
        agent = EvalAgent(ClaudeAgent(
            system_prompt=evaluate_system,
        ))
    elif args.evaluator == 'critic':
        agent = EvalAgent(CriticAgent(
            system_prompt=evaluate_system,
        ))
    elif args.evaluator == 'qwen':
        agent = EvalAgent(QwenAgent(
            system_prompt=evaluate_system, #"You are Qwen, a helpful assistant from Alibaba Cloud."
        ))

    id_query_criteria_map,_ = load_query_criteria(args.query_criteria_file)

    process(agent, args.input_file, args.output_file, id_query_criteria_map)
