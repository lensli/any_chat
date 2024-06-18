import logging,os,sys
sys.path.insert(0,os.path.dirname(__file__))
import gradio as gr
from lib.login import user_login
import logging,time
from database import User_Db    


def getuser_info(user_name,request: gr.Request):
    
    if hasattr(request, "username") and request.username:  # is not None or is not ""
        logging.info(f"Get User Name: {request.username}")
        user_name = request.username
        return user_name
def update_database(user_name,dropdown,password, consumption, recharge, reset_times, use_costs, limit_costs, enable_models, ip_whitelist):
                              
    # 这里应该是更新数据库的逻辑
    # 比如，使用SQL语句更新相应的数据库记录
    # 为简化演示，这里仅打印输入值
    if "加载中..." in dropdown:
        return "请点击“获取所有子用户”"
    enable_models_str = ', '.join(enable_models)
    show_result = ''''''
    if "all" in dropdown:
        updated_options = get_user_for_db(user_name)
        dropdown = updated_options
     
    for user_name in dropdown:
        udb =User_Db()

        results = udb.update_user_info(user_name, password, consumption, recharge, reset_times, use_costs, limit_costs, enable_models_str, ip_whitelist)
        udb.__del__()
        result = results[0]
        show_result = show_result + f'''
"账号",{result[0]}
"密码:", {result[1]}
"总花费:", {result[2]}
"充值总数:", {result[3]}
"频率限制时间间隔:", {result[4]}
"频率限制内以花费:", {result[5]}
"频率限制周期内额度:", {result[6]}
"允许模型:", {result[7]}
"IP白名单:", {result[8]}

        '''

    return show_result  # 假设数据库更新成功



def get_user_for_db(username):

    udb = User_Db()
    results = udb.get_sub_username(username)
    if results is None:
        return []
    first_elements = [item[0] for table in [results] for item in table]
    udb.__del__()

    # 根据需要来更新和获取下拉列表的选项
    # 为了简化，这里返回一个固定的选项列表，实际使用中，这里可以是从数据库动态获取的数据
    return first_elements

def refresh_dropdown(request: gr.Request):
    
    # 这个函数被用来刷新下拉列表的选项
    # 它调用 get_options_for_user() 来获取更新后的选项列表并返回
    updated_options = get_user_for_db(request.username)
    updated_options.insert(0, "all")
      # 更新 Dropdown 组件的选项
    return gr.Dropdown.update(choices=updated_options)
def delee_database_data(dropdown):
    show_txt = ""
    for user_name in dropdown:
        udb = User_Db()
        result = udb.delete_user_by_username(user_name)
        show_txt += result+"\n"

    return show_txt
def add_database_data(add_user,admin_name):
    df_remaining = add_user.iloc[:]
    # 使用values和tolist将DataFrame转换为列表
    list_data = df_remaining.values.tolist()
    show_text = ""
    for username,password,recharge,reset_times,limit_costs,enable_models, ip_whitelist in list_data:
        print(username,password,recharge,reset_times,limit_costs,enable_models, ip_whitelist)
        sql_data = [username,password,0,recharge,reset_times,0,limit_costs,None,enable_models,admin_name,ip_whitelist]
        udb = User_Db()
        result = udb.insert_users(sql_data)
        show_text += result
        udb.__del__()

    return show_text

with gr.Blocks() as demo:
    gr.Markdown("后台管理系统")
    user_name = gr.Textbox("", visible=False)

    with gr.Row():
        dropdown = gr.Dropdown(label="请选择,可多选", choices=["加载中..."], multiselect=True)
        refresh_button = gr.Button("获取所有子用户")
    refresh_button.click(refresh_dropdown, inputs= None, outputs=dropdown)
    with gr.Tab("配置子用户"):


        gr.Markdown('"不更改"和 "-1"表示不更改')

        with gr.Row():
            password = gr.Textbox(label="重置密码为",value="不更改")
            consumption = gr.Number(label="总花费",value=-1)
            recharge = gr.Number(label="充值总数",value=-1)
            reset_times = gr.Number(label="频率限制时间间隔",value=-1)
            use_costs = gr.Number(label="频率限制内以花费",value=-1)
            limit_costs = gr.Number(label="频率限制周期内额度",value=-1)

        enable_models = gr.CheckboxGroup(label="可用模型", choices=["all","不更改"],value = "不更改")
        ip_whitelist = gr.Textbox(label="IP白名单",value="不更改")
        submit_button = gr.Button("更改用户数据")

        submit_button.click(
            fn=update_database, 
            inputs=[user_name,dropdown,password, consumption, recharge, reset_times, use_costs, limit_costs, enable_models, ip_whitelist],
            outputs=gr.Textbox(label="更改的数据")
        )

    with gr.Tab("注册子用户"):
        add_user = gr.Dataframe(
            headers=["用户名", "密码","充值总数","频率限制时间","频率限制周期内额度","可用模型","ip白名单"],
            datatype=["str","str", "number","number","number","str","str",],
            label="用户批量注册",
            col_count = (7,"fixed"),
            height = "1000",
            value = [["user01","123456",50,3600,5,"all","all"]]
        )
        add_button = gr.Button("批量注册子用户")

        add_button.click(fn= add_database_data,inputs= [add_user,user_name],outputs=[gr.Textbox(label="增加的用户")])
        gr.Examples(
            inputs=[add_user],
            examples=[
            [[
                # ["用户名", "密码","充值总数","频率限制时间","频率限制周期内额度","可用模型","ip白名单"], 
                ["user01","123456",50,3600,5,"all","all"],
                ["user02","123456",50,3600,5,"all","all"],
                ["user03","123456",50,3600,5,"all","all"],
                ["user04","123456",50,3600,5,"all","all"],
                ["user05","123456",50,3600,5,"all","all"],
                ["user06","123456",50,3600,5,"all","all"],
            ]],
            ]

        )

        pass
    with gr.Tab("删除子用户"):

        delete_button = gr.Button("删除所选子用户")

        delete_button.click(
            fn = delee_database_data,inputs = [dropdown],outputs=[gr.Textbox(label="删除的用户")]
        )


    demo.load( getuser_info, inputs=[user_name], outputs=[user_name])
if __name__ == "__main__":
    CONCURRENT_COUNT = 100
    server_name = "0.0.0.0"
    server_port = 9093
    demo.queue(concurrency_count=CONCURRENT_COUNT).launch(
        server_name=server_name,
        server_port=server_port,
        share=False,
        auth=user_login,
        auth_message = "后台管理系统登录",

    )