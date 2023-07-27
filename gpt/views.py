from rest_framework.views import APIView
from rest_framework import status
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
                # 생성된 대화의 최대 토큰(텍스트단위) 수
                max_tokens=1024,
                # 생성할 대화의 개수
                n=5,
                # 생성된 대화의 중단 조건
                stop=None,
                # 생성된 텍스트의 다양성 조절, 0~1까지이며 높을수록 무작위, 낮을수록 일관성 있음
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

    def delete(self, request, *args, **kwargs):
        # request body에서 id값 확인
        conversation_id = request.data.get('id')
        if conversation_id is None:
            return Response(
                {'message': 'No conversation ID provided'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 해당 ID를 가진 대화를 데이터베이스에서 찾음
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {'message': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND
            )

        # 대화를 삭제
        conversation.delete()

        # 세션에서 해당 대화를 찾아 삭제
        session_conversations = request.session.get('conversations', [])
        session_conversations = [
            c for c in session_conversations if c['id'] != conversation_id
        ]
        request.session['conversations'] = session_conversations
        request.session.modified = True

        return Response(
            {'message': f'Conversation {conversation_id} deleted'},
            status=status.HTTP_200_OK,
        )
