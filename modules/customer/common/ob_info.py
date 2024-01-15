"ChuanhuChatbot.py"   
 #服务器启动时 设置初始状态 适用与所有用户
    demo.load(create_greeting, inputs=None, outputs=[
              user_info, user_name, current_model, like_dislike_area, saveFileName, systemPromptTxt, chatbot, single_turn_checkbox, temperature_slider, top_p_slider, n_choices_slider, stop_sequence_txt, max_context_length_slider, max_generation_slider, presence_penalty_slider, frequency_penalty_slider, logit_bias_txt, user_identifier_txt, historySelectList], api_name="load")
#模型切换时 
model_select_dropdown.change(get_model, [model_select_dropdown, lora_select_dropdown, user_api_key, temperature_slider, top_p_slider, systemPromptTxt, user_name, current_model], [
                                 current_model, status_display, chatbot, lora_select_dropdown, user_api_key, keyTxt], show_progress=True, api_name="get_model")

#推理函数输入 输出
chatgpt_predict_args = dict(
    fn=predict,
    inputs=[
        current_model,
        user_question,
        chatbot,
        use_streaming_checkbox,
        use_websearch_checkbox,
        index_files,
        language_select_dropdown,
    ],
    outputs=[chatbot, status_display],
    show_progress=True,
)
#模型显示