from rest_framework.views import APIView
from rest_framework.response import Response
from dotenv import load_dotenv
import openai
import os
from .models import Conversation

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


class ChatView(APIView):
    def get(self, request, *args, **kwargs):
        conversations = request.session.get('conversations', [])
        return Response({'conversations': conversations}, status=200)

    def post(self, request, *args, **kwargs):
        prompt = request.POST.get('prompt')
        if prompt:
            # 이전 대화 기록 가져오기
            session_conversations = request.session.get('conversations', [])
            previous_conversations = "\n".join(
                [
                    f"User: {c['prompt']}\nAI: {c['response']}"
                    for c in session_conversations
                ]
            )
            prompt_with_previous = f"{previous_conversations}\nUser: {prompt}\nAI:"

            model_engine = "text-davinci-003"
            completions = openai.Completion.create(
                engine=model_engine,
                prompt=prompt_with_previous,
                max_tokens=1024,
                n=5,
                stop=None,
                temperature=0.5,
            )
            response = completions.choices[0].text.strip()

            conversation = Conversation(prompt=prompt, response=response)
            conversation.save()

            # 대화 기록에 새로운 응답 추가
            session_conversations.append({'prompt': prompt, 'response': response})
            request.session['conversations'] = session_conversations
            # 세션 내용 변화를 감지해 변경 내용을 추가로 SQLite에 저장
            request.session.modified = True

        return self.get(request, *args, **kwargs)
