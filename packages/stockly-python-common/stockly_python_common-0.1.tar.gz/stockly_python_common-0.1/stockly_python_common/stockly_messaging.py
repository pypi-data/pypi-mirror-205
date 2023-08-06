"""
_summary_: this module is used to get the matrix connection to share the different types of media 

"""
import os
import io
import re
from get_image_size import get_image_size_from_bytesio
from matrix_client.room import Room
from matrix_client.client import MatrixClient
from stockly_python_common.static import ALLOWED_ATTRIBUTES, ALLOWED_TAGS
import bleach


class StocklyMessagingClient(Room):

    """_summary_ :This class represents the custom matrix client

    Args:
        Room (_type_): Inheritance of matrix client base class
    """

    def __init__(self, homeserver_url: str, mxid: str, token: str) -> None:
        self.client = MatrixClient(
            base_url=homeserver_url, user_id=mxid, token=token)

    def send_image(self, room_id: str, path: str, remove=False) -> str:
        """_summary_:This function is used to send the image to matrix

        Returns:
            str: room_id,event_type and content
        """
        with open(f"{path}", "rb") as image:
            plot = image.read()

        mxc_url = self.client.upload(plot, content_type="image/jpg")

        image_data = get_image_size_from_bytesio(io.BytesIO(plot), len(plot))

        content = {
            "body": room_id,
            "msgtype": "m.image",
            "url": mxc_url,
            'info': {'w': image_data[0], 'h': image_data[1],
                     'mimetype': 'image/jpg', 'size': len(plot)}
        }
        if remove==True:
            if os.path.exists(f"{path}"):
                os.remove(f"{path}")

        return self.client.api.send_message_event(
            room_id=room_id, event_type="m.room.message",
            content=content

        )

    def send_file(self, room_id: str, path: str, remove: bool=False) -> str:
        """_summary_: This function is used to send the file to matrix

        Returns:
            str: room_id,event_type and content
        """
        with open(f"{path}", "rb") as file:
            file = file.read()

        mxc_url = self.client.upload(file, content_type="application/pdf")

        content = {
            "body": room_id,
            "msgtype": "m.file",
            "url": mxc_url,
            'info': {'mimetype': 'application/pdf', 'size': len(file)}
        }
        if remove==True:
            if os.path.exists(f"{path}"):
                os.remove(f"{path}")

        return self.client.api.send_message_event(
            room_id=room_id, event_type="m.room.message",
            content=content
        )
    
    def send_text(self,room_id,text):
        """Send a plain text message to the room."""
        return self.client.api.send_message(room_id, text)


    def send_html(self,room_id:str, html: str, html_type: str = 'table') -> str:
            """_summary_:This function is used to send the html to matrix

            Args:
                html (_type_): _description_
                html_type (str, optional): _description_. Defaults to 'table'.

            Returns:
                str: room_id,event_type and content
            """
            return self.client.api.send_message_event(
                room_id=room_id, event_type="m.room.message",
                content=self.get_html_content(html, html_type)
            )


    def clean(self,html, **kwargs):
        """
        Sanitise HTML fragments.

        A version of `bleach.clean` but with Element's allowed tags and ``strip=True``
        by default.
        """
        defaults = {
            "strip": True,
            "tags": ALLOWED_TAGS,
            "attributes": ALLOWED_ATTRIBUTES,
            "protocols": ["https", "http", "mxc"],
        }
        defaults.update(kwargs)

        return bleach.clean(html, **defaults)


    def get_html_content(self,message,html_type, body=None, msgtype="m.text"):
        """
        Get HTML from a message.

        Return the json representation of the message in
        "org.Stockly.custom.html" format.
        """
        # Markdown leaves a <p></p> around standard messages that we want to strip:
        if message.startswith("<p>"):
            message = message[3:]
            if message.endswith("</p>"):
                message = message[:-4]

        clean_html = self.clean(message)
        
        content = {
            # Strip out any tags from the markdown to make the body
            "body": body if body else re.sub("<[^<]+?>", "", clean_html),
            "msgtype": msgtype,
            "format": "org.matrix.custom.html",
            "formatted_body": clean_html,
            "html_type": html_type
        }

        return content