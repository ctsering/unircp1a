import os
import json
import boto3

from todos import decimalencoder

dynamodb = boto3.resources('dynamodb')
translate = boto3.client('translate')
comprehend = boto3.client('comprehend')

def detect_languaje_task(task):
    response = comprehend.detect_dominant_language(Text='string')
    
    return response
    
def translate_task(task, source, target):
    
    response = translate.translate_text(
    Text=task,
    SourceLanguageCode = source,
    TargetLanguageCode = target)
    
    return response
    
def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
            }
        )
    
    target = event['pathParameters']['lang']
    
    task = result['Item']['text']
    
    source_result = detect_languaje_task(task)
    
    source = source_result['Languages'][0]['LanguageCode']
    
    task_translated = translate_task(task, source, target)
    result['item']['text'] = task_translated['TranslatedText']
    
    response = { 
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                            cls=decimalencoder.DecimalEncoder)
    }
return response

#translate = boto3.client('translate')
#result = translate.translate_text(Text="Hello, World",
#                                  SourceLanguageCode="en",
#                                  TargetLanguageCode="de")
#print(f'TranslatedText: {result["TranslatedText"]}')
#print(f'SourceLanguageCode: {result["SourceLanguageCode"]}')
#print(f'TargetLanguageCode: {result["TargetLanguageCode"]}')