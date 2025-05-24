import pypandoc
import pandas as pd
def convert_latex_to_html(latex_content):
    """
    Convert LaTeX content to HTML using pypandoc.
    
    :param latex_content: str, LaTeX content to convert
    :return: str, converted HTML content
    """
    try:
        html_content = pypandoc.convert_text(latex_content, 'html', format='latex')
        return html_content
    except Exception as e:
        print(f"Error converting LaTeX to HTML: {e}")
        return None
srp_df=pd.read_csv("srp-full.csv")
srp_df['ABSTRACT'] = srp_df['ABSTRACT'].apply(convert_latex_to_html)
srp_df.to_csv("srp-full-converted.csv", index=False)
