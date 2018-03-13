# Estimate Delta V and Damage Severity

Use a CNN to estimate what Delta V should be from using images of rear end accidents. I used images for the vehicle that was hit and excluded other vehicles.

These are experimental scripts to illustrate the viability the ability to predict Delta V from images.

Steps:

1. `get_RearEndAccidents.py`

2. `get_images.py`

3. `identify_rearended_vehicle.py`

4. `preprocess_images.py`

5. `Multi Input NNet.py` and `Train NNet.py` (if desired)

6. `LoadModel.py`


Current Progress

    Epoch 1/10
    2098/2098 [==============================] - 205s 98ms/step - loss: 197.4529 - val_loss: 136.2317
    Epoch 2/10
    2098/2098 [==============================] - 203s 97ms/step - loss: 144.4718 - val_loss: 159.0200
    Epoch 3/10
    2098/2098 [==============================] - 211s 101ms/step - loss: 131.5757 - val_loss: 201.8629
    Epoch 4/10
    2098/2098 [==============================] - 214s 102ms/step - loss: 132.5892 - val_loss: 181.9824
    Epoch 5/10
    2098/2098 [==============================] - 212s 101ms/step - loss: 126.1608 - val_loss: 181.5997
    Epoch 6/10
    2098/2098 [==============================] - 208s 99ms/step - loss: 124.6029 - val_loss: 180.1158
    Epoch 7/10
    2098/2098 [==============================] - 206s 98ms/step - loss: 113.3940 - val_loss: 200.0680
    Epoch 8/10
    2098/2098 [==============================] - 210s 100ms/step - loss: 108.1605 - val_loss: 178.2120
    Epoch 9/10
    2098/2098 [==============================] - 216s 103ms/step - loss: 113.2584 - val_loss: 152.7049
    Epoch 10/10
    2098/2098 [==============================] - 213s 101ms/step - loss: 109.5950 - val_loss: 137.5998
