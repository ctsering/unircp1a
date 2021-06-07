import boto3

translate = boto3.client('translate')
result = translate.translate_text(Text="Hello, World",
                                  SourceLanguageCode="en",
                                  TargetLanguageCode="de")
print(f'TranslatedText: {result["TranslatedText"]}')
print(f'SourceLanguageCode: {result["SourceLanguageCode"]}')
print(f'TargetLanguageCode: {result["TargetLanguageCode"]}')