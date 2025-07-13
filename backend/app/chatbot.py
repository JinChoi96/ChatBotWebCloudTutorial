import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 모델과 토크나이저 로딩
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# 히스토리를 하나의 텍스트로 관리 (간단한 방식)
chat_history_ids = None

def get_chatbot_response(user_input: str) -> str:
    global chat_history_ids

    print(f"사용자 입력: {user_input}")
    # 사용자 입력 토크나이즈
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # 모델에게 응답 생성 요청
    if chat_history_ids is not None:
        input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
    else:
        input_ids = new_input_ids

    output_ids = model.generate(
        input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.8,
    )

    chat_history_ids = output_ids  # 대화 히스토리 유지 (전체 누적)

    # 모델 응답 디코딩
    response = tokenizer.decode(output_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    print(f"챗봇 응답: {response}")
    return response