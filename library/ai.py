from library.event import Event
from model.events import Events


class AI:

    tracking_by_username = {}

    options = {
        "new event": {
            "tclass": Event(),
            "tmodel": Events()
        }
    }

    async def process_message(self, client, message):

        compare = message.clean_content.lower()
        username = message.author.display_name.lower()

        if username not in self.tracking_by_username.keys():
            self.tracking_by_username[username] = {}
            self.tracking_by_username[username]['model'] = None
            self.tracking_by_username[username]['prev'] = None
            self.tracking_by_username[username]['next'] = None

        # Is input valid for tree marker, Are we going down a current tree?
        if compare in self.options.keys() or self.tracking_by_username[username]['next'] is not None:

            if self.tracking_by_username[username]['next'] is None or compare in self.options.keys():
                self.tracking_by_username[username]['next'] = self.options[compare]['tclass']
                self.tracking_by_username[username]['model'] = self.options[compare]['tmodel']

            response = getattr(self.tracking_by_username[username]['next'], "process_message")(
                self.tracking_by_username[username]['model'], message)

            if response is False:
                return await getattr(self.tracking_by_username[username]['next'], "rebuttal")(message)

            self.tracking_by_username[username]['model'] = response

            await getattr(self.tracking_by_username[username]['next'], "respond")(message,
                                                                                  self.tracking_by_username[username][
                                                                                      'model'], client)

            self.tracking_by_username[username]['prev'] = self.tracking_by_username[username]['next']
            self.tracking_by_username[username]['next'] = getattr(self.tracking_by_username[username]['next'], "next")()

        # Default return
        return
