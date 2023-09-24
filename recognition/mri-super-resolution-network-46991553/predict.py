"""
Example usage of the trained model
"""
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from dataset import *
from config import *
from modules import SuperResolutionModel


def generate_model_output(model: nn.Module, data_loader: DataLoader, prefix='', device='cpu', show=False):
    with torch.no_grad():
        for expected_outputs, _ in data_loader:
            inputs = downsample_tensor(expected_outputs)

            inputs = inputs.to(device)
            expected_outputs = expected_outputs.to(device)
            
            # Get the dimensions of the first input image
            first_input_image = inputs[0]
            
            # Get the dimensions of the first output image
            first_output_image = expected_outputs[0]

            # Actual model output
            first_model_output = model(first_input_image)
            # Scale output to be in correct RGB range
            first_model_output = torch.clamp(first_model_output, 0, 1.0)
            
            # Display the first input image
            plt.figure(figsize=(18, 6))
            plt.subplot(1, 3, 1) # first column
            # Convert tensor to numpy format (C, H, W) -> (H, W, C)
            input_img_formatted = first_input_image.cpu().permute(1, 2, 0)
            plt.imshow(input_img_formatted)
            plt.title("Input Image")
            plt.axis('off')  # Turn off axis labels
            
            # Display the first output image
            plt.subplot(1, 3, 3) # third column
            # Convert tensor to numpy format (C, H, W) -> (H, W, C)
            output_img_formatted = first_output_image.cpu().permute(1, 2, 0)
            plt.imshow(output_img_formatted)
            plt.title("Target Image")
            plt.axis('off')  # Turn off axis labels

            # Display the first model output
            plt.subplot(1, 3, 2) # second column
            # Convert tensor to numpy format (C, H, W) -> (H, W, C)
            output_img_formatted = first_model_output.cpu().permute(1, 2, 0)
            output_img_formatted = torch.clamp(output_img_formatted, 0, 1)
            plt.imshow(output_img_formatted)
            plt.title(f"Model Output")
            plt.axis('off')  # Turn off axis labels
            
            filename = image_dir + prefix + 'output.png'

            if show:
                plt.show()
            else:
                plt.savefig(filename)
                print("Saved model output to", filename)
            plt.close()
            
            break  # Stop after the first batch to print/display only the first pair of images


def main():
    model = SuperResolutionModel()
    try:
        model.load_state_dict(torch.load(model_filename, map_location=torch.device('cpu')))
    except IOError:
        print("Couldn't load model from file:", model_filename)
        exit(1)

    data_loader = get_test_dataloader()
    generate_model_output(model, data_loader, show=True)


if __name__ == '__main__':
    main()