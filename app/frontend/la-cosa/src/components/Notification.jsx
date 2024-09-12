// Notification box component, used to display notifications to the user
// It has an "OK" button to close the notification
// It renders the string passed to it as a prop
//
function Notification(props) {
    return (
        <div className="notification">
            <div className="notification-content">
                <div className="notification-text">
                    {props.text}
                </div>
                <div className="notification-button">
                    <button onClick={props.handleOKClick}>OK</button>
                </div>
            </div>
        </div>
    );
}

export default Notification;
  