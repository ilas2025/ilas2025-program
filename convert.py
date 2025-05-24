import pypandoc
import pandas as pd
def convert_latex_to_markdown(latex_str):
    """
    Convert LaTeX string to Markdown using pypandoc.
    """
    try:
        # Attempt to convert the LaTeX string to Markdown
        return pypandoc.convert_text(latex_str, 'markdown', format='latex')
    except:
        return f"Conversion error, original LaTeX retained: {latex_str}"
srp_df=pd.read_csv("srp-full.csv")
srp_df['ABSTRACT'] = srp_df['ABSTRACT'].apply(convert_latex_to_markdown)
srp_df.to_csv("srp-full-converted.csv", index=False)
