import gradio as gr
import os


APP_DIR = os.path.dirname(os.path.abspath(__file__))


def process_image(input_image):
    return input_image


def create_ui():
    image_input = gr.Image(shape=(1024, 1024))
    ui = gr.Interface(
        fn=process_image,
        inputs=image_input,
        outputs='image',
        title="Computer Vision Algorithm Demo",
        description="Upload an image to see the output of the computer vision algorithm.",
        examples=[os.path.join(APP_DIR, 'examples', x) for x in os.listdir(os.path.join(APP_DIR, 'examples'))]
    )
    return ui


def main():
    ui = create_ui()
    ui.launch()


if __name__ == '__main__':
    main()