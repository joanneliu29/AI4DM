from transformers import MusicgenForConditionalGeneration
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
from openai import OpenAI
import torch
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model.to(device);
# Use a pipeline as a high-level helper
from transformers import pipeline
from dotenv import load_dotenv
from transformers import AutoProcessor
import scipy

def poemGenerator(msg):

  client = OpenAI()

  msg_list = [
      {"role": "system", "content": "You are a expert poem writer. Using deep meaning and short lines or words you generate poem in less than 20 words based on the given emotion."},
    ]

  msg_list.append(msg)
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0.2,
    max_completion_tokens=100,
    messages = msg_list
  )

  out_message = response.choices[0].message.content
  return out_message

def runModels(emotion):
    message = {"role": "user", "content": emotion}
    poem = poemGenerator(message)
    return poem

def music(poem):
    audio_length_in_s = 512 / model.config.audio_encoder.frame_rate

    audio_length_in_s
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")

    inputs = processor(
        text=["background music with light melody for the poem" + poem],
        padding=True,
        return_tensors="pt",
    )

    audio_values = model.generate(**inputs.to(device), do_sample=True, guidance_scale=3, max_new_tokens=512)
    sampling_rate = model.config.audio_encoder.sampling_rate
    output_filename = 'musicgen_out.wav'
    scipy.io.wavfile.write(output_filename, rate=sampling_rate, data=audio_values[0, 0].numpy())
    return output_filename