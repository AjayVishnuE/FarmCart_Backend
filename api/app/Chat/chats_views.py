import openai
from decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ChatGPTView(APIView):

    def post(self, request):
        user_query = request.data.get('query', '')
        if not user_query:
            return Response({"error": "The query is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Assuming you have your OpenAI API key stored in an .env file
        openai_api_key = config('OPENAIAPI')
        openai.api_key = openai_api_key

        try:
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",  # Make sure to use an available model
                prompt=user_query,
                temperature=0.7,
                max_tokens=150
            )
            return Response({"response": response.choices[0].text.strip()})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
