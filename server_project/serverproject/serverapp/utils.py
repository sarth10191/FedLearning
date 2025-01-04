import numpy as np
from  tensorflow.keras import models, Layers

def create_and_save_model(path):
    model = models.Sequential([
        Layers.Flatten(input_shape = (50,50,3)),
        Layers.Dense(128, activation='relu'),
        Layers.Dense(2, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.save(path)
    return model



def aggregate_client_files(selected_clients: list, server_path = "../server_model/server_file"):
    if not selected_clients:
        raise ValueError("No clients provided for aggregation.")

    models = []
    for client in selected_clients:
        model_file = client.model_file
        try:
            model = models.load_model(model_file)
            models.append(model)
        except Exception as e:
            print(f"Error loading model from {model_file}: {e}")
            continue

    if not models:
        raise ValueError("No valid models were loaded for aggregation.")

    weights_list = [model.get_weights() for model in models]
    avg_weights = []
    num_models = len(weights_list)

    for weights in zip(*weights_list):
        avg_weights.append(np.mean(np.array(weights), axis=0))

    aggregated_model = models[0]
    aggregated_model.set_weights(avg_weights)

    try:
        aggregated_model.save(server_path)
        print(f"Aggregated model saved to {server_path}")
    except Exception as e:
        print(f"Error saving aggregated model: {e}")

# Example usage:
# selected_clients = [Client(model_file='client1.h5'), Client(model_file='client2.h5')]
# aggregate_client_files(selected_clients, 'aggregated_model.h5')
