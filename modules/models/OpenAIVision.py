from __future__ import annotations

import json
import logging
import traceback
import base64
from math import ceil

import colorama
import requests
from io import BytesIO
import uuid

import requests
from PIL import Image

from .. import shared
from ..config import retrieve_proxy, sensitive_id, usage_limit
from ..index_func import *
from ..presets import *
from ..utils import *
from .base_model import BaseLLMModel



class OpenAIVisionClient(BaseLLMModel):
    def __init__(
        self,
        model_name,
        api_key,
        user_name=""
    ) -> None:
        super().__init__(
            model_name=model_name,
            user=user_name,
            config={
                "api_key": api_key
            }
        )
        
        deepseek_api = "https://aigcbest.top/"
        deepseek_key = "sk-S4P3HS25sTHolaI0g2eW6UCL15lCTYqvvENzNA2FyKaKJxKj"

        duoduo_api = "https://aigcbest.top/"
        duoduo_standard = "sk-S4P3HS25sTHolaI0g2eW6UCL15lCTYqvvENzNA2FyKaKJxKj"
        duoduo_key = "sk-JZO63ifL5sbBLhsWbe1LqV6atSwWim8VDYhO533RJJyViQgP"
        duoduo_models = "问答模型o1,问答模型4o-online,问答模型o1-pre,问答模型o3-mini"
        if self.api_host is not None:

            if model_name in duoduo_models:
                self.chat_completion_url, self.images_completion_url, self.openai_api_base, self.balance_api_url, self.usage_api_url = shared.format_openai_host(duoduo_api)
                self.api_key = duoduo_standard
            elif model_name in "deepseekv3,deepseek-reasoner":
                self.chat_completion_url, self.images_completion_url, self.openai_api_base, self.balance_api_url, self.usage_api_url = shared.format_openai_host(deepseek_api)
                self.api_key = deepseek_key
            else:
                self.chat_completion_url, self.images_completion_url, self.openai_api_base, self.balance_api_url, self.usage_api_url = shared.format_openai_host(self.api_host)
        else:
            if model_name in duoduo_models:
                self.chat_completion_url, self.images_completion_url, self.openai_api_base, self.balance_api_url, self.usage_api_url = shared.format_openai_host(duoduo_api)
                self.api_key = duoduo_standard
            elif model_name in "deepseekv3,deepseek-reasoner":
                self.chat_completion_url, self.images_completion_url, self.openai_api_base, self.balance_api_url, self.usage_api_url = shared.format_openai_host(deepseek_api)
                self.api_key = deepseek_key
                
            else:
                self.api_host, self.chat_completion_url, self.images_completion_url, self.openai_api_base, self.balance_api_url, self.usage_api_url = shared.state.api_host, shared.state.chat_completion_url, shared.state.images_completion_url, shared.state.openai_api_base, shared.state.balance_api_url, shared.state.usage_api_url
        self._refresh_header()

    def get_answer_stream_iter(self):
        if self.model_name in "o1-preview,o1-mini":
            # 使用生成器将 content 的内容逐步返回
            content, total_token_count = self.get_answer_at_once()
            partial_text = ""
            batch = []
            batch_size = 10 
            for i in content:
                batch.append(i)
                if len(batch) >= batch_size:
                    partial_text += ''.join(batch)
                    batch.clear()
                    yield partial_text
            yield partial_text
            return
        response = self._get_response(stream=True)
        if response is not None:
            iter = self._decode_chat_response(response)
            partial_text = ""
            batch = []
            batch_size = 10
            for i in iter:
                batch.append(i)
                if len(batch) >= batch_size:
                    partial_text += ''.join(batch)
                    batch.clear()
                    yield partial_text
            partial_text += ''.join(batch)
            yield partial_text
        else:
            yield STANDARD_ERROR_MSG + GENERAL_ERROR_MSG

    def get_answer_at_once(self):
        response = self._get_response()
        response = json.loads(response.text)
        content = response["choices"][0]["message"]["content"]
        total_token_count = response["usage"]["total_tokens"]
        return content, total_token_count


    def count_token(self, user_input):
        input_token_count = count_token(construct_user(user_input))
        if self.system_prompt is not None and len(self.all_token_counts) == 0:
            system_prompt_token_count = count_token(
                construct_system(self.system_prompt)
            )
            return input_token_count + system_prompt_token_count
        return input_token_count

    def count_image_tokens(self, width: int, height: int):
        h = ceil(height / 512)
        w = ceil(width / 512)
        n = w * h
        total = 85 + 170 * n
        return total

    def billing_info(self):
        try:
            curr_time = datetime.datetime.now()
            last_day_of_month = get_last_day_of_month(
                curr_time).strftime("%Y-%m-%d")
            first_day_of_month = curr_time.replace(day=1).strftime("%Y-%m-%d")
            usage_url = f"{shared.state.usage_api_url}?start_date={first_day_of_month}&end_date={last_day_of_month}"
            try:
                usage_data = self._get_billing_data(usage_url)
            except Exception as e:
                # logging.error(f"获取API使用情况失败: " + str(e))
                if "Invalid authorization header" in str(e):
                    return i18n("**获取API使用情况失败**，需在填写`config.json`中正确填写sensitive_id")
                elif "Incorrect API key provided: sess" in str(e):
                    return i18n("**获取API使用情况失败**，sensitive_id错误或已过期")
                return i18n("**获取API使用情况失败**")
            # rounded_usage = "{:.5f}".format(usage_data["total_usage"] / 100)
            rounded_usage = round(usage_data["total_usage"] / 100, 5)
            usage_percent = round(usage_data["total_usage"] / usage_limit, 2)
            from ..webui import get_html

            # return i18n("**本月使用金额** ") + f"\u3000 ${rounded_usage}"
            return get_html("billing_info.html").format(
                    label = i18n("本月使用金额"),
                    usage_percent = usage_percent,
                    rounded_usage = rounded_usage,
                    usage_limit = usage_limit
                )
        except requests.exceptions.ConnectTimeout:
            status_text = (
                STANDARD_ERROR_MSG + CONNECTION_TIMEOUT_MSG + ERROR_RETRIEVE_MSG
            )
            return status_text
        except requests.exceptions.ReadTimeout:
            status_text = STANDARD_ERROR_MSG + READ_TIMEOUT_MSG + ERROR_RETRIEVE_MSG
            return status_text
        except Exception as e:
            import traceback
            traceback.print_exc()
            logging.error(i18n("获取API使用情况失败:") + str(e))
            return STANDARD_ERROR_MSG + ERROR_RETRIEVE_MSG

    def _get_gpt4v_style_history(self):
        history = []
        image_buffer = []
        for message in self.history:
            if message["role"] == "user":
                content = []
                if image_buffer:
                    for image in image_buffer:
                        content.append(
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{self.get_image_type(image)};base64,{self.get_base64_image(image)}",
                                }
                            },
                        )
                if content:
                    content.insert(0, {"type": "text", "text": message["content"]})
                    history.append(construct_user(content))
                    image_buffer = []
                else:
                    history.append(message)
            elif message["role"] == "assistant":
                history.append(message)
            elif message["role"] == "image":
                image_buffer.append(message["content"])
        return history


    @shared.state.switching_api_key  # 在不开启多账号模式的时候，这个装饰器不会起作用
    def _get_response(self, stream=False):

        openai_api_key = self.api_key
        system_prompt = self.system_prompt
        history = self._get_gpt4v_style_history()

        logging.debug(colorama.Fore.YELLOW +
                      f"{history}" + colorama.Fore.RESET)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}",
        }

        # "问答模型o1-pre",
        # "问答模型o1-mini",

        if system_prompt is not None and "o1" not in self.model_name:
            history = [construct_system(system_prompt), *history]

        if self.model_name in "o1-preview,o1-mini":
            payload = {
                "model": self.model_name,
                "messages": history,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "n": self.n_choices,
            }
        else:
            payload = {
                "model": self.model_name,
                "messages": history,
                "temperature": self.temperature,
                "top_p": self.top_p,
                "n": self.n_choices,
                "stream": stream,
            }

        if self.max_generation_token:
            payload["max_tokens"] = self.max_generation_token
        if self.presence_penalty:
            payload["presence_penalty"] = self.presence_penalty
        if self.frequency_penalty:
            payload["frequency_penalty"] = self.frequency_penalty
        if self.stop_sequence:
            payload["stop"] = self.stop_sequence
        if self.logit_bias is not None:
            payload["logit_bias"] = self.encoded_logit_bias()
        if self.user_identifier:
            payload["user"] = self.user_identifier

        if stream:
            timeout = TIMEOUT_STREAMING
        else:
            timeout = TIMEOUT_ALL

        with retrieve_proxy():
            try:
                response = requests.post(
                    self.chat_completion_url,
                    headers=headers,
                    json=payload,
                    stream=stream,
                    timeout=timeout,
                )
            except:
                traceback.print_exc()
                return None
        return response

    def _refresh_header(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {sensitive_id}",
        }


    def _get_billing_data(self, billing_url):
        with retrieve_proxy():
            response = requests.get(
                billing_url,
                headers=self.headers,
                timeout=TIMEOUT_ALL,
            )

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(
                f"API request failed with status code {response.status_code}: {response.text}"
            )
    def _decode_chat_response(self, response):
        error_msg = ""
        first_content = False
        first_reasoning_content = False
        two_n = 0
        for chunk in response.iter_lines():
            if not chunk:
                continue  # 跳过空行

            try:
                chunk_str = chunk.decode('utf-8')  # 解码为字符串
            except UnicodeDecodeError as e:
                logging.error(f"解码错误: {e}，原始数据: {chunk}")
                error_msg += chunk.decode('utf-8', errors='ignore')
                continue

            if chunk_str.startswith("data: "):
                data_str = chunk_str[len("data: "):]
                if data_str == "[DONE]":
                    break  # 结束标志
                try:
                    chunk_json = json.loads(data_str)
                    {'content': '', 'reasoning_content': '嗯', 'role': 'assistant'}
                except json.JSONDecodeError as e:
                    logging.error(f"JSON解析错误: {e}，数据: {data_str}")
                    error_msg += data_str
                    continue

                try:
                    model = chunk_json.get("model", "")
                    if model == "gpt-4o-all":
                        # 专门处理 gpt-4o-all 模型的响应
                        content = chunk_json["choices"][0]["delta"].get("content", "")
                        reasoning_content = chunk_json["choices"][0]["delta"].get("reasoning_content", "")
                        if content:
                            yield content
                        if reasoning_content:
                            yield reasoning_content
                    else:
                        # 处理其他模型的响应
                        try:
                            delta = chunk_json["choices"][0]["delta"]
                            content = delta.get("content", "")
                            reasoning_content = chunk_json["choices"][0]["delta"].get("reasoning_content", "")
                        except Exception as e:
                            content = ""
                        if content:
                            if first_content is False:
                                first_content = True
                                # yield f"最终输出\n================================\n"
                                yield f"\n"
                            yield content
                        if reasoning_content:
                            if first_reasoning_content is False:
                                first_reasoning_content = True
                                yield f"思考中\n================================\n> "
                            if "\n\n" in reasoning_content:
                                yield reasoning_content.replace("\n\n","\n> \n") + "> "
                            else:
                                yield reasoning_content
                except KeyError as e:
                    logging.error(f"解析 JSON 时缺少键: {e}，完整数据: {chunk_json}")
                    continue
            else:
                logging.warning(f"收到未知格式的数据: {chunk_str}")
                continue

        if error_msg and error_msg != "[DONE]":
            raise Exception(error_msg)
    def _decode_chat_response_ssssssssssssssssss(self, response):
        error_msg = ""
        for chunk in response.iter_lines():
            if chunk:
                chunk = chunk.decode()
                chunk_length = len(chunk)
                try:
                    chunk = json.loads(chunk[6:])
                except:
                    print(i18n("JSON解析错误,收到的内容: ") + f"{chunk}")
                    error_msg += chunk
                    continue
                try:
                    if chunk.get("model",None) in "gpt-4o-all":
                        try:
                            data = chunk["choices"][0]["delta"]["content"]
                            yield data

                        except Exception as e:
                            # logging.error(f"Error: {e}")
                            continue
                        
                    else:    
                        if chunk_length > 6 and "delta" in chunk["choices"][0]:
                            if "finish_details" in chunk["choices"][0]:
                                finish_reason = chunk["choices"][0]["finish_details"]
                            elif "finish_reason" in chunk["choices"][0]:
                                finish_reason = chunk["choices"][0]["finish_reason"]
                            else:
                                finish_reason = chunk["finish_details"]
                            if finish_reason == "stop":
                                break
                            try:
                                yield chunk["choices"][0]["delta"]["content"]
                            except Exception as e:
                                # logging.error(f"Error: {e}")
                                continue
                except:
                    traceback.print_exc()
                    print(f"ERROR: {chunk}")
                    continue
        if error_msg and not error_msg=="data: [DONE]":
            raise Exception(error_msg)

    def set_key(self, new_access_key):
        ret = super().set_key(new_access_key)
        self._refresh_header()
        return ret

    def _single_query_at_once(self, history, temperature=1.0):
        timeout = TIMEOUT_ALL
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "temperature": f"{temperature}",
        }
        payload = {
            "model": RENAME_MODEL if RENAME_MODEL is not None else self.model_name,
            "messages": history,
        }

        with retrieve_proxy():
            response = requests.post(
                self.chat_completion_url,
                headers=headers,
                json=payload,
                stream=False,
                timeout=timeout,
            )

        return response

    def auto_name_chat_history(self, name_chat_method, user_question, single_turn_checkbox):
        if len(self.history) == 2 and not single_turn_checkbox and not hide_history_when_not_logged_in:
            user_question = self.history[0]["content"]
            if name_chat_method == i18n("模型自动总结（消耗tokens）"):
                ai_answer = self.history[1]["content"]
                try:
                    history = [
                        { "role": "system", "content": SUMMARY_CHAT_SYSTEM_PROMPT},
                        { "role": "user", "content": f"Please write a title based on the following conversation:\n---\nUser: {user_question}\nAssistant: {ai_answer}"}
                    ]
                    response = self._single_query_at_once(history, temperature=0.0)
                    response = json.loads(response.text)
                    content = response["choices"][0]["message"]["content"]
                    filename = replace_special_symbols(content) + ".json"
                except Exception as e:
                    logging.info(f"自动命名失败。{e}")
                    filename = replace_special_symbols(user_question)[:16] + ".json"
                return self.rename_chat_history(filename)
            elif name_chat_method == i18n("第一条提问"):
                filename = replace_special_symbols(user_question)[:16] + ".json"
                return self.rename_chat_history(filename)
            else:
                return gr.update()
        else:
            return gr.update()
