# 👨👩 Speaker Gender Classifier

Classify speech using spectrogram feature engineering and neural network.

## Goal

The goal of this project is to extract speakers' genders from recordings. Gender is one of the most impersonal personal information but you can definitely think of how this technique can be applied to other kinds of personal information.

You can also think of personal information as metadata. Metadata is the information ABOUT a speaker, not the information CONVEYED by his/her speech. For example, if I’m the speaker of interest, my metadata is that I’m a male under 30 with an Asian accent and the information conveyed by my speech is, for example, “Welcome to my project”.

## Dataset

The dataset I chose for this [AudioMNIST](https://github.com/soerenab/AudioMNIST). I’ve copied and pasted the information about this dataset below:

> #### data (audioMNIST)
>
> - The dataset consists of 30000 audio samples of spoken digits (0-9) of 60 different speakers.
> - There is one directory per speaker holding the audio recordings.
> - Additionally "audioMNIST_meta.txt" provides meta information such as gender or age of each speaker.

What I really like about this dataset is that it "provides meta information such as gender or age of each speaker”. 

I plan not to model age because the age range available in this project is very small (22 - 41) and a neural network trained on age cannot generalize to any age below or beyond that range. I plan to model gender because 

1. It’s a binary classification task. This makes the interpretation of a neural network much easier since I only need to visualize how it respond differently to TWO classes.
2. There’s plenty of data available for each gender. There are 12 female speakers (12/60 * 30000 = 6000 recordings) and 48 male speakers (48/60 * 30000 = 24000 recordings). 

My concern with modeling gender: since there are only 12 female speakers, I don’t know how well a neural network trained on gender generalizes to unheard-of speakers. To improve generalizability, I plan to first train a neural network from scratch and then compare it with a fine-tuned version of a pretrained network. 

Here are some exploratory data analysis:

<img src='https://raw.githubusercontent.com/zhihanyang2022/speaker_info_classification/master/pngs/eda.png'>

## Feature Engineering













































