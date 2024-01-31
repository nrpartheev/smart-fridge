# smart-fridge
Smart Fridge which can manage items in fridge along with generating recipe suggestions. Computer vision project for the purpose of academics. Uses OpenAI's API for generating the text as well as performing custom functions by understanding sentiments. 

Why seperate Client and Server?

It is easier this way to update to new ML model as the images are sent to the server and the server will predict the results of the image. If we are using client side to host the ML model it will be hard for us to not only update the model but also there will be a problem of computation that will be arising.

Client:
Has the logic of taking required screenshots and sending it to the server's required API.
Has the logic of text generation by getting the text from OpenAI's API.
Has the logic of speech to text and text to speech generation.

Server:
Hosts the ML model required and send the predicted results to the client.
