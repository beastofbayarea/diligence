import os
from google.cloud.aiplatform.gapic import ModelServiceClient
from google.cloud.aiplatform.gapic import PredictionServiceClient

project = os.environ.get('GCP_PROJECT_ID')
region = os.environ.get('GCP_REGION','us-central1')
if not project:
    print('GCP_PROJECT_ID not set; aborting')
    raise SystemExit(1)
parent = f'projects/{project}/locations/{region}'
print('Parent:', parent)
client = ModelServiceClient(client_options={'api_endpoint': f'{region}-aiplatform.googleapis.com'})
models = client.list_models(parent=parent)
models_list = list(models)
print(f'Found {len(models_list)} models')
for m in models_list:
    print('MODEL:', m.name, '| display_name=', getattr(m,'display_name',None))
# pick candidates with 'gemini' or 'flash' in display name or model name
candidates = [m.name for m in models_list if ('gemini' in (m.display_name or '').lower()) or ('flash' in (m.display_name or '').lower() ) or ('gemini' in m.name.lower() ) ]
print('Candidates:', candidates)
if not candidates and models_list:
    candidates = [models_list[0].name]
# Try predict on each candidate with a small test prompt
client_pred = PredictionServiceClient(client_options={'api_endpoint': f'{region}-aiplatform.googleapis.com'})
for model_name in candidates[:3]:
    print('\nTrying predict on', model_name)
    try:
        instances = [{'content':'Say hello in one short sentence.'}]
        params = {}
        resp = client_pred.predict(endpoint=model_name, instances=instances, parameters=params)
        print('Predict response type:', type(resp))
        try:
            for p in resp.predictions:
                print('PRED:', p)
        except Exception as e:
            print('Could not iterate predictions:', e)
    except Exception as e:
        print('Predict failed for', model_name, '->', e)
