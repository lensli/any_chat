
import base64,os
def get_image_absolute_path() -> str:
    # 获取当前文件（logo_html.py）的绝对路径
    current_file_path = os.path.abspath(__file__)
    # 确定项目根目录（假设 'modules' 是固定的根目录名），计算根目录绝对路径
    project_root = current_file_path.split(os.sep + 'modules' + os.sep)[0]
    # 图片的相对路径于 modules 文件夹
    relative_image_path = os.path.join('modules', 'customer', 'dlm', 'dlm-ico-192.png')
    # 计算图片的绝对路径
    image_absolute_path = os.path.join(project_root, relative_image_path)
    return image_absolute_path

def image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def generate_inline_logo_html(image_path: str, alt_text: str = "Logo") -> str:
    base64_image = image_to_base64(image_path)
    html = f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{base64_image}" alt="{alt_text}" style="max-width: 100%; height: auto;">
    </div>
    """
    return html
# Example usage:
image_path = get_image_absolute_path()
logo_html = generate_inline_logo_html(image_path, alt_text="请输入账号密码")
