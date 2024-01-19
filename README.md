# Resbot-UI
This is the UI for the Resbot project. It is a React app that uses the [Material-UI](https://material-ui.com/) framework.

This project is using rasa-webchat widget by botfront (modified to suit our project needs).

Rasa Webchat is a highly customizable chat widget powered by Botfront that allows you to easily integrate your Rasa chatbot into your website. This document provides an overview of the main components available in the Rasa Webchat UI and explains how to use them in your Rasa action server.

Components
The Rasa Webchat UI consists of the following components:

* **Chat Widget**: The main chat interface that users interact with.
* **Quick Replies**: Predefined responses or actions that users can select to quickly reply to the chatbot.
* **Buttons**: Interactive buttons that can trigger specific actions or intents in your chatbot.
* **Carousels**: A horizontal scrolling list of cards, each containing an image, title, subtitle, and buttons.
* **Images**: Allows you to display images within the chat interface.
* **Links**: Embed hyperlinks in your chatbot's messages to direct users to external resources.
* **Custom Components**: Allows you to create custom components to extend the functionality of the chat widget.
* **Custom CSS**: Allows you to customize the look and feel of the chat widget.
* **Custom Themes**: Allows you to customize the look and feel of the chat widget using Material-UI themes.

## Usage
To use these components in your Rasa action server, you will need to send custom responses. The following sections demonstrate how to send each type of component as a custom response from your action server.

### 1. Chat Widget
To integrate the Rasa Webchat widget into your website, include the following code snippet in your HTML file:

* Check out the [Rasa Webchat documentation](https://botfront.io/docs/rasa-webchat) for more information on how to customize the chat widget.

### 2. Quick Replies
In your custom Rasa action, return a BotUttered event with a quick_replies attribute:
from rasa_sdk.events import BotUttered


    

    class ActionShowQuickReplies(Action):

        def name(self) -> Text:
            return "action_show_quick_replies"
    
        def run(self, dispatcher, tracker, domain):
            quick_replies = [
                {"title": "Option 1", "payload": "/intent_1"},
                {"title": "Option 2", "payload": "/intent_2"},
            ]

            dispatcher.utter_message(text="Choose an option:", json_message={"quick_replies": quick_replies})

            return []

### 3. Buttons
To include buttons in a custom Rasa action, return a BotUttered event with a buttons attribute:

    class ActionShowButtons(Action):

        def name(self) -> Text:
            return "action_show_buttons"
    
        def run(self, dispatcher, tracker, domain):
            buttons = [
                {"title": "Option 1", "payload": "/intent_1"},
                {"title": "Option 2", "payload": "/intent_2"},
            ]

            dispatcher.utter_message(text="Choose an option:", json_message={"buttons": buttons})

            return []
#### 3.1 Buttons with entities

    class ActionShowButtons(Action):

        def name(self) -> Text:
            return "action_show_buttons"
    
        def run(self, dispatcher, tracker, domain):
            buttons = [
                {"title": "Option 1", "payload": "/intent_1{\"entity\": \"value\"}"},
                {"title": "Option 2", "payload": "/intent_2{\"entity\": \"value\"}"},
                {"title": "Large", "payload": "/choose_size{\"size\": \"large\"}"}, # example
            ]

            dispatcher.utter_message(text="Choose an option:", json_message={"buttons": buttons})

            return []

### 4. Carousels
A carousel is a horizontal scrolling list of cards, each containing an image, title, subtitle, and buttons.

To send a carousel in a custom Rasa action, return a BotUttered event with an elements attribute:

    class ActionShowCarousels(Action):

        def name(self) -> Text:
            return "action_show_carousels"
    
        def run(self, dispatcher, tracker, domain):
            elements = [
                {
                    "title": "Title 1",
                    "subtitle": "Subtitle 1",
                    "image": "https://i.imgur.com/7Y8o8zR.png",
                    "buttons": [
                        {"title": "Option 1", "payload": "/intent_1"},
                        {"title": "Option 2", "payload": "/intent_2"},
                    ],
                },
                {
                    "title": "Title 2",
                    "subtitle": "Subtitle 2",
                    "image": "https://i.imgur.com/7Y8o8zR.png",
                    # button with entities
                    "buttons": [
                        {"title": "Option 1", "payload": "/intent_1{\"entity\": \"value\"}"},
                        {"title": "Option 2", "payload": "/intent_2{\"entity\": \"value\"}"},
                    ],
                },
            ]

            dispatcher.utter_message(text="Choose an option:", json_message={"elements": elements})

            return []

### 5. Images
To send an image in a custom Rasa action, return a BotUttered event with an image attribute:

    class ActionShowImage(Action):

        def name(self) -> Text:
            return "action_show_image"
    
        def run(self, dispatcher, tracker, domain):
            image = "https://i.imgur.com/7Y8o8zR.png"

            dispatcher.utter_message(text="Here's an image:", json_message={"image": image})

            return []

### 6. Links
To send a link in a custom Rasa action, return a BotUttered event with a link attribute:

    from rasa_sdk.events import BotUttered

    class ActionShowLink(Action):

        def name(self) -> Text:
        return "action_show_link"
    
        def run(self, dispatcher, tracker, domain):
            link_url = "https://example.com"
            link_text = "Visit our website"
            message = f'<a href="{link_url}" target="_blank">{link_text}</a>'
            dispatcher.utter_message(text=message)
            return []

### 7. Persistent Menu
The Persistent Menu is a feature in the Rasa Webchat widget that provides a fixed menu in the chat interface, allowing users to access predefined options or actions at any time. To implement a persistent menu, you need to configure it in the init function when you add the Webchat widget to your website.

     window.webChat.init({
          websiteToken: "YOUR-RASA-WEBSITE-TOKEN",
          socketUrl: "YOUR-RASA-SOCKET-URL",
          customData: {"language": "en"},
          menuItems: [
            {
              title: "Help",
              payload: "/help",
            },
            {
              title: "Settings",
              payload: "/settings",
            },
            {
              title: "Contact Us",
              url: "https://example.com/contact",
            },
          ],
        });

### 8. User Input Disabling

In the Rasa Webchat widget, you can disable user input temporarily or permanently. This can be helpful in guiding users through specific scenarios or when you want to limit their responses to predefined options like buttons or quick replies.

To disable user input, you can send a custom message from your Rasa action server that sets the metadata field with a disable_text_input property.

Here's an example of how to disable user input in a custom Rasa action:

    from rasa_sdk import Action
    from rasa_sdk.events import BotUttered
    
    class ActionDisableUserInput(Action):
    
        def name(self) -> Text:
        return "action_disable_user_input"
    
        def run(self, dispatcher, tracker, domain):
            dispatcher.utter_message(text="User input is now disabled.", metadata={"disable_text_input": True})
            return []

To re-enable user input, you can send another custom message with the disable_text_input property set to False.

Here's an example of how to enable user input in a custom Rasa action:
    
    from rasa_sdk import Action
    from rasa_sdk.events import BotUttered
    
    class ActionEnableUserInput(Action):
        def name(self) -> Text:
        return "action_enable_user_input"
    
        def run(self, dispatcher, tracker, domain):
            dispatcher.utter_message(text="User input is now enabled.", metadata={"disable_text_input": False})
            return []

By sending these custom messages from your action server, you can control when user input is disabled or enabled during the conversation.




# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)

