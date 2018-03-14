## Model 1 Methodology

For rear end accidents, pass images where we use only `back left` and `back right` images.

Current Model


    Adam = keras.optimizers.Adam(lr=0.0005, beta_1=0.95, beta_2=0.999, epsilon=0.00001, decay=0.00001, amsgrad=False)


    print('building regression model')
    # First, define the vision modules
    digit_input = Input(shape=(600, 800, 3))
    x = Conv2D(32, kernel_size=(3, 3), strides=(2,2))(digit_input)
    x = Activation('relu')(x)
    x = Conv2D(32, kernel_size=(3, 3), strides=(2,2))(x) ## change back to 16
    x = Activation('relu')(x)
    x = MaxPooling2D((2, 2))(x)
    x = Flatten()(x)
    x = Dense(32, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(16, activation='relu', kernel_initializer='random_uniform')(x)
    x = Dropout(0.25)(x)
    out = Dense(m, activation='linear', kernel_initializer='random_uniform')(x)


Current Performance

    ...
    Epoch 1/50
    345/345 [==============================] - 37s 108ms/step - loss: 637.4275 - val_loss: 424.7724
    Epoch 2/50
    345/345 [==============================] - 36s 105ms/step - loss: 296.9037 - val_loss: 183.8578
    Epoch 3/50
    345/345 [==============================] - 36s 105ms/step - loss: 228.6247 - val_loss: 136.1902
    Epoch 4/50
    345/345 [==============================] - 36s 104ms/step - loss: 220.0763 - val_loss: 139.0871
    Epoch 5/50
    345/345 [==============================] - 37s 106ms/step - loss: 197.9448 - val_loss: 106.1103
    ...
    Epoch 44/50
    345/345 [==============================] - 37s 106ms/step - loss: 75.9444 - val_loss: 66.3759
    Epoch 45/50
    345/345 [==============================] - 38s 110ms/step - loss: 75.4483 - val_loss: 121.2864
    Epoch 46/50
    345/345 [==============================] - 38s 110ms/step - loss: 75.6165 - val_loss: 62.4702
    Epoch 47/50
    345/345 [==============================] - 36s 105ms/step - loss: 76.6835 - val_loss: 70.7959
    Epoch 48/50
    345/345 [==============================] - 36s 106ms/step - loss: 56.1362 - val_loss: 66.0893
    Epoch 49/50
    345/345 [==============================] - 36s 105ms/step - loss: 63.1947 - val_loss: 60.5049
    Epoch 50/50
    345/345 [==============================] - 36s 105ms/step - loss: 64.6096 - val_loss: 77.1716



## Evaluating Model

    jn107154@dell:~/Documents/ImageNASS/RearEndAccidents/Model 1$ python LoadModel.py 
    ...
    Loaded model from disk
    432/432 [==============================] - 12s 27ms/step
    train loss 47.0447069804
    432/432 [==============================] - 11s 26ms/step
    Reading in images
    107it [00:03, 31.14it/s]
    107/107 [==============================] - 3s 29ms/step
    test loss 130.767211558

Test MSE still seems large...it may need auxillary data