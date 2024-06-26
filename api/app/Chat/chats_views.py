# import openai
# from decouple import config
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .data import RESPONSES
from api.models import CustomUser
from api.user.authentication import get_user_id
from .chats_serializer import ChatSerializer, ComplaintSerializer


class ChatbotView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)  
        message = request.data['message']
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            user_message = serializer.validated_data['message'].lower()
            response_message = RESPONSES.get(user_message, "Sorry, I don't understand that.")
            return Response({'message': message, 'response': response_message})
        return Response(serializer.errors, status=400)


class ComplaintAPIView(APIView):
    def post(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        user_id = get_user_id(token)
        if user_id is None:
            return Response({"error": "Authentication credentials were not provided or are invalid."}, status=401)
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise Http404("No user found with this ID")

        serializer = ComplaintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# class ChatGPTView(APIView):
#     def post(self, request):
#         user_query = request.data.get('message', '')
#         if not user_query:
#             return Response({"error": "The query is required."}, status=status.HTTP_400_BAD_REQUEST)
#         openai_api_key = config('OPENAIAPI')
#         openai.api_key = openai_api_key
#         try:
#             messages = [
#                 {"role": "system", "content": "You are FarmCart AI, and the query coming to you is from a e-commerce application made to buy and sell organic vegitables and fruits.since you are a chatbot make sure your answers are short and on point."},
#                 {"role": "user", "content": user_query}
#             ]
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo", 
#                 messages=messages,
#                 temperature=0.7,
#                 max_tokens=150
#             )
#             if response.choices:
#                 response_text = response.choices[0].message['content'].strip()
#             else:
#                 response_text = "No response generated."
#             return Response({"response": response_text})
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





























# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from transformers import AutoTokenizer, AutoModelForQuestionAnswering
# import torch

# tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
# model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")

# def answer_question(question, context):
#     inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
#     output = model(**inputs)
    
#     answer_start_scores, answer_end_scores = output.start_logits, output.end_logits
    
#     # Debug outputs
#     print("Start logits:", answer_start_scores)
#     print("End logits:", answer_end_scores)
    
#     answer_start = torch.argmax(answer_start_scores)  # Index of the start of the answer
#     answer_end = torch.argmax(answer_end_scores) + 1  # Index of the end of the answer

#     # Ensure start and end indices are valid
#     if answer_start >= answer_end:
#         print("Invalid span found: Start index is after the end index.")
#         return ""
    
#     # Convert tokens to answer string
#     answer_tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end])
#     answer = tokenizer.convert_tokens_to_string(answer_tokens)
#     return answer


# def qa_model(user_input):
#     # Example context — in a real application, the context should be relevant to the user's question
#     context = "Contextual information relevant to the user's question."
#     return answer_question(user_input, context)


# class ChatAPIView(APIView):
#     def post(self, request):
#         user_input = request.data.get('input', None)
#         if not user_input:
#             return Response({'error': 'No input provided'}, status=status.HTTP_400_BAD_REQUEST)
        
#         answer = qa_model(user_input)  # Adapt this to call your QA model correctly
        
#         return Response({'response': answer})











# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from transformers import pipeline

# # Initialize the model
# chat_model = pipeline("text-generation", model="gpt2")

# class ChatAPIView(APIView):
#     def post(self, request):
#         user_input = request.data.get('input', None)
#         if not user_input:
#             return Response({'error': 'No input provided'}, status=status.HTTP_400_BAD_REQUEST)
#         responses = chat_model(user_input, max_length=50, num_return_sequences=1)
#         response_text = responses[0]['generated_text']
#         return Response({'response': response_text})







# from transformers import GPT2Tokenizer

# tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
# def encode_input_output_pairs(data):
#     inputs = tokenizer(data["input"], padding='max_length', truncation=True, max_length=512)
#     outputs = tokenizer(data["response"], padding='max_length', truncation=True, max_length=512)
#     return inputs, outputs

# from transformers import GPT2LMHeadModel

# model = GPT2LMHeadModel.from_pretrained('gpt2')


# from transformers import TrainingArguments

# training_args = TrainingArguments(
#     output_dir='./model_save',
#     overwrite_output_dir=True,
#     num_train_epochs=4,
#     per_device_train_batch_size=2,
#     save_steps=100,
#     save_total_limit=2,
#     logging_dir='./logs',
#     logging_steps=10
# )

# train_dataset = [
#     {
#         "input": "I am an organic farmer and my crops are being attacked by insects and bugs, so what should I do?",
#         "response": "To address insect and bug infestations in your organic crops, consider the following integrated pest management strategies: Identify the pests, Biological control, Cultural practices, Physical barriers, Botanical insecticides, Soil health, Regular monitoring."
#     }

# ]
# eval_texts = ["Sample eval text 1", "Sample eval text 2"]  # Replace with your actual evaluation texts
# eval_dataset = MyDataset(eval_texts, tokenizer, max_length=512)
# from transformers import Trainer

# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=train_dataset,
#     eval_dataset=eval_dataset
# )

# trainer.train()
