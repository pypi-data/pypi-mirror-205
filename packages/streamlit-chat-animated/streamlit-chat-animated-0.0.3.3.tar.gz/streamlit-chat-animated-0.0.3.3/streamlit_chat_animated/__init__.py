import streamlit.components.v1 as components
import os, random, time
from typing import Optional, Union

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


_RELEASE = True
COMPONENT_NAME = "streamlit_chat_animated"

if _RELEASE:  # use the build instead of development if release is true
    root_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(root_dir, "frontend/build")

    _streamlit_chat = components.declare_component(
        COMPONENT_NAME,
        path = build_dir
    )
else:
    _streamlit_chat = components.declare_component(
        COMPONENT_NAME,
        url = "http://localhost:3000"
    )

# data type for avatar style
AvatarStyle = Literal[
    "adventurer",
    "adventurer-neutral",
    "avataaars",
    "avataaars-neutral",
    "big-ears",
    "big-ears-neutral",
    "big-smile",
    "bottts",
    "bottts-neutral",
    "croodles",
    "croodles-neutral",
    "fun-emoji",
    "icons",
    "identicon",
    "initials",
    "lorelei",
    "lorelei-neutral",
    "micah",
    "miniavs",
    "open-peeps",
    "personas",
    "pixel-art",
    "pixel-art-neutral",
    "shapes",
    "thumbs",
]

def message(message: str, 
            is_user: Optional[bool] = False, 
            animated: Optional[bool] = False,
            key: Optional[str] = None 
            ):
    """
    Creates a new instance of streamlit-chat component

    Parameters
    ----------
    message: str
        The message to be displayed in the component
    is_user: bool 
        if the sender of the message is user, if `True` will align the 
        message to right, default is False.
    avatar_style: Literal or False
        The style for the avatar of the sender of message, default is bottts
        for not user, and pixel-art-neutral for user.
        st-chat uses https://www.dicebear.com/styles for the avatar
    seed: int or str
        The seed for choosing the avatar to be used, default is 42.
    key: str or False
        An optional key that uniquely identifies this component. If this is
     False, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns: False
    """

    _streamlit_chat(message=str(message).replace("\n", ""), isUser=is_user, animated=animated)


if not _RELEASE:
    import streamlit as st  
    # testing
    long_message = """A chatbot or chatterbot is a software application used to conduct an on-line chat conversation via text or text-to-speech, in lieu of providing direct contact with a live human agent. 
    Designed to convincingly simulate the way a human would behave as a conversational partner, chatbot systems. 
    """
    longer_message = """Where does it come from?
Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock,
 a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word 
 in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by
   Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes
 from a line in section 1.10.32. The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus
   Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.
Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock,
 a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word 
 in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by
   Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes
 from a line in section 1.10.32. The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus
   Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.
Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock,
 a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word 
 in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by
   Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes
 from a line in section 1.10.32. The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus
   Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.
    """

    messages = [{'message':"Hello", 'isUser':True, 'animated': False, 'key': time.time() + random.randint(1,100)}, 
                {'message':"Hi", 'isUser': False, 'animated': False, 'key': time.time() + random.randint(1,100)}, 
                {'message':"How are you?", 'isUser':True, 'animated': False, 'key': time.time() + random.randint(1,100)},
                {'message':"I'm great!, and you", 'isUser': False, 'animated': False, 'key': time.time() + random.randint(1,100)}, 
                {'message':"I'm good, thanks!", 'isUser':True, 'animated': False, 'key': time.time() + random.randint(1,100)},
                {'message':"Give me a history lesson", 'isUser':True, 'animated': False, 'key': time.time() + random.randint(1,100)},
                {'message':long_message, 'isUser':False, 'animated': False, 'key': time.time() + random.randint(1,100)}
                ]
    for index, mess in enumerate(messages):
            
            message(mess['message'], is_user=mess['isUser'], animated=mess['animated'], key=mess['key'])
    st.text_input("Message:")