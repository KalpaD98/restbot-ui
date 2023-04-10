import React from 'react'
import Widget from 'rasa-webchat';

function ChatWidget() {
    const myCustomData = {
        inputTextFieldDelay: 300,
        language: "en"
    }

    return (<Widget
        // socketUrl={"http://192.168.8.102:5005"}
        socketUrl={"http://localhost:5005"}
        initPayload={"/greet"}
        customData={myCustomData} // arbitrary custom data. Stay minimal as this will be added to the socket
        title={"ResBot"}
        subtitle={"Powered by Code Masters"}
        //params={{"storage": "session"}}
        autoClearCache={true}
        customComponent={({text}) => <div><p>{text}{text}{text}</p></div>}
        displayUnreadCount={true}
        onWidgetEvent={{
            onChatClose: () => {
                localStorage.clear();
            }, onChatOpen: () => {
                localStorage.clear();
            }
        }}
        params={{
            storage: 'local',
        }}
    />)
}

export default ChatWidget;