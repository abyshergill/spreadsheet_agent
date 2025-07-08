import pandas as pd
from typing import Optional,Any
import traceback

from .validator import Validator

def Executor(code: str, df: pd.DataFrame) -> tuple[Optional[pd.DataFrame], Optional[str], Optional[Any]]:
    is_safe, safety_msg = Validator(code)
    if not is_safe:
        return None, safety_msg, None
    
    safe_globals = {
        'pd': pd,
        'pandas': pd,
        'df': df.copy()
    }
    
    try:
        import numpy as np
        safe_globals['np'] = np
        safe_globals['numpy'] = np
    except ImportError:
        pass
    
    try:
        exec(code, safe_globals)  
        result_df = safe_globals.get('df')
        result_var = None
        for var_name in ['result', 'output', 'new_df']:
            if var_name in safe_globals:
                result_var = safe_globals[var_name]
                break
        
        return result_df, None, result_var
        
    except Exception as e:
        return None, f"Execution error: {str(e)}\n\n{traceback.format_exc()}", None