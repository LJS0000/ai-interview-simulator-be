from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv
import openai
import os
from .models import Conversation


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


class ChatView(APIView):
    # 사용자 인증
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # 사용자가 생성한 채팅만 조회
        user = request.user
        conversations = Conversation.objects.filter(user=user)
        conversations_data = [
            {'id': c.id, 'prompt': c.prompt, 'response': c.response}
            for c in conversations
        ]
        return Response({'conversations': conversations_data}, status=200)

    def post(self, request, *args, **kwargs):
        user = request.user
        prompt = request.POST.get('prompt')

        # 하루에 5번만 채팅을 입력하도록 제한
        if user.daily_chats >= 5:
            return Response(
                {"message": "You have exceeded the daily limit for chats."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 채팅 생성
        if prompt:
            self.handle_chat(prompt, user, request)

        # 처리 완료 후 채팅 최신 상태 조회
        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user = request.user
        # request body에서 id값 확인
        conversation_id = request.data.get('id')

        try:
            conversation = Conversation.objects.get(id=conversation_id, user=user)
            conversation.delete()
        except Conversation.DoesNotExist:
            return Response(
                {'message': 'Conversation not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {'message': f'Conversation {conversation_id} deleted'},
            status=status.HTTP_200_OK,
        )

    def handle_chat(self, prompt, user, request):
        # 이전 대화 기록 가져오기
        session_conversations = Conversation.objects.filter(user=user)
        previous_conversations = "\n".join(
            [f"User: {c.prompt}\nAI: {c.response}" for c in session_conversations]
        )
        prompt_with_previous = f"{previous_conversations}\nUser: {prompt}\nAI:"

        model_engine = "text-davinci-003"
        completions = openai.Completion.create(
            engine=model_engine,
            prompt=prompt_with_previous,
            max_tokens=1024,  # 생성된 대화의 최대 토큰(텍스트단위) 수
            n=1,  # 생성할 대화의 개수
            stop=None,  # 생성된 대화의 중단 조건
            temperature=0.5,  # 생성된 텍스트의 다양성 조절, 0~1까지이며 높을수록 무작위, 낮을수록 일관성 있음
        )
        response = completions.choices[0].text.strip()

        conversation = Conversation(user=user, prompt=prompt, response=response)
        conversation.save()

        user.daily_chats += 1
        user.save()
