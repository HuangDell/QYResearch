from src.util.record_item import RecordItem
import os
import json

class RecordItemManager:
    def __init__(self,filename):
        self.filename = filename

    def save(self, item: RecordItem):
        """Save the RecordItem to the file."""
        with open(self.filename, 'w') as file:
            json.dump(item.to_dict(), file)

    def load(self) -> RecordItem:
        """Load the RecordItem from the file."""
        if not os.path.exists(self.filename):
            return RecordItem()  # Return default RecordItem if file doesn't exist
        with open(self.filename, 'r') as file:
            data = json.load(file)
            return RecordItem.from_dict(data)

    def update(self, page: int, index: int) -> RecordItem:
        """Update the RecordItem with new values."""
        item = self.load()
        item.page = page
        item.index = index
        self.save(item)
        return item

    def delete(self):
        """Delete the RecordItem file."""
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def exists(self) -> bool:
        """Check if the RecordItem file exists."""
        return os.path.exists(self.filename)
