# Prerequisites:
# pip install onnxruntime
# pip install onnxruntime-gpu
from transformers import AutoConfig, AutoProcessor
from transformers.image_utils import load_image
import onnxruntime
import numpy as np
import os
from docling_core.types.doc import DoclingDocument
from docling_core.types.doc.document import DocTagsDocument

os.environ["OMP_NUM_THREADS"] = "1"
# cuda
os.environ["ORT_CUDA_USE_MAX_WORKSPACE"] = "1"

# 1. Load models
## Load config and processor
model_path = "/Users/edward/documents/sources/playground/huggingmodel/SmolDocling-256M-preview"
config = AutoConfig.from_pretrained(model_path)
processor = AutoProcessor.from_pretrained(model_path)

vision_encoder="/Users/edward/documents/sources/playground/huggingmodel/smoldocling-onnx/vision_encoder.onnx"
embed_tokens="/Users/edward/documents/sources/playground/huggingmodel/smoldocling-onnx/embed_tokens.onnx"
model_merged="/Users/edward/documents/sources/playground/huggingmodel/smoldocling-onnx/decoder_model_merged.onnx"

## Load sessions
# !wget https://huggingface.co/ds4sd/SmolDocling-256M-preview/resolve/main/onnx/vision_encoder.onnx
# !wget https://huggingface.co/ds4sd/SmolDocling-256M-preview/resolve/main/onnx/embed_tokens.onnx
# !wget https://huggingface.co/ds4sd/SmolDocling-256M-preview/resolve/main/onnx/decoder_model_merged.onnx
# cpu
# vision_session = onnxruntime.InferenceSession("vision_encoder.onnx")
# embed_session = onnxruntime.InferenceSession("embed_tokens.onnx")
# decoder_session = onnxruntime.InferenceSession("decoder_model_merged.onnx"

# cuda
vision_session = onnxruntime.InferenceSession(vision_encoder)
embed_session = onnxruntime.InferenceSession(embed_tokens)
decoder_session = onnxruntime.InferenceSession(model_merged)

## Set config values
num_key_value_heads = config.text_config.num_key_value_heads
head_dim = config.text_config.head_dim
num_hidden_layers = config.text_config.num_hidden_layers
eos_token_id = config.text_config.eos_token_id
image_token_id = config.image_token_id
end_of_utterance_id = processor.tokenizer.convert_tokens_to_ids("<end_of_utterance>")

# 2. Prepare inputs
## Create input messages
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": "Convert this page to docling."}
        ]
    },
]

## Load image and apply processor
image = load_image("test.jpeg")
prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
inputs = processor(text=prompt, images=[image], return_tensors="np")

## Prepare decoder inputs
batch_size = inputs['input_ids'].shape[0]
past_key_values = {
    f'past_key_values.{layer}.{kv}': np.zeros([batch_size, num_key_value_heads, 0, head_dim], dtype=np.float32)
    for layer in range(num_hidden_layers)
    for kv in ('key', 'value')
}
image_features = None
input_ids = inputs['input_ids']
attention_mask = inputs['attention_mask']
position_ids = np.cumsum(inputs['attention_mask'], axis=-1)


# 3. Generation loop
max_new_tokens = 8192
generated_tokens = np.array([[]], dtype=np.int64)
for i in range(max_new_tokens):
  inputs_embeds = embed_session.run(None, {'input_ids': input_ids})[0]

  if image_features is None:
    ## Only compute vision features if not already computed
    image_features = vision_session.run(
        ['image_features'],  # List of output names or indices
        {
            'pixel_values': inputs['pixel_values'],
            'pixel_attention_mask': inputs['pixel_attention_mask'].astype(np.bool_)
        }
    )[0]
    
    ## Merge text and vision embeddings
    inputs_embeds[inputs['input_ids'] == image_token_id] = image_features.reshape(-1, image_features.shape[-1])

  logits, *present_key_values = decoder_session.run(None, dict(
      inputs_embeds=inputs_embeds,
      attention_mask=attention_mask,
      position_ids=position_ids,
      **past_key_values,
  ))

  ## Update values for next generation loop
  input_ids = logits[:, -1].argmax(-1, keepdims=True)
  attention_mask = np.ones_like(input_ids)
  position_ids = position_ids[:, -1:] + 1
  for j, key in enumerate(past_key_values):
    past_key_values[key] = present_key_values[j]

  generated_tokens = np.concatenate([generated_tokens, input_ids], axis=-1)
  if (input_ids == eos_token_id).all() or (input_ids == end_of_utterance_id).all():
    break  # Stop predicting

doctags = processor.batch_decode(
    generated_tokens,
    skip_special_tokens=False,
)[0].lstrip()

print(doctags)

doctags_doc = DocTagsDocument.from_doctags_and_image_pairs([doctags], [image])
print(doctags)
# create a docling document
doc = DoclingDocument(name="Document")
doc.load_from_doctags(doctags_doc)

print(doc.export_to_markdown())
