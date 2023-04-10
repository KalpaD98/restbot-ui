import React from 'react'
import Widget from 'rasa-webchat';

function ChatWidget() {

    const myCustomData = {
        inputTextFieldDelay: 300,
        language: "en"
    }

    function calculateMessageDelay(message) {
        let delay = message.length * 12; // Change this value to adjust the delay per character
        if (delay > 1400) delay = 1400; // Set an upper limit for the delay
        if (delay < 400) delay = 400; // Set a lower limit for the delay
        return delay;
    }

    return (<Widget
        // socketUrl={"http://192.168.8.102:5005"}
        socketUrl={"http://localhost:5005"}
        initPayload={"/greet"}
        customData={myCustomData} // arbitrary custom data. Stay minimal as this will be added to the socket
        title={"ResBot"}
        subtitle={"Powered by Code Masters"}
        autoClearCache={true}
        displayUnreadCount={true}
        //params={{"storage": "session"}}
        params={{
            storage: 'local',
        }}
        customMessageDelay={calculateMessageDelay}
        customComponent={({text}) => <div><p>{text}{text}{text}</p></div>}
        onWidgetEvent={{
            onChatClose: () => {
                localStorage.clear();
            }, onChatOpen: () => {
                localStorage.clear();
            }
        }}
    />)
}

export default ChatWidget;