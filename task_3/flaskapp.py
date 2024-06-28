from flask import Flask, request, Response, stream_with_context, send_file
from diffusers import StableDiffusionPipeline
import torch
import uuid
from io import BytesIO
import threading
import queue

app = Flask(__name__)

# Load your model here
pipe = StableDiffusionPipeline.from_pretrained("hf-internal-testing/tiny-stable-diffusion-torch")

# Store generated images and progress
generated_images = {}
progress_queues = {}


def generate_image(description, image_id, progress_queue):
    def callback_on_step_end(pipe,step: int, timestep: int, latents: torch.FloatTensor, **kwargs):
        progress_queue.put(step)
        return latents

    try:
        # Generate the image
        image = pipe(description, num_inference_steps=50, callback_on_step_end=callback_on_step_end).images[0]
        generated_images[image_id] = image
        progress_queue.put('done')
    except Exception as e:
        progress_queue.put(f'Error: {e}')


@app.route('/generate_progress', methods=['POST'])
def generate_progress():
    description = request.json.get("text")
    image_id = str(uuid.uuid4())

    # Create a queue for progress updates
    progress_queue = queue.Queue()
    progress_queues[image_id] = progress_queue

    # Start image generation in a separate thread
    threading.Thread(target=generate_image, args=(description, image_id, progress_queue)).start()

    def generate():
        while True:
            progress = progress_queue.get()
            print(progress)
            if progress == 'done':
                yield f'data: image_id:{image_id}\n\n'
                break
            elif isinstance(progress, str) and progress.startswith('Error'):
                yield f'data: {progress}\n\n'
                break
            else:

                yield f'data:{progress/50}'

    return Response(stream_with_context(generate()), content_type='text/event-stream')


@app.route('/get_generated_image/<image_id>', methods=['GET'])
def get_generated_image(image_id):
    print(image_id)
    image = generated_images.get(image_id.split(':')[-1])
    if image:
        img_io = BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    return "Image not found", 404


if __name__ == '__main__':
    app.run(debug=True)
