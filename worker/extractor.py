"""
This file try find the code pattern from llm response
"""
import re

def Extractor(response: str) -> str:
    code_block_pattern = r'```(?:python)?\n?(.*?)```'
    matches = re.findall(code_block_pattern, response, re.DOTALL)
    
    if matches:
        return matches[0].strip()
    
    lines = response.split('\n')
    code_lines = []
    in_code = False
    
    for line in lines:
        if any(phrase in line.lower() for phrase in ['here is', 'here\'s', 'the code', 'solution:', 'answer:']):
            in_code = True
            continue
        
        if any(keyword in line for keyword in ['df[', 'df.', 'import ', 'pd.', 'np.', '=', 'def ', 'for ', 'if ']):
            in_code = True
        
        if in_code and line.strip():
            code_lines.append(line)
    
    return '\n'.join(code_lines) if code_lines else response.strip()