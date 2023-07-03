import matplotlib.pyplot as plt


def plot_learning_curve(history):
    # Get training loss values
    loss = history.history['loss']

    # Get training accuracy values
    accuracy = history.history['accuracy']

    # Create subplots for loss and accuracy
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

    # Plot loss curve
    ax1.plot(loss, label='Training Loss')
    ax1.legend(loc='upper right')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Loss')
    ax1.set_title('Training Loss')

    # Plot accuracy curve
    ax2.plot(accuracy, label='Training Accuracy')
    ax2.legend(loc='lower right')
    ax2.set_xlabel('Epochs')
    ax2.set_ylabel('Accuracy')
    ax2.set_title('Training Accuracy')

    # Display the plot
    plt.tight_layout()
    plt.show()
