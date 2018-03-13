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

    Epoch 1/20
    2233/2233 [==============================] - 217s 97ms/step - loss: 196.9814 - val_loss: 120.9237
    Epoch 2/20
    2233/2233 [==============================] - 216s 97ms/step - loss: 140.8082 - val_loss: 146.6130
    Epoch 3/20
    2233/2233 [==============================] - 213s 96ms/step - loss: 130.2426 - val_loss: 124.2262
    Epoch 4/20
    2233/2233 [==============================] - 218s 97ms/step - loss: 126.0698 - val_loss: 123.4020
    Epoch 5/20
    2233/2233 [==============================] - 217s 97ms/step - loss: 119.9671 - val_loss: 104.4470
    Epoch 6/20
    2233/2233 [==============================] - 218s 97ms/step - loss: 115.6154 - val_loss: 152.9959
    Epoch 7/20
    2233/2233 [==============================] - 220s 99ms/step - loss: 99.8461 - val_loss: 154.0001
    Epoch 8/20
    2233/2233 [==============================] - 219s 98ms/step - loss: 90.8464 - val_loss: 102.1104
    Epoch 9/20
    2233/2233 [==============================] - 217s 97ms/step - loss: 72.4195 - val_loss: 156.2463
    Epoch 10/20
    2233/2233 [==============================] - 217s 97ms/step - loss: 70.5511 - val_loss: 122.0178
    Epoch 11/20
    2233/2233 [==============================] - 217s 97ms/step - loss: 60.0297 - val_loss: 81.9432
    Epoch 12/20
    2233/2233 [==============================] - 216s 97ms/step - loss: 53.4408 - val_loss: 103.2084
    Epoch 13/20
    2233/2233 [==============================] - 217s 97ms/step - loss: 46.7320 - val_loss: 101.1037
    Epoch 14/20
    2233/2233 [==============================] - 217s 97ms/step - loss: 43.4021 - val_loss: 95.9248
    Epoch 15/20
    2233/2233 [==============================] - 219s 98ms/step - loss: 38.7371 - val_loss: 94.4535
    Epoch 16/20
    2233/2233 [==============================] - 215s 96ms/step - loss: 37.9047 - val_loss: 109.5088
    Epoch 17/20
    2233/2233 [==============================] - 218s 97ms/step - loss: 32.0828 - val_loss: 55.5722
    Epoch 18/20
    2233/2233 [==============================] - 216s 97ms/step - loss: 28.5769 - val_loss: 88.8654
    Epoch 19/20
    2233/2233 [==============================] - 216s 97ms/step - loss: 27.2250 - val_loss: 106.9570
    Epoch 20/20
    2233/2233 [==============================] - 216s 97ms/step - loss: 27.1995 - val_loss: 73.5245
