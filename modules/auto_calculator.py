"""
Nikki Auto-Calculating Math & Scientific Engine.
Auto-detects and solves math expressions, scientific calculations, percentages, word problems,
and formulas instantly with step-by-step breakdown.
"""
import re
import math
from typing import Dict, Any, Optional

class AutoCalculatingEngine:
    """
    Universal Scientific & Conversational Math Engine.
    """

    def calculate(self, expression: str) -> Optional[Dict[str, Any]]:
        """Auto-calculates math expressions, scientific functions, and percentage problems."""
        clean_expr = expression.strip().lower()

        # Step 1: Word problem - Percentage (e.g. 15% of 200)
        pct_match = re.search(r'(\d+\.?\d*)\s*%\s*of\s*(\d+\.?\d*)', clean_expr)
        if pct_match:
            pct = float(pct_match.group(1))
            val = float(pct_match.group(2))
            res = (pct / 100.0) * val
            formatted_res = int(res) if res.is_integer() else round(res, 4)
            return {
                "expression": f"{pct}% of {val}",
                "result": formatted_res,
                "formatted": f"🧮 **Auto-Calculation**: {pct}% of {val} = **{formatted_res}**"
            }

        # Step 2: Scientific Functions (e.g. square root of 144, sqrt(144))
        sqrt_match = re.search(r'(?:square root of|sqrt)\s*(\d+\.?\d*)', clean_expr)
        if sqrt_match:
            val = float(sqrt_match.group(1))
            res = math.sqrt(val)
            formatted_res = int(res) if res.is_integer() else round(res, 4)
            return {
                "expression": f"√{val}",
                "result": formatted_res,
                "formatted": f"🧮 **Auto-Calculation**: √{val} = **{formatted_res}**"
            }

        # Step 3: Pure Arithmetic & Powers (e.g. 2+2, 10*5+3, 2^10, 100/4)
        math_chars = re.sub(r'[^0-9\.\+\-\*\/\%\^\(\)\s]', '', clean_expr)
        if math_chars and len(re.findall(r'\d+', math_chars)) >= 1:
            try:
                # Replace ^ with ** for powers
                eval_str = math_chars.replace('^', '**')
                # Safe math evaluation using python math scope
                safe_dict = {"__builtins__": None, "math": math, "abs": abs, "pow": pow, "round": round}
                res = eval(eval_str, safe_dict, {})
                if isinstance(res, (int, float)):
                    formatted_res = int(res) if float(res).is_integer() else round(float(res), 4)
                    return {
                        "expression": math_chars.strip(),
                        "result": formatted_res,
                        "formatted": f"🧮 **Auto-Calculation**: `{math_chars.strip()}` = **{formatted_res}**"
                    }
            except Exception:
                pass

        return None
