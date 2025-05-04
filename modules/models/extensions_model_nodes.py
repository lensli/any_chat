# from .base_model import ModelType
from ..webui_locale import I18nAuto
from enum import Enum
i18n = I18nAuto()
class ModelType(Enum):
    Unknown = -1
    OpenAI = 0
    ChatGLM = 1
    LLaMA = 2
    XMChat = 3
    StableLM = 4
    MOSS = 5
    YuanAI = 6
    Minimax = 7
    ChuanhuAgent = 8
    GooglePaLM = 9
    LangchainChat = 10
    Midjourney = 11
    Spark = 12
    OpenAIInstruct = 13
    Claude = 14
    Qwen = 15
    OpenAIVision = 16
    ERNIE = 17
    DALLE3 = 18
    GoogleGemini = 19
    GoogleGemma = 20
    Ollama = 21
    Groq = 22
    Suno = 23
    Vedio = 24
    Dance = 25
URLKEYS = {
    "云雾API":
    {
        "default":{
            "url":"https://yunwu.ai",
            "key":"sk-CpQpb21q3sbL6agoCMTGeZpmR1UN33Zk6urUjADNYieIdY6h",
            "group_name":"default"},
        "openai3x":{
            "url":"https://yunwu.ai",
            "key":"sk-lLJkBjWaROkiGTqjsjzw5EtDiVy3aEzwrBuMOEjc745qIHD6",
            "group_name":"openai3x"},
        "openai6x":{
            "url":"https://yunwu.ai",
            "key":"sk-GhFPrx6suIDVmgPmPM0GGsD6kV0hiA0cQUgNDz6vUICyho3m",
            "group_name":"openai6x"},
        "claude4x":{
            "url":"https://yunwu.ai",
            "key":"sk-9ppwLrUq5GW8tKBbbt8Ekc2YhjKsBTEQNmOCRqR3wv3Uh1i3",
            "group_name":"claude4x"},
        "openai8x":{   
            "url":"https://yunwu.ai",
            "key":"sk-LLT7A2Ae5QevaB8Gvo4YTnKdPXsRppabMzehFll9wJzkjhD3",
            "group_name":"openai8x",
            "cost_rate":4
        },
    }
} 

MODEL_METADATA = {

    "GPT-4.1":{
        "model_name": "gpt-4.1-2025-04-14",
        "urls":[                
                {
                    "url":"https://yunwu.ai",
                    "key":"sk-CpQpb21q3sbL6agoCMTGeZpmR1UN33Zk6urUjADNYieIdY6h",
                    "group_name":"default",
                    "cost_rate":3

                },
            ],
        "input_cost":2,
        "output_cost":8,
        "token_limit": 1047576 ,
        "multimodal": True,
        "model_type": ModelType.OpenAIVision,
        "stream": True,
        "description": "用于复杂任务的最强模型。适合解决跨知识领域问题",
        "placeholder": {
            "logo": "file=web_assets/model_logos/gpt-4.1.png",
            "slogan": i18n("用于复杂任务的最强模型。适合解决跨知识领域问题"),
        }
    },
    "claude-3-7-sonnet":{
        "model_name": "claude-3-7-sonnet-20250219-thinking",
        "urls":[
                {
                    "url":"https://yunwu.ai",
                    "key":"sk-CpQpb21q3sbL6agoCMTGeZpmR1UN33Zk6urUjADNYieIdY6h",
                    "group_name":"default",
                    "cost_rate":3

                },

            ],
        "input_cost":3,
        "output_cost":15,
        "token_limit": 200000,
        "reasoning":True,
        "multimodal": True,
        "model_type": ModelType.OpenAIVision,
        "stream": True,
        "description": "Claude 在代码能力方面全面领先。",
        "placeholder": {
            "logo": "file=web_assets/model_logos/claude.png",
            "slogan": i18n("Claude 在代码能力方面全面领先。"),
        }
    },
    "OpenAI-o3":{
        "model_name": "o3",
        "urls":[
                    {   
                        "url":"https://yunwu.ai",
                        "key":"sk-LLT7A2Ae5QevaB8Gvo4YTnKdPXsRppabMzehFll9wJzkjhD3",
                        "group_name":"openai8x",
                        "cost_rate":4
                    },
                    {
                        "url":"https://yunwu.ai",
                        "key":"sk-lLJkBjWaROkiGTqjsjzw5EtDiVy3aEzwrBuMOEjc745qIHD6",
                        "group_name":"openai3x",
                        "cost_rate":1
                    },
                    {
                        "url":"https://yunwu.ai",
                        "key":"sk-GhFPrx6suIDVmgPmPM0GGsD6kV0hiA0cQUgNDz6vUICyho3m",
                        "group_name":"openai6x",
                        "cost_rate":2
                    },

                ],
        "input_cost":30,
        "output_cost":120,
        "token_limit": 200000,
        "reasoning":True,
        "multimodal": True,
        "model_type": ModelType.OpenAIVision,
        "stream": True,
        "description": "O3 是一个全面而强大的跨领域模型。它为数学、科学、编码和视觉推理任务设定了新标准。它还擅长技术写作和指导遵循。使用它来思考涉及跨文本、代码和图像分析的多步骤问题。",
        "placeholder": {
            "logo": "file=web_assets/model_logos/o3.png",
            "slogan": i18n("O3 是一个全面而强大的跨领域模型。它为数学、科学、编码和视觉推理任务设定了新标准。它还擅长技术写作和指导遵循。使用它来思考涉及跨文本、代码和图像分析的多步骤问题。"),
        }
    },
    "deepseek-reasoner":{
        "model_name": "deepseek-reasoner",
        "urls":[
                    {
                        "url":"https://yunwu.ai",
                        "key":"sk-CpQpb21q3sbL6agoCMTGeZpmR1UN33Zk6urUjADNYieIdY6h",
                        "group_name":"default",
                        "cost_rate":1
                    },

            ],
        "input_cost":4,
        "output_cost":16,
        "token_limit": 200000,
        "reasoning":True,
        "multimodal": True,
        "model_type": ModelType.OpenAIVision,
        "stream": True,
        "description": "DeepSeek-R1 在后训练阶段大规模使用了强化学习技术，在仅有极少标注数据的情况下，极大提升了模型推理能力。在数学、代码、自然语言推理等任务上，性能比肩 OpenAI o1 正式版。",
        "placeholder": {
            "logo": "file=web_assets/model_logos/deepseek-r1.png",
            "slogan": i18n("DeepSeek-R1 在后训练阶段大规模使用了强化学习技术，在仅有极少标注数据的情况下，极大提升了模型推理能力。在数学、代码、自然语言推理等任务上，性能比肩 OpenAI o1 正式版。"),
        }
    },
    "OpenAI-o4-mini":{
        "model_name": "o4-mini",
        "urls":[                
                {
                    "url":"https://yunwu.ai",
                    "key":"sk-CpQpb21q3sbL6agoCMTGeZpmR1UN33Zk6urUjADNYieIdY6h",
                    "group_name":"default",
                    "cost_rate":1

                },
            ],
        "input_cost":1.1,
        "output_cost":4.4,
        "token_limit": 200000  ,
        "multimodal": True,
        "model_type": ModelType.OpenAIVision,
        "stream": True,
        "description": "O4-mini 是我们最新的小型 O 系列型号。它针对快速、有效的推理进行了优化，在编码和可视化任务中具有非常高效的性能",
        "placeholder": {
            "logo": "file=web_assets/model_logos/o4-mini.png",
            "slogan": i18n("O4-mini 是我们最新的小型 O 系列型号。它针对快速、有效的推理进行了优化，在编码和可视化任务中具有非常高效的性能"),
        }
    },
    # "GPT-Image-1":{},
    # "claude-3-7-sonnet":{},
    # "OpenAI-o4-mini":{},
    # "GPT-4.1-mini":{},
    # "GPT-4.1-nano":{},
}

ONLINE_MODELS = []
LOCAL_MODELS = []
deduction_tables_input={}
deduction_tables_output={}

ONLINE_MODELS = list(MODEL_METADATA.keys())

for model_name in MODEL_METADATA.keys():
    deduction_tables_input[model_name] = deduction_tables_input.get("input_cost",1)
for model_name in MODEL_METADATA.keys():
    deduction_tables_output[model_name] = deduction_tables_input.get("output_cost",1)

def get_deduction_amount(txt,model_name,mode):
    if mode == "input":
        deduction_tables = deduction_tables_input
    if mode == "output":
        deduction_tables = deduction_tables_output
    return len(txt) *deduction_tables.get(model_name,1)/500000